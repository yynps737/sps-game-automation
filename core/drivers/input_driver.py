"""
输入驱动 - 简单的点击和滑动
"""

import time
import random
from typing import Tuple, Optional, List
from loguru import logger

from core import Result
from .adb_driver import ADBDriver


class InputDriver:
    """简单的输入驱动"""
    
    def __init__(self, adb: ADBDriver):
        """
        初始化
        
        Args:
            adb: ADB驱动实例
        """
        self.adb = adb
        self._last_action_time = 0
        self._min_interval = 0.1  # 最小操作间隔
    
    def tap(self, x: int, y: int, duration: int = 50) -> Result[bool]:
        """
        点击屏幕
        
        Args:
            x: X坐标
            y: Y坐标
            duration: 按压时长（毫秒）
            
        Returns:
            Result[bool]: 操作结果
        """
        # 添加随机偏移（防止总是点击同一像素）
        x += random.randint(-2, 2)
        y += random.randint(-2, 2)
        
        # 确保最小间隔
        self._wait_min_interval()
        
        # 执行点击
        cmd = f"input tap {x} {y}"
        if duration > 50:
            cmd = f"input swipe {x} {y} {x} {y} {duration}"
        
        result = self.adb.shell(cmd)
        
        if result.is_ok():
            logger.debug(f"Tap at ({x}, {y})")
            self._last_action_time = time.time()
            return Result.ok(True)
        else:
            return Result.fail(f"Tap failed: {result.error}")
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, 
              duration: int = 500) -> Result[bool]:
        """
        滑动屏幕
        
        Args:
            x1, y1: 起始坐标
            x2, y2: 结束坐标
            duration: 滑动时长（毫秒）
            
        Returns:
            Result[bool]: 操作结果
        """
        # 确保最小间隔
        self._wait_min_interval()
        
        # 添加轻微随机
        x1 += random.randint(-2, 2)
        y1 += random.randint(-2, 2)
        x2 += random.randint(-2, 2)
        y2 += random.randint(-2, 2)
        
        # 执行滑动
        cmd = f"input swipe {x1} {y1} {x2} {y2} {duration}"
        result = self.adb.shell(cmd)
        
        if result.is_ok():
            logger.debug(f"Swipe from ({x1}, {y1}) to ({x2}, {y2})")
            self._last_action_time = time.time()
            return Result.ok(True)
        else:
            return Result.fail(f"Swipe failed: {result.error}")
    
    def long_press(self, x: int, y: int, duration: int = 1000) -> Result[bool]:
        """
        长按
        
        Args:
            x: X坐标
            y: Y坐标
            duration: 按压时长（毫秒）
            
        Returns:
            Result[bool]: 操作结果
        """
        return self.tap(x, y, duration)
    
    def text(self, content: str) -> Result[bool]:
        """
        输入文本
        
        Args:
            content: 文本内容
            
        Returns:
            Result[bool]: 操作结果
        """
        # 确保最小间隔
        self._wait_min_interval()
        
        # 转义特殊字符
        content = content.replace(' ', '%s')
        content = content.replace('"', '\\"')
        content = content.replace("'", "\\'")
        
        cmd = f'input text "{content}"'
        result = self.adb.shell(cmd)
        
        if result.is_ok():
            logger.debug(f"Input text: {content[:20]}...")
            self._last_action_time = time.time()
            return Result.ok(True)
        else:
            return Result.fail(f"Text input failed: {result.error}")
    
    def key_event(self, keycode: int) -> Result[bool]:
        """
        发送按键事件
        
        Args:
            keycode: 按键码（如：3=HOME, 4=BACK）
            
        Returns:
            Result[bool]: 操作结果
        """
        # 确保最小间隔
        self._wait_min_interval()
        
        cmd = f"input keyevent {keycode}"
        result = self.adb.shell(cmd)
        
        if result.is_ok():
            logger.debug(f"Key event: {keycode}")
            self._last_action_time = time.time()
            return Result.ok(True)
        else:
            return Result.fail(f"Key event failed: {result.error}")
    
    def back(self) -> Result[bool]:
        """返回键"""
        return self.key_event(4)
    
    def home(self) -> Result[bool]:
        """主页键"""
        return self.key_event(3)
    
    def recent(self) -> Result[bool]:
        """最近任务键"""
        return self.key_event(187)
    
    def _wait_min_interval(self) -> None:
        """确保最小操作间隔"""
        elapsed = time.time() - self._last_action_time
        if elapsed < self._min_interval:
            wait_time = self._min_interval - elapsed
            # 添加10-30ms随机延迟
            wait_time += random.uniform(0.01, 0.03)
            time.sleep(wait_time)
    
    def set_min_interval(self, interval: float) -> None:
        """
        设置最小操作间隔
        
        Args:
            interval: 间隔时间（秒）
        """
        self._min_interval = max(0.05, interval)  # 最小50ms