
from behave import *
import logging
from features.environment import call_tool_sync, get_tool_json

# --- auto-generated step ---
@step('Launch Edge')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="app_launch", 
        arguments={'arguments': None, 'caller': 'behave-automation'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Click address bar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'ACCESSIBILITY_ID',
            'locator_value': 'Address and search bar'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Enter Wikipedia URL')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="send_keys_on_macos", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'ACCESSIBILITY_ID',
            'locator_value': 'Address and search bar',
            'text': 'https://www.wikipedia.org'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Press Enter to navigate')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="press_key", 
        arguments={'caller': 'behave-automation', 'key': 'return'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Wait for page to load')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="time_sleep", 
        arguments={'caller': 'behave-automation', 'seconds': 3}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Right click on Wikipedia tab')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="right_click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'XPATH',
            'locator_value': "//XCUIElementTypeTab[@label='Wikipedia']"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Click Duplicate Tab menu item')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'XPATH',
            'locator_value': "//XCUIElementTypeMenuItem[@title='Duplicate Tab']"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Verify both tabs show same URL')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_attribute", 
        arguments={'attribute_name': 'value',
            'caller': 'behave-automation',
            'expected_value': 'https://www.wikipedia.org',
            'locator_strategy': 'ACCESSIBILITY_ID',
            'locator_value': 'Address and search bar',
            'rule': '=='}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Close Edge after recording')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="app_close", 
        arguments={'caller': 'behave-automation'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 
