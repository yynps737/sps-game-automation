# 官方 ADB (Android SDK Platform Tools) 安装指南

## 📥 官方下载地址

**Google官方下载页面**: https://developer.android.com/tools/releases/platform-tools

## 🔧 Windows 安装步骤

### 步骤 1: 下载

1. 访问官方页面: https://developer.android.com/tools/releases/platform-tools
2. 点击 **"Download SDK Platform-Tools for Windows"**
3. 接受条款并下载 `platform-tools-latest-windows.zip`
4. 文件大小约 7-8 MB

### 步骤 2: 解压

1. 创建目录: `C:\Android\` 或 `D:\tools\`
2. 将下载的ZIP文件解压到该目录
3. 解压后路径应该是: `C:\Android\platform-tools\` 或 `D:\tools\platform-tools\`
4. 确认存在文件: `adb.exe`, `fastboot.exe` 等

### 步骤 3: 添加到系统 PATH

#### 方法A: 通过系统设置 (推荐)
1. 按 `Win + X`，选择 **"系统"**
2. 点击 **"高级系统设置"**
3. 点击 **"环境变量"**
4. 在系统变量中找到 **"Path"**，点击 **"编辑"**
5. 点击 **"新建"**，添加: `C:\Android\platform-tools`
6. 点击 **"确定"** 保存所有窗口

#### 方法B: 通过命令行 (需要管理员权限)
```powershell
# PowerShell (管理员)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Android\platform-tools", [EnvironmentVariableTarget]::Machine)
```

### 步骤 4: 验证安装

1. **重新打开** 命令提示符或 PowerShell (重要!)
2. 运行测试命令:

```cmd
adb version
```

应该显示:
```
Android Debug Bridge version 1.0.41
Version 35.0.2-12147458
Installed as C:\Android\platform-tools\adb.exe
```

## 🔌 连接 MuMu12 模拟器

### 1. 启动 MuMu12

### 2. 开启 USB 调试
- 设置 → 关于平板电脑
- 连续点击 "版本号" 7次 开启开发者选项
- 返回设置 → 开发者选项
- 开启 "USB 调试"

### 3. 连接模拟器

```cmd
# MuMu12 默认端口
adb connect 127.0.0.1:16384

# 或者尝试备用端口
adb connect 127.0.0.1:7555
```

### 4. 验证连接

```cmd
adb devices
```

应该显示:
```
List of devices attached
127.0.0.1:16384 device
```

## 📊 包含的工具

Platform Tools 包含:
- **adb.exe** - Android Debug Bridge
- **fastboot.exe** - Fastboot 工具
- **etc1tool.exe** - ETC1 压缩工具
- **hprof-conv.exe** - HPROF 转换工具
- **sqlite3.exe** - SQLite 数据库工具

## ⚠️ 常见问题

### 问题: adb不是内部或外部命令
**解决**: 
- 确保已添加到 PATH
- 重启命令行窗口
- 使用完整路径: `C:\Android\platform-tools\adb.exe`

### 问题: cannot connect to 127.0.0.1:16384
**解决**:
- 确认 MuMu12 已启动
- 确认 USB 调试已开启
- 尝试其他端口: 7555, 5555

### 问题: unauthorized device
**解决**:
- 在模拟器中允许 USB 调试授权
- 重新连接: `adb kill-server` 然后 `adb connect`

## 📌 版本信息

- **最新版本**: 35.0.2 (2024年)
- **官方网站**: https://developer.android.com
- **支持系统**: Windows 7/8/10/11

## 🚀 在项目中使用

安装完成后，在项目目录运行:

```cmd
cd D:\pyproject\sps-game-automation
python quick_start.py
```

程序会自动检测 ADB 安装位置！