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


def before_all(context):
    import threading
    
    # 配置日志 - 简化版本
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)  # Logger 级别控制
    logger.propagate = False
    
    # 添加控制台处理器（使用 Logger 的级别，不重复设置）
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.info("Logging configured successfully")

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
                    server_params = StdioServerParameters(command=command, args=args, env=env)

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
    logger.info(f"before_step - Executing step: '{step.name}'")
    
    try:
        dialog_handled = handle_system_dialogs(context)
        if dialog_handled:
            logger.info(f"before_step - System dialog was handled before step: '{step.name}'")
        else:
            logger.debug(f"before_step - No system dialog handling needed for step: '{step.name}'")
    except Exception as e:
        logger.error(f"before_step - Exception: {e}")


def after_step(context, step):
    """在每个步骤执行后运行"""
    pass


def handle_system_dialogs(context):
    """处理常见的系统弹窗"""
    try:
        # 定义多种可能的按钮文本格式
        button_texts = [
            'Use "Edge Canary"',  # 带引号格式
            'Use Edge Canary',    # 不带引号格式
            '"Use Edge Canary"',  # 完整引号格式
        ]
        
        logger.debug("Checking for system dialogs using native macOS methods")
        
        # 尝试匹配任意一种按钮文本格式
        for button_text in button_texts:
            dialog_exists = _check_system_dialog_exists_native(button_text)
            logger.debug(f"Dialog existence check for '{button_text}': {dialog_exists}")
            
            if dialog_exists:
                # 如果存在，则点击 - 使用原生方法
                click_success = _try_click_system_dialog_button_native(button_text)
                logger.debug(f"Dialog click result for '{button_text}': {click_success}")
                if click_success:
                    logger.info(f"Handled system dialog by clicking '{button_text}'")
                    return True
                else:
                    logger.warning(f"Failed to handle system dialog '{button_text}'")
        
        logger.debug("No system dialogs found with any known button text format")
        return False
        
    except Exception as e:
        logger.error(f'Exception while handling system dialogs: {e}')
        return False


def _check_system_dialog_exists_native(button_text):
    """使用macOS原生方法检查系统对话框是否存在"""
    try:
        logger.debug(f"Checking for system dialog with button text: '{button_text}'")
        
        # 转义AppleScript中的引号
        escaped_button_text = button_text.replace('"', '\\"')
        
        # 使用osascript检查系统对话框 - 更全面的进程检查
        script = f'''
        tell application "System Events"
            set dialogExists to false
            set processNames to {{}}
            set dialogInfo to ""
            try
                -- 获取所有进程名称用于调试
                set allProcesses to every process
                repeat with aProcess in allProcesses
                    set processNames to processNames & name of aProcess & ","
                end repeat
                
                -- 检查可能包含系统对话框的进程
                set targetProcesses to every process whose name contains "CoreServicesUIAgent" or name contains "UserNotificationCenter" or name contains "loginwindow" or name contains "SecurityAgent" or name contains "authd"
                
                repeat with aProcess in targetProcesses
                    set processName to name of aProcess
                    set theWindows to every window of aProcess
                    set dialogInfo to dialogInfo & "Process:" & processName & ",Windows:" & (count of theWindows) & ";"
                    repeat with aWindow in theWindows
                        try
                            set theButtons to every button of aWindow
                            repeat with aButton in theButtons
                                set buttonName to name of aButton
                                set dialogInfo to dialogInfo & "Button:" & buttonName & ";"
                                -- 使用精确匹配而不是contains
                                if buttonName is equal to "{escaped_button_text}" then
                                    set dialogExists to true
                                    set dialogInfo to dialogInfo & "FOUND_TARGET_BUTTON!"
                                    exit repeat
                                end if
                            end repeat
                            if dialogExists then exit repeat
                        on error buttonError
                            set dialogInfo to dialogInfo & "ButtonError:" & buttonError & ";"
                        end try
                    end repeat
                    if dialogExists then exit repeat
                end repeat
            on error errMsg
                set dialogInfo to dialogInfo & "MainError:" & errMsg & ";"
            end try
            
            -- 返回结果和调试信息
            return (dialogExists as string) & "|PROCESSES:" & processNames & "|DIALOGS:" & dialogInfo
        end tell
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script], 
            capture_output=True, 
            text=True, 
            timeout=15
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            logger.debug(f"AppleScript output: {output}")
            
            parts = output.split('|')
            dialog_found = parts[0] == 'true'
            
            # 记录详细的调试信息
            for part in parts[1:]:
                if part.startswith('PROCESSES:'):
                    processes = part[10:200]  # 限制长度
                    logger.debug(f"Available processes: {processes}")
                elif part.startswith('DIALOGS:'):
                    dialogs = part[8:]
                    logger.debug(f"Dialog details: {dialogs}")
            
            logger.debug(f"System dialog check result: {dialog_found}")
            return dialog_found
        else:
            logger.warning(f"AppleScript error checking dialog: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.warning("AppleScript timeout while checking system dialog")
        return False
    except Exception as e:
        logger.error(f"Exception checking system dialog with AppleScript: {e}")
        return False


def _try_click_system_dialog_button_native(button_text):
    """使用macOS原生方法点击系统对话框按钮"""
    try:
        # 转义AppleScript中的引号
        escaped_button_text = button_text.replace('"', '\\"')
        
        # 使用osascript点击系统对话框按钮
        script = f'''
        tell application "System Events"
            set buttonClicked to false
            try
                set theDialogs to every window of every process whose name contains "CoreServicesUIAgent" or name contains "UserNotificationCenter" or name contains "loginwindow"
                repeat with aDialog in theDialogs
                    try
                        set theButtons to every button of aDialog
                        repeat with aButton in theButtons
                            -- 使用精确匹配而不是contains
                            if name of aButton is equal to "{escaped_button_text}" then
                                click aButton
                                set buttonClicked to true
                                exit repeat
                            end if
                        end repeat
                        if buttonClicked then exit repeat
                    end try
                end repeat
            end try
            return buttonClicked
        end tell
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            clicked = result.stdout.strip() == 'true'
            if clicked:
                logger.info(f"Successfully clicked system dialog button '{button_text}' using AppleScript")
                time.sleep(0.5)  # 等待对话框消失
            return clicked
        else:
            logger.warning(f"AppleScript error clicking dialog: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Exception clicking system dialog with AppleScript: {e}")
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
            logger.info(f'Screenshot pattern: *{test_name_pattern}*.png')
            return str(screenshot_path)
        else:
            logger.error(f'Screenshot failed: {result.stderr}')
            return None

    except Exception as e:
        logger.error(f'Error taking screenshot: {str(e)}')
        return None


def after_scenario(context, scenario):
    # Take screenshot after scenario completion
    try:
        screenshot_path = take_screenshot(scenario.name)
        if screenshot_path:
            logger.info(f'Screenshot captured for scenario: {scenario.name}')
    except Exception as e:
        logger.warning(f'Screenshot failed for scenario {scenario.name}: {str(e)}')


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
