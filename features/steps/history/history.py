from behave import *
import logging
from features.environment import call_tool_sync, get_tool_json


# --- auto-generated step ---
@when('I navigate to "https://www.cgtn.com" in address bar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='send_keys',
            arguments={
                'caller': 'behave-automation',
                'locator_value': 'Address and search bar',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'text': 'https://www.cgtn.com',
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
@then('the "cgtn" website should be opnened')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_value': '//XCUIElementTypeTab[@label="CGTN | Breaking News, China News, World News and Video"]',
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
@when('I click "Settings and more" button in toolbar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': 'Settings and more',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "History" button')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': 'History ⌘Y ⌘Y',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

    # Add a small wait to ensure the History panel has time to appear
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='time_sleep',
            arguments={'caller': 'behave-automation', 'need_snapshot': 0, 'seconds': 1},
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I hover over the "cgtn" website in History panel')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='mouse_hover',
            arguments={
                'caller': 'behave-automation',
                'locator_value': '//XCUIElementTypeStaticText[@value="CGTN | Breaking News, China News, World News and Video"]',
                'locator_strategy': 'AppiumBy.XPATH',
                'duration': 1.0,
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "Delete" button in History panel')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': 'Delete',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "cgtn" website should not be displayed in History panel')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_not_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_value': '//XCUIElementTypeStaticText[@value="CGTN | Breaking News, China News, World News and Video"]',
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
@step('I right click "History" button in menu')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='right_click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': 'History ⌘Y ⌘Y',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "Show in toolbar" in menu')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': 'Show in Toolbar',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('"History" should be displayed in toolbar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_value': 'History',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I navigate to "https://www.cgtn.com"')
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
                'locator_value': 'Address and search bar',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'text': 'https://www.cgtn.com',
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
@step('I input "cgtn" in Search history box')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': 'Search history',
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
                'locator_value': 'Search history',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'text': 'cgtn',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I input "mscaaa" in Search history box')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_value': 'Clear search',
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
                'locator_value': 'Search history',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'text': 'mscaaa',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "cgtn" website should be displayed in History panel')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeStaticText[@value='CGTN']",
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('shows "No results found for \'mscaaa\'" in History panel')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='find_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeStaticText[contains(@value, 'No results found')]",
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
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeStaticText[@value="No results found for \'mscaaa\'"]',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "Close tab" button on the "cgtn" tab')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeTab[@label="CGTN | Breaking News, China '
                'News, World News and '
                'Video"]//XCUIElementTypeButton[@label="Close tab"]',
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
            arguments={'caller': 'behave-automation', 'need_snapshot': 0, 'seconds': 2},
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "cgtn" tab cannot be found in the tab bar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_not_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeTab[@label="CGTN | Breaking News, China '
                'News, World News and Video"]',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I press "cmd" and "Y" keys')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='press_key',
            arguments={
                'caller': 'behave-automation',
                'key': 'cmd+y',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "Recently closed" in History panel')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeTab[@title="Recently Closed"]',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "cgtn" website should be displayed in "Recently closed" in History panel')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeStaticText[@value="CGTN | Breaking News, '
                'China News, World News and Video"]',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "cgtn" website should be displayed in "All" in History panel')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.NAME',
                'locator_value': 'All',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I click "cgtn" website in "All" in History panel')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.NAME',
                'locator_value': 'CGTN | Breaking News, China News, World News and Video',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('the "cgtn" website should be opened')
def step_impl(context):
    # Wait for page to load
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
    
    # Verify that the CGTN website is opened by checking the tab title or URL
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_value': '//XCUIElementTypeTab[contains(@label,"CGTN")]',
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
@then('History panel should appear')
def step_impl(context):
    # Add a small wait to ensure the panel has time to appear
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='time_sleep',
            arguments={'caller': 'behave-automation', 'need_snapshot': 0, 'seconds': 1},
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

    # The History panel should contain a "Pin history" button which indicates it's open
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Pin history',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "Pin history" button in History panel')
def step_impl(context):
    # When History panel first opens, we should click "Pin history" button
    # Try ACCESSIBILITY_ID first, then fallback to NAME if needed
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Pin history',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)

    # If ACCESSIBILITY_ID fails, try NAME strategy
    if result_json.get('status') != 'success':
        result = call_tool_sync(
            context,
            context.session.call_tool(
                name='click_element',
                arguments={
                    'caller': 'behave-automation',
                    'locator_strategy': 'AppiumBy.NAME',
                    'locator_value': 'Pin history',
                    'need_snapshot': 0,
                },
            ),
        )
        result_json = get_tool_json(result)

    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('History pane still should be displayed')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.NAME',
                'locator_value': 'Side pane',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "Close history" button in History pane')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.NAME',
                'locator_value': 'Close history',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('History pane should be displayed')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Side pane',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('Wait for history panel to appear')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='time_sleep',
            arguments={'caller': 'behave-automation', 'need_snapshot': 0, 'seconds': 2},
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "History" in toolbar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeButton[@label="History"]',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('History panel should be closed')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_not_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeWindow[@title="History"]',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )
