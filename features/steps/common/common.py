from behave import given, when, then, step
from features.environment import call_tool_sync, get_tool_json


@given('Edge is launched')
def step_impl(context):
    print("DEBUG: Executing 'Edge is launched' step")
    result = call_tool_sync(context, context.session.call_tool(name="app_launch", arguments={'caller': 'behave-automation', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

