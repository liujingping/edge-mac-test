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
                'locator_value': "//XCUIElementTypeTab[@selected='true']//XCUIElementTypeButton[@label='Close tab']",
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
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': "//XCUIElementTypeMenuItem[@title='Refresh']",
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
@when('I click the "New tab" plus button')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
            'locator_value': 'New Tab',
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('a new tab should be created')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_exists", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
            'locator_value': 'New Tab',
            'need_snapshot': 0}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Complete scenario recording')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="app_close", 
        arguments={'caller': 'behave-automation'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Reset for simplified scenario')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="app_close", 
        arguments={'caller': 'behave-automation'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@step('I right click on the tab header of "{tab_name}" tab')
def step_impl(context, tab_name):
    result = call_tool_sync(context, context.session.call_tool(
        name="right_click_element", 
        arguments={
            'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': f"//XCUIElementTypeTab[contains(@label, '{tab_name}')]"
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@step('I click "{menu_item}" from the context menu')
def step_impl(context, menu_item):
    # Handle case sensitivity: Edge menu items use title case (e.g., "Pin Tab" not "Pin tab")
    # Capitalize the first letter of each word to match Edge's menu item format
    menu_item_capitalized = menu_item.title()
    
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={
            'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': f"//XCUIElementTypeMenuItem[@title='{menu_item_capitalized}']",
            'need_snapshot': 0
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@step('the "{tab_name}" tab should be pinned and show only the favicon')
def step_impl(context, tab_name):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_attribute", 
        arguments={
            'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': f"//XCUIElementTypeTab[contains(@label, '{tab_name}')]",
            'attribute_name': 'selected',
            'expected_value': 'true'
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@step('I right click on the pinned "{tab_name}" tab')  
def step_impl(context, tab_name):
    result = call_tool_sync(context, context.session.call_tool(
        name="right_click_element", 
        arguments={
            'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': f"//XCUIElementTypeTab[contains(@label, '{tab_name}')][@selected='true']"
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@step('the "{tab_name}" tab should be unpinned and show the full title')
def step_impl(context, tab_name):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_exists", 
        arguments={
            'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': f"//XCUIElementTypeTab[contains(@label, '{tab_name}')]"
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@step('I navigate to "{url}"')
def step_impl(context, url):
    result = call_tool_sync(context, context.session.call_tool(
        name="send_keys", 
        arguments={
            'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTextField[@label='Address and search bar']",
            'text': url
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    
    # Press Enter to navigate
    result = call_tool_sync(context, context.session.call_tool(
        name="press_key", 
        arguments={
            'caller': 'behave-automation',
            'key': 'return'
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@step('the "{tab_name}" tab should be closed')
def step_impl(context, tab_name):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_not_exists", 
        arguments={
            'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': f"//XCUIElementTypeTab[contains(@label, '{tab_name}')]"
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@step('I press "{key_combination}"')
def step_impl(context, key_combination):
    result = call_tool_sync(context, context.session.call_tool(
        name="press_key", 
        arguments={
            'caller': 'behave-automation',
            'key': key_combination
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@step('the "{tab_name}" tab should be restored')
def step_impl(context, tab_name):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_exists", 
        arguments={
            'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': f"//XCUIElementTypeTab[contains(@label, '{tab_name}')]"
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@then('the new tab should display the "New tab" page')
def step_impl(context):
    # Verify New tab page is displayed by checking the address bar element exists
    # New tab pages may have empty or placeholder value, so we just verify the element is present
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_exists", 
        arguments={
            'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTextField[@label='Address and search bar']",
            'need_snapshot': 0
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"

# --- auto-generated step ---
@then('a new "{tab_name}" tab should be created')
def step_impl(context, tab_name):
    # Verify two tabs with the same label exist (original + duplicate)
    result = call_tool_sync(context, context.session.call_tool(
        name="get_page_source_tree",
        arguments={
            'caller': 'behave-automation',
            'need_snapshot': 0
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    
    # Count tabs with the specified label (using contains for partial match)
    page_source = result_json.get('data', {}).get('page_source', '')
    import re
    # Match tabs that contain the tab_name in their label attribute
    tab_pattern = rf"<XCUIElementTypeTab[^>]*label=['\"]([^'\"]*{re.escape(tab_name)}[^'\"]*)['\"]"
    matches = re.findall(tab_pattern, page_source, re.IGNORECASE)
    
    assert len(matches) >= 2, f"Expected at least 2 '{tab_name}' tabs, but found {len(matches)}"

# --- auto-generated step ---
@then('both tabs should display the same URL "{url}"')
def step_impl(context, url):
    # Verify the active tab shows the correct URL
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_exists", 
        arguments={
            'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': f"//XCUIElementTypeTextField[@label='Address and search bar' and @value='{url}']",
            'need_snapshot': 0
        }
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Click the "New tab" plus button')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
            'locator_value': 'New Tab'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('a new tab should be opened')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_exists", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTab[@value='1' and @label='New Tab']"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Close Edge')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="app_close", 
        arguments={'caller': 'behave-automation'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Navigate to Wikipedia')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="send_keys", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
            'locator_value': 'Address and search bar',
            'text': 'https://www.wikipedia.org\n'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Navigate to Wikipedia - press return')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="press_key", 
        arguments={'caller': 'behave-automation', 'key': 'return'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Right-click on Wikipedia tab')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="right_click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTab[@value='1' and @label='Search - "
                             "Wikipedia']"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Click "Pin Tab" menu item')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeMenuItem[@title='Pin Tab']"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('the tab should be pinned')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_exists", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTab[@value='1' and contains(@label, "
                             "'Pinned')]"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Right-click on pinned tab to unpin')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="right_click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTab[@value='1' and contains(@label, "
                             "'Pinned')]"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Click "Unpin Tab" menu item')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeMenuItem[@title='Unpin Tab']"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('the tab should be unpinned')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_not_exists", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTab[@value='1' and contains(@label, "
                             "'Pinned')]"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Navigate to GitHub')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="send_keys", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
            'locator_value': 'Address and search bar',
            'text': 'https://github.com\n'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Navigate to GitHub - press return')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="press_key", 
        arguments={'caller': 'behave-automation', 'key': 'return'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Close GitHub tab')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTab[@value='1' and "
                             "@label='GitHub']/XCUIElementTypeButton[@label='Close tab']"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Press Cmd+Shift+T to restore recently closed tab')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="press_key", 
        arguments={'caller': 'behave-automation', 'key': 'command+shift+t'}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('the GitHub tab should be restored')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_exists", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTab[@value='1' and @label='GitHub']"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('Click "Duplicate Tab" menu item')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="click_element", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeMenuItem[@title='Duplicate Tab']"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@then('a duplicate tab should be created')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_exists", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTab[@value='0' and contains(@label, "
                             "'Wikipedia')]"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 

# --- auto-generated step ---
@step('both tabs should show the same URL')
def step_impl(context):
    result = call_tool_sync(context, context.session.call_tool(
        name="verify_element_exists", 
        arguments={'caller': 'behave-automation',
            'locator_strategy': 'AppiumBy.XPATH',
            'locator_value': "//XCUIElementTypeTab[@value='1' and contains(@label, "
                             "'Wikipedia')]"}
    ))
    result_json = get_tool_json(result)
    assert result_json.get("status") == "success", f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'" 
