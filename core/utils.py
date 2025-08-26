"""
工具函数 - 只保留必要的
"""

import time
import functools
from typing import Any, Callable, Optional
from loguru import logger


def retry(times: int = 3, delay: float = 1.0):
    """
    简单的重试装饰器
    
    Args:
        times: 重试次数
        delay: 重试间隔（秒）
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == times - 1:
                        raise
                    logger.warning(f"Retry {i+1}/{times}: {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def timer(name: str = None):
    """
    计时装饰器
    
    Args:
        name: 计时器名称
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            
            func_name = name or func.__name__
            logger.debug(f"{func_name} took {duration:.3f}s")
            return result
        return wrapper
    return decorator


class SimpleCache:
    """简单的内存缓存"""
    
    def __init__(self, max_size: int = 100):
        self._cache = {}
        self._max_size = max_size
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        return self._cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """设置缓存值"""
        if len(self._cache) >= self._max_size:
            # 删除最早的项
            first_key = next(iter(self._cache))
            del self._cache[first_key]
        self._cache[key] = value
    
    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()


def normalize_coordinate(x: int, y: int, 
                        source_width: int, source_height: int,
                        target_width: int, target_height: int) -> tuple:
    """
    坐标归一化
    
    Args:
        x, y: 原坐标
        source_width, source_height: 源分辨率
        target_width, target_height: 目标分辨率
        
    Returns:
        (new_x, new_y): 转换后的坐标
    """
    new_x = int(x * target_width / source_width)
    new_y = int(y * target_height / source_height)
    return new_x, new_y


def wait(seconds: float, message: str = None) -> None:
    """
    等待
    
    Args:
        seconds: 等待秒数
        message: 等待消息
    """
    if message:
        logger.debug(f"{message} ({seconds}s)")
    time.sleep(seconds)