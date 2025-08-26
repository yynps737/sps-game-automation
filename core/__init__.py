"""
SPS Game Automation Framework Core Module
"""

__version__ = "0.1.0"
__author__ = "SPS Team"

from typing import TypeVar, Generic, Optional, Union

T = TypeVar('T')

class Result(Generic[T]):
    """统一的结果返回类型"""
    
    def __init__(self, success: bool, data: Optional[T] = None, error: Optional[str] = None):
        self.success = success
        self.data = data
        self.error = error
    
    @classmethod
    def ok(cls, data: T) -> 'Result[T]':
        """成功结果"""
        return cls(True, data, None)
    
    @classmethod
    def fail(cls, error: str) -> 'Result[T]':
        """失败结果"""
        return cls(False, None, error)
    
    def is_ok(self) -> bool:
        return self.success
    
    def is_fail(self) -> bool:
        return not self.success
    
    def unwrap(self) -> T:
        """获取数据，失败时抛出异常"""
        if self.success and self.data is not None:
            return self.data
        raise ValueError(f"Result is not ok: {self.error}")
    
    def unwrap_or(self, default: T) -> T:
        """获取数据，失败时返回默认值"""
        if self.success and self.data is not None:
            return self.data
        return default

class SPSError(Exception):
    """框架基础异常类"""
    pass

class DriverError(SPSError):
    """驱动层异常"""
    pass

class EngineError(SPSError):
    """引擎层异常"""
    pass

class ConfigError(SPSError):
    """配置异常"""
    pass