from behave import given, when, then, step
from features.environment import call_tool_sync, get_tool_json


# --- auto-generated step ---
@step('I click the "Add this page to favorites" icon in the address bar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Add this page to favorites (⌘D)', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

@step('I click "Done" button in the favorites dialog')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Done', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I Press "alt+cmd+B" to open Favorite bar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'alt+cmd+B', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('"Microsoft" should appear in my favorites list')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': 'Microsoft - AI、クラウド、生産性向上、コンピューティング、ゲーム、アプリ', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 
