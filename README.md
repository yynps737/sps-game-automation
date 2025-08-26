# SPS Game Automation Framework

Minimal game automation framework for 杖剑传说 (Staff and Sword Legend) mobile game.

## ✨ Features

- 🎮 **MuMu12 Emulator Support** - Optimized for MuMu12 Android emulator
- 📱 **Simple ADB Control** - Direct subprocess calls, no complex dependencies  
- 🔍 **Image Recognition** - OpenCV-based template matching
- 🎯 **Clean Architecture** - Only ~1400 lines of essential code
- ⚡ **Fast & Lightweight** - Minimal dependencies, quick startup

## 🚀 Quick Start

### Prerequisites
- Python 3.11.8+
- MuMu12 Emulator
- ADB (Android Debug Bridge)

### Installation

```bash
# Clone repository
git clone https://github.com/yynps737/sps-game-automation.git
cd sps-game-automation

# Install dependencies
pip install -r requirements-minimal.txt
```

### Basic Usage

```python
from core.game import Game

# Connect to MuMu12
game = Game("127.0.0.1:16384")
game.connect()

# Basic operations
game.tap(500, 300)                    # Tap coordinates
game.tap_image("button.png")          # Find and tap image
game.swipe(500, 1000, 500, 200)      # Swipe up
game.wait_for("loading.png", 10)      # Wait for image

# Disconnect
game.disconnect()
```

### Test Connection

```bash
# Test MuMu12 connection
python test_connection.py

# Quick functionality test
python quick_start.py
```

## 📁 Project Structure

```
sps-game-automation/
├── core/               # Core framework
│   ├── game.py        # Main game controller
│   ├── drivers/       # ADB and input drivers
│   └── config/        # Configuration management
├── config.yaml        # Settings
├── main.py           # Entry point
└── requirements-minimal.txt  # Dependencies
```

## 🛠️ Configuration

Edit `config.yaml`:

```yaml
device:
  id: "127.0.0.1:16384"  # MuMu12 default port
  
game:
  name: "杖剑传说"
  package: "com.sstudio.zjcs"
```

## 📦 Minimal Dependencies

- opencv-python - Image recognition
- numpy - Array operations  
- PyYAML - Configuration
- loguru - Logging
- Pillow - Image handling

## 🎯 Design Philosophy

- **YAGNI** - You Aren't Gonna Need It
- **KISS** - Keep It Simple, Stupid
- **Clean Code** - Removed 72% of over-engineered code
- **Practical** - Solve real problems, not imaginary ones

## 📄 License

MIT License

## 🤝 Contributing

Pull requests are welcome. Keep it simple and practical.

---

*"The perfect is the enemy of the good."*