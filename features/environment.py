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
from applicationinsights import TelemetryClient

# Import system dialog handler
try:
    from features.utils.system_dialog_handler import (
        get_dialog_handler,
        enable_dialog_handling,
    )

    DIALOG_HANDLER_AVAILABLE = True
except ImportError as e:
    DIALOG_HANDLER_AVAILABLE = False
    logging.warning(f'System dialog handler not available: {e}')

# Import network throttling manager
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
    Trigger screenshot permission dialog beforehand to ensure subsequent test runs won't be interrupted
    If permission dialog appears, it will be automatically authorized; if handling fails, tests will be terminated
    
    Returns:
        bool: True if permission is granted, False if permission acquisition failed and tests should be terminated
    """
    try:
        logger.info("Checking screenshot permission...")
        
        # Create temporary screenshot file path
        temp_dir = pathlib.Path(__file__).parent.parent / 'screenshots'
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_screenshot = temp_dir / 'permission_test.png'
        
        # Check if system dialog handler is available
        dialog_handler = None
        if DIALOG_HANDLER_AVAILABLE:
            from features.utils.system_dialog_handler import get_dialog_handler
            dialog_handler = get_dialog_handler()
            logger.info("System dialog handler is ready, will automatically handle permission dialogs if they appear")
        
        # Use screencapture command to trigger permission request
        cmd = ['screencapture', '-x', str(temp_screenshot)]
        
        # Start screenshot command (may trigger permission dialog)
        logger.info("Executing screenshot command to trigger permission check...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for permission dialog to appear
        time.sleep(2)
        
        # Check if permission dialog appeared
        if dialog_handler:
            logger.info("Checking for permission dialogs...")
            detected_dialogs = dialog_handler.quick_check()
            
            if detected_dialogs:
                logger.info(f"Detected permission dialogs: {detected_dialogs}")
                handled = dialog_handler.check_and_handle_dialogs(detected_dialogs)
                
                if handled:
                    logger.info("✅ Permission dialog automatically handled, authorization granted")
                    # Wait a bit more for permission to take effect
                    time.sleep(2)
                else:
                    logger.error("❌ Failed to handle permission dialog, unable to grant authorization automatically")
                    process.terminate()
                    return False
            else:
                logger.info("No permission dialogs detected, permission may already exist")
        
        # Wait for screenshot command to complete
        try:
            stdout, stderr = process.communicate(timeout=10)
            return_code = process.returncode
        except subprocess.TimeoutExpired:
            logger.error("Screenshot command timed out")
            process.kill()
            return False
        
        if return_code == 0:
            logger.info("✅ Screenshot permission test successful, permission granted")
            # Delete temporary screenshot file
            if temp_screenshot.exists():
                temp_screenshot.unlink()
                logger.debug("Temporary screenshot file deleted")
            return True
        else:
            logger.error(f"❌ Screenshot command execution failed: {stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Error occurred while triggering screenshot permission: {str(e)}")
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

    # Initialize Application Insights telemetry client
    telemetry_client = TelemetryClient('6cfcacca-7f4d-476e-85f4-c184d70ccff9')
    context.telemetry_client = telemetry_client

    # Configure logging - for all loggers
    # Get root logger to configure global logging
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.DEBUG)

    # Add console handler
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Ensure specific logger works properly
    logger.setLevel(logging.DEBUG)
    logger.info('Logging configured successfully')

    # Trigger screenshot permission dialog beforehand (Critical: handle permission issues before all tests start)
    logger.info("=" * 80)
    logger.info("Checking and configuring screenshot permissions...")
    permission_granted = trigger_screenshot_permission()
    
    if permission_granted:
        logger.info("✅ Screenshot permission confirmed, tests can proceed normally")
    else:
        logger.error("❌ Screenshot permission acquisition failed, cannot continue running tests")
        logger.error("   Please ensure relevant permissions are added in System Settings > Privacy & Security > Screen Recording")
        logger.error("   Or check if system dialog handler configuration is correct")
        logger.info("=" * 80)
        # Permission acquisition failed, terminate test execution
        raise RuntimeError("Screenshot permission not granted, cannot continue with tests")
    
    logger.info("=" * 80)

    # Initialize system dialog handler
    if DIALOG_HANDLER_AVAILABLE:
        dialog_handler = get_dialog_handler()
        context.dialog_handler = dialog_handler
        logger.info('System dialog handler initialized')

        # Check if dialog handling is disabled via environment variable
        if os.environ.get('DISABLE_DIALOG_HANDLER', '').lower() == 'true':
            enable_dialog_handling(False)
            logger.info('System dialog handling disabled via environment variable')
        else:
            enable_dialog_handling(True)
            logger.info('System dialog handling enabled')

    # Initialize global scenario counter and total count
    # Use global variables to ensure continuity across feature files
    if not hasattr(before_all, '_global_counter'):
        before_all._global_counter = 0
        before_all._total_scenarios = count_all_scenarios()

    # Use setattr to avoid ContextMaskWarning
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

    # Handle network throttling tags
    if NETWORK_THROTTLING_AVAILABLE:
        throttling_manager = get_throttling_manager()

        # Check for network throttling related tags
        throttling_applied = False
        for tag in scenario.tags:
            # Check predefined throttling profile tags
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


def save_edge_flags_state(context, scenario_name):
    """
    Save Edge flags state by navigating to edge://metrics-internals/#variations
    and saving the page as HTML file with the same naming convention as screenshots
    
    Args:
        context: Behave context object with session
        scenario_name: Name of the scenario for file naming
        
    Returns:
        str: Path to saved HTML file or None if failed
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

        # Add timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{test_name_pattern}_{timestamp}.html'

        # Full path for the HTML file
        html_path = screenshot_dir / filename

        logger.info(f'Attempting to save Edge flags state to: {html_path}')

        # Check if Edge is still running, if not, relaunch it
        logger.info('Checking if Edge is still running...')
        result = call_tool_sync(
            context,
            context.session.call_tool(
                name='app_state',
                arguments={
                    'caller': 'behave-automation',
                    'need_snapshot': 0,
                },
            ),
        )
        result_json = get_tool_json(result)
        
        # Check if app is launched
        app_launched = False
        if result_json and result_json.get('status') == 'success':
            data = result_json.get('data', {})
            app_launched = data.get('is_app_launched', False)
            logger.info(f'Edge app state: launched={app_launched}')
        
        # If Edge is not running, relaunch it using the same implementation as initial launch
        if not app_launched:
            logger.warning('Edge appears to have crashed or is not running. Attempting to relaunch...')
            try:
                from features.steps.common.common import launch_edge_implementation
                launch_edge_implementation(context)
                logger.info('Edge relaunched successfully')
                # Wait a bit for Edge to fully start
                time.sleep(2)
            except Exception as e:
                logger.error(f'Error relaunching Edge: {str(e)}')
                return None

        # Navigate to edge://metrics-internals/#variations
        logger.info('Navigating to edge://metrics-internals/#variations')
        result = call_tool_sync(
            context,
            context.session.call_tool(
                name='send_keys',
                arguments={
                    'caller': 'behave-automation',
                    'locator_value': 'Address and search bar',
                    'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                    'text': 'edge://metrics-internals/#variations',
                    'need_snapshot': 0,
                },
            ),
        )
        result_json = get_tool_json(result)
        if result_json.get('status') != 'success':
            logger.error(f'Failed to enter URL: {result_json.get("error")}')
            return None

        # Press Enter to navigate
        result = call_tool_sync(
            context,
            context.session.call_tool(
                name='press_key',
                arguments={
                    'caller': 'behave-automation',
                    'key': 'return',
                    'need_snapshot': 0,
                },
            ),
        )
        result_json = get_tool_json(result)
        if result_json.get('status') != 'success':
            logger.error(f'Failed to press Enter: {result_json.get("error")}')
            return None

        # Wait for page to load
        time.sleep(3)

        # Detect the actual Edge process name (could be "Microsoft Edge", "Microsoft Edge Canary", "Microsoft Edge Beta", etc.)
        detect_process_script = '''
        tell application "System Events"
            set edgeProcesses to {"Microsoft Edge", "Microsoft Edge Canary", "Microsoft Edge Beta", "Microsoft Edge Dev"}
            repeat with processName in edgeProcesses
                if exists (process processName) then
                    return processName
                end if
            end repeat
            return ""
        end tell
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', detect_process_script],
                capture_output=True,
                text=True,
                timeout=5
            )
            edge_process_name = result.stdout.strip()
            if not edge_process_name:
                logger.error('Could not detect Edge process name')
                return None
            logger.info(f'Detected Edge process: {edge_process_name}')
        except Exception as e:
            logger.error(f'Error detecting Edge process: {str(e)}')
            # Fallback to default name
            edge_process_name = "Microsoft Edge"

        # Use AppleScript to save page as HTML
        # We'll use Command+S to trigger Save dialog, then automate the save process
        applescript = f'''
        tell application "System Events"
            -- Activate the detected Edge process
            tell process "{edge_process_name}"
                set frontmost to true
                delay 0.5
                
                -- Press Command+S to open Save dialog
                keystroke "s" using command down
                delay 1.5
                
                -- Type the filename in the save dialog
                keystroke "{filename}"
                delay 0.5
                
                -- Press Command+Shift+G to open Go to Folder dialog
                keystroke "g" using {{command down, shift down}}
                delay 1
                
                -- Type the directory path
                keystroke "{str(screenshot_dir)}"
                delay 0.5
                
                -- Press Enter to go to the directory
                keystroke return
                delay 0.5
                
                -- Make sure "Web Page, Complete" format is selected
                -- Click on Format dropdown
                try
                    click pop up button 1 of group 1 of group 1 of sheet 1 of window 1
                    delay 0.3
                    
                    -- Look for "Web Page, HTML Only" or similar option
                    -- We'll try to find the HTML-only option
                    click menu item "Web Page, HTML Only" of menu 1 of pop up button 1 of group 1 of group 1 of sheet 1 of window 1
                    delay 0.3
                end try
                
                -- Press Enter to save
                keystroke return
                delay 1
            end tell
        end tell
        '''

        logger.debug(f'Executing AppleScript to save HTML file with process: {edge_process_name}')
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode == 0:
            # Verify the file was created
            if html_path.exists():
                logger.info(f'Edge flags state saved successfully: {html_path}')
                return str(html_path)
            else:
                logger.warning(f'AppleScript executed but file not found at: {html_path}')
                # Try to find the file with similar name
                pattern = f'{test_name_pattern}_*.html'
                matching_files = list(screenshot_dir.glob(pattern))
                if matching_files:
                    latest_file = max(matching_files, key=lambda p: p.stat().st_mtime)
                    logger.info(f'Found HTML file: {latest_file}')
                    return str(latest_file)
                return None
        else:
            logger.error(f'AppleScript failed: {result.stderr}')
            return None

    except Exception as e:
        logger.error(f'Error saving Edge flags state: {str(e)}')
        import traceback
        logger.debug(f'Exception details: {traceback.format_exc()}')
        return None


def after_scenario(context, scenario):
    # Print scenario completion info
    status = 'Passed' if scenario.status == 'passed' else 'Failed'
    logger.info(f'-' * 80)
    logger.info(f'DEBUG: Finished Scenario: {scenario.name} - {status}')
    
    # Track scenario execution status telemetry
    if scenario.status != 'skipped' and 'RUN_SOURCE' in os.environ and getattr(scenario, '_current_retry', 0) == getattr(scenario, '_max_attempts', 1) - 1:
        context.telemetry_client.track_metric(
            "TestScenarioExecuted", 1,
            properties={
                "Platform": "Mac",
                "Status": status,
                "RunSource": os.environ.get('RUN_SOURCE', 'Local'),
                "ScenarioName": scenario.name
            }
        )
        context.telemetry_client.flush()

    # Check and handle system dialogs
    if DIALOG_HANDLER_AVAILABLE and hasattr(context, 'dialog_handler'):
        try:
            # Quick check for dialogs with shorter timeout to avoid blocking
            logger.debug('Starting quick dialog check after scenario...')
            detected = []
            
            try:
                detected = context.dialog_handler.quick_check()
            except Exception as e:
                logger.debug(f'Dialog check failed: {e}')
                detected = []
                    
            if detected:
                logger.info(f'Detected system dialogs after scenario: {detected}')
                # Capture screenshot immediately when system dialog is detected
                screenshot_path = take_system_dialog_screenshot(scenario.name, str(detected))
                if screenshot_path:
                    logger.info(f'System dialog screenshot captured before handling')

                # Handle dialogs - only handle actually detected dialogs
                logger.debug('Attempting to handle detected dialogs...')
                if context.dialog_handler.check_and_handle_dialogs(detected):
                    logger.info(f'Handled system dialog after scenario: {scenario.name}')
                    # Wait a bit to ensure dialog handling is complete
                    time.sleep(0.5)
                else:
                    logger.warning(f'Failed to handle detected dialogs for scenario: {scenario.name}')
            else:
                logger.debug('No system dialogs detected after scenario, skipping dialog handling')
        except Exception as e:
            logger.warning(f'Error checking for system dialogs after scenario: {e}')
            # Don't interrupt tests due to dialog handling failure
            # But log detailed error info for debugging
            import traceback
            logger.debug(f'Dialog handling exception details: {traceback.format_exc()}')

    # Remove network throttling (if applied)
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

    # Take screenshot after scenario completion
    try:
        screenshot_path = take_screenshot(scenario.name)
    except Exception as e:
        logger.warning(f'Screenshot failed for scenario {scenario.name}: {str(e)}')

    # Save Edge flags state if scenario failed on the last retry attempt
    # Only save on the final retry to avoid duplicate captures
    current_retry = getattr(scenario, '_current_retry', 0)
    max_attempts = getattr(scenario, '_max_attempts', 1)
    is_last_attempt = current_retry == max_attempts - 1
    
    logger.debug(f'Retry info - current_retry: {current_retry}, max_attempts: {max_attempts}, is_last_attempt: {is_last_attempt}')
    
    if scenario.status == 'failed' and is_last_attempt:
        logger.info(f'Scenario failed on final retry attempt ({current_retry + 1}/{max_attempts}), saving Edge flags state...')
        try:
            flags_html_path = save_edge_flags_state(context, scenario.name)
            if flags_html_path:
                logger.info(f'Edge flags state saved successfully: {flags_html_path}')
            else:
                logger.warning(f'Failed to save Edge flags state for scenario: {scenario.name}')
        except Exception as e:
            logger.error(f'Error saving Edge flags state: {str(e)}')
            import traceback
            logger.debug(f'Exception details: {traceback.format_exc()}')

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


def after_step(context, step):
    if step.status != 'skipped' and 'RUN_SOURCE' in os.environ:
        context.telemetry_client.track_metric(
            "TestStepExecuted", 1,
            properties={
                "Platform": "Mac", 
                "Status": 'Passed' if step.status == 'passed' else 'Failed',
                "RunSource": os.environ.get('RUN_SOURCE', 'Local')
            }
        )
        context.telemetry_client.flush()
