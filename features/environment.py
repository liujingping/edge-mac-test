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
    feature_files = glob.glob(str(current_dir / "**/*.feature"), recursive=True)
    
    for feature_file in feature_files:
        try:
            feature = parse_file(feature_file)
            total_scenarios += len(feature.scenarios)
            logger.debug(f"Feature {feature_file}: {len(feature.scenarios)} scenarios")
        except Exception as e:
            logger.warning(f"Failed to parse {feature_file}: {e}")
    
    logger.info(f"Total scenarios found across all features: {total_scenarios}")
    return total_scenarios


def before_all(context):
    import threading

    # 配置日志 - 简化版本
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)  # Logger 级别控制
    logger.propagate = False

    # 添加控制台处理器（使用 Logger 的级别，不重复设置）
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info('Logging configured successfully')

    # 初始化全局scenario计数器和总数
    # 使用全局变量来确保跨feature文件的连续性
    if not hasattr(before_all, '_global_counter'):
        before_all._global_counter = 0
        before_all._total_scenarios = count_all_scenarios()
    
    # 使用 setattr 来避免 ContextMaskWarning
    setattr(context, 'scenario_counter', before_all._global_counter)
    setattr(context, 'total_scenarios', before_all._total_scenarios)

    # ===== 录屏功能初始化（新增）=====
    # Setup recording directory and initialize recording context variables
    try:
        context.recording_dir = setup_recording_directory()
        context.current_recording = None
        context.recording_started = False
    except Exception as e:
        logger.warning(f"⚠️ Recording setup failed (non-critical): {e}")
        # Set dummy values to prevent errors
        context.recording_dir = pathlib.Path.cwd() / "recordings"
        context.current_recording = None
        context.recording_started = False
    # ===== 录屏功能初始化结束 =====

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


# ===== 录屏功能相关函数（新增）=====

def setup_recording_directory():
    """Setup directory for screen recordings using environment variables"""
    # Try to get recording directory from environment variable
    recording_dir = os.environ.get('SCREENSHOT_DIR')
    
    if not recording_dir:
        # Fallback to project directory
        current_dir = pathlib.Path(__file__).parent.parent
        recording_dir = current_dir / "recordings"
    else:
        recording_dir = pathlib.Path(recording_dir)
    
    # Create directory if it doesn't exist
    recording_dir.mkdir(parents=True, exist_ok=True)
    
    # Set environment variable for the tools to use
    os.environ['SCREENSHOT_DIR'] = str(recording_dir)
    
    logger.info(f"🎬 Screen recordings will be saved to: {recording_dir}")
    return recording_dir


def start_recording(context, scenario_name):
    """Start screen recording for the scenario"""
    try:
        logger.info(f"🎬 Starting screen recording for scenario: {scenario_name}")
        
        # Configure recording options for Mac
        recording_options = {
            'fps': 15,
            'captureCursor': True,
            'captureClicks': True,
            'deviceId': 0,
            'timeLimit': 1800,  # 30 minutes max
            'preset': 'veryfast'
        }
        
        result = call_tool_sync(
            context, 
            context.session.call_tool(
                name="start_screen_recording", 
                arguments={
                    "caller": "behave-automation-mac",
                    "scenario": scenario_name,
                    "step": "Start scenario recording",
                    **recording_options
                }
            ),
            timeout=30
        )
        
        result_json = get_tool_json(result)
        if result_json and result_json.get("status") == "success":
            logger.info("✅ Screen recording started successfully")
            context.recording_started = True
            context.recording_start_time = datetime.now()
        else:
            error_msg = result_json.get('error', 'Unknown error') if result_json else 'No response'
            logger.warning(f"⚠️ Failed to start screen recording: {error_msg}")
            context.recording_started = False
            
    except Exception as e:
        logger.warning(f"⚠️ Exception while starting screen recording (non-critical): {e}")
        context.recording_started = False


