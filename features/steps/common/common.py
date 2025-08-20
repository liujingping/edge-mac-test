from behave import given, when, then, step
from features.environment import call_tool_sync, get_tool_json
import os
import uuid
import tempfile
import shutil
import atexit
import logging


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
