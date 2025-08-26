"""
直接测试MuMu12连接 - 使用完整路径
"""
import subprocess
import os
import time

def test_adb_direct():
    """直接使用可能的ADB路径测试"""
    
    print("=" * 50)
    print("🔍 寻找并测试ADB")
    print("=" * 50)
    
    # 可能的ADB位置
    adb_paths = [
        r"D:\tools\platform-tools\adb.exe",
        r"C:\platform-tools\adb.exe",
        r"C:\Android\sdk\platform-tools\adb.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Android\Sdk\platform-tools\adb.exe",
        r"C:\Program Files\Netease\MuMuPlayer-12.0\shell\adb.exe",  # MuMu12自带
        r"C:\Program Files\MuMu\emulator\nemu12\shell\adb.exe",     # MuMu12备选路径
        "adb.exe",  # 如果在PATH中
    ]
    
    adb_found = None
    
    # 寻找ADB
    for path in adb_paths:
        path = os.path.expandvars(path)  # 展开环境变量
        if path == "adb.exe":
            # 检查是否在PATH中
            try:
                result = subprocess.run(["where", "adb"], capture_output=True, text=True)
                if result.returncode == 0:
                    adb_found = "adb"
                    print(f"✅ 找到ADB (在PATH中): {result.stdout.strip()}")
                    break
            except:
                pass
        elif os.path.exists(path):
            adb_found = path
            print(f"✅ 找到ADB: {path}")
            break
    
    if not adb_found:
        print("❌ 未找到ADB!")
        print("\n请安装ADB:")
        print("1. 运行: install_adb.bat")
        print("2. 或者从MuMu12安装目录复制adb.exe")
        return False
    
    # 使用找到的ADB测试连接
    print(f"\n📱 使用ADB连接MuMu12...")
    print(f"   命令: {adb_found} connect 127.0.0.1:16384")
    
    try:
        # 连接MuMu12
        result = subprocess.run(
            [adb_found, "connect", "127.0.0.1:16384"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        print(f"   输出: {result.stdout.strip()}")
        
        if "connected" in result.stdout.lower() or "already" in result.stdout.lower():
            print("   ✅ 连接成功!")
            
            # 列出设备
            print("\n📋 设备列表:")
            devices_result = subprocess.run(
                [adb_found, "devices"],
                capture_output=True,
                text=True
            )
            print(devices_result.stdout)
            
            # 获取设备信息
            print("📱 设备信息:")
            info_result = subprocess.run(
                [adb_found, "-s", "127.0.0.1:16384", "shell", "getprop", "ro.product.model"],
                capture_output=True,
                text=True
            )
            if info_result.returncode == 0:
                print(f"   型号: {info_result.stdout.strip()}")
            
            # 测试截图
            print("\n📷 测试截图...")
            screenshot_result = subprocess.run(
                [adb_found, "-s", "127.0.0.1:16384", "exec-out", "screencap", "-p"],
                capture_output=True,
                timeout=5
            )
            if screenshot_result.returncode == 0 and len(screenshot_result.stdout) > 0:
                print(f"   ✅ 截图成功! 大小: {len(screenshot_result.stdout)} bytes")
                
                # 保存截图
                with open("test_direct.png", "wb") as f:
                    f.write(screenshot_result.stdout)
                print("   📁 已保存: test_direct.png")
            else:
                print("   ❌ 截图失败")
            
            return True
            
        else:
            print("   ❌ 连接失败!")
            print("\n可能的原因:")
            print("1. MuMu12未启动")
            print("2. MuMu12未开启USB调试")
            print("3. 端口不对，可以尝试:")
            print("   - 127.0.0.1:7555")
            print("   - 127.0.0.1:5555")
            
            # 尝试其他端口
            for port in ["7555", "5555"]:
                print(f"\n尝试端口 127.0.0.1:{port}...")
                retry_result = subprocess.run(
                    [adb_found, "connect", f"127.0.0.1:{port}"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if "connected" in retry_result.stdout.lower():
                    print(f"✅ 在端口 {port} 连接成功!")
                    return True
            
            return False
            
    except subprocess.TimeoutExpired:
        print("   ⏱️ 连接超时")
        return False
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False


if __name__ == "__main__":
    success = test_adb_direct()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 测试成功! MuMu12可以正常使用")
        print("\n下一步:")
        print("1. 如果ADB不在PATH中，将其添加到环境变量")
        print("2. 重新运行 setup_and_run.cmd")
    else:
        print("❌ 测试失败")
        print("\n解决方案:")
        print("1. 确保MuMu12模拟器正在运行")
        print("2. 在MuMu12设置中开启'开发者选项' → 'USB调试'")
        print("3. 运行 install_adb.bat 安装ADB")
    print("=" * 50)