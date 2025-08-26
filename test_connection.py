#!/usr/bin/env python
"""
测试MuMu12连接和截图识别
"""

import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from core import Result
from core.drivers import ADBDriver


def test_mumu12_connection():
    """测试MuMu12连接流程"""
    print("=" * 50)
    print("🔍 测试MuMu12连接和截图功能")
    print("=" * 50)
    
    # 创建ADB驱动
    adb = ADBDriver()
    
    # 测试连接MuMu12
    print("\n1️⃣ 连接MuMu12模拟器...")
    print("   尝试端口: 127.0.0.1:16384")
    
    result = adb.connect("127.0.0.1:16384")
    
    if result.is_fail():
        print(f"   ❌ 连接失败: {result.error}")
        print("\n   可能的原因:")
        print("   1. MuMu12未启动")
        print("   2. MuMu12的ADB未开启")
        print("   3. 端口不对，尝试 127.0.0.1:7555")
        
        # 尝试备用端口
        print("\n   尝试备用端口: 127.0.0.1:7555")
        result = adb.connect("127.0.0.1:7555")
        
        if result.is_fail():
            print(f"   ❌ 备用端口也失败: {result.error}")
            return False
    
    print("   ✅ 连接成功!")
    
    # 获取屏幕分辨率
    print("\n2️⃣ 获取屏幕分辨率...")
    size_result = adb.get_screen_size()
    
    if size_result.is_ok():
        width, height = size_result.unwrap()
        print(f"   ✅ 分辨率: {width} x {height}")
    else:
        print(f"   ⚠️ 获取失败: {size_result.error}")
    
    # 测试截图
    print("\n3️⃣ 测试截图功能...")
    screenshot_result = adb.screenshot()
    
    if screenshot_result.is_ok():
        data = screenshot_result.unwrap()
        print(f"   ✅ 截图成功! 大小: {len(data)} bytes")
        
        # 保存截图
        with open("test_screenshot.png", "wb") as f:
            f.write(data)
        print("   📷 已保存到: test_screenshot.png")
    else:
        print(f"   ❌ 截图失败: {screenshot_result.error}")
    
    # 测试shell命令
    print("\n4️⃣ 测试Shell命令...")
    shell_result = adb.shell("getprop ro.product.model")
    
    if shell_result.is_ok():
        model = shell_result.unwrap()
        print(f"   ✅ 设备型号: {model}")
    else:
        print(f"   ❌ Shell失败: {shell_result.error}")
    
    # 断开连接
    print("\n5️⃣ 断开连接...")
    adb.disconnect()
    print("   ✅ 已断开")
    
    return True


def analyze_data_flow():
    """分析数据流"""
    print("\n" + "=" * 50)
    print("📊 数据流分析")
    print("=" * 50)
    
    print("""
MuMu12连接和识别数据流:

1. 连接阶段:
   Windows用户 → adb connect 127.0.0.1:16384
   ↓
   ADB Server → TCP Socket → MuMu12 ADB Service
   ↓
   验证连接: adb shell echo test
   
2. 截图数据流:
   Game.screenshot() 
   ↓
   ADBDriver.screenshot()
   ↓
   subprocess: adb exec-out screencap -p
   ↓
   MuMu12 → PNG二进制数据 → Python bytes
   
3. 图像识别数据流:
   PNG bytes → cv2.imdecode() → numpy.ndarray
   ↓
   cv2.imread(template) → 模板图像
   ↓
   cv2.matchTemplate() → 相似度矩阵
   ↓
   cv2.minMaxLoc() → 最佳匹配位置
   ↓
   返回中心点坐标 (x, y)
   
4. 点击操作数据流:
   Game.tap_image() → 找到坐标
   ↓
   InputDriver.tap(x, y)
   ↓
   ADBDriver.shell("input tap x y")
   ↓
   subprocess → adb → MuMu12 → 模拟点击
    """)


if __name__ == "__main__":
    # 运行测试
    success = test_mumu12_connection()
    
    if success:
        analyze_data_flow()
        print("\n✅ 测试完成！MuMu12连接和截图功能正常")
    else:
        print("\n❌ 测试失败，请检查MuMu12是否正确启动")
        print("\n提示：")
        print("1. 确保MuMu12模拟器已启动")
        print("2. 在MuMu12设置中开启'ADB调试'")
        print("3. Windows防火墙允许ADB连接")
        print("4. 尝试命令: adb connect 127.0.0.1:16384")