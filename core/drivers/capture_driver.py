"""
截图驱动 - 屏幕捕获实现
"""

import time
import numpy as np
from io import BytesIO
from typing import Optional, Tuple
from PIL import Image
from loguru import logger

from core import Result, DriverError
from .adb_driver import ADBDriver


class CaptureDriver:
    """截图驱动，提供多种截图方式"""
    
    def __init__(self, adb_driver: ADBDriver):
        """
        初始化截图驱动
        
        Args:
            adb_driver: ADB驱动实例
        """
        self.adb = adb_driver
        self._resolution: Optional[Tuple[int, int]] = None
        self._capture_method = "screencap"  # screencap, minicap, scrcpy
        
    def capture(self) -> Result[np.ndarray]:
        """
        捕获屏幕截图
        
        Returns:
            Result[np.ndarray]: BGR格式的numpy数组
        """
        if not self.adb.connected:
            return Result.fail("Device not connected")
        
        # 根据方法选择截图方式
        if self._capture_method == "screencap":
            return self._capture_screencap()
        elif self._capture_method == "minicap":
            return self._capture_minicap()
        else:
            return self._capture_screencap()
    
    def _capture_screencap(self) -> Result[np.ndarray]:
        """使用screencap截图（标准方法）"""
        try:
            start_time = time.time()
            
            # 执行截图命令
            result = self.adb.shell("screencap -p", timeout=5)
            if result.is_fail():
                return Result.fail(f"Screencap failed: {result.error}")
            
            # 获取原始数据
            png_data = result.unwrap()
            
            # 转换为PIL Image
            image = Image.open(BytesIO(png_data.encode('latin-1')))
            
            # 转换为numpy数组 (RGB -> BGR for OpenCV)
            img_array = np.array(image)
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_array = img_array[:, :, ::-1]  # RGB to BGR
            
            # 更新分辨率信息
            self._resolution = (img_array.shape[1], img_array.shape[0])
            
            elapsed = time.time() - start_time
            logger.debug(f"Screenshot captured in {elapsed:.3f}s, size: {self._resolution}")
            
            return Result.ok(img_array)
            
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return Result.fail(str(e))
    
    def _capture_minicap(self) -> Result[np.ndarray]:
        """使用minicap截图（需要额外安装）"""
        # TODO: 实现minicap支持
        return self._capture_screencap()
    
    def capture_region(self, x: int, y: int, width: int, height: int) -> Result[np.ndarray]:
        """
        捕获屏幕指定区域
        
        Args:
            x: 左上角x坐标
            y: 左上角y坐标
            width: 宽度
            height: 高度
            
        Returns:
            Result[np.ndarray]: 裁剪后的图像
        """
        # 先截全屏
        result = self.capture()
        if result.is_fail():
            return result
        
        try:
            img = result.unwrap()
            
            # 边界检查
            img_h, img_w = img.shape[:2]
            x = max(0, min(x, img_w - 1))
            y = max(0, min(y, img_h - 1))
            x2 = min(x + width, img_w)
            y2 = min(y + height, img_h)
            
            # 裁剪
            cropped = img[y:y2, x:x2]
            
            if cropped.size == 0:
                return Result.fail("Invalid region")
            
            return Result.ok(cropped)
            
        except Exception as e:
            return Result.fail(str(e))
    
    def save_screenshot(self, filepath: str) -> Result[bool]:
        """
        保存截图到文件
        
        Args:
            filepath: 保存路径
        """
        result = self.capture()
        if result.is_fail():
            return Result.fail(result.error)
        
        try:
            img = result.unwrap()
            # BGR to RGB for saving
            if len(img.shape) == 3 and img.shape[2] == 3:
                img = img[:, :, ::-1]
            
            Image.fromarray(img).save(filepath)
            logger.info(f"Screenshot saved to {filepath}")
            return Result.ok(True)
            
        except Exception as e:
            return Result.fail(str(e))
    
    def get_resolution(self) -> Result[Tuple[int, int]]:
        """
        获取屏幕分辨率
        
        Returns:
            Result[Tuple[int, int]]: (width, height)
        """
        if self._resolution:
            return Result.ok(self._resolution)
        
        # 从ADB获取
        result = self.adb.get_screen_size()
        if result.is_ok():
            self._resolution = result.unwrap()
        
        return result
    
    def set_capture_method(self, method: str) -> None:
        """
        设置截图方法
        
        Args:
            method: screencap/minicap/scrcpy
        """
        if method in ["screencap", "minicap", "scrcpy"]:
            self._capture_method = method
            logger.info(f"Capture method set to: {method}")