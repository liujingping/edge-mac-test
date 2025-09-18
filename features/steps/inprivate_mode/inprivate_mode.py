
from behave import *
import logging
from features.environment import call_tool_sync, get_tool_json



# --- auto-generated step ---
@step('I click "New InPrivate Window" button')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
            'locator_value': 'New InPrivate Window ⇧⌘N ⇧⌘N',
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 


# --- auto-generated step ---
@step('I click "InPrivate" button in toolbar')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.NAME',
            'locator_value': 'InPrivate browsing',
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('I click "Close InPrivate Window" button')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.NAME',
            'locator_value': 'Close InPrivate Window',
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('InPrivate Window should be closed')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_not_exists", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.NAME',
            'locator_value': 'InPrivate browsing',
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@then('"https://www.apple.com" should not be displayed in History panel')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_not_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_value': '//XCUIElementTypeStaticText[@value="https://www.apple.com"]',
                'locator_strategy': 'AppiumBy.XPATH',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )
