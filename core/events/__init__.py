"""
事件系统 - 简单的发布订阅
"""

from .event_bus import EventBus, Event, event_bus, on

__all__ = ['EventBus', 'Event', 'event_bus', 'on']