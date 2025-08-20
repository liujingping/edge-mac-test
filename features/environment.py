import json
import re
import sys
import time
import threading
import asyncio
import janus
import queue
import pathlib
import os
import subprocess
import logging
import glob
from datetime import datetime
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters

# 导入系统弹窗处理器
try:
    from features.utils.system_dialog_handler import (
        get_dialog_handler,
        check_and_handle_system_dialogs,
        enable_dialog_handling,
    )

    DIALOG_HANDLER_AVAILABLE = True
except ImportError as e:
    DIALOG_HANDLER_AVAILABLE = False
    logging.warning(f'System dialog handler not available: {e}')

# 导入网络限速管理器
try:
    from features.utils.network_throttling import (
        get_throttling_manager,
        apply_profile,
        THROTTLING_PROFILES,
    )

    NETWORK_THROTTLING_AVAILABLE = True
except ImportError as e:
    NETWORK_THROTTLING_AVAILABLE = False
    logging.warning(f'Network throttling not available: {e}')

logger = logging.getLogger('behave_environment')

session_ready = threading.Event()
TRANSPORT = 'stdio'  # Default transport method, can be changed to "sse" if needed


def load_mcp_config():
    current_dir = pathlib.Path(__file__).parent.parent
    mcp_config_path = current_dir / '.vscode' / 'mcp.json'

    if not mcp_config_path.exists():
        raise FileNotFoundError(f'MCP config file not found: {mcp_config_path}')

    with open(mcp_config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Find server configuration starting with bdd-auto-mcp
    servers = config.get('servers', {})
    for server_name, server_config in servers.items():
        if server_name.startswith('bdd-auto-mcp'):
            command = server_config.get('command')
            args = server_config.get('args', [])
            env = server_config.get('env', {})
            logger.info(f'Found MCP server configuration: command={command}')
            logger.info(f'Found MCP server configuration: args={args}')
            logger.info(f'Found MCP server configuration: env={env}')
            return command, args, env

    raise ValueError('No bdd-auto-mcp server configuration found in mcp.json')


def count_all_scenarios():
    """Count total scenarios across all feature files"""
    from behave.parser import parse_file
    import glob

    total_scenarios = 0
    current_dir = pathlib.Path(__file__).parent
    feature_files = glob.glob(str(current_dir / '**/*.feature'), recursive=True)

    for feature_file in feature_files:
        try:
            feature = parse_file(feature_file)
            total_scenarios += len(feature.scenarios)
            logger.debug(f'Feature {feature_file}: {len(feature.scenarios)} scenarios')
        except Exception as e:
            logger.warning(f'Failed to parse {feature_file}: {e}')

    logger.info(f'Total scenarios found across all features: {total_scenarios}')
    return total_scenarios


def before_all(context):
    import threading

    # 配置日志 - 为所有logger配置
    # 获取根logger来配置全局日志
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.DEBUG)

    # 添加控制台处理器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 确保特定的logger也能正常工作
    logger.setLevel(logging.DEBUG)
    logger.info('Logging configured successfully')

    # 初始化系统弹窗处理器
    if DIALOG_HANDLER_AVAILABLE:
        dialog_handler = get_dialog_handler()
        context.dialog_handler = dialog_handler
        logger.info('System dialog handler initialized')

        # 检查是否通过环境变量禁用弹窗处理
        if os.environ.get('DISABLE_DIALOG_HANDLER', '').lower() == 'true':
            enable_dialog_handling(False)
            logger.info('System dialog handling disabled via environment variable')
        else:
            enable_dialog_handling(True)
            logger.info('System dialog handling enabled')

    # 初始化全局scenario计数器和总数
    # 使用全局变量来确保跨feature文件的连续性
    if not hasattr(before_all, '_global_counter'):
        before_all._global_counter = 0
        before_all._total_scenarios = count_all_scenarios()

    # 使用 setattr 来避免 ContextMaskWarning
    setattr(context, 'scenario_counter', before_all._global_counter)
    setattr(context, 'total_scenarios', before_all._total_scenarios)

    context._task_queue = janus.Queue()
    context._result_queue = janus.Queue()
    session_ready = threading.Event()

    def run_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def mcp_worker():
            try:
                if TRANSPORT == 'stdio':
                    logger.info('Using stdio transport for MCP server')
                    # Load configuration from mcp.json
                    command, args, env = load_mcp_config()
                    logger.info(f'Loading MCP server with command: {command}')
                    logger.info(f'Args: {args}')

                    # Define MCP server parameters
                    server_params = StdioServerParameters(
                        command=command, args=args, env=env
                    )

                    # Connect to server using stdio_client
                    async with stdio_client(server_params) as streams:
                        async with ClientSession(*streams) as session:
                            await session.initialize()
                            context.session = session
                            session_ready.set()

                            while True:
                                task = await context._task_queue.async_q.get()
                                if task is None:
                                    break

                                coro = task
                                result = await coro
                                await context._result_queue.async_q.put(result)
                else:
                    logger.info('Using SSE transport for MCP server')
                    # Connect to server using sse_client
                    logger.info('Connecting to SSE server at http://localhost:8000/sse')
                    async with sse_client('http://localhost:8000/sse') as streams:
                        async with ClientSession(*streams) as session:
                            await session.initialize()
                            context.session = session
                            session_ready.set()

                            while True:
                                task = await context._task_queue.async_q.get()
                                if task is None:
                                    break

                                start = time.time()
                                coro = task
                                result = await coro
                                await context._result_queue.async_q.put(result)

            except Exception as e:
                logger.error(f'MCP init failed: {repr(e)}')
                session_ready.set()

        loop.run_until_complete(mcp_worker())

    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()

    session_ready.wait()


