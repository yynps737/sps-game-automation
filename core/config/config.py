"""
简单的配置管理 - 只保留基础功能
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger


class Config:
    """简单的配置管理器"""
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
    
    def load(self, file_path: str) -> bool:
        """
        加载配置文件
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            是否成功
        """
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"Config file not found: {path}")
            return False
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    self._data = yaml.safe_load(f) or {}
                elif path.suffix == '.json':
                    self._data = json.load(f)
                else:
                    logger.error(f"Unsupported config format: {path.suffix}")
                    return False
            
            logger.info(f"Config loaded from {path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔如 'game.window.width'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        keys = key.split('.')
        
        if len(keys) == 1:
            self._data[key] = value
        else:
            # 导航到父节点
            parent = self._data
            for k in keys[:-1]:
                if k not in parent:
                    parent[k] = {}
                parent = parent[k]
            
            parent[keys[-1]] = value
    
    def save(self, file_path: str) -> bool:
        """
        保存配置到文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否成功
        """
        path = Path(file_path)
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    yaml.safe_dump(self._data, f, allow_unicode=True)
                elif path.suffix == '.json':
                    json.dump(self._data, f, indent=2, ensure_ascii=False)
                else:
                    logger.error(f"Unsupported format: {path.suffix}")
                    return False
            
            logger.info(f"Config saved to {path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    def clear(self) -> None:
        """清空配置"""
        self._data.clear()


# 全局配置实例
config = Config()