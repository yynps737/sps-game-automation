"""
游戏控制器 - 串联所有功能的简单控制器
"""

import time
import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, List
from loguru import logger

from core import Result
from core.drivers import ADBDriver, InputDriver
from core.config import config
from core.utils import retry, wait


class Game:
    """游戏主控制器"""
    
    def __init__(self, device_id: str = None):
        """
        初始化游戏控制器
        
        Args:
            device_id: 设备ID
        """
        self.device_id = device_id
        self.adb = ADBDriver()
        self.input = None
        self.connected = False
        self.screen_width = 1920
        self.screen_height = 1080
    
    def connect(self) -> bool:
        """
        连接设备
        
        Returns:
            是否成功
        """
        # 连接ADB
        result = self.adb.connect(self.device_id)
        if result.is_fail():
            logger.error(f"Failed to connect: {result.error}")
            return False
        
        # 初始化输入驱动
        self.input = InputDriver(self.adb)
        
        # 获取屏幕分辨率
        size_result = self.adb.get_screen_size()
        if size_result.is_ok():
            self.screen_width, self.screen_height = size_result.unwrap()
            logger.info(f"Screen size: {self.screen_width}x{self.screen_height}")
        
        self.connected = True
        logger.info(f"Connected to device: {self.device_id or 'default'}")
        return True
    
    def screenshot(self) -> Optional[np.ndarray]:
        """
        截图
        
        Returns:
            图像数组
        """
        if not self.connected:
            logger.error("Device not connected")
            return None
        
        result = self.adb.screenshot()
        if result.is_fail():
            logger.error(f"Screenshot failed: {result.error}")
            return None
        
        # 转换为numpy数组
        image_bytes = result.unwrap()
        image = cv2.imdecode(
            np.frombuffer(image_bytes, np.uint8),
            cv2.IMREAD_COLOR
        )
        return image
    
    def find_image(self, template_path: str, 
                   threshold: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        查找图片
        
        Args:
            template_path: 模板图片路径
            threshold: 匹配阈值
            
        Returns:
            坐标(x, y)或None
        """
        # 截图
        screen = self.screenshot()
        if screen is None:
            return None
        
        # 加载模板
        template = cv2.imread(template_path)
        if template is None:
            logger.error(f"Template not found: {template_path}")
            return None
        
        # 模板匹配
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            # 返回中心点坐标
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            logger.debug(f"Found {template_path} at ({center_x}, {center_y})")
            return (center_x, center_y)
        
        return None
    
    def tap_image(self, template_path: str, 
                  threshold: float = 0.8) -> bool:
        """
        点击图片
        
        Args:
            template_path: 模板图片路径
            threshold: 匹配阈值
            
        Returns:
            是否成功
        """
        pos = self.find_image(template_path, threshold)
        if pos is None:
            logger.warning(f"Image not found: {template_path}")
            return False
        
        result = self.input.tap(pos[0], pos[1])
        return result.is_ok()
    
    def wait_for(self, template_path: str, 
                 timeout: int = 10,
                 interval: float = 1.0) -> bool:
        """
        等待图片出现
        
        Args:
            template_path: 模板图片路径
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
            
        Returns:
            是否找到
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.find_image(template_path):
                logger.debug(f"Found {template_path}")
                return True
            wait(interval)
        
        logger.warning(f"Timeout waiting for {template_path}")
        return False
    
    def tap(self, x: int, y: int) -> bool:
        """
        点击坐标
        
        Args:
            x, y: 坐标
            
        Returns:
            是否成功
        """
        if not self.connected:
            logger.error("Device not connected")
            return False
        
        result = self.input.tap(x, y)
        return result.is_ok()
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int,
              duration: int = 500) -> bool:
        """
        滑动
        
        Args:
            x1, y1: 起始坐标
            x2, y2: 结束坐标
            duration: 持续时间（毫秒）
            
        Returns:
            是否成功
        """
        if not self.connected:
            logger.error("Device not connected")
            return False
        
        result = self.input.swipe(x1, y1, x2, y2, duration)
        return result.is_ok()
    
    def text(self, content: str) -> bool:
        """
        输入文本
        
        Args:
            content: 文本内容
            
        Returns:
            是否成功
        """
        if not self.connected:
            logger.error("Device not connected")
            return False
        
        result = self.input.text(content)
        return result.is_ok()
    
    def back(self) -> bool:
        """返回键"""
        if not self.connected:
            return False
        return self.input.back().is_ok()
    
    def home(self) -> bool:
        """主页键"""
        if not self.connected:
            return False
        return self.input.home().is_ok()
    
    @retry(times=3, delay=2)
    def run_task(self, task_func) -> bool:
        """
        运行任务
        
        Args:
            task_func: 任务函数
            
        Returns:
            是否成功
        """
        try:
            logger.info(f"Running task: {task_func.__name__}")
            result = task_func(self)
            if result:
                logger.info(f"Task completed: {task_func.__name__}")
            else:
                logger.warning(f"Task failed: {task_func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Task error: {e}")
            return False
    
    def disconnect(self) -> None:
        """断开连接"""
        if self.adb:
            self.adb.disconnect()
        self.connected = False
        logger.info("Disconnected from device")