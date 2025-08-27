"""
ADB驱动 - 基于官方文档的正确实现
"""

import subprocess
import time
import os
from typing import Optional, Tuple, List
from loguru import logger

from core import Result


class ADBDriver:
    """
    ADB驱动 - 正确处理MuMu12和标准Android模拟器
    
    基于官方文档：
    - emulator-XXXX格式是标准Android模拟器串行号
    - MuMu12使用端口16384，但显示为emulator-5554保持兼容性
    - 端口递增规律：MuMu12多开时每个实例+32
    """
    
    def __init__(self):
        self.device_id = None
        self.connected = False
        self.adb_cmd = self._find_adb()
        
    def _find_adb(self) -> str:
        """查找ADB命令"""
        # 可能的ADB位置
        adb_paths = [
            r"D:\tools\platform-tools\adb.exe",
            r"C:\platform-tools\adb.exe", 
            r"C:\Android\sdk\platform-tools\adb.exe",
            r"C:\Program Files\Netease\MuMuPlayer-12.0\shell\adb.exe",
            r"C:\Program Files\MuMu\emulator\nemu12\shell\adb.exe",
        ]
        
        # 检查环境变量中的ADB_PATH
        if os.environ.get('ADB_PATH'):
            adb_paths.insert(0, os.environ['ADB_PATH'])
        
        # 查找存在的ADB
        for path in adb_paths:
            if os.path.exists(path):
                logger.info(f"Found ADB at: {path}")
                return f'"{path}"'  # 加引号处理路径中的空格
        
        # 如果都没找到，假设在PATH中
        logger.warning("ADB not found in common locations, trying PATH...")
        return "adb"
    
    def list_devices(self) -> Result[List[str]]:
        """
        列出所有连接的设备
        
        Returns:
            Result[List[str]]: 设备ID列表
        """
        try:
            cmd = f"{self.adb_cmd} devices"
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                encoding='utf-8', 
                errors='ignore', 
                timeout=5
            )
            
            # 解析输出
            lines = result.stdout.strip().split('\n')
            devices = []
            for line in lines[1:]:  # 跳过标题行
                if '\t' in line:
                    device_id, status = line.split('\t')
                    if status == 'device':
                        devices.append(device_id)
            
            return Result.ok(devices)
            
        except Exception as e:
            return Result.fail(f"Failed to list devices: {e}")
    
    def connect(self, device_id: Optional[str] = None) -> Result[bool]:
        """
        连接设备 - 智能处理不同场景
        
        处理逻辑：
        1. 如果未指定device_id，自动检测可用设备
        2. 如果指定了emulator-XXXX格式，直接使用（已连接）
        3. 如果指定了IP:端口格式，执行adb connect
        4. 自动尝试MuMu12常用端口
        
        Args:
            device_id: 设备ID（可选）
            
        Returns:
            Result[bool]: 连接结果
        """
        try:
            # 首先列出当前设备
            devices_result = self.list_devices()
            if devices_result.is_ok():
                current_devices = devices_result.unwrap()
                logger.info(f"Current devices: {current_devices}")
            else:
                current_devices = []
            
            # 场景1：未指定设备ID，自动检测
            if device_id is None:
                # 优先使用已连接的设备
                if current_devices:
                    device_id = current_devices[0]
                    logger.info(f"Using existing device: {device_id}")
                    self.device_id = device_id
                    self.connected = True
                    
                    # 验证设备响应
                    test_result = self.shell("echo test")
                    if test_result.is_ok():
                        return Result.ok(True)
                    else:
                        self.connected = False
                        logger.warning(f"Device {device_id} not responding, trying to connect MuMu12...")
                
                # 尝试连接MuMu12的常用端口
                logger.info("No connected device, trying MuMu12 ports...")
                for port in [16384, 16416, 7555, 5555]:
                    target = f"127.0.0.1:{port}"
                    logger.info(f"Trying to connect: {target}")
                    
                    cmd = f"{self.adb_cmd} connect {target}"
                    result = subprocess.run(
                        cmd, 
                        shell=True, 
                        capture_output=True, 
                        encoding='utf-8', 
                        errors='ignore', 
                        timeout=3
                    )
                    
                    if "connected" in result.stdout.lower() and "cannot" not in result.stdout.lower():
                        # 连接成功后，获取实际的设备ID
                        time.sleep(0.5)  # 等待连接稳定
                        devices_after = self.list_devices()
                        if devices_after.is_ok():
                            new_devices = devices_after.unwrap()
                            if new_devices:
                                # 使用新出现的设备ID（可能是emulator-5554格式）
                                self.device_id = new_devices[0]
                                self.connected = True
                                logger.info(f"Connected to MuMu12, device ID: {self.device_id}")
                                return Result.ok(True)
                
                return Result.fail("Could not find or connect to any device")
            
            # 场景2：指定了emulator-XXXX格式（已连接的设备）
            if "emulator-" in device_id and ":" not in device_id:
                if device_id in current_devices:
                    logger.info(f"Device {device_id} is already connected")
                    self.device_id = device_id
                    self.connected = True
                    
                    # 验证设备响应
                    test_result = self.shell("echo test")
                    if test_result.is_ok():
                        return Result.ok(True)
                    else:
                        self.connected = False
                        return Result.fail(f"Device {device_id} not responding")
                else:
                    # 设备不在列表中，可能需要先连接MuMu12
                    logger.warning(f"Device {device_id} not found, trying to connect MuMu12...")
                    # 尝试连接MuMu12端口
                    for port in [16384, 16416, 7555, 5555]:
                        target = f"127.0.0.1:{port}"
                        cmd = f"{self.adb_cmd} connect {target}"
                        result = subprocess.run(
                            cmd, 
                            shell=True, 
                            capture_output=True, 
                            encoding='utf-8', 
                            errors='ignore', 
                            timeout=3
                        )
                        
                        if "connected" in result.stdout.lower():
                            time.sleep(0.5)
                            # 再次检查设备列表
                            devices_after = self.list_devices()
                            if devices_after.is_ok() and device_id in devices_after.unwrap():
                                self.device_id = device_id
                                self.connected = True
                                logger.info(f"Successfully connected to {device_id}")
                                return Result.ok(True)
                    
                    return Result.fail(f"Could not connect to device {device_id}")
            
            # 场景3：指定了IP:端口格式
            if ":" in device_id:
                logger.info(f"Connecting to {device_id}...")
                cmd = f"{self.adb_cmd} connect {device_id}"
                result = subprocess.run(
                    cmd, 
                    shell=True, 
                    capture_output=True, 
                    encoding='utf-8', 
                    errors='ignore', 
                    timeout=5
                )
                
                if "connected" in result.stdout.lower() or "already connected" in result.stdout.lower():
                    # 获取连接后的实际设备ID
                    time.sleep(0.5)
                    devices_after = self.list_devices()
                    if devices_after.is_ok():
                        new_devices = devices_after.unwrap()
                        if new_devices:
                            # 使用设备列表中的ID（可能是emulator格式）
                            self.device_id = new_devices[0] if len(new_devices) == 1 else device_id
                            self.connected = True
                            logger.info(f"Connected successfully, using device ID: {self.device_id}")
                            
                            # 验证连接
                            test_result = self.shell("echo test")
                            if test_result.is_ok():
                                return Result.ok(True)
                
                return Result.fail(f"Failed to connect to {device_id}: {result.stdout}")
            
            # 场景4：其他设备序列号
            if device_id in current_devices:
                self.device_id = device_id
                self.connected = True
                logger.info(f"Using existing device: {device_id}")
                return Result.ok(True)
            else:
                return Result.fail(f"Unknown device: {device_id}")
                
        except subprocess.TimeoutExpired:
            return Result.fail("Connection timeout")
        except FileNotFoundError:
            return Result.fail(f"ADB not found. Please install ADB or set ADB_PATH environment variable")
        except Exception as e:
            return Result.fail(f"Connection error: {e}")
    
    def disconnect(self) -> Result[bool]:
        """断开连接"""
        if not self.connected:
            return Result.ok(True)
        
        try:
            # 只有IP:端口格式需要disconnect
            if self.device_id and ":" in self.device_id:
                cmd = f"{self.adb_cmd} disconnect {self.device_id}"
                subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            
            self.connected = False
            self.device_id = None
            logger.info("Disconnected")
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
        if not self.connected or not self.device_id:
            return Result.fail("Device not connected")
        
        try:
            cmd = f"{self.adb_cmd} -s {self.device_id} shell {command}"
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                encoding='utf-8', 
                errors='ignore', 
                timeout=timeout
            )
            
            # 某些命令返回非0也是正常的
            if result.returncode != 0 and result.stderr and "error" in result.stderr.lower():
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
        if not self.connected or not self.device_id:
            return Result.fail("Device not connected")
        
        try:
            # 使用screencap（更兼容）
            cmd = f"{self.adb_cmd} -s {self.device_id} exec-out screencap -p"
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                timeout=10  # 增加超时时间
            )
            
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
            # 尝试另一种方法
            result = self.shell("dumpsys power | grep mScreenOn")
            if result.is_fail():
                return Result.fail("Failed to check screen state")
        
        output = result.unwrap()
        return Result.ok("ON" in output.upper() or "true" in output.lower())