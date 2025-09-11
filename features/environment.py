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
from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry

# 导入系统弹窗处理器
try:
    from features.utils.system_dialog_handler import (
        get_dialog_handler,
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


def trigger_screenshot_permission():
    """
    预先触发截图权限弹窗，确保后续测试运行时不会被权限弹窗中断
    如果出现权限弹窗，会自动点击授权；如果处理失败，会导致测试终止
    
    Returns:
        bool: True表示权限已获得，False表示权限获取失败，应该终止测试
    """
    try:
        logger.info("正在检查截图权限...")
        
        # 创建临时截图文件路径
        temp_dir = pathlib.Path(__file__).parent.parent / 'screenshots'
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_screenshot = temp_dir / 'permission_test.png'
        
        # 检查是否有系统弹窗处理器可用
        dialog_handler = None
        if DIALOG_HANDLER_AVAILABLE:
            from features.utils.system_dialog_handler import get_dialog_handler
            dialog_handler = get_dialog_handler()
            logger.info("系统弹窗处理器已就绪，如有权限弹窗将自动处理")
        
        # 使用 screencapture 命令触发权限请求
        cmd = ['screencapture', '-x', str(temp_screenshot)]
        
        # 启动截图命令（可能会触发权限弹窗）
        logger.info("正在执行截图命令以触发权限检查...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 等待一小段时间让权限弹窗出现
        time.sleep(2)
        
        # 检查是否有权限弹窗出现
        if dialog_handler:
            logger.info("检查是否有权限弹窗...")
            detected_dialogs = dialog_handler.quick_check()
            
            if detected_dialogs:
                logger.info(f"检测到权限弹窗: {detected_dialogs}")
                handled = dialog_handler.check_and_handle_dialogs(detected_dialogs)
                
                if handled:
                    logger.info("✅ 权限弹窗已自动处理，已点击授权")
                    # 再等待一下让权限生效
                    time.sleep(2)
                else:
                    logger.error("❌ 权限弹窗处理失败，无法自动授权")
                    process.terminate()
                    return False
            else:
                logger.info("未检测到权限弹窗，可能权限已存在")
        
        # 等待截图命令完成
        try:
            stdout, stderr = process.communicate(timeout=10)
            return_code = process.returncode
        except subprocess.TimeoutExpired:
            logger.error("截图命令超时")
            process.kill()
            return False
        
        if return_code == 0:
            logger.info("✅ 截图权限测试成功，权限已获得")
            # 删除临时截图文件
            if temp_screenshot.exists():
                temp_screenshot.unlink()
                logger.debug("已删除临时截图文件")
            return True
        else:
            logger.error(f"❌ 截图命令执行失败: {stderr}")
            return False
            
    except Exception as e:
        logger.error(f"触发截图权限时发生错误: {str(e)}")
        return False


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

    # 预先触发截图权限弹窗（关键：在所有测试开始前处理权限问题）
    logger.info("=" * 80)
    logger.info("正在检查和配置截图权限...")
    permission_granted = trigger_screenshot_permission()
    
    if permission_granted:
        logger.info("✅ 截图权限已确认，测试可以正常进行")
    else:
        logger.error("❌ 截图权限获取失败，无法继续运行测试")
        logger.error("   请确保在系统设置 > 隐私与安全性 > 屏幕录制中已添加相关权限")
        logger.error("   或检查系统弹窗处理器配置是否正确")
        logger.info("=" * 80)
        # 权限获取失败，终止测试执行
        raise RuntimeError("Screenshot permission not granted, cannot continue with tests")
    
    logger.info("=" * 80)

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

    # 检查并处理系统弹窗
    if DIALOG_HANDLER_AVAILABLE and hasattr(context, 'dialog_handler'):
        try:
            # 快速检查是否有弹窗，设置较短的超时时间避免阻塞
            logger.debug('Starting quick dialog check...')
            detected = []
            
            try:
                detected = context.dialog_handler.quick_check()
            except Exception as e:
                logger.debug(f'Dialog check failed: {e}')
                detected = []
                    
            if detected:
                logger.info(f'Detected system dialogs: {detected}')
                # 检测到系统弹窗时立即截图
                screenshot_path = take_system_dialog_screenshot(scenario.name, str(detected))
                if screenshot_path:
                    logger.info(f'System dialog screenshot captured before handling')

                # 处理弹窗 - 只处理实际检测到的弹窗
                logger.debug('Attempting to handle detected dialogs...')
                if context.dialog_handler.check_and_handle_dialogs(detected):
                    logger.info(f'Handled system dialog before scenario: {scenario.name}')
                    # 稍微等待一下确保弹窗处理完成
                    time.sleep(0.5)
                else:
                    logger.warning(f'Failed to handle detected dialogs for scenario: {scenario.name}')
            else:
                logger.debug('No system dialogs detected, skipping dialog handling')
        except Exception as e:
            logger.warning(f'Error checking for system dialogs: {e}')
            # 不要因为弹窗处理失败而中断测试
            # 但记录详细错误信息以便调试
            import traceback
            logger.debug(f'Dialog handling exception details: {traceback.format_exc()}')


def before_step(context, step):
    pass


def _take_screenshot_internal(scenario_name, screenshot_type="", dialog_info=""):
    """
    Internal function to take screenshots with different types
    
    Args:
        scenario_name: Name of the scenario
        screenshot_type: Type of screenshot ("system_dialog" or "")
        dialog_info: Additional dialog information for logging
    
    Returns:
        str: Path to saved screenshot or None if failed
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

        # Clean test name for use as filename
        test_name_pattern = clean_test_name(scenario_name)

        # Add timestamp and type indicator
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if screenshot_type:
            filename = f'{test_name_pattern}_{screenshot_type}_{timestamp}.png'
        else:
            filename = f'{test_name_pattern}_{timestamp}.png'

        # Full path for the screenshot
        screenshot_path = screenshot_dir / filename

        # Use macOS screencapture command to take full screen screenshot
        cmd = ['screencapture', '-x', str(screenshot_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            if screenshot_type == "system_dialog":
                logger.info(f'System dialog screenshot saved: {screenshot_path}')
                if dialog_info:
                    logger.info(f'Dialog details: {dialog_info}')
            else:
                logger.info(f'Screenshot saved: {screenshot_path}')
            return str(screenshot_path)
        else:
            logger.error(f'Screenshot failed: {result.stderr}')
            return None

    except Exception as e:
        logger.error(f'Error taking screenshot: {str(e)}')
        return None


def take_system_dialog_screenshot(scenario_name, dialog_info=""):
    """
    Take a screenshot when system dialog is detected
    Screenshot naming convention: *{test_name}_system_dialog*.png
    Storage location: SCREENSHOT_DIR environment variable
    """
    return _take_screenshot_internal(scenario_name, "system_dialog", dialog_info)


def take_screenshot(scenario_name):
    """
    Take a full screen screenshot on macOS and save it with the scenario name
    Screenshot naming convention: *{test_name}*.png
    Storage location: SCREENSHOT_DIR environment variable
    """
    return _take_screenshot_internal(scenario_name)


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


def before_feature(context, feature):
    for scenario in feature.scenarios:
        patch_scenario_with_autoretry(scenario, max_attempts=2)
