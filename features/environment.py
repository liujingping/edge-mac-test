import json
import re
import time
import threading
import asyncio
import janus
import queue
import pathlib
import os
import subprocess
from datetime import datetime
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters

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
            print(f'Found MCP server configuration: command={command}')
            print(f'Found MCP server configuration: args={args}')
            return command, args

    raise ValueError('No bdd-auto-mcp server configuration found in mcp.json')


def before_all(context):
    import threading

    context._task_queue = janus.Queue()
    context._result_queue = janus.Queue()
    session_ready = threading.Event()

    def run_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def mcp_worker():
            try:
                if TRANSPORT == 'stdio':
                    print('Using stdio transport for MCP server')
                    # Load configuration from mcp.json
                    command, args = load_mcp_config()
                    print(f'Loading MCP server with command: {command}')
                    print(f'Args: {args}')

                    # Define MCP server parameters
                    server_params = StdioServerParameters(command=command, args=args)

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
                    print('Using SSE transport for MCP server')
                    # Connect to server using sse_client
                    print('Connecting to SSE server at http://localhost:8000/sse')
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
                print(f'MCP init failed: {repr(e)}')
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
        print(f'Error getting tool JSON: {e}')

    return None


def before_scenario(context, scenario):
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


def before_step(context, step):
    """在每个步骤执行前运行"""   
    # 处理系统弹窗
    handle_system_dialogs(context)


def handle_system_dialogs(context):
    """处理常见的系统弹窗"""
    try:
        # 目前只处理Edge Canary的弹窗，后续可以慢慢补充
        button_text = 'Use "Edge Canary"'
        
        # 先检查弹窗是否存在
        if _check_system_dialog_exists(context, button_text):
            # 如果存在，则点击
            if _try_click_system_dialog_button(context, button_text):
                print(f"DEBUG: Handled system dialog by clicking '{button_text}'")
                return True
                    
        return False
        
    except Exception as e:
        print(f'DEBUG: Exception while handling system dialogs: {e}')
        return False


def _check_system_dialog_exists(context, button_text):
    """检查系统对话框是否存在"""
    try:
        # 使用find_element检查按钮是否存在
        result = call_tool_sync(
            context,
            context.session.call_tool(
                name='find_element',
                arguments={
                    'caller': 'behave-automation',
                    'locator_value': button_text,
                    'locator_strategy': 'AppiumBy.NAME',
                    'step': 'system_dialog_checker',
                    'step_raw': f'Check system dialog: {button_text}',
                    'scenario': 'System Dialog Handler',
                },
            ),
            timeout=2  # 很短的超时时间，只是检查存在性
        )
        result_json = get_tool_json(result)
        return result_json and result_json.get('status') == 'success'
        
    except Exception as e:
        return False


def _try_click_system_dialog_button(context, button_text):
    """尝试点击系统对话框按钮"""
    try:
        # 尝试使用NAME定位器
        result = call_tool_sync(
            context,
            context.session.call_tool(
                name='click_element',
                arguments={
                    'caller': 'behave-automation',
                    'locator_value': button_text,
                    'locator_strategy': 'AppiumBy.NAME',
                    'step': 'system_dialog_handler',
                    'step_raw': f'Handle system dialog: {button_text}',
                    'scenario': 'System Dialog Handler',
                },
            ),
            timeout=3  # 短超时时间
        )
        result_json = get_tool_json(result)
        if result_json and result_json.get('status') == 'success':
            import time
            time.sleep(0.5)  # 短暂等待对话框消失
            return True
            
        return False
        
    except Exception as e:
        # 静默处理异常，因为大多数时候不会有对话框
        return False


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
            print(
                f'⚠️  SCREENSHOT_DIR environment variable not set, using default: {screenshot_dir}'
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
            print(f'📸 Screenshot saved: {screenshot_path}')
            print(f'📁 Screenshot pattern: *{test_name_pattern}*.png')
            return str(screenshot_path)
        else:
            print(f'❌ Screenshot failed: {result.stderr}')
            return None

    except Exception as e:
        print(f'💥 Error taking screenshot: {str(e)}')
        return None


def after_scenario(context, scenario):
    # Take screenshot after scenario completion
    try:
        screenshot_path = take_screenshot(scenario.name)
        if screenshot_path:
            print(f'Screenshot captured for scenario: {scenario.name}')
    except Exception as e:
        print(f'Warning: Screenshot failed for scenario {scenario.name}: {str(e)}')


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
