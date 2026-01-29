
# Plants vs Zombies - Python 项目

## 项目简介
这是一个用 **Python + Pygame** 开发的 **Plants vs Zombies（植物大战僵尸）** 游戏示例项目，实现了游戏的基本功能，支持在 **Windows 平台** 运行。 项目包含音频和图片资源。  
玩家可以通过鼠标操作进行游戏。

---

## 项目结构

```
final_project/
├─ src/                  # 游戏源码
│  ├─ Controllers/       # 控制逻辑
│  ├─ Plants/            # 植物类
│  ├─ Zombies/           # 僵尸类
│  └─ main.py            # 游戏入口
├─ audio/                # 音频资源
│  ├─ click/
│  ├─ plants/
│  ├─ ready/
│  └─ zombies/
├─ image/                # 图片资源
│  ├─ gaming/
│  ├─ init/
│  ├─ Plants/
│  ├─ start/
│  └─ Zombies/
├─ save/                 # 游戏存档
├─ dist/                 # PyInstaller 输出 EXE（打包后生成）
└─ build/                # PyInstaller 临时目录（打包时生成）
```

---

## 运行方法

### 方案一：使用 Python 源码运行
1. 在项目根目录下创建环境：
   ```bash
   conda env create -f environment.yml
   conda activate pvz
   ```
2. 运行游戏：
   ```bash
   python src\main.py
   ```
   即可看到游戏运行界面。

### 方案二：运行打包后的 EXE
- 双击 `dist\pvz_game.exe`，即可直接启动游戏。

---
