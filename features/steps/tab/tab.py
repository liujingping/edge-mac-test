from behave import *
import logging
from features.environment import call_tool_sync, get_tool_json


# --- auto-generated step ---
@when('I new a tab and navigate to "https://www.apple.com"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeButton[@label='New Tab']",
                'locator_strategy': 'AppiumBy.XPATH',
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
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeTextField[@label='Address and search bar']",
                'locator_strategy': 'AppiumBy.XPATH',
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
                'locator_value': "//XCUIElementTypeTextField[@label='Address and search bar']",
                'locator_strategy': 'AppiumBy.XPATH',
                'text': 'https://www.apple.com',
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
            name='app_state',
            arguments={
                'caller': 'behave-automation',
                'locator_value': '',
                'locator_type': '',
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
            name='find_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeTab[@selected='true' and contains(@label, 'Apple')]",
                'locator_strategy': 'AppiumBy.XPATH',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click the "Close Tab" button on tab header')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeTab[@label='Apple' and @selected='true']//XCUIElementTypeButton[@label='Close tab']",
                'locator_strategy': 'AppiumBy.XPATH',
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
            name='app_state',
            arguments={
                'caller': 'behave-automation',
                'locator_value': '',
                'locator_type': '',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "Apple" tab should be closed')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_not_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeTab[@label='Apple']",
                'locator_strategy': 'AppiumBy.XPATH',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I navigate to "https://www.apple.com"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeTextField[@label='Address and search bar']",
                'locator_strategy': 'AppiumBy.XPATH',
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
                'locator_value': "//XCUIElementTypeTextField[@label='Address and search bar']",
                'locator_strategy': 'AppiumBy.XPATH',
                'text': 'https://www.apple.com',
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
                'key': 'return',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I navigate to "https://www.youtube.com"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': 'Address and search bar',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
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
                'locator_value': "//XCUIElementTypeTextField[@label='Address and search bar']",
                'locator_strategy': 'AppiumBy.XPATH',
                'text': 'https://www.youtube.com',
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
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': '//XCUIElementTypeWebView',
                'locator_strategy': 'AppiumBy.XPATH',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I right click on the tab header of "Youtube" tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='right_click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeTab[@label='YouTube']",
                'locator_strategy': 'AppiumBy.XPATH',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "Refresh" from the context menu')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeMenuItem[@label='Refresh ⌘R ⌘R']",
                'locator_strategy': 'AppiumBy.XPATH',
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
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeWebView[@title='YouTube']",
                'locator_strategy': 'AppiumBy.XPATH',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the page should be refreshed')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeStaticText[@value='Try searching to get started']",
                'locator_strategy': 'AppiumBy.XPATH',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('the address bar still displays the complete URL "https://www.youtube.com"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeTextField[@label='Address and search bar' and @value='https://www.youtube.com']",
                'locator_strategy': 'AppiumBy.XPATH',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click the "Close Tab" button on the "Apple" tab header')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeTab[@label='Apple']//XCUIElementTypeButton[@label='Close tab']",
                'locator_strategy': 'AppiumBy.XPATH',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I press "cmd+shift+t" to reopen the closed tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='press_key',
            arguments={
                'caller': 'behave-automation',
                'key': 'command+shift+t',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "Apple" tab should be reopened')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_value': "//XCUIElementTypeTab[@label='Apple']",
                'locator_strategy': 'AppiumBy.XPATH',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I new a tab and navigate to "https://www.google.com"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'New Tab',
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
            name='directly_send_keys',
            arguments={
                'caller': 'behave-automation',
                'need_snapshot': 0,
                'text': 'https://www.google.com',
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
@step('I drag the "Google" tab to the far left of the "Apple" tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='drag_element_to_element',
            arguments={
                'caller': 'behave-automation',
                'drop_position': 'left_edge',
                'need_snapshot': 0,
                'source_xpath': "//XCUIElementTypeTab[@label='Google']",
                'target_xpath': "//XCUIElementTypeTab[@label='Apple']",
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('"Google" tab is on the left of the "Apple" tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_elements_order',
            arguments={
                'caller': 'behave-automation',
                'direction': 'horizontal',
                'element_xpaths': [
                    "//XCUIElementTypeTab[@label='Google']",
                    "//XCUIElementTypeTab[@label='Apple']",
                ],
                'expected_orders': [],
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I new a tab and navigate to "https://www.google.com/"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'New Tab',
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
                'text': 'https://www.google.com/',
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
@step('Close the edit tab group dialog')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='press_key',
            arguments={
                'caller': 'behave-automation',
                'key': 'escape',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('Close edit tab group dialog')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='press_key',
            arguments={
                'caller': 'behave-automation',
                'key': 'escape',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "Add tab to new group" from the right-click context menu')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Add Tab to New Group',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I new a tab and navigate to "https://www.youtube.com"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'New Tab',
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
                'text': 'https://www.youtube.com',
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
@then('a new tab group should be created with the "Youtube" tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'YouTube tab group ("YouTube") - Expanded',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('the tab group should be named "YouTube"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_attribute',
            arguments={
                'attribute_name': 'label',
                'caller': 'behave-automation',
                'expected_value': 'YouTube tab group ("YouTube") - Expanded',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'YouTube tab group ("YouTube") - Expanded',
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
@step('I right click on the tab header of "bing" tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='right_click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeTab[@label='Search - Microsoft Bing']",
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "Open new tab to the right" from the right-click context menu')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'New Tab to the Right',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('a new tab should be opened to the right of the "bing" tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeTab[@value='1' and @label='New Tab' and "
                "@selected='true']",
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "Turn on vertical tabs" from the right-click context menu')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.NAME',
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
@step('I click "Close tab" from the right-click context menu')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.NAME',
                'locator_value': 'Close Tab ⌘W ⌘W',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "bing" tab should be closed')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_not_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeTab[@label='Search - Microsoft Bing']",
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click on the Address and search bar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.NAME',
                'locator_value': 'Address and search bar',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I right click on the tab header of "New Tab" tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='right_click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeTab[@value='1' and @label='New Tab']",
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I press "cmd+w"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='press_key',
            arguments={
                'caller': 'behave-automation',
                'key': 'command+w',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "New Tab" tab should be closed')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_not_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeTab[@label='New Tab' and @selected='true' "
                "and count(//XCUIElementTypeTab[@label='New Tab']) = 1]",
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click the "Refresh" button on the toolbar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeButton[@label="Refresh"]',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I right click on the tab header of "Apple" tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='right_click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeTab[@label='Apple']",
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I right click on the "Search - Microsoft Bing" tab on the vertical tab bar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='find_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.NAME',
                'locator_value': 'Search - Microsoft Bing',
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
            name='right_click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeTabGroup[@label='Tab "
                "bar']//XCUIElementTypeTab[@value='1'][@label='Search - "
                "Microsoft Bing']",
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "Pin tab" from the right-click context menu')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.NAME',
                'locator_value': 'Pin Tab',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "bing" tab should be pinned')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_attribute',
            arguments={
                'attribute_name': 'title',
                'caller': 'behave-automation',
                'expected_value': 'Search - Microsoft Bing - Pinned - Microsoft Edge Canary',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeGroup[@title='Search - Microsoft Bing - "
                "Pinned - Microsoft Edge Canary']",
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
@then('the address bar should contains "www.bing.com"')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_attribute',
            arguments={
                'attribute_name': 'value',
                'caller': 'behave-automation',
                'expected_value': 'https://www.bing.com',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeTextField[@label='Address and search bar']",
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
@step('I right click on the tab header of "Search - Microsoft Bing" tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='right_click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeTab[@label='Search - Microsoft Bing']",
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I press escape to close popup')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='press_key',
            arguments={
                'caller': 'behave-automation',
                'key': 'escape',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click the "Search - Microsoft Bing" tab in the vertical tab bar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeTab[@value="1"]',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )
