"""
系统弹窗自动处理器
在每个测试步骤前自动检查并处理系统弹窗
"""

import subprocess
import json
import os
import logging
import time
from pathlib import Path

logger = logging.getLogger('behave_environment')


class SystemDialogHandler:
    """系统弹窗处理器"""

    def __init__(self, config_path=None):
        """初始化处理器

        Args:
            config_path: 配置文件路径，默认为 features/config/system_dialogs.json
        """
        if config_path is None:
            # 获取项目根目录下的配置文件
            current_dir = Path(__file__).parent.parent
            config_path = current_dir / 'config' / 'system_dialogs.json'

        self.config = self._load_config(config_path)
        self.enabled = self.config.get('enabled', True)
        self.check_interval = self.config.get('check_interval', 0.5)
        self.dialogs = self.config.get('dialogs', [])
        self.handled_dialogs = set()  # 记录已处理的弹窗，避免重复处理

    def _load_config(self, config_path):
        """加载配置文件"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f'Dialog config file not found: {config_path}')
                return {'enabled': False, 'dialogs': []}
        except Exception as e:
            logger.error(f'Failed to load dialog config: {e}')
            return {'enabled': False, 'dialogs': []}

    def check_and_handle_dialogs(self):
        """检查并处理系统弹窗

        Returns:
            bool: 是否处理了弹窗
        """
        if not self.enabled:
            return False

        handled = False

        # 检查每个配置的弹窗
        for dialog_config in self.dialogs:
            if self._handle_dialog(dialog_config):
                handled = True
                dialog_name = dialog_config.get('name', 'Unknown')
                self.handled_dialogs.add(dialog_name)
                logger.info(f'Handled system dialog: {dialog_name}')

        return handled

    def _handle_dialog(self, dialog_config):
        """处理单个弹窗配置

        Args:
            dialog_config: 弹窗配置字典

        Returns:
            bool: 是否成功处理
        """
        process_name = dialog_config.get('process')
        window_name = dialog_config.get('window')
        buttons = dialog_config.get('buttons', [])

        if not process_name or not buttons:
            return False

        # 按优先级排序按钮
        buttons = sorted(buttons, key=lambda x: x.get('priority', 999))

        for button in buttons:
            button_name = button.get('name')
            action = button.get('action', 'click')

            if action == 'skip':
                continue

            if self._click_button(process_name, window_name, button_name):
                return True

        return False

    def _click_button(self, process_name, window_name, button_name):
        """点击指定的按钮

        Args:
            process_name: 进程名称
            window_name: 窗口名称（可选）
            button_name: 按钮名称

        Returns:
            bool: 是否成功点击
        """
        if window_name:
            # 如果指定了窗口名称
            script = f'''
            tell application "System Events"
                if exists process "{process_name}" then
                    tell process "{process_name}"
                        if exists window "{window_name}" then
                            if exists button "{button_name}" of window "{window_name}" then
                                click button "{button_name}" of window "{window_name}"
                                return "Clicked: {button_name}"
                            end if
                        end if
                    end tell
                end if
            end tell
            return ""
            '''
        else:
            # 如果没有指定窗口名称，搜索所有窗口
            script = f'''
            tell application "System Events"
                if exists process "{process_name}" then
                    tell process "{process_name}"
                        repeat with win in windows
                            if exists button "{button_name}" of win then
                                click button "{button_name}" of win
                                return "Clicked: {button_name}"
                            end if
                        end repeat
                    end tell
                end if
            end tell
            return ""
            '''

        try:
            result = subprocess.run(
                ['osascript', '-e', script], capture_output=True, text=True, timeout=2
            )

            if result.stdout.strip() and 'Clicked' in result.stdout:
                logger.debug(f'Successfully clicked button: {button_name}')
                return True

        except subprocess.TimeoutExpired:
            logger.debug(f'Timeout while trying to click: {button_name}')
        except Exception as e:
            logger.debug(f'Error clicking button: {e}')

        return False

    def quick_check(self):
        """快速检查是否有任何已知的系统弹窗

        Returns:
            list: 检测到的弹窗列表
        """
        detected_dialogs = []

        # 获取所有进程和窗口信息
        script = """
        tell application "System Events"
            set dialogInfo to {}
            repeat with proc in application processes
                if name of proc is in {"universalAccessAuthWarn", "UserNotificationCenter", "System Events"} then
                    if (count of windows of proc) > 0 then
                        set end of dialogInfo to (name of proc)
                    end if
                end if
            end repeat
            return dialogInfo
        end tell
        """

        try:
            result = subprocess.run(
                ['osascript', '-e', script], capture_output=True, text=True, timeout=1
            )

            if result.stdout.strip():
                logger.info(
                    f'Detected system processes with dialogs: {result.stdout.strip()}'
                )
                processes = result.stdout.strip().split(', ')
                for proc in processes:
                    for dialog in self.dialogs:
                        if dialog.get('process') == proc:
                            dialog_name = dialog.get('name', proc)
                            detected_dialogs.append(dialog_name)
                            logger.info(
                                f'Found system dialog: {dialog_name} (process: {proc})'
                            )

        except Exception as e:
            logger.debug(f'Error during quick check: {e}')

        return detected_dialogs

    def reset_handled_dialogs(self):
        """重置已处理的弹窗记录"""
        self.handled_dialogs.clear()


# 全局实例
_dialog_handler = None


def get_dialog_handler():
    """获取全局弹窗处理器实例"""
    global _dialog_handler
    if _dialog_handler is None:
        _dialog_handler = SystemDialogHandler()
    return _dialog_handler


def check_and_handle_system_dialogs():
    """便捷函数：检查并处理系统弹窗"""
    handler = get_dialog_handler()
    return handler.check_and_handle_dialogs()


def enable_dialog_handling(enabled=True):
    """启用或禁用弹窗处理"""
    handler = get_dialog_handler()
    handler.enabled = enabled
    logger.info(f'System dialog handling {"enabled" if enabled else "disabled"}')
