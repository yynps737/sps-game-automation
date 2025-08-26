"""
简单的事件总线 - 只保留必要功能
"""

import time
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from collections import defaultdict
from loguru import logger


@dataclass
class Event:
    """事件"""
    name: str
    data: Any = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class EventBus:
    """简单的事件总线 - 发布订阅模式"""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)
        self._enabled = True
    
    def on(self, event_name: str, handler: Callable) -> None:
        """
        订阅事件
        
        Args:
            event_name: 事件名称
            handler: 处理函数
        """
        self._handlers[event_name].append(handler)
        logger.debug(f"Handler registered for '{event_name}'")
    
    def off(self, event_name: str, handler: Callable) -> None:
        """
        取消订阅
        
        Args:
            event_name: 事件名称
            handler: 处理函数
        """
        if event_name in self._handlers:
            try:
                self._handlers[event_name].remove(handler)
                logger.debug(f"Handler unregistered from '{event_name}'")
            except ValueError:
                pass
    
    def emit(self, event_name: str, data: Any = None) -> int:
        """
        发送事件
        
        Args:
            event_name: 事件名称
            data: 事件数据
            
        Returns:
            处理器数量
        """
        if not self._enabled:
            return 0
        
        event = Event(name=event_name, data=data)
        handlers = self._handlers.get(event_name, [])
        
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in handler for '{event_name}': {e}")
        
        return len(handlers)
    
    def clear(self, event_name: Optional[str] = None) -> None:
        """
        清空订阅
        
        Args:
            event_name: 事件名称，None表示清空所有
        """
        if event_name:
            self._handlers.pop(event_name, None)
        else:
            self._handlers.clear()
    
    def disable(self) -> None:
        """禁用事件总线"""
        self._enabled = False
    
    def enable(self) -> None:
        """启用事件总线"""
        self._enabled = True


# 全局实例
event_bus = EventBus()


# 装饰器：简化使用
def on(event_name: str):
    """
    事件订阅装饰器
    
    Usage:
        @on('game.started')
        def handle_game_start(event):
            print(f"Game started: {event.data}")
    """
    def decorator(func):
        event_bus.on(event_name, func)
        return func
    return decorator