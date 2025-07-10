
from behave import *
import logging
from features.environment import call_tool_sync, get_tool_json

# --- auto-generated step ---
@given('Edge is launched')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="app_launch", arguments={'caller': 'behave-automation', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@when('I navigate to "https://www.bing.com"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'text': 'https://www.bing.com', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': '_XCUI:CloseWindow', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'escape', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'command+a', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'text': 'https://www.bing.com', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'escape', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': '_XCUI:CloseWindow', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="session_close", arguments={'caller': 'behave-automation', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@when('I input "www.163.com" in address bar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'text': 'www.163.com', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I press the "Enter" key')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Checking address bar content')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Clicking address bar to focus')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Closing file dialog')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'CancelButton', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('"163" website should be opened')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': '网易', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('the address bar should display the complete URL "https://www.163.com"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 


# --- auto-generated step ---
@step('I open a new tab')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'command+t', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@when('I input "cat" in address bar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.NAME', 'text': 'cat', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('the tab should jump to the search results page related to "cat"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': "//*[contains(@label, 'Search') or contains(@title, 'cat - Search')]", 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('the "cat" should be displayed in the Bing search box')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeSearchField[@value="cat"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@given('Edge is launched in horizontal mode')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="app_launch", arguments={'caller': 'behave-automation', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@when('I navigate to "https://www.microsoft.com"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'text': 'https://www.microsoft.com', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': 'Close tab', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I click the "Close Tab" button on tab header')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Close tab', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('the "Microsoft Bing" tab should be closed')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_not_exists", arguments={'caller': 'behave-automation', 'locator_value': 'Microsoft Bing', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@when('I navigate to "https://getsamplefiles.com/download/pdf/sample-1.pdf"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'escape', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'command+a', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="directly_send_keys", arguments={'caller': 'behave-automation', 'text': 'https://getsamplefiles.com/download/pdf/sample-1.pdf', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('the Downloads pane should appear')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': 'Downloads', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@when('I navigate to "edge://downloads"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'escape', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'command+a', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="directly_send_keys", arguments={'caller': 'behave-automation', 'text': 'edge://downloads', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('"sample-1.pdf" should appear in download list')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': 'sample-1.pdf', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I click the "Add this page to favorites" icon in the address bar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Add this page to favorites (⌘D)', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I click "Done" button in the favorites dialog')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Done', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
# @when('I Press "alt+cmd+B" to open Favorite bar')
# # # def step_impl(context):
#     result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'alt+cmd+b', 'need_snapshot': 0}))
#     result_json = get_tool_json(result)
#     assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

#     result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': 'Microsoft', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
#     result_json = get_tool_json(result)
#     assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('"Microsoft" should appear in my favorites list')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': 'Microsoft - AI、クラウド、生産性向上、コンピューティング、ゲーム、アプリ', 'locator_strategy': 'AppiumBy.NAME', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
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

# --- auto-generated step ---
@then('the "Apple" tab should be closed')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="verify_element_not_exists", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeTab[@label="Apple"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I new a tab and navigate to "https://bing.com"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeButton[@label="New Tab"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'text': 'https://bing.com', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I drag the Bing tab to the far left of the Apple tab')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeTab[@value="1"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeTab[@value="1"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeTab[@value="0"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I Press "alt+cmd+B" to open Favorite bar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'alt+cmd+B', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Find Apple website in Favorites hub')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': 'Apple', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@when('I right click on the "Apple" website in Favorites hub')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': '//XCUIElementTypeStaticText[@value="Apple"]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'control', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'alt+cmd+b', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@when('I input "www.baidu.com" in address bar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'text': 'www.baidu.com', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I press enter')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'Return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('"Baidu" website should be opened')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': '//*[contains(@title, "百度") or contains(@label, "百度") or contains(@title, "Baidu") or contains(@label, "Baidu")]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Close', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': '//*[contains(@title, "百度") or contains(@label, "百度") or contains(@title, "Baidu") or contains(@label, "Baidu")]', 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I new a tab and navigate to "https://163.com"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(name="find_element", arguments={'caller': 'behave-automation', 'locator_value': 'New Tab', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'command+t', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="send_keys", arguments={'caller': 'behave-automation', 'locator_value': 'Address and search bar', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'text': 'https://163.com', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="press_key", arguments={'caller': 'behave-automation', 'key': 'return', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="verify_element_exists", arguments={'caller': 'behave-automation', 'locator_value': "//XCUIElementTypeTab[@value='1' and contains(@label, '网易')]", 'locator_strategy': 'AppiumBy.XPATH', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

    result = call_tool_sync(context, context.session.call_tool(name="click_element", arguments={'caller': 'behave-automation', 'locator_value': 'Close', 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID', 'need_snapshot': 0}))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 
