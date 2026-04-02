from behave import given, when, then, step
from features.environment import call_tool_sync, get_tool_json, take_screenshot
import os
import uuid
import tempfile
import shutil
import atexit
import logging
import time
import subprocess

# Import network throttling manager
try:
    from features.utils.network_throttling import (
        get_throttling_manager,
        apply_profile,
        THROTTLING_PROFILES,
    )

    NETWORK_THROTTLING_AVAILABLE = True
except ImportError as e:
    NETWORK_THROTTLING_AVAILABLE = False
    logging.warning(f'Network throttling not available: {e}')

# Import system dialog handler
try:
    from features.utils.system_dialog_handler import get_dialog_handler
    SYSTEM_DIALOG_HANDLER_AVAILABLE = True
except ImportError as e:
    SYSTEM_DIALOG_HANDLER_AVAILABLE = False
    logging.warning(f'System dialog handler not available: {e}')


logger = logging.getLogger('behave_environment')  # Use the same logger name as environment.py


# Global variable to store temporary directories to cleanup
_temp_directories_to_cleanup = []


def cleanup_temp_directories():
    """Cleanup all created temporary directories"""
    for temp_dir in _temp_directories_to_cleanup:
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.info(f'DEBUG: Cleaned up temporary directory: {temp_dir}')
        except Exception as e:
            logger.info(f'DEBUG: Failed to cleanup directory {temp_dir}: {e}')
    _temp_directories_to_cleanup.clear()


# Register cleanup function on exit
atexit.register(cleanup_temp_directories)


def create_profile_directory():
    """
    Create temporary profile directory
    Use system temporary directory directly, create random named folder under it
    """
    # Use system temporary directory
    profile_root = tempfile.gettempdir()

    # Generate random folder name
    random_folder_name = f'edge-profile-{uuid.uuid4().hex[:8]}'
    profile_path = os.path.join(profile_root, random_folder_name)

    # Create directory
    os.makedirs(profile_path, exist_ok=True)
    logger.info(f'DEBUG: Created profile directory: {profile_path}')

    # Add to cleanup list
    _temp_directories_to_cleanup.append(profile_path)

    return profile_path


def launch_edge_implementation(context):
    """Implementation of launching Edge application"""
    # Check if profile_path already exists in context, reuse if yes, create new if no
    if (
        hasattr(context, 'profile_path')
        and context.profile_path
        and os.path.exists(context.profile_path)
    ):
        profile_path = context.profile_path
        logger.info(f'DEBUG: Reusing existing profile path: {profile_path}')
    else:
        # Create profile directory
        profile_path = create_profile_directory()
        # Store profile path in context for possible future cleanup
        context.profile_path = profile_path

    # Launch the Edge application
    def _launch():
        return call_tool_sync(
            context,
            context.session.call_tool(
                name='app_launch',
                arguments={
                    'caller': 'behave-automation',
                    'need_snapshot': 0,
                    'arguments': [
                        '--no-first-run',
                        '--enable-benchmarking',
                        '--disable-field-trial-config',
                        f'--user-data-dir={profile_path}',
                    ],
                },
            ),
        )
    
    result = _launch()
    result_json = get_tool_json(result)

    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )
    logger.info('DEBUG: Edge application launched successfully')
    
    # Check and handle system dialogs
    if SYSTEM_DIALOG_HANDLER_AVAILABLE:
        logger.info('DEBUG: Checking for system dialogs after Edge launch...')
        try:
            dialog_handler = get_dialog_handler()
            
            # Wait for a while to let system dialogs appear
            time.sleep(2)
            
            # Quickly check if there are system dialogs
            detected_dialogs = dialog_handler.quick_check()
            
            if detected_dialogs:
                logger.info(f'DEBUG: Detected system dialogs: {detected_dialogs}')
                handled = dialog_handler.check_and_handle_dialogs(detected_dialogs)
                
                if handled:
                    logger.info('DEBUG: ✅ System dialogs automatically handled')
                    # Wait for a while to let handling take effect
                    time.sleep(1)
                else:
                    logger.warning('DEBUG: ⚠️ Failed to handle some system dialogs')
            else:
                logger.info('DEBUG: No system dialogs detected')
                
        except Exception as e:
            logger.warning(f'DEBUG: Error during system dialog handling: {e}')
    else:
        logger.info('DEBUG: System dialog handler not available, skipping dialog check')


@given('Edge is launched')
def given_edge_launched(context):
    launch_edge_implementation(context)


@step('I close and restart Edge')
def step_close_and_restart_edge(context):
    launch_edge_implementation(context)


