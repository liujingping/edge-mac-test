"""
Behave environment file for FSQ AI Testcases Mac with screen recording support
This file should be placed at: /Users/liujingping/projects/FSQ_AI_Testcases_Mac/features/environment.py
"""
import json
import time
import threading
import asyncio
import janus
import pathlib
import queue
import os
from datetime import datetime
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.sse import sse_client
import logging


session_ready = threading.Event()


def load_mcp_config():
    """Load MCP configuration from .vscode/mcp.json"""
    current_dir = pathlib.Path(__file__).parent.parent
    mcp_config_path = current_dir / ".vscode" / "mcp.json"
    
    if not mcp_config_path.exists():
        raise FileNotFoundError(f"MCP config file not found: {mcp_config_path}")
    
    with open(mcp_config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Find server configuration starting with bdd-auto-mcp or appium
    servers = config.get("servers", {})
    for server_name, server_config in servers.items():
        if "appium" in server_name.lower() or server_name.startswith("bdd-auto-mcp"):
            command = server_config.get("command")
            args = server_config.get("args", [])
            print(f"Found MCP server configuration: {server_name}")
            print(f"Command: {command}")
            print(f"Args: {args}")
            return command, args
    
    raise ValueError("No appium or bdd-auto-mcp server configuration found in mcp.json")


def setup_recording_directory():
    """Setup directory for screen recordings using environment variables"""
    # Try to get recording directory from environment variable
    recording_dir = os.environ.get('SCREENSHOT_DIR')
    
    if not recording_dir:
        # Fallback to project directory
        project_dir = pathlib.Path(__file__).parent.parent
        recording_dir = project_dir / "recordings"
    else:
        recording_dir = pathlib.Path(recording_dir)
    
    # Create directory if it doesn't exist
    recording_dir.mkdir(parents=True, exist_ok=True)
    
    # Set environment variable for the tools to use
    os.environ['SCREENSHOT_DIR'] = str(recording_dir)
    
    print(f"Screen recordings will be saved to: {recording_dir}")
    return recording_dir


def before_all(context):
    """Initialize MCP session and setup recording directory"""
    import threading
    
    # Setup recording directory
    context.recording_dir = setup_recording_directory()
    context.current_recording = None
    
    # Setup MCP communication queues
    context._task_queue = janus.Queue()
    context._result_queue = janus.Queue()
    context._proj_path = pathlib.Path(__file__).parent.parent
    session_ready = threading.Event()

    def run_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)        
        
        async def mcp_worker():
            try:
                # Load configuration from mcp.json
                command, args = load_mcp_config()
                print(f"Loading MCP server with command: {command}")
                print(f"Args: {args}")
                
                # Define MCP server parameters
                server_params = StdioServerParameters(
                    command=command,
                    args=args
                )
                
                # Connect to server using stdio_client
                async with stdio_client(server_params) as streams:
                    async with ClientSession(*streams) as session:
                        await session.initialize()
                        context.session = session
                        session_ready.set()
                        print("MCP session initialized successfully")

                        while True:
                            task = await context._task_queue.async_q.get()
                            if task is None:
                                break

                            coro = task
                            result = await coro
                            await context._result_queue.async_q.put(result)

            except Exception as e:
                print(f"MCP initialization failed: {repr(e)}")
                session_ready.set()

        loop.run_until_complete(mcp_worker())

    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()

    session_ready.wait()
    print("MCP session setup completed")


def after_all(context):
    """Clean up MCP session"""
    if hasattr(context, "_task_queue"):
        context._task_queue.sync_q.put_nowait(None)
    print("MCP session cleanup completed")


def call_tool_sync(context, coro, timeout=60):
    """Synchronously call MCP tool with timeout"""
    start = time.time()
    context._task_queue.sync_q.put(coro)
    while True:
        try:
            result = context._result_queue.sync_q.get_nowait()
            return result
        except queue.Empty:
            if time.time() - start > timeout:
                raise TimeoutError(f"MCP tool invocation timed out after {timeout} seconds.")
            time.sleep(0.1)


def get_tool_json(result):
    """Extract JSON response from MCP tool result"""
    try:
        if isinstance(result, str):
            return json.loads(result) if result.startswith('{') else {"status": "success", "data": result}
        items = getattr(result, "content", None)
        if items:
            for item in items:
                if getattr(item, "text", None):
                    text = getattr(item, "text", None)
                    return json.loads(text)
    except Exception as e:
        print(f"Error getting tool JSON: {e}")
        print(f"Raw result: {result}")
        
    return {"status": "error", "error": "Failed to parse tool response"}


def start_recording(context, scenario_name):
    """Start screen recording for the scenario"""
    try:
        print(f"🎬 Starting screen recording for scenario: {scenario_name}")
        
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
        if result_json.get("status") == "success":
            print("✅ Screen recording started successfully")
            context.recording_started = True
            context.recording_start_time = datetime.now()
        else:
            print(f"⚠️ Failed to start screen recording: {result_json.get('error', 'Unknown error')}")
            context.recording_started = False
            
    except Exception as e:
        print(f"❌ Exception while starting screen recording: {e}")
        context.recording_started = False


def stop_recording(context, scenario_name, scenario_status):
    """Stop screen recording and save the video"""
    if not getattr(context, 'recording_started', False):
        print("⚠️ No active recording to stop")
        return
        
    try:
        print(f"⏹️ Stopping screen recording for scenario: {scenario_name}")
        
        # Generate filename with scenario name and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_scenario_name = "".join(c for c in scenario_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_scenario_name = safe_scenario_name.replace(' ', '_')
        
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
        if result_json.get("status") == "success":
            video_path = result_json.get("data", {}).get("video_saved", save_path)
            file_size_mb = result_json.get("data", {}).get("file_size_mb", 0)
            
            duration = datetime.now() - getattr(context, 'recording_start_time', datetime.now())
            duration_str = str(duration).split('.')[0]  # Remove microseconds
            
            print(f"✅ Screen recording saved: {video_path}")
            print(f"   📁 File size: {file_size_mb} MB")
            print(f"   ⏱️  Duration: {duration_str}")
            
            context.current_recording = video_path
        else:
            print(f"⚠️ Failed to stop screen recording: {result_json.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Exception while stopping screen recording: {e}")
    finally:
        context.recording_started = False


def before_scenario(context, scenario):
    """Setup before each scenario - start recording only"""
    context.scenario = scenario
    scenario_name = scenario.name
    
    print(f"\n🚀 Starting scenario: {scenario_name}")
    
    # Start screen recording
    # Note: App launch/close is handled within test cases
    start_recording(context, scenario_name)


def after_scenario(context, scenario):
    """Cleanup after each scenario - stop recording only"""
    scenario_name = scenario.name
    scenario_status = scenario.status.name.lower()  # passed, failed, skipped
    
    print(f"\n🏁 Finishing scenario: {scenario_name} (Status: {scenario_status})")
    
    # Stop screen recording
    # Note: App launch/close is handled within test cases
    stop_recording(context, scenario_name, scenario_status)
    
    print(f"✅ Scenario cleanup completed: {scenario_name}")


def before_step(context, step):
    """Optional: Log step start (uncomment if needed)"""
    # print(f"  🔹 Step: {step.name}")
    pass


def after_step(context, step):
    """Optional: Log step completion and handle failures (uncomment if needed)"""
    # step_status = step.status.name.lower()
    # if step_status == "failed":
    #     print(f"  ❌ Step failed: {step.name}")
    # else:
    #     print(f"  ✅ Step passed: {step.name}")
    pass
