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
            arguments={'caller': 'behave-automation', 'need_snapshot': 0},
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )

    # Check if "Welcome to Microsoft Edge" dialog appears and handle it
    try:
        # Try to find the "Start Microsoft Edge" button in the welcome dialog
        find_result = call_tool_sync(
            context,
            context.session.call_tool(
                name='find_element',
                arguments={
                    'caller': 'behave-automation',
                    'locator_value': 'Start Microsoft Edge',
                    'locator_strategy': 'AppiumBy.NAME',
                    'step': 'Edge is launched',
                    'step_raw': 'Given Edge is launched',
                    'scenario': 'Edge Launch',
                },
            ),
        )
        find_result_json = get_tool_json(find_result)

        if find_result_json.get('status') == 'success':
            print(
                "DEBUG: Found 'Welcome to Microsoft Edge' dialog, clicking 'Start Microsoft Edge' button"
            )
            # Click the "Start Microsoft Edge" button
            click_result = call_tool_sync(
                context,
                context.session.call_tool(
                    name='click_element',
                    arguments={
                        'caller': 'behave-automation',
                        'locator_value': 'Start Microsoft Edge',
                        'locator_strategy': 'AppiumBy.NAME',
                        'step': 'Edge is launched',
                        'step_raw': 'Given Edge is launched',
                        'scenario': 'Edge Launch',
                    },
                ),
            )
            click_result_json = get_tool_json(click_result)
            assert click_result_json.get('status') == 'success', (
                f"Failed to click 'Start Microsoft Edge' button: {click_result_json.get('error')}"
            )
            print("DEBUG: Successfully clicked 'Start Microsoft Edge' button")
        else:
            print(
                "DEBUG: No 'Welcome to Microsoft Edge' dialog found, Edge may already be running"
            )

    except Exception as e:
        print(f'DEBUG: Exception while handling welcome dialog: {e}')
        # Continue execution even if welcome dialog handling fails
        pass

    # Check if sync dialog appears and handle it
    try:
        # Try to find the "Not now" button in the sync dialog
        sync_find_result = call_tool_sync(
            context,
            context.session.call_tool(
                name='find_element',
                arguments={
                    'caller': 'behave-automation',
                    'locator_value': 'Not now',
                    'locator_strategy': 'AppiumBy.NAME',
                    'step': 'Edge is launched',
                    'step_raw': 'Given Edge is launched',
                    'scenario': 'Edge Launch',
                },
            ),
        )
        sync_find_result_json = get_tool_json(sync_find_result)

        if sync_find_result_json.get('status') == 'success':
            print("DEBUG: Found sync dialog, clicking 'Not now' button")
            # Click the "Not now" button
            sync_click_result = call_tool_sync(
                context,
                context.session.call_tool(
                    name='click_element',
                    arguments={
                        'caller': 'behave-automation',
                        'locator_value': 'Not now',
                        'locator_strategy': 'AppiumBy.NAME',
                        'step': 'Edge is launched',
                        'step_raw': 'Given Edge is launched',
                        'scenario': 'Edge Launch',
                    },
                ),
            )
            sync_click_result_json = get_tool_json(sync_click_result)
            assert sync_click_result_json.get('status') == 'success', (
                f"Failed to click 'Not now' button: {sync_click_result_json.get('error')}"
            )
            print("DEBUG: Successfully clicked 'Not now' button in sync dialog")

            # Add a small delay to allow the dialog to dismiss
            import time

            time.sleep(2)  # Wait 2 seconds for the dialog to close
        else:
            print('DEBUG: No sync dialog found, Edge may be ready to use')

    except Exception as e:
        print(f'DEBUG: Exception while handling sync dialog: {e}')
        # Continue execution even if sync dialog handling fails
        pass

    # Create a new profile using edge://settings/profiles
    try:
        print("DEBUG: Starting new profile creation process via edge://settings/profiles")
        
        # Step 1: Navigate to edge://settings/profiles
        print("DEBUG: Navigating to edge://settings/profiles")
        
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
        time.sleep(3)
        
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
        time.sleep(2)
        
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
        time.sleep(2)
        
    except Exception as e:
        print(f'DEBUG: Exception during profile creation: {e}')
        # Continue execution even if profile creation fails
        pass