@step('I enable slow network')
def enable_slow_network(context):
    """
    Enable slow network mode
    Use default slow_download profile
    """
    if not NETWORK_THROTTLING_AVAILABLE:
        logger.warning('Network throttling is not available on this system')
        return

    try:
        manager = get_throttling_manager()

        # Use slow_download profile
        profile_name = 'slow_download'
        success = apply_profile(manager, profile_name)

        if success:
            # Mark network throttling as active in context
            setattr(context, 'network_throttling_active', True)
            setattr(context, 'network_throttling_profile', profile_name)

            profile = THROTTLING_PROFILES[profile_name]
            logger.info(
                f"Enabled slow network with profile '{profile_name}': {profile['description']}"
            )
        else:
            logger.error(f"Failed to enable slow network with profile '{profile_name}'")
            raise Exception(
                f"Failed to enable slow network with profile '{profile_name}'"
            )

    except Exception as e:
        logger.error(f'Error enabling slow network: {e}')
        raise


@step('I disable slow network')
def disable_slow_network(context):
    """
    Disable slow network mode, restore normal network speed
    """
    if not NETWORK_THROTTLING_AVAILABLE:
        logger.warning('Network throttling is not available on this system')
        return

    try:
        manager = get_throttling_manager()

        # Check if network throttling is active
        is_active = getattr(context, 'network_throttling_active', False)
        current_profile = getattr(context, 'network_throttling_profile', 'unknown')

        if not is_active:
            logger.info('Network throttling is not currently active')
            return

        success = manager.remove_throttling()

        if success:
            # Clear network throttling mark in context
            setattr(context, 'network_throttling_active', False)
            setattr(context, 'network_throttling_profile', None)

            logger.info(
                f"Disabled slow network (was using profile '{current_profile}')"
            )
        else:
            logger.error('Failed to disable slow network')
            raise Exception('Failed to disable slow network')

    except Exception as e:
        logger.error(f'Error disabling slow network: {e}')
        raise


def get_edge_downloads_path(context):
    """
    Get Edge browser download folder path
    Edge browser defaults to Downloads folder in user directory
    """
    # Edge browser always uses Downloads folder in user directory
    downloads_path = os.path.expanduser('~/Downloads')
    
    return downloads_path


@step('I clean Edge downloads folder')
def clean_edge_downloads_folder(context):
    """
    Clean Edge browser download folder
    """
    downloads_path = get_edge_downloads_path(context)
    
    try:
        if not os.path.exists(downloads_path):
            logger.info(f'DEBUG: Downloads folder does not exist: {downloads_path}')
            return
            
        # Get all files and folders in download folder
        items_to_remove = []
        for item in os.listdir(downloads_path):
            item_path = os.path.join(downloads_path, item)
            items_to_remove.append(item_path)
        
        # Remove all files and folders
        removed_count = 0
        for item_path in items_to_remove:
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    removed_count += 1
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    removed_count += 1
            except Exception as e:
                logger.warning(f'DEBUG: Failed to remove {item_path}: {e}')
        
        logger.info(f'DEBUG: Cleaned Edge downloads folder, removed {removed_count} items from {downloads_path}')
        
    except Exception as e:
        logger.error(f'Error cleaning Edge downloads folder: {e}')
        raise


@step('I clean Edge downloads file "{filename}"')
def clean_edge_downloads_file(context, filename):
    """
    Remove specified file from Edge browser download folder
    
    Args:
        filename: Filename to remove
    """
    downloads_path = get_edge_downloads_path(context)
    file_path = os.path.join(downloads_path, filename)
    
    try:
        if not os.path.exists(file_path):
            logger.info(f'DEBUG: File does not exist: {file_path}')
            return
            
        if os.path.isfile(file_path):
            os.remove(file_path)
            logger.info(f'DEBUG: Removed file: {file_path}')
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            logger.info(f'DEBUG: Removed directory: {file_path}')
        else:
            logger.warning(f'DEBUG: Unknown file type, cannot remove: {file_path}')
            
    except Exception as e:
        logger.error(f'Error removing file {filename} from Edge downloads folder: {e}')
        raise


@step('I save current screenshot')
def save_current_screenshot(context):
    if hasattr(context, 'scenario'):
        take_screenshot(context.scenario.name)
    else:
        logger.warning('DEBUG: No scenario context found for screenshot')



@step('I press Enter key')
def press_enter_key(context):
    """Press Enter key"""
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


@step('I open a new tab')
def open_new_tab(context):
    """Open a new tab"""
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='press_key',
            arguments={
                'caller': 'behave-automation',
                'key': 'cmd+t',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )
