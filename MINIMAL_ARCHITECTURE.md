# 精简架构 - 真正的地基

## 🏗️ 核心理念

**"吃什么买什么，吃多少买多少"** - 需求驱动，拒绝过度设计

## 📁 极简目录结构

```
sps_game/
├── core/               # 核心地基（20%的代码，80%的功能）
│   ├── __init__.py    # Result[T] 错误处理
│   ├── drivers/       # 驱动层 - 与设备交互
│   │   ├── adb.py     # ADB连接和命令
│   │   ├── screen.py  # 截图
│   │   └── input.py   # 点击、滑动
│   ├── vision/        # 识别层 - 看懂游戏
│   │   ├── template.py # 模板匹配
│   │   └── ocr.py     # 文字识别（需要时再加）
│   ├── game.py        # 游戏主逻辑
│   └── utils.py       # 简单工具函数
├── games/             # 具体游戏实现
│   └── sps/          # 杖剑传说
│       ├── tasks.py  # 任务脚本
│       └── assets/   # 图片资源
├── main.py           # 程序入口
└── config.yaml       # 配置文件
```

## ✅ 保留的核心功能（真正的地基）

### 1. **ADB驱动** - 没它啥都干不了
```python
class ADBDriver:
    def connect(device_id) -> Result[bool]
    def shell(command) -> Result[str]
    def screenshot() -> Result[bytes]
```

### 2. **屏幕驱动** - 得看见游戏
```python
class ScreenDriver:
    def capture() -> Result[Image]
    def save_screenshot(path)
```

### 3. **输入驱动** - 得能操作
```python
class InputDriver:
    def tap(x, y) -> Result[bool]
    def swipe(x1, y1, x2, y2) -> Result[bool]
    def text(content) -> Result[bool]
```

### 4. **模板识别** - 得知道点哪
```python
class TemplateRecognizer:
    def find(template, image) -> Result[Location]
    def find_all(template, image) -> Result[List[Location]]
```

### 5. **游戏控制** - 串起来
```python
class Game:
    def __init__(adb, screen, input, recognizer)
    def tap_image(template_path) -> Result[bool]
    def wait_for(template_path, timeout=10) -> Result[bool]
    def run_task(task_func)
```

## ❌ 删除的过度设计（80%的废物）

- ~~EventDispatcher~~ - 完全不需要
- ~~EventQueue持久化~~ - SQLite对游戏自动化毫无意义
- ~~ConfigValidator/Migrator~~ - 过早优化
- ~~热重载~~ - 配置改动频率极低
- ~~Prometheus导出~~ - 单机程序不需要工业级监控
- ~~火焰图~~ - 性能瓶颈很明显（图像识别）
- ~~贝塞尔曲线~~ - 大部分游戏不检测
- ~~复杂的Result[T]用法~~ - 简单try-except就够了

## 🎯 使用示例

```python
# main.py - 极简的使用方式
from core import Game
from games.sps import tasks

# 初始化
game = Game(device_id="emulator-5554")

# 连接设备
if not game.connect():
    print("连接失败")
    exit()

# 运行任务
game.run_task(tasks.daily_energy)  # 领体力
game.run_task(tasks.daily_dungeon)  # 刷副本
```

```python
# games/sps/tasks.py - 简单的任务定义
def daily_energy(game):
    """领取每日体力"""
    game.tap_image("assets/main_menu.png")
    game.wait_for("assets/energy_icon.png")
    game.tap_image("assets/claim_button.png")
    return True
```

## 📊 对比

| 指标 | 原架构 | 精简架构 |
|-----|-------|---------|
| 代码行数 | ~5000 | ~1000 |
| 文件数 | 30+ | 10 |
| 依赖项 | 20+ | 5 |
| 启动时间 | 3s | <0.5s |
| 理解成本 | 高 | 低 |
| 维护成本 | 高 | 低 |

## 🚀 下一步

1. **先跑起来** - 连接设备、截图、点击
2. **解决实际问题** - 遇到什么问题解决什么
3. **按需添加** - 需要OCR时再加OCR，需要状态机时再加状态机

## 💡 核心原则

- **YAGNI** (You Aren't Gonna Need It) - 不要提前实现
- **KISS** (Keep It Simple, Stupid) - 保持简单
- **DRY** (Don't Repeat Yourself) - 但不要过度抽象
- **问题驱动** - 有问题再解决，没问题别创造问题

---

**记住：地基打好，房子才稳。先让它能跑，再让它跑得快。**