from behave import *
import logging
from features.environment import call_tool_sync, get_tool_json


# --- auto-generated step ---
@then('Reading Mode toolbar should appear')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeGroup[@label="Toolbar"]',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I can see reading mode icon in the address bar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Exit Immersive Reader (F9)',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('Analyze the screenshot to verify the webpage is in reading mode')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_visual_task',
            arguments={
                'caller': 'behave-automation',
                'need_snapshot': 0,
                'task_description': 'Verify the webpage is in reading mode - the page URL should show "read://" instead of "https://"',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "Exit Immersive Reader" button in Reading Mode toolbar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Exit Immersive Reader (F9)',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@then('Reading Mode toolbar should be closed')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_not_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.XPATH',
                'locator_value': '//XCUIElementTypeGroup[@label="Toolbar"]',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('Analyze the screenshot to verify the webpage is exited from reading mode')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_visual_task',
            arguments={
                'caller': 'behave-automation',
                'need_snapshot': 0,
                'task_description': 'Verify the webpage has exited from reading mode - the page URL should show "https://" instead of "read://"',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "Read Aloud" button in Reading Mode toolbar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Read Aloud',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@when('I click "Exit Immersive Reader" button on address bar')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'Exit Immersive Reader (F9)',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('I open Reading Mode')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='click_element',
            arguments={
                'caller': 'behave-automation',
                'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
                'locator_value': 'More actions',
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
                'locator_value': 'Immersive reader F9 F9',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('Analyze the screenshot to verify the webpage in shadow mode')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_visual_task',
            arguments={
                'caller': 'behave-automation',
                'need_snapshot': 0,
                'task_description': 'Verify that the webpage is displayed in shadow mode or '
                'dark/dimmed appearance with reduced contrast or gray '
                'overlay indicating the reading mode is active',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )


# --- auto-generated step ---
@step('Analyze the screenshot to verify the webpage exit shadow mode')
def step_impl(context):
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_visual_task',
            arguments={
                'caller': 'behave-automation',
                'need_snapshot': 0,
                'task_description': 'Verify that the webpage has exited shadow mode and returned to '
                'normal appearance with full contrast and no gray overlay, '
                'indicating the reading mode shadow/dimmed effect is no longer active',
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

# # --- auto-generated step ---
# @when('I click "Text Preferences" button in Reading Mode toolbar')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='click_element',
#             arguments={
#                 'caller': 'behave-automation',
#                 'locator_strategy': 'AppiumBy.ACCESSIBILITY_ID',
#                 'locator_value': 'Text Preferences',
#                 'need_snapshot': 0,
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @then('Text Preferences panel should appear')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='verify_element_exists',
#             arguments={
#                 'caller': 'behave-automation',
#                 'locator_strategy': 'AppiumBy.XPATH',
#                 'locator_value': '//XCUIElementTypeGroup[@label="Text Preferences"]',
#                 'need_snapshot': 0,
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @when('I turn on "Text Spacing"')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='click_element',
#             arguments={
#                 'caller': 'behave-automation',
#                 'locator_strategy': 'AppiumBy.XPATH',
#                 'locator_value': "//XCUIElementTypeCheckBox[@title='Text Spacing']",
#                 'need_snapshot': 0,
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @then('Analyze the screenshot to verify the Text Spacing is increased')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='verify_visual_task',
#             arguments={
#                 'caller': 'behave-automation',
#                 'need_snapshot': 0,
#                 'task_description': 'Verify that the Text Spacing is increased in the reading '
#                 'mode content. The text should show wider spacing between '
#                 'letters and words compared to the default spacing.',
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @when('I click "Comic Sans" in Text Type')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='click_element',
#             arguments={
#                 'caller': 'behave-automation',
#                 'locator_strategy': 'AppiumBy.XPATH',
#                 'locator_value': "//XCUIElementTypeRadioButton[@title='Comic Sans']",
#                 'need_snapshot': 0,
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @then('Analyze the screenshot to verify the Text Type should change to Comic Sans font')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='verify_visual_task',
#             arguments={
#                 'caller': 'behave-automation',
#                 'need_snapshot': 0,
#                 'task_description': 'Verify that the text type has changed to Comic Sans font '
#                 'in the reading mode content. The text should appear in '
#                 'Comic Sans font style, which is characterized by a more '
#                 'casual, rounded, handwritten appearance compared to '
#                 'standard fonts.',
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @when('I click "Wide column" in Text Column Style')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='click_element',
#             arguments={
#                 'caller': 'behave-automation',
#                 'locator_strategy': 'AppiumBy.XPATH',
#                 'locator_value': "//XCUIElementTypeRadioButton[@label='Wide column']",
#                 'need_snapshot': 0,
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @then(
#     'Analyze the screenshot to verify the Text Column Style should change to Wide column'
# )
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='verify_visual_task',
#             arguments={
#                 'caller': 'behave-automation',
#                 'need_snapshot': 0,
#                 'task_description': 'Verify that the text column style has changed to Wide '
#                 'column format in the reading mode content. The text '
#                 'should now display in a wider column layout that spans '
#                 'more of the available width compared to narrow or medium '
#                 'column styles.',
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @when('I click "More Themes"')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='click_element',
#             arguments={
#                 'caller': 'behave-automation',
#                 'locator_strategy': 'AppiumBy.XPATH',
#                 'locator_value': "//XCUIElementTypeButton[@title='More Themes']",
#                 'need_snapshot': 0,
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @step('I click "Orchid" in Page Themes')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='click_element',
#             arguments={
#                 'caller': 'behave-automation',
#                 'locator_strategy': 'AppiumBy.XPATH',
#                 'locator_value': "//XCUIElementTypeRadioButton[@title='Orchid Theme']",
#                 'need_snapshot': 0,
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @then('Analyze the screenshot to verify the Page Themes should change to Orchid theme')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='verify_visual_task',
#             arguments={
#                 'caller': 'behave-automation',
#                 'need_snapshot': 0,
#                 'task_description': 'Verify that the page theme has changed to Orchid theme in '
#                 'the reading mode content. The Orchid theme should display '
#                 'with orchid/purple background color scheme and the Orchid '
#                 'Theme option should be selected in the Page Themes '
#                 'settings.',
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @when('I press "Esc" key')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='press_key',
#             arguments={
#                 'caller': 'behave-automation',
#                 'key': 'escape',
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )


# # --- auto-generated step ---
# @then('Text Preferences panel should be closed')
# def step_impl(context):
#     result = call_tool_sync(
#         context,
#         context.session.call_tool(
#             name='verify_element_not_exists',
#             arguments={
#                 'caller': 'behave-automation',
#                 'locator_strategy': 'AppiumBy.XPATH',
#                 'locator_value': '//XCUIElementTypeGroup[@label="Text Preferences"]',
#                 'need_snapshot': 0,
#             },
#         ),
#     )
#     result_json = get_tool_json(result)
#     assert result_json.get('status') == 'success', (
#         f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
#     )