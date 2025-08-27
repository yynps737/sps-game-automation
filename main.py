"""
主程序入口 - 极简启动
"""

import sys
from loguru import logger

from core.game import Game
from core.config import config


def main():
    """主函数"""
    # 配置日志
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add("logs/game.log", rotation="1 day", level="DEBUG")
    
    # 加载配置
    if not config.load("config.yaml"):
        logger.warning("Using default config")
    
    # 连接设备
    device_id = config.get("device.id", "emulator-5554")
    game = Game(device_id)
    
    if not game.connect():
        logger.error("Failed to connect to device")
        return 1
    
    try:
        # 这里可以运行任务
        logger.info("Game automation started")
        
        # 示例：截图
        logger.info("Attempting to capture screenshot...")
        screen = game.screenshot()
        if screen is not None:
            logger.info(f"Screenshot captured successfully, size: {screen.shape}")
            import cv2
            cv2.imwrite("screenshot_test.png", screen)
            logger.info("Screenshot saved as screenshot_test.png")
        else:
            logger.warning("Screenshot returned None")
        
        # 示例：点击坐标
        if game.tap(500, 500):
            logger.info("Tap successful")
        
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        game.disconnect()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())