def stop_recording(context, scenario_name, scenario_status):
    """Stop screen recording and save the video"""
    if not getattr(context, 'recording_started', False):
        logger.debug("⚠️ No active recording to stop")
        return
        
    try:
        logger.info(f"⏹️ Stopping screen recording for scenario: {scenario_name}")
        
        # Generate filename with scenario name and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_scenario_name = clean_test_name(scenario_name)  # 使用现有的清理函数
        
        # Include scenario status in filename
        status_suffix = "PASS" if scenario_status == "passed" else "FAIL"
        filename = f"recording_{safe_scenario_name}_{status_suffix}_{timestamp}.mp4"
        save_path = os.path.join(context.recording_dir, filename)
        
        result = call_tool_sync(
            context,
            context.session.call_tool(
                name="stop_screen_recording",
                arguments={
                    "caller": "behave-automation-mac", 
                    "scenario": scenario_name,
                    "step": "Stop scenario recording",
                    "save_path": save_path
                }
            ),
            timeout=60
        )
        
        result_json = get_tool_json(result)
        if result_json and result_json.get("status") == "success":
            data = result_json.get("data", {})
            video_path = data.get("video_saved", save_path)
            file_size_mb = data.get("file_size_mb", 0)
            
            duration = datetime.now() - getattr(context, 'recording_start_time', datetime.now())
            duration_str = str(duration).split('.')[0]  # Remove microseconds
            
            logger.info(f"✅ Screen recording saved: {video_path}")
            logger.info(f"   📁 File size: {file_size_mb} MB")
            logger.info(f"   ⏱️  Duration: {duration_str}")
            
            context.current_recording = video_path
        else:
            error_msg = result_json.get('error', 'Unknown error') if result_json else 'No response'
            logger.warning(f"⚠️ Failed to stop screen recording: {error_msg}")
            
    except Exception as e:
        logger.warning(f"⚠️ Exception while stopping screen recording (non-critical): {e}")
    finally:
        context.recording_started = False

# ===== 录屏功能相关函数结束 =====


def before_scenario(context, scenario):
    # 递增全局scenario计数器
    before_all._global_counter += 1
    # 使用 setattr 来避免 ContextMaskWarning
    setattr(context, 'scenario_counter', before_all._global_counter)
    
    # 获取总数和进度信息
    total = getattr(context, 'total_scenarios', 0)
    progress_info = f"({context.scenario_counter}/{total})" if total > 0 else f"#{context.scenario_counter}"
    
    # 打印当前scenario信息，包括feature名称
    feature_name = scenario.feature.name if scenario.feature else "Unknown Feature"
    logger.info(f"=" * 80)
    logger.info(f"DEBUG: Starting Scenario {progress_info}: {scenario.name}")
    logger.info(f"DEBUG: Feature: {feature_name}")
    
    # ===== 录屏功能启动（新增）=====
    # Start screen recording for this scenario
    try:
        start_recording(context, scenario.name)
    except Exception as e:
        logger.warning(f"⚠️ Failed to start recording (non-critical): {e}")
    # ===== 录屏功能启动结束 =====
    
    # context.scenario = scenario
    # try:
    #     result = call_tool_sync(context, context.session.call_tool(name="app_launch", arguments={"caller": "behave"}), timeout=60)
    #     # Add error checking to prevent test from failing silently
    #     tool_json = get_tool_json(result)
    #     if tool_json and tool_json.get("status") != "success":
    #         print(f"Warning: app_launch failed with error: {tool_json.get('error')}")
    # except TimeoutError as e:
    #     print(f"Warning: app_launch timed out: {str(e)}")
    #     # Allow the test to continue even if this fails
    #     pass
    # except Exception as e:
    #     print(f"Warning: app_launch error: {str(e)}")
    # Allow the test to continue even if this fails
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
    # 获取总数和进度信息
    total = getattr(context, 'total_scenarios', 0)
    scenario_counter = getattr(context, 'scenario_counter', 0)
    progress_info = f"({scenario_counter}/{total})" if total > 0 else f"#{scenario_counter}"
    
    # 打印scenario结束信息
    status = "PASSED" if scenario.status == "passed" else "FAILED"
    feature_name = scenario.feature.name if scenario.feature else "Unknown Feature"
    logger.info(f"-" * 80)
    logger.info(f"DEBUG: Finished Scenario {progress_info}: {scenario.name} - {status}")
    logger.info(f"DEBUG: Feature: {feature_name}")
    
    # ===== 录屏功能停止（新增）=====
    # Stop screen recording for this scenario
    try:
        stop_recording(context, scenario.name, scenario.status.name.lower())
    except Exception as e:
        logger.warning(f"⚠️ Failed to stop recording (non-critical): {e}")
    # ===== 录屏功能停止结束 =====
    
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

    logger.info(f"-" * 80)


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
