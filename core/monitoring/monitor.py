"""
简单的性能监控 - 只保留基础指标
"""

import time
from typing import Dict, Optional
from collections import deque
from loguru import logger


class Monitor:
    """简单的性能监控器"""
    
    def __init__(self):
        self._fps_history = deque(maxlen=100)
        self._last_frame_time = time.time()
        self._counters: Dict[str, int] = {}
        self._timers: Dict[str, float] = {}
    
    def frame_tick(self) -> float:
        """
        记录帧
        
        Returns:
            当前FPS
        """
        current_time = time.time()
        delta = current_time - self._last_frame_time
        
        if delta > 0:
            fps = 1.0 / delta
            self._fps_history.append(fps)
        else:
            fps = 0.0
        
        self._last_frame_time = current_time
        return fps
    
    def get_fps(self) -> float:
        """获取平均FPS"""
        if not self._fps_history:
            return 0.0
        return sum(self._fps_history) / len(self._fps_history)
    
    def count(self, name: str, value: int = 1) -> None:
        """
        增加计数器
        
        Args:
            name: 计数器名称
            value: 增加值
        """
        if name not in self._counters:
            self._counters[name] = 0
        self._counters[name] += value
    
    def get_count(self, name: str) -> int:
        """获取计数器值"""
        return self._counters.get(name, 0)
    
    def timer_start(self, name: str) -> None:
        """开始计时"""
        self._timers[name] = time.time()
    
    def timer_end(self, name: str) -> Optional[float]:
        """
        结束计时
        
        Returns:
            耗时（秒）
        """
        if name not in self._timers:
            return None
        
        duration = time.time() - self._timers[name]
        del self._timers[name]
        return duration
    
    def reset(self) -> None:
        """重置所有指标"""
        self._fps_history.clear()
        self._counters.clear()
        self._timers.clear()
        self._last_frame_time = time.time()
    
    def log_stats(self) -> None:
        """输出统计信息到日志"""
        stats = {
            'fps': f"{self.get_fps():.1f}",
            'counters': self._counters
        }
        logger.info(f"Monitor stats: {stats}")


# 全局监控实例
monitor = Monitor()


# 上下文管理器：简化计时
class Timer:
    """计时器上下文管理器"""
    
    def __init__(self, name: str, log: bool = False):
        self.name = name
        self.log = log
        self.duration = 0.0
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        self.duration = time.time() - self.start_time
        if self.log:
            logger.debug(f"{self.name} took {self.duration:.3f}s")