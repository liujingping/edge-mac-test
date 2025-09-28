
from behave import *
import logging
from features.environment import call_tool_sync, get_tool_json


# --- auto-generated step ---
@step('I press "ctrl+cmd+f" keys to enter full screen mode')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="press_key", 
        arguments={'caller': 'behave-automation', 'key': 'ctrl+cmd+f', 'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 


# --- auto-generated step ---
@when('I press "ctrl+cmd+f" keys to exit full screen mode')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="press_key", 
        arguments={'caller': 'behave-automation', 'key': 'ctrl+cmd+f', 'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 


# --- auto-generated step ---
@step('I click "Exit Full Screen" button from the dropdown menu')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
            'locator_value': 'Exit Full Screen',
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 



# --- auto-generated step ---
@then('verify the tooltip text contains "Move & Resize"')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_attribute", 
        arguments={'attribute_name': 'title',
            'caller': 'behave-automation',
            'expected_value': 'Move & Resize',
            'locator_strategy': '',
            'locator_value': 'Move & Resize',
            'need_snapshot': 0,
            'rule': 'contains'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 



# --- auto-generated step ---
@step('I move the mouse to the top left corner and hover on the Zoom button in the small screen')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="mouse_hover", 
        arguments={'caller': 'behave-automation',
            'duration': 1.0,
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeButton[@identifier='_XCUI:FullScreenWindow']",
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 


# --- auto-generated step ---
@step('move the mouse to the top left corner and hover on the Zoom button in the small screen')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="mouse_hover", 
        arguments={'caller': 'behave-automation',
            'duration': 2.0,
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeButton[@identifier='_XCUI:FullScreenWindow']",
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('click "Full Screen" button from the dropdown menu')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeMenuItem[@title='Full Screen']",
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('click "Entire Screen" button from next dropdown menu')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeMenuItem[@title='Entire Screen']",
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 


# --- auto-generated step ---
@step('I input "aaaaaa" in Search history box')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="send_keys", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
            'locator_value': 'Search history',
            'need_snapshot': 0,
            'text': 'aaaaaa'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('shows No results found for "aaaaaa" in History panel')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        
        name="verify_element_attribute", 
        arguments={'attribute_name': 'value',
            'caller': 'behave-automation',
            'expected_value': 'No results found',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeStaticText[contains(@value, 'No results "
                             "found')]",
            'need_snapshot': 0,
            'rule': 'contains'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 


# --- auto-generated step ---
@when('I click the Zoom button on the top left corner in small screen')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
            'locator_value': '_XCUI:FullScreenWindow',
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 


# --- auto-generated step ---
@step('I click the Zoom button on the top left corner in full screen')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeButton[@identifier='_XCUI:ZoomWindow']",
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 
