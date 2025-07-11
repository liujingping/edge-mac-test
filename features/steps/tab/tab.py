# --- auto-generated step ---
@given('Edge is launched in horizontal mode')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="app_launch", arguments={'caller': 'behave-automation', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

@when('I navigate to "https://www.apple.com"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'text': 'https://www.apple.com', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeTab[@label="Apple" or contains(@label, "Apple")]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

@step('I click the "Close Tab" button on tab header')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Close tab', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

@then('the "Apple" tab should be closed')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_not_exists", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeTab[@label="Apple"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 
