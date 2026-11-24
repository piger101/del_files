机制	             说明
默认预演	           先列出所有匹配文件和大小，输入 y 确认后才动手
默认进回收站	       不直接删，移入 _回收站_时间戳 文件夹，反悔了还能整体搬回去
删除清单	           回收站里自动生成 删除清单.txt，记录删了什么、从哪删的
大小写兼容	         .JPG 和 .jpg 都能匹配；e heic、e .heic、-e .HEIC 写法都接受
路径防呆	            目录不存在会直接报错退出，路径含空格/中文建议加引号

使用方法：

# 删除 D:\Photos 下所有 heic 文件（默认会先列出，输入 y 才执行）
python del_files.py "D:\Photos" -e heic

# 一次删除多种类型
python del_files.py "D:\Photos" -e heic tmp log bak

# 只删顶层目录的 .tmp，不动子文件夹
python del_files.py "D:\Downloads" -e tmp --no-recurse

# 自动化脚本里用：跳过确认
python del_files.py "D:\Photos" -e heic --confirm
