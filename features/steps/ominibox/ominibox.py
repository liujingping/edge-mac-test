from behave import given, when, then, step
from features.environment import call_tool_sync, get_tool_json


@when('I input "www.163.com" in address bar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'text': 'www.163.com', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

@step('I press the "Enter" key')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

@then('"163" website should be opened')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': '网易', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 


@step('the address bar should display the complete URL "https://www.163.com"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

@step('I open a new tab')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'command+t', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

@when('I input "cat" in address bar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.NAME', 'text': 'cat', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

@then('the tab should jump to the search results page related to "cat"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': "//*[contains(@label, 'Search') or contains(@title, 'cat - Search')]", 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

@step('the "cat" should be displayed in the Bing search box')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeSearchField[@value="cat"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 
