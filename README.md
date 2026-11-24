# del_files.py — 按扩展名批量删除文件

> 一个安全优先的命令行工具：默认预演（dry-run）+ 确认交互 + 回收站备份，杜绝误删。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![No Dependencies](https://img.shields.io/badge/依赖-纯标准库-success)

## 特性

- **默认预演** — 先列出所有待删文件及大小，确认后才动手
- **回收站机制** — 删除的文件移入 `_回收站_时间戳` 文件夹，随时反悔
- **删除清单** — 自动生成 `删除清单.txt`，可追溯每一张被删文件的来源
- **递归扫描** — 默认深入所有子目录，保持目录结构
- **大小写兼容** — `.JPG` / `.jpg`均可匹配
- **零依赖** — 只用 Python 标准库，无需 pip 安装任何东西

## 快速开始

### 安装

无需安装依赖，克隆或直接下载 `del_files.py` 即可：

```bash
git clone https://github.com/yourname/del_files.git
cd del_files
```

### 基本用法

```bash
# 删除当前目录所有 .tmp 文件（会先预演并列出，输入 y 确认）
python del_files.py

# 指定目录和多种扩展名
python del_files.py "D:\Photos" -e heic jpg

# 跳过确认，直接执行（适合脚本自动化）
python del_files.py "D:\Photos" -e heic --confirm

# 只处理顶层目录，不进子文件夹
python del_files.py "D:\Downloads" -e tmp --no-recurse

# 永久删除（不进回收站，危险！）
python del_files.py "D:\Photos" -e heic --permanent
```

## 命令行参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `src` | 目标目录 | 当前目录 `.` |
| `-e, --ext <扩展名...>` | 要删除的扩展名，可多个 | `tmp` |
| `--confirm` | 跳过交互确认 | 关 |
| `--no-recurse` | 只处理顶层，不进子目录 | 关 |
| `--permanent` | 永久删除，不移入回收站 | 关（默认进回收站） |

## 安全设计

1. **预演优先** — 扫描后先完整列出匹配文件（含大小）。
2. **回收站缓冲** — 实际删除时文件被移入源目录下的 `_回收站_时间戳/`，保留原有目录结构，需要时可整体搬回。
3. **清单留痕** — 回收站内自动生成 `删除清单.txt`，记录删除时间、来源目录及所有文件。

> `--permanent` 会绕过回收站直接调用 `os.remove`，请确认后再使用。
