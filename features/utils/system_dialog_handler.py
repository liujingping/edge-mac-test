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
        
        # 固定的超时时间
        self.quick_check_timeout = 3
        self.button_click_timeout = 5
        
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

    def check_and_handle_dialogs(self, detected_dialogs):
        """处理系统弹窗

        Args:
            detected_dialogs: 已检测到的弹窗列表

        Returns:
            bool: 是否处理了弹窗
        """
        if not self.enabled:
            return False

        # 如果没有检测到任何弹窗，直接返回
        if not detected_dialogs:
            logger.debug('No dialogs detected, skipping dialog handling')
            return False

        handled = False

        # 只检查已检测到的弹窗
        for detected_dialog_name in detected_dialogs:
            # 查找对应的配置
            dialog_config = None
            for config in self.dialogs:
                if config.get('name') == detected_dialog_name:
                    dialog_config = config
                    break

            if dialog_config:
                logger.debug(f'Attempting to handle detected dialog: {detected_dialog_name}')
                result = self._handle_dialog(dialog_config)
                if result:
                    handled = True
                    dialog_name = dialog_config.get('name', 'Unknown')
                    
                    # 如果返回了实际弹窗信息，使用它；否则使用配置名称
                    if isinstance(result, tuple) and len(result) == 2:
                        success, actual_info = result
                        if actual_info and actual_info.strip():
                            logger.info(f'Handled system dialog: {actual_info.strip()} (config: {dialog_name})')
                        else:
                            logger.info(f'Handled system dialog: {dialog_name}')
                    else:
                        logger.info(f'Handled system dialog: {dialog_name}')
                    
                    self.handled_dialogs.add(dialog_name)
                else:
                    logger.warning(f'Failed to handle detected dialog: {detected_dialog_name}')
            else:
                logger.warning(f'No configuration found for detected dialog: {detected_dialog_name}')

        return handled

    def _handle_dialog(self, dialog_config):
        """处理单个弹窗配置

        Args:
            dialog_config: 弹窗配置字典

        Returns:
            tuple: (是否成功处理, 实际弹窗信息) 或 False
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

            result = self._click_button(process_name, window_name, button_name)
            if result:
                # 获取实际的弹窗信息
                actual_dialog_info = self._get_dialog_info(process_name, window_name)
                return True, actual_dialog_info

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
                ['osascript', '-e', script], capture_output=True, text=True, timeout=self.button_click_timeout
            )

            if result.stdout.strip() and 'Clicked' in result.stdout:
                logger.debug(f'Successfully clicked button: {button_name}')
                return True

        except subprocess.TimeoutExpired:
            logger.debug(f'Timeout while trying to click: {button_name} (timeout: {self.button_click_timeout}s)')
        except Exception as e:
            logger.debug(f'Error clicking button: {e}')

        return False

    def _get_dialog_info(self, process_name, window_name=None):
        """获取弹窗的实际信息

        Args:
            process_name: 进程名称
            window_name: 窗口名称（可选）

        Returns:
            str: 弹窗的描述信息
        """
        if window_name:
            # 如果指定了窗口名称，获取该窗口的详细信息
            script = f'''
            tell application "System Events"
                if exists process "{process_name}" then
                    tell process "{process_name}"
                        if exists window "{window_name}" then
                            set windowTitle to name of window "{window_name}"
                            set staticTexts to {{}}
                            try
                                repeat with st in static text of window "{window_name}"
                                    if value of st is not "" then
                                        set end of staticTexts to value of st
                                    end if
                                end repeat
                            end try
                            if (count of staticTexts) > 0 then
                                return windowTitle & ": " & (item 1 of staticTexts)
                            else
                                return windowTitle
                            end if
                        end if
                    end tell
                end if
            end tell
            return ""
            '''
        else:
            # 如果没有指定窗口名称，搜索所有窗口并获取信息
            script = f'''
            tell application "System Events"
                if exists process "{process_name}" then
                    tell process "{process_name}"
                        repeat with win in windows
                            set windowTitle to name of win
                            set staticTexts to {{}}
                            try
                                repeat with st in static text of win
                                    if value of st is not "" then
                                        set end of staticTexts to value of st
                                    end if
                                end repeat
                            end try
                            if (count of staticTexts) > 0 then
                                return windowTitle & ": " & (item 1 of staticTexts)
                            else if windowTitle is not "" then
                                return windowTitle
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

            if result.stdout.strip():
                return result.stdout.strip()

        except Exception as e:
            logger.debug(f'Error getting dialog info: {e}')

        return ""

    def quick_check(self):
        """快速检查是否有任何已知的系统弹窗

        Returns:
            list: 检测到的弹窗列表
        """
        detected_dialogs = []

        # 使用更简单的方法，逐个检查进程以避免超时
        target_processes = ["universalAccessAuthWarn", "UserNotificationCenter", "System Events"]
        
        for process_name in target_processes:
            try:
                # 简化的脚本，一次只检查一个进程
                script = f'''
                tell application "System Events"
                    try
                        if exists process "{process_name}" then
                            if (count of windows of process "{process_name}") > 0 then
                                return "{process_name}"
                            end if
                        end if
                    end try
                    return ""
                end tell
                '''

                result = subprocess.run(
                    ['osascript', '-e', script], capture_output=True, text=True, timeout=self.quick_check_timeout
                )

                if result.stdout.strip():
                    proc = result.stdout.strip()
                    logger.info(f'Detected system process with dialogs: {proc}')
                    
                    # 查找匹配的对话框配置
                    for dialog in self.dialogs:
                        if dialog.get('process') == proc:
                            dialog_name = dialog.get('name', proc)
                            detected_dialogs.append(dialog_name)
                            logger.info(f'Found system dialog: {dialog_name} (process: {proc})')

            except subprocess.TimeoutExpired:
                logger.debug(f'Timeout checking process: {process_name} (timeout: {self.quick_check_timeout}s)')
                continue
            except Exception as e:
                logger.debug(f'Error checking process {process_name}: {e}')
                continue

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


def enable_dialog_handling(enabled=True):
    """启用或禁用弹窗处理"""
    handler = get_dialog_handler()
    handler.enabled = enabled
    logger.info(f'System dialog handling {"enabled" if enabled else "disabled"}')
