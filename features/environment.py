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

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler('behave_debug.log', mode='a')  # 输出到文件
    ]
)

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
    
    # 重新配置日志，确保在behave初始化后仍然有效
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # 防止传播到根logger，避免重复日志
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 添加文件处理器
    file_handler = logging.FileHandler('behave_debug.log', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(console_formatter)
    logger.addHandler(file_handler)
    
    logger.info("before_all - Logging configured successfully")
    print("[BEFORE_ALL] Logging configured successfully")

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
    # 使用多种方式确保日志能够被看到
    print(f"[BEFORE_STEP] Executing step: '{step.name}'")  # 直接print到控制台
    logger.info(f"before_step - Executing step: '{step.name}'")  # 改为info级别
    logger.debug(f"before_step - Debug log test")
    
    # 强制刷新日志
    import sys
    sys.stdout.flush()
    
    try:
        dialog_handled = handle_system_dialogs(context)
        if dialog_handled:
            print(f"[BEFORE_STEP] System dialog was handled before step: '{step.name}'")
            logger.info(f"before_step - System dialog was handled before step: '{step.name}'")
        else:
            print(f"[BEFORE_STEP] No system dialog handling needed for step: '{step.name}'")
            logger.debug(f"before_step - No system dialog handling needed for step: '{step.name}'")
    except Exception as e:
        print(f"[BEFORE_STEP] Exception in before_step: {e}")
        logger.error(f"before_step - Exception: {e}")


def after_step(context, step):
    """在每个步骤执行后运行"""
    if step.status == 'failed':
        logger.error(f"after_step - Step failed: '{step.name}', attempting to get page source")
        try:
            if hasattr(context, 'session') and context.session:
                # 获取页面源码用于调试失败的步骤
                page_source_result = call_tool_sync(
                    context,
                    context.session.call_tool(
                        name='get_page_source_tree',
                        arguments={'caller': 'behave-automation'}
                    ),
                    timeout=5
                )
                page_source_json = get_tool_json(page_source_result)
                if page_source_json and page_source_json.get('status') == 'success':
                    page_source = page_source_json.get('data', {}).get('page_source', 'No page source available')
                    logger.error(f"FAILED STEP PAGE SOURCE for '{step.name}':\n{'-'*80}\n{page_source}\n{'-'*80}")
                else:
                    logger.error(f"Failed to get page source for failed step: '{step.name}'")
            else:
                logger.error(f"No active session to get page source for failed step: '{step.name}'")
        except Exception as e:
            logger.error(f"Exception getting page source for failed step '{step.name}': {e}")
    else:
        logger.debug(f"after_step - Step passed: '{step.name}'")


def handle_system_dialogs(context):
    """处理常见的系统弹窗"""
    try:
        # 目前只处理Edge Canary的弹窗，后续可以慢慢补充
        button_text = 'Use "Edge Canary"'
        
        logger.debug("Checking for system dialogs using native macOS methods")
        
        # 直接使用原生方法检查和处理系统对话框，不依赖Appium driver状态
        dialog_exists = _check_system_dialog_exists_native(button_text)
        logger.debug(f"Dialog existence check result: {dialog_exists}")
        
        if dialog_exists:
            # 如果存在，则点击 - 使用原生方法
            click_success = _try_click_system_dialog_button_native(button_text)
            logger.debug(f"Dialog click result: {click_success}")
            if click_success:
                logger.info(f"Handled system dialog by clicking '{button_text}'")
                return True
            else:
                logger.warning(f"Failed to handle system dialog '{button_text}'")
        else:
            logger.debug("No system dialogs found")
                    
        return False
        
    except Exception as e:
        logger.error(f'Exception while handling system dialogs: {e}')
        return False


def _check_system_dialog_exists_native(button_text):
    """使用macOS原生方法检查系统对话框是否存在"""
    try:
        logger.debug(f"Checking for system dialog with button text: '{button_text}'")
        
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
                                if buttonName contains "{button_text}" then
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
                            if name of aButton contains "{button_text}" then
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
def _check_system_dialog_exists_appium(context, button_text):
    try:
        # 额外的安全检查
        if not hasattr(context, 'session') or not context.session:
            logger.debug("_check_system_dialog_exists - No session available")
            return False
        
        logger.debug(f"_check_system_dialog_exists - Looking for button: '{button_text}'")
        
        # 首先获取页面源码用于调试
        try:
            page_source_result = call_tool_sync(
                context,
                context.session.call_tool(
                    name='get_page_source_tree',
                    arguments={'caller': 'behave-automation'}
                ),
                timeout=3
            )
            page_source_json = get_tool_json(page_source_result)
            if page_source_json and page_source_json.get('status') == 'success':
                page_source = page_source_json.get('data', {}).get('page_source', 'No page source available')
                logger.debug(f"Current page source:\n{page_source[:2000]}...")  # 限制输出长度
                
                # 检查页面源码中是否包含目标按钮文本
                if button_text in page_source:
                    logger.debug(f"Button text '{button_text}' found in page source")
                else:
                    logger.debug(f"Button text '{button_text}' NOT found in page source")
            else:
                logger.warning("Failed to get page source for debugging")
        except Exception as e:
            logger.error(f"Exception getting page source: {e}")
            
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
            timeout=1  # 更短的超时时间，快速检查
        )
        result_json = get_tool_json(result)
        
        if result_json:
            logger.debug(f"find_element result - status: {result_json.get('status')}, error: {result_json.get('error', 'No error')}")
            if result_json.get('status') == 'success':
                logger.info(f"Successfully found dialog button: '{button_text}'")
                return True
            else:
                logger.debug(f"Dialog button '{button_text}' not found - {result_json.get('error', 'Unknown reason')}")
        else:
            logger.warning("find_element returned no result")
            
        return False
        
    except Exception as e:
        # 静默处理异常，因为大多数时候不会有对话框，或者没有活跃的driver会话
        logger.debug(f'Exception in _check_system_dialog_exists: {e}')
        return False


