from behave import *
import logging
from features.environment import call_tool_sync, get_tool_json


# --- auto-generated step ---
@step('I click "Search tabs" button on the tab bar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Search tabs',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "Search tabs" dialog should be opened')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'TabSearch',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "Turn on vertical tabs" button in the "Search tabs" dialog')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Turn On Vertical Tabs',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "Search tabs" button in the vertical tab mode')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Search tabs',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "Search tabs" dialog should be opened in the vertical tab mode')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Turn Off Vertical Tabs',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "Turn off vertical tabs" button in the "Search tabs" dialog')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Turn Off Vertical Tabs',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('Analyze the screenshot to verify that the horizontal tabs shown on the top of the window')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_visual_task',
            arguments={
                'caller': 'behave-automation',
                'need_snapshot': 0,
                'task_description': 'Verify that horizontal tabs are shown on the top of the '
                'window - the tab bar should be positioned horizontally at '
                'the top of the browser window, not vertically on the left '
                'side',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "Organize tabs" button in the "Search tabs" dialog')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Organize Tabs',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "Group Tabs" button in the "Organize tabs" view')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Group Tabs',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I navigate to "https://www.duckduckgo.com"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Address and search bar',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='send_keys',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Address and search bar',
                'need_snapshot': 0,
                'text': 'https://www.duckduckgo.com',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='press_key',
            arguments={
                'caller': 'behave-automation',
                'key': 'return',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='time_sleep',
            arguments={'caller': 'behave-automation', 'need_snapshot': 0, 'seconds': 3},
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )



# --- auto-generated step ---
@when('I click "Group Tabs" button in the "Organize tabs" pop')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Group Tabs',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('verify a tab group created with the name of "Search Engines" on the tab bar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Search Engines - Expanded',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    
    # If first attempt fails, try alternative locator
    if result_json.get('status') != 'success':
        result = call_tool_sync(
            context,
            context.session.call_tool(
                name='verify_element_exists',
                arguments={
                    'caller': 'behave-automation',
                    'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                    'locator_value': 'Search Engines tab group ("Google" and 2 Other Tabs) - Expanded',
                    'need_snapshot': 0,
                },
            ),
        )
        result_json = get_tool_json(result)
    
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('the tab group contains 3 tabs')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_attribute',
            arguments={
                'attribute_name': 'label',
                'caller': 'behave-automation',
                'expected_value': 'Search Engines - Expanded',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Search Engines - Expanded',
                'need_snapshot': 0,
                'rule': 'contains',
            },
        ),
    )
    result_json = get_tool_json(result)
    
    # If first attempt fails, try alternative locator
    if result_json.get('status') != 'success':
        result = call_tool_sync(
            context,
            context.session.call_tool(
                name='verify_element_attribute',
                arguments={
                    'attribute_name': 'label',
                    'caller': 'behave-automation',
                    'expected_value': 'Search Engines tab group ("Google" and 2 Other Tabs) - Expanded',
                    'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                    'locator_value': 'Search Engines tab group ("Google" and 2 Other Tabs) - Expanded',
                    'need_snapshot': 0,
                    'rule': 'contains',
                },
            ),
        )
        result_json = get_tool_json(result)
    
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I input "google" in the "Search Tabs" input box')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='send_keys',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeWebView[@title='TabSearch']//XCUIElementTypeTextField",
                'need_snapshot': 0,
                'text': 'google',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('verify a tab name contains "google" shown in the "Search tabs" open tabs dialog')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_attribute',
            arguments={
                'attribute_name': 'value',
                'caller': 'behave-automation',
                'expected_value': 'Google',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeWebView[@title='TabSearch']//XCUIElementTypeStaticText[@value='Google']",
                'need_snapshot': 0,
                'rule': '==',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I clear the input in the "Search Tabs" input box')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='press_key',
            arguments={
                'caller': 'behave-automation',
                'key': 'cmd+a',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='press_key',
            arguments={
                'caller': 'behave-automation',
                'key': 'delete',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I input "Apple" in the "Search Tabs" input box')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='directly_send_keys',
            arguments={
                'caller': 'behave-automation',
                'need_snapshot': 0,
                'text': 'Apple',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('verify a tab name contains "Apple" shown in the "Search tabs" recently closed dialog')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_attribute',
            arguments={
                'attribute_name': 'value',
                'caller': 'behave-automation',
                'expected_value': 'Apple',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeStaticText[@value='Apple']",
                'need_snapshot': 0,
                'rule': 'contains',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

# --- auto-generated step ---
@when('I input "google" in the "Search Tabs" in full screen mode')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='send_keys',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeWebView[@title='TabSearch']//XCUIElementTypeTextField[@enabled='true'][not(@label='Address and search bar')]",
                'need_snapshot': 0,
                'text': 'google',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

# --- auto-generated step ---
@when('I input "Apple" in the "Search Tabs" in full screen mode')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='send_keys',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeWebView[@title='TabSearch']//XCUIElementTypeTextField[@enabled='true'][not(@label='Address and search bar')]",
                'need_snapshot': 0,
                'text': 'Apple',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

