# 开发约束文档

## 开发环境

**开发环境**：WSL (Windows Subsystem for Linux)

**开发工具**：Claude Code 4.1 大模型

**语言版本**：Python 3.11.8+ (3.11.8 或 3.11.9)
- WSL: Python 3.11.8
- Windows: Python 3.11.9
- 完全兼容，无需统一

**GUI框架**：PyQt6

## 开发流程约束

### 1. 代码编写阶段（WSL）

**只做**：
- 语法编写
- 语法验证
- 代码结构设计
- 逻辑实现

**不做**：
- 编译操作
- PyQt运行测试
- 打包构建
- UI预览

### 2. 版本管理流程

```
WSL编写 → Git推送 → GitHub仓库 → Windows拉取 → 本地运行
```

**具体步骤**：
1. WSL中完成代码编写和语法验证
2. `git add .` + `git commit` + `git push`
3. Windows环境拉取最新代码
4. Windows环境运行PyQt程序和测试

### 3. 文件系统约束

**WSL路径**：`/home/kkb/sps_game/`

**禁止**：
- 直接在WSL中运行GUI程序
- 使用绝对Windows路径
- 硬编码平台相关路径

**必须**：
- 使用相对路径
- 使用`pathlib.Path`处理路径
- 配置文件使用平台无关格式

### 4. 依赖管理

**requirements.txt**：
```
PyQt6>=6.6.0
opencv-python>=4.9.0
numpy>=1.24.0
pyyaml>=6.0
pillow>=10.0.0
adbutils>=1.0.0
```

**安装命令**：
```bash
# WSL (仅语法检查需要)
pip install --no-deps -r requirements.txt

# Windows (完整安装)
pip install -r requirements.txt
```

### 5. 代码规范

**类型注解**：全部函数必须有类型注解
```python
def process_image(img: np.ndarray) -> tuple[bool, dict[str, Any]]:
    pass
```

**文档字符串**：核心函数必须有docstring
```python
def critical_function(param: str) -> None:
    """
    功能描述
    
    Args:
        param: 参数说明
    
    Returns:
        返回值说明
    """
    pass
```

**导入规范**：
```python
# 标准库
import os
import sys

# 第三方库
import numpy as np
from PyQt6.QtCore import Qt

# 本地模块
from core.engine import ImageEngine
```

### 6. 测试约束

**WSL测试**：
- 单元测试（非GUI部分）
- 语法检查（flake8/pylint）
- 类型检查（mypy）

**Windows测试**：
- GUI集成测试
- 实际游戏连接测试
- 性能测试

### 7. 提交规范

**Commit Message格式**：
```
<type>: <subject>

<body>
```

**Type类型**：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具

**示例**：
```
feat: 添加图像识别引擎基础框架

- 实现模板匹配算法
- 添加多尺度支持
- 集成缓存机制
```

### 8. 分支策略

**主分支**：
- `main`: 稳定版本
- `develop`: 开发版本

**功能分支**：
- `feature/xxx`: 新功能
- `bugfix/xxx`: 问题修复
- `hotfix/xxx`: 紧急修复

### 9. 注意事项

**PyQt特殊说明**：
- PyQt程序必须在有图形界面的环境运行
- WSL默认不支持GUI，需Windows运行
- 可在WSL中编写和验证逻辑代码
- GUI相关代码只做语法检查

**ADB连接**：
- Windows运行时连接实际设备/模拟器
- WSL中可编写ADB命令逻辑
- 使用mock对象进行逻辑测试

### 10. 项目结构要求

```
sps_game/
├── ARCHITECTURE.md          # 架构文档
├── DEVELOPMENT_CONSTRAINTS.md # 本文档
├── README.md                # 项目说明
├── requirements.txt         # 依赖清单
├── .gitignore              # Git忽略
├── core/                   # 核心框架
├── games/                  # 游戏适配
├── gui/                    # PyQt界面
├── plugins/                # 插件系统
├── tests/                  # 测试用例
└── scripts/                # 辅助脚本
```

---

**记住**：WSL只写代码，Windows才运行。

**原则**：代码平台无关，运行平台相关。