def _try_click_system_dialog_button_appium(context, button_text):
    """尝试点击系统对话框按钮"""
    try:
        # 额外的安全检查
        if not hasattr(context, 'session') or not context.session:
            logger.debug("_try_click_system_dialog_button - No session available")
            return False
        
        logger.debug(f"_try_click_system_dialog_button - Attempting to click: '{button_text}'")
            
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
            timeout=2  # 更短的超时时间
        )
        result_json = get_tool_json(result)
        
        if result_json:
            logger.debug(f"click_element result - status: {result_json.get('status')}, error: {result_json.get('error', 'No error')}")
            if result_json.get('status') == 'success':
                logger.info(f"Successfully clicked dialog button: '{button_text}'")
                import time
                time.sleep(0.5)  # 短暂等待对话框消失
                
                # 点击后再次获取页面源码确认对话框是否消失
                try:
                    page_source_result = call_tool_sync(
                        context,
                        context.session.call_tool(
                            name='get_page_source_tree',
                            arguments={'caller': 'behave-automation'}
                        ),
                        timeout=2
                    )
                    page_source_json = get_tool_json(page_source_result)
                    if page_source_json and page_source_json.get('status') == 'success':
                        page_source = page_source_json.get('data', {}).get('page_source', '')
                        if button_text not in page_source:
                            logger.info(f"Dialog successfully dismissed - button '{button_text}' no longer found in page source")
                        else:
                            logger.warning(f"Dialog may still be present - button '{button_text}' still found in page source")
                except Exception as e:
                    logger.error(f"Exception checking page source after click: {e}")
                
                return True
            else:
                logger.warning(f"Failed to click dialog button: {result_json.get('error', 'Unknown error')}")
        else:
            logger.warning("click_element returned no result")
            
        return False
        
    except Exception as e:
        # 静默处理异常，因为大多数时候不会有对话框，或者没有活跃的driver会话
        logger.debug(f'Exception in _try_click_system_dialog_button: {e}')
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