def after_all(context):
    if hasattr(context, '_task_queue'):
        context._task_queue.sync_q.put_nowait(None)


def call_tool_sync(context, coro, timeout=400):
    start = time.time()
    context._task_queue.sync_q.put(coro)
    while True:
        try:
            result = context._result_queue.sync_q.get_nowait()
            return result
        except queue.Empty:
            if time.time() - start > timeout:
                raise TimeoutError('MCP tool invocation timed out.')
            time.sleep(0.1)


def get_tool_json(result):
    try:
        if isinstance(result, str):
            return result
        items = getattr(result, 'content', None)
        if items:
            for item in items:
                if getattr(item, 'text', None):
                    text = getattr(item, 'text', None)
                    return json.loads(text)
    except Exception as e:
        logger.error(f'Error getting tool JSON: {e}')

    return None


def before_scenario(context, scenario):
    # 递增全局scenario计数器
    before_all._global_counter += 1
    # 使用 setattr 来避免 ContextMaskWarning
    setattr(context, 'scenario_counter', before_all._global_counter)

    # 获取总数和进度信息
    total = getattr(context, 'total_scenarios', 0)
    progress_info = (
        f'({context.scenario_counter}/{total})'
        if total > 0
        else f'#{context.scenario_counter}'
    )

    logger.info(f'=' * 80)
    logger.info(f'DEBUG: Starting Scenario {progress_info}: {scenario.name}')

    # 处理网络限速标签
    if NETWORK_THROTTLING_AVAILABLE:
        throttling_manager = get_throttling_manager()

        # 检查是否有网络限速相关的标签
        throttling_applied = False
        for tag in scenario.tags:
            # 检查预定义的限速配置文件标签
            if tag in THROTTLING_PROFILES:
                logger.info(f'Applying network throttling profile: {tag}')
                if apply_profile(throttling_manager, tag):
                    throttling_applied = True
                    setattr(context, 'network_throttling_active', True)
                    setattr(context, 'network_throttling_profile', tag)
                    logger.info(f'Network throttling "{tag}" applied successfully')
                else:
                    logger.error(f'Failed to apply network throttling profile: {tag}')
                break

        if not throttling_applied:
            setattr(context, 'network_throttling_active', False)
    else:
        setattr(context, 'network_throttling_active', False)

    pass


