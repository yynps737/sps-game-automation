# Windows 部署指南

## 📦 迁移到 Windows (D:\pyproject)

### 1️⃣ 在WSL中打包
```bash
cd /home/kkb/sps_game
tar -czf sps_game.tar.gz --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' .
```

### 2️⃣ 复制到Windows
```bash
# 方法1: 直接复制到Windows路径
cp sps_game.tar.gz /mnt/d/pyproject/

# 方法2: 使用Windows Explorer
# 在WSL中运行:
explorer.exe .
# 然后手动复制 sps_game.tar.gz 到 D:\pyproject
```

### 3️⃣ 在Windows解压
```powershell
# 在 PowerShell 中:
cd D:\pyproject
tar -xzf sps_game.tar.gz -C sps_game
# 或使用 7-Zip/WinRAR 解压
```

### 4️⃣ 安装Python依赖
```powershell
cd D:\pyproject\sps_game
pip install -r requirements-minimal.txt
```

### 5️⃣ 配置MuMu12
1. 启动MuMu12模拟器
2. 在MuMu12设置中开启"开发者选项" → "USB调试"
3. 确保Windows防火墙允许ADB连接

### 6️⃣ 测试连接
```powershell
# 测试ADB连接
adb connect 127.0.0.1:16384

# 运行测试脚本
python test_connection.py
```

### 7️⃣ 运行主程序
```powershell
python main.py
```

## 🔧 Windows特定配置

### ADB安装
如果没有adb命令:
1. 下载 [Android Platform Tools](https://developer.android.com/studio/releases/platform-tools)
2. 解压到 `D:\tools\platform-tools`
3. 添加到系统PATH环境变量

### Python路径
确保使用Python 3.11.9:
```powershell
python --version
# Python 3.11.9
```

### 目录结构
```
D:\pyproject\
└── sps_game\
    ├── core\           # 核心框架
    ├── games\          # 游戏脚本
    ├── config.yaml     # 配置文件
    ├── main.py         # 主程序
    └── test_connection.py  # 测试脚本
```

## 🚀 快速开始

```python
# D:\pyproject\sps_game\quick_start.py
from core.game import Game

# 连接MuMu12
game = Game("127.0.0.1:16384")
if game.connect():
    print("✅ 连接成功")
    
    # 截图测试
    screen = game.screenshot()
    if screen:
        print("✅ 截图成功")
    
    # 断开连接
    game.disconnect()
else:
    print("❌ 连接失败")
```

## ⚠️ 常见问题

### 问题1: adb不是内部命令
**解决**: 下载并配置Android Platform Tools到PATH

### 问题2: MuMu12连接失败
**解决**: 
- 确保MuMu12已启动
- 尝试端口 127.0.0.1:7555
- 检查防火墙设置

### 问题3: ImportError: No module named 'cv2'
**解决**: `pip install opencv-python==4.9.0.80`

### 问题4: numpy版本冲突
**解决**: `pip install numpy==1.26.4 --force-reinstall`