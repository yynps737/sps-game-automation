"""
快速开始 - Windows测试脚本
在 D:\pyproject\sps_game 下运行
"""

from core.game import Game


def quick_test():
    """快速测试MuMu12连接"""
    print("=" * 50)
    print("🚀 快速测试 MuMu12")
    print("=" * 50)
    
    # 连接MuMu12
    print("\n📱 连接MuMu12...")
    game = Game("127.0.0.1:16384")
    
    if not game.connect():
        print("❌ 连接失败！")
        print("\n请检查：")
        print("1. MuMu12是否已启动")
        print("2. 开发者选项-USB调试是否开启")
        print("3. 尝试运行: adb connect 127.0.0.1:16384")
        return
    
    print("✅ 连接成功！")
    
    # 截图测试
    print("\n📷 测试截图...")
    screen = game.screenshot()
    
    if screen is not None:
        print(f"✅ 截图成功！尺寸: {screen.shape}")
        
        # 保存截图
        import cv2
        cv2.imwrite("test_mumu12.png", screen)
        print("📁 截图已保存: test_mumu12.png")
    else:
        print("❌ 截图失败")
    
    # 测试点击
    print("\n🖱️ 测试点击...")
    if game.tap(500, 500):
        print("✅ 点击成功")
    else:
        print("❌ 点击失败")
    
    # 断开连接
    print("\n🔌 断开连接...")
    game.disconnect()
    print("✅ 已断开")
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！框架运行正常")
    print("=" * 50)


if __name__ == "__main__":
    quick_test()