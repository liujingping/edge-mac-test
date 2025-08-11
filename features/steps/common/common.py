from behave import given, when, then, step
from features.environment import call_tool_sync, get_tool_json


@given('Edge is launched')
def step_impl(context):
    print("DEBUG: Executing 'Edge is launched' step")

    # Launch the Edge application
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='app_launch',
            arguments={'caller': 'behave-automation', 'need_snapshot': 0, "arguments": ["--no-first-run"]}
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

    # Create a new profile using edge://settings/profiles
    try:
        print("DEBUG: Starting new profile creation process via edge://settings/profiles")
        
        # Click the address bar
        call_tool_sync(
            context,
            context.session.call_tool(
                name='click_element',
                arguments={
                    'caller': 'behave-automation',
                    'locator_value': '//XCUIElementTypeTextField[@label="Address and search bar"]',
                    'locator_strategy': 'AppiumBy.XPATH',
                    'step': 'Edge is launched',
                    'step_raw': 'Given Edge is launched',
                    'scenario': 'Edge Launch',
                },
            ),
        )
        
        # Type the URL
        call_tool_sync(
            context,
            context.session.call_tool(
                name='send_keys',
                arguments={
                    'caller': 'behave-automation',
                    'locator_value': '//XCUIElementTypeTextField[@label="Address and search bar"]',
                    'locator_strategy': 'AppiumBy.XPATH',
                    'text': 'edge://settings/profiles',
                    'step': 'Edge is launched',
                    'step_raw': 'Given Edge is launched',
                    'scenario': 'Edge Launch',
                },
            ),
        )
        
        # Press Enter to navigate
        call_tool_sync(
            context,
            context.session.call_tool(
                name='press_key',
                arguments={
                    'caller': 'behave-automation',
                    'key': 'return',
                    'step': 'Edge is launched',
                    'step_raw': 'Given Edge is launched',
                    'scenario': 'Edge Launch',
                },
            ),
        )
        
        # Wait for the settings page to load
        import time
        time.sleep(1)
        
        # Step 2: Click "Add profile" button
        call_tool_sync(
            context,
            context.session.call_tool(
                name='click_element',
                arguments={
                    'caller': 'behave-automation',
                    'locator_value': 'Add profile',
                    'locator_strategy': 'AppiumBy.NAME',
                    'step': 'Edge is launched',
                    'step_raw': 'Given Edge is launched',
                    'scenario': 'Edge Launch',
                },
            ),
        )
        
        # Wait for dialog to appear
        time.sleep(1)
        
        # Step 3: Click "Add" confirmation button
        call_tool_sync(
            context,
            context.session.call_tool(
                name='click_element',
                arguments={
                    'caller': 'behave-automation',
                    'locator_value': 'Add',
                    'locator_strategy': 'AppiumBy.NAME',
                    'step': 'Edge is launched',
                    'step_raw': 'Given Edge is launched',
                    'scenario': 'Edge Launch',
                },
            ),
        )
        
        # Wait for new profile window to be created
        time.sleep(1)
        
    except Exception as e:
        print(f'DEBUG: Exception during profile creation: {e}')
        # Continue execution even if profile creation fails
        pass