def before_step(context, step):
    # """在每个测试步骤前检查并处理系统弹窗"""
    # if DIALOG_HANDLER_AVAILABLE and hasattr(context, 'dialog_handler'):
    #     try:
    #         # 快速检查是否有弹窗
    #         detected = context.dialog_handler.quick_check()
    #         if detected:
    #             logger.debug(f'Detected system dialogs: {detected}')

    #         # 处理弹窗
    #         if context.dialog_handler.check_and_handle_dialogs():
    #             logger.info(f'Handled system dialog before step: {step.name}')
    #             # 稍微等待一下确保弹窗处理完成
    #             time.sleep(0.5)
    #     except Exception as e:
    #         logger.debug(f'Error checking for system dialogs: {e}')
    #         # 不要因为弹窗处理失败而中断测试
    pass


def take_screenshot(scenario_name):
    """
    Take a full screen screenshot on macOS and save it with the scenario name
    Screenshot naming convention: *{test_name}*.png
    Storage location: SCREENSHOT_DIR environment variable
    """
    try:
        # Get screenshot directory from environment variable
        screenshot_dir = os.environ.get('SCREENSHOT_DIR')
        if not screenshot_dir:
            # Fallback to default location if env var not set
            current_dir = pathlib.Path(__file__).parent.parent
            screenshot_dir = current_dir / 'screenshots'
            logger.warning(
                f'SCREENSHOT_DIR environment variable not set, using default: {screenshot_dir}'
            )
        else:
            screenshot_dir = pathlib.Path(screenshot_dir)

        # Create screenshots directory if it doesn't exist
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Get testcase name (scenario_name is the testcase name)
        name = scenario_name

        # Clean test name for use as filename - replace spaces with underscores
        # Screenshot naming convention: *{test_name}*.png
        test_name_pattern = clean_test_name(name)

        # Add timestamp to avoid filename conflicts while following the pattern
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{test_name_pattern}_{timestamp}.png'

        # Full path for the screenshot
        screenshot_path = screenshot_dir / filename

        # Use macOS screencapture command to take full screen screenshot
        cmd = ['screencapture', '-x', str(screenshot_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info(f'Screenshot saved: {screenshot_path}')
            return str(screenshot_path)
        else:
            logger.error(f'Screenshot failed: {result.stderr}')
            return None

    except Exception as e:
        logger.error(f'Error taking screenshot: {str(e)}')
        return None


def after_scenario(context, scenario):
    # 打印scenario结束信息
    status = 'PASSED' if scenario.status == 'passed' else 'FAILED'
    logger.info(f'-' * 80)
    logger.info(f'DEBUG: Finished Scenario: {scenario.name} - {status}')

    # 移除网络限速（如果已应用）
    if NETWORK_THROTTLING_AVAILABLE and getattr(
        context, 'network_throttling_active', False
    ):
        throttling_manager = get_throttling_manager()
        profile = getattr(context, 'network_throttling_profile', 'unknown')
        logger.info(f'Removing network throttling profile: {profile}')
        if throttling_manager.remove_throttling():
            logger.info('Network throttling removed successfully')
        else:
            logger.error('Failed to remove network throttling')

    # Clean up temporary profile directory if it exists
    if hasattr(context, 'profile_path'):
        try:
            import shutil

            profile_path = context.profile_path
            if os.path.exists(profile_path):
                shutil.rmtree(profile_path)
                logger.info(f'Cleaned up temporary profile directory: {profile_path}')
        except Exception as e:
            logger.warning(f'Failed to cleanup profile directory: {str(e)}')

    # Take screenshot after scenario completion
    try:
        screenshot_path = take_screenshot(scenario.name)
    except Exception as e:
        logger.warning(f'Screenshot failed for scenario {scenario.name}: {str(e)}')

    logger.info(f'-' * 80)


def clean_test_name(name):
    """
    Clean test case name by removing/replacing special characters

    Args:
        name: Original test case name

    Returns:
        str: Cleaned name suitable for file pattern matching
    """
    if not name:
        return ''

    # Replace common problematic characters with underscore
    # Keep only alphanumeric, underscore, hyphen, and space
    cleaned = re.sub(r'[^\w\s\-]', '_', name)

    # Replace multiple spaces with single space, then replace spaces with underscore
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    cleaned = cleaned.replace(' ', '_')

    # Replace multiple underscores with single underscore
    cleaned = re.sub(r'_+', '_', cleaned)

    # Remove leading and trailing underscores
    cleaned = cleaned.strip('_')

    return cleaned
