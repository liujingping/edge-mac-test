import json
import time
import threading
import asyncio
import janus
import queue
import pathlib
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters

session_ready = threading.Event()
TRANSPORT = "stdio"  # Default transport method, can be changed to "sse" if needed

def load_mcp_config():
    current_dir = pathlib.Path(__file__).parent.parent
    mcp_config_path = current_dir / ".vscode" / "mcp.json"
    
    if not mcp_config_path.exists():
        raise FileNotFoundError(f"MCP config file not found: {mcp_config_path}")
    
    with open(mcp_config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Find server configuration starting with bdd-auto-mcp
    servers = config.get("servers", {})
    for server_name, server_config in servers.items():
        if server_name.startswith("bdd-auto-mcp"):
            command = server_config.get("command")
            args = server_config.get("args", [])
            print(f"Found MCP server configuration: command={command}")
            print(f"Found MCP server configuration: args={args}")
            return command, args
    
    raise ValueError("No bdd-auto-mcp server configuration found in mcp.json")


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
                if TRANSPORT == "stdio":
                    print("Using stdio transport for MCP server")
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

                            while True:
                                task = await context._task_queue.async_q.get()
                                if task is None:
                                    break

                                coro = task
                                result = await coro
                                await context._result_queue.async_q.put(result)
                else:
                    print("Using SSE transport for MCP server")
                    # Connect to server using sse_client
                    print("Connecting to SSE server at http://localhost:8000/sse")
                    async with sse_client("http://localhost:8000/sse") as streams:
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
                print(f"MCP init failed: {repr(e)}")
                session_ready.set()

        loop.run_until_complete(mcp_worker())

    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()

    session_ready.wait()




def after_all(context):
    if hasattr(context, "_task_queue"):
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
                raise TimeoutError("MCP tool invocation timed out.")
            time.sleep(0.1)


def get_tool_json(result):
    try:
        if isinstance(result, str):
            return result
        items = getattr(result, "content", None)
        if items:
            for item in items:
                if getattr(item, "text", None):
                    text = getattr(item, "text", None)
                    return json.loads(text)
    except Exception as e:
        print(f"Error getting tool JSON: {e}")
        
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
        #Allow the test to continue even if this fails
        pass

def after_scenario(context, scenario):
    # context.scenario = scenario
    # try:
    #     result = call_tool_sync(context, context.session.call_tool(name="app_close", arguments={"caller": "behave"}), timeout=60)
    #     # Add error checking
    #     tool_json = get_tool_json(result)
    #     if tool_json and tool_json.get("status") != "success":
    #         print(f"Warning: app_close failed with error: {tool_json.get('error')}")
    # except TimeoutError as e:
    #     print(f"Warning: app_close timed out: {str(e)}")
    #     # Continue even if this fails
    #     pass
    # except Exception as e:
    #     print(f"Warning: app_close error: {str(e)}")
    #     # Continue even if this fails
        pass
