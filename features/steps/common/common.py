from behave import given, when, then, step
from features.environment import call_tool_sync, get_tool_json
import os
import uuid
import tempfile
import shutil
import atexit
import logging

# 导入网络限速管理器
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


logger = logging.getLogger('behave_environment')  # 使用与environment.py相同的logger名称


# 全局变量存储需要清理的临时目录
_temp_directories_to_cleanup = []


def cleanup_temp_directories():
    """清理所有创建的临时目录"""
    for temp_dir in _temp_directories_to_cleanup:
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.info(f'DEBUG: Cleaned up temporary directory: {temp_dir}')
        except Exception as e:
            logger.info(f'DEBUG: Failed to cleanup directory {temp_dir}: {e}')
    _temp_directories_to_cleanup.clear()


# 注册退出时的清理函数
atexit.register(cleanup_temp_directories)


def create_profile_directory():
    """
    创建临时 profile 目录
    直接使用系统临时目录，在下面创建随机命名的文件夹
    """
    # 使用系统临时目录
    profile_root = tempfile.gettempdir()

    # 生成随机文件夹名
    random_folder_name = f'edge-profile-{uuid.uuid4().hex[:8]}'
    profile_path = os.path.join(profile_root, random_folder_name)

    # 创建目录
    os.makedirs(profile_path, exist_ok=True)
    logger.info(f'DEBUG: Created profile directory: {profile_path}')

    # 添加到清理列表
    _temp_directories_to_cleanup.append(profile_path)

    return profile_path


def launch_edge_implementation(context):
    """启动Edge应用程序的具体实现"""
    # 检查context中是否已经有profile_path，如果有就复用，没有就创建新的
    if (
        hasattr(context, 'profile_path')
        and context.profile_path
        and os.path.exists(context.profile_path)
    ):
        profile_path = context.profile_path
        logger.info(f'DEBUG: Reusing existing profile path: {profile_path}')
    else:
        # 创建 profile 目录
        profile_path = create_profile_directory()
        # 将profile路径存储到context中，以便后续可能的清理
        context.profile_path = profile_path

    # Launch the Edge application
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='app_launch',
            arguments={
                'caller': 'behave-automation',
                'need_snapshot': 0,
                'arguments': [
                    '--no-first-run',
                    f'--user-data-dir={profile_path}',
                ],
            },
        ),
    )
    result_json = get_tool_json(result)
    assert result_json.get('status') == 'success', (
        f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
    )
    logger.info('DEBUG: Edge application launched successfully')


@given('Edge is launched')
def given_edge_launched(context):
    launch_edge_implementation(context)


@step('I close and restart Edge')
def step_close_and_restart_edge(context):
    launch_edge_implementation(context)


@step('I enable slow network')
def enable_slow_network(context):
    """
    启用低网速模式
    使用默认的slow_download配置文件
    """
    if not NETWORK_THROTTLING_AVAILABLE:
        logger.warning('Network throttling is not available on this system')
        return

    try:
        manager = get_throttling_manager()

        # 使用slow_download配置文件
        profile_name = 'slow_download'
        success = apply_profile(manager, profile_name)

        if success:
            # 在context中标记网络节流已激活
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
    禁用低网速模式，恢复正常网速
    """
    if not NETWORK_THROTTLING_AVAILABLE:
        logger.warning('Network throttling is not available on this system')
        return

    try:
        manager = get_throttling_manager()

        # 检查是否已激活网络节流
        is_active = getattr(context, 'network_throttling_active', False)
        current_profile = getattr(context, 'network_throttling_profile', 'unknown')

        if not is_active:
            logger.info('Network throttling is not currently active')
            return

        success = manager.remove_throttling()

        if success:
            # 清除context中的网络节流标记
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
    获取Edge浏览器的下载文件夹路径
    Edge浏览器默认使用用户目录下的Downloads文件夹
    """
    # Edge浏览器始终使用用户目录下的Downloads文件夹
    downloads_path = os.path.expanduser('~/Downloads')
    
    return downloads_path


@step('I clean Edge downloads folder')
def clean_edge_downloads_folder(context):
    """
    清空Edge浏览器的下载文件夹
    """
    downloads_path = get_edge_downloads_path(context)
    
    try:
        if not os.path.exists(downloads_path):
            logger.info(f'DEBUG: Downloads folder does not exist: {downloads_path}')
            return
            
        # 获取下载文件夹中的所有文件和文件夹
        items_to_remove = []
        for item in os.listdir(downloads_path):
            item_path = os.path.join(downloads_path, item)
            items_to_remove.append(item_path)
        
        # 删除所有文件和文件夹
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
    删除Edge浏览器下载文件夹中的指定文件
    
    Args:
        filename: 要删除的文件名
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
