"""
ADB驱动 - 简化版，直接使用subprocess调用adb命令
"""

import subprocess
import time
from typing import Optional, Tuple
from loguru import logger

from core import Result


class ADBDriver:
    """简化的ADB驱动"""
    
    def __init__(self):
        self.device_id = None
        self.connected = False
    
    def connect(self, device_id: Optional[str] = None) -> Result[bool]:
        """
        连接设备
        
        MuMu12模拟器：
          - 默认端口: 127.0.0.1:16384
          - 备用端口: 127.0.0.1:7555
          
        其他模拟器：
          - 雷电: 127.0.0.1:5555
          - 夜神: 127.0.0.1:62001
          - 逍遥: 127.0.0.1:21503
        
        Args:
            device_id: 设备ID，如 "127.0.0.1:16384"
            
        Returns:
            Result[bool]: 连接结果
        """
        # MuMu12默认端口
        if device_id is None:
            device_id = "127.0.0.1:16384"
        
        try:
            # 先尝试连接
            cmd = f"adb connect {device_id}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            
            if "connected" in result.stdout or "already connected" in result.stdout:
                self.device_id = device_id
                self.connected = True
                logger.info(f"Connected to device: {device_id}")
                
                # 验证连接
                devices_result = self.shell("echo test")
                if devices_result.is_fail():
                    self.connected = False
                    return Result.fail("Device connected but not responding")
                
                return Result.ok(True)
            else:
                # 如果是MuMu12，尝试启动ADB
                if "16384" in device_id or "7555" in device_id:
                    logger.info("Trying to start MuMu12 ADB service...")
                    # MuMu12的adb通常在: C:\Program Files\Netease\MuMuPlayer-12.0\shell\adb.exe
                    # 但我们使用系统的adb即可
                    
                    # 重试连接
                    time.sleep(2)
                    retry_result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                    if "connected" in retry_result.stdout:
                        self.device_id = device_id
                        self.connected = True
                        logger.info(f"Connected to MuMu12: {device_id}")
                        return Result.ok(True)
                
                return Result.fail(f"Failed to connect: {result.stdout}")
                
        except subprocess.TimeoutExpired:
            return Result.fail("Connection timeout")
        except Exception as e:
            return Result.fail(f"Connection error: {e}")
    
    def disconnect(self) -> Result[bool]:
        """断开连接"""
        if not self.connected:
            return Result.ok(True)
        
        try:
            cmd = f"adb disconnect {self.device_id}"
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            self.connected = False
            logger.info(f"Disconnected from {self.device_id}")
            return Result.ok(True)
        except Exception as e:
            return Result.fail(f"Disconnect error: {e}")
    
    def shell(self, command: str, timeout: float = 10) -> Result[str]:
        """
        执行shell命令
        
        Args:
            command: shell命令
            timeout: 超时时间
            
        Returns:
            Result[str]: 命令输出
        """
        if not self.connected:
            return Result.fail("Device not connected")
        
        try:
            cmd = f"adb -s {self.device_id} shell {command}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode != 0:
                return Result.fail(f"Command failed: {result.stderr}")
            
            return Result.ok(result.stdout.strip())
            
        except subprocess.TimeoutExpired:
            return Result.fail(f"Command timeout: {command}")
        except Exception as e:
            return Result.fail(f"Shell error: {e}")
    
    def screenshot(self) -> Result[bytes]:
        """
        截图
        
        Returns:
            Result[bytes]: PNG图片数据
        """
        if not self.connected:
            return Result.fail("Device not connected")
        
        try:
            # 方案1：使用screencap（更兼容）
            cmd = f"adb -s {self.device_id} exec-out screencap -p"
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            
            if result.returncode != 0:
                return Result.fail("Screenshot failed")
            
            # 返回PNG数据
            return Result.ok(result.stdout)
            
        except subprocess.TimeoutExpired:
            return Result.fail("Screenshot timeout")
        except Exception as e:
            return Result.fail(f"Screenshot error: {e}")
    
    def get_screen_size(self) -> Result[Tuple[int, int]]:
        """
        获取屏幕分辨率
        
        Returns:
            Result[Tuple[int, int]]: (width, height)
        """
        result = self.shell("wm size")
        if result.is_fail():
            return Result.fail("Failed to get screen size")
        
        try:
            # 解析输出: "Physical size: 1920x1080"
            output = result.unwrap()
            if "Physical size:" in output:
                size_str = output.split("Physical size:")[1].strip()
            else:
                size_str = output.strip()
            
            if "x" in size_str:
                width, height = size_str.split("x")
                return Result.ok((int(width), int(height)))
            else:
                return Result.fail(f"Invalid size format: {output}")
                
        except Exception as e:
            return Result.fail(f"Parse size error: {e}")
    
    def is_screen_on(self) -> Result[bool]:
        """检查屏幕是否亮着"""
        result = self.shell("dumpsys power | grep 'Display Power'")
        if result.is_fail():
            return Result.fail("Failed to check screen state")
        
        output = result.unwrap()
        return Result.ok("ON" in output or "state=ON" in output)