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

# --- auto-generated step ---
@when('I navigate to "https://www.github.com"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'text': 'https://www.github.com', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@when('I right click on the "https://www.github.com" website in Favorites hub')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="right_click_element", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeOutlineRow[@title="GitHub · Build and ship software on a single, collaborative platform · GitHub"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('"github" should disappear in my favorites list')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_not_exists", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeOutlineRow[@title="GitHub · Build and ship software on a single, collaborative platform · GitHub"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 


# --- auto-generated step ---
@step('I click "Delete" button in the drop-down menu')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Delete', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0, 'step': 'And I click "Delete" button in the drop-down menu'}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I click "Favorites" to open Favorite pane')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Favorites', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0, 'step': 'And I click "Favorites" to open Favorite pane'}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Finding Github item in favorites')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': 'GitHub · Build and ship software on a single, collaborative platform · GitHub', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I drag the "Github" item to the top of "copilot" item')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="drag_element_to_element", arguments={'caller': 'behave-automation', 'source_xpath': "//XCUIElementTypeOutlineRow[@title='GitHub · Build and ship software on a single, collaborative platform · GitHub']", 'target_xpath': "//XCUIElementTypeOutlineRow[@title='Copilot']", 'drop_position': 'top', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('the favorites item order should be "Github", "Copilot"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_elements_order", arguments={'caller': 'behave-automation', 'element_xpaths': ["//XCUIElementTypeOutlineRow[@title='GitHub · Build and ship software on a single, collaborative platform · GitHub']", "//XCUIElementTypeOutlineRow[@title='Copilot']"], 'expected_orders': [0, 1], 'direction': 'vertical', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 
