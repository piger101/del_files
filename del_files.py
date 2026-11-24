# -*- coding: utf-8 -*-
"""
按扩展名删除文件的工具
用法:
    python del_files.py                          # 删除当前目录所有 .tmp 文件（先预演）
    python del_files.py D:\Photos -e heic jpg    # 删除多种类型
    python del_files.py D:\Photos -e log --confirm   # 跳过确认直接执行
    python del_files.py D:\Photos -e tmp --no-recurse # 只处理顶层，不进子目录
"""
import os
import sys
import shutil
import argparse
from datetime import datetime

def find_matches(src_dir, exts, recursive):
    """扫描目录，返回所有匹配扩展名的文件路径"""
    matched = []
    if recursive:
        walker = os.walk(src_dir)
    else:
        # 只看顶层：walk 的第一步就是 src_dir 本身
        walker = [next(os.walk(src_dir))]
    for root, _, files in walker:
        for f in files:
            if os.path.splitext(f)[1].lower().lstrip(".") in exts:
                matched.append(os.path.join(root, f))
    return matched

def main():
    parser = argparse.ArgumentParser(
        description="按扩展名删除文件（默认先预演，需确认后才真正删除，删除的文件移入回收站）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例: python del_files.py D:\\Photos -e heic")
    parser.add_argument("src", nargs="?", default=".", help="目标目录，默认当前目录")
    parser.add_argument("-e", "--ext", nargs="+", default=["tmp"],
                        help="要删除的扩展名，可多个，如: -e heic jpg png")
    parser.add_argument("--confirm", action="store_true",
                        help="跳过交互确认，直接执行（慎用）")
    parser.add_argument("--no-recurse", action="store_true",
                        help="只处理该目录顶层，不进入子目录")
    parser.add_argument("--permanent", action="store_true",
                        help="直接永久删除，不移入回收站（危险！默认移入回收站）")
    args = parser.parse_args()

    src_dir = os.path.abspath(args.src)
    if not os.path.isdir(src_dir):
        print(f"目录不存在: {src_dir}")
        sys.exit(1)

    exts = {e.lower().lstrip(".") for e in args.ext}   # 统一成无点小写
    recursive = not args.no_recurse

    # ---------- 第一步：预演（只列出，不删除） ----------
    matched = find_matches(src_dir, exts, recursive)
    if not matched:
        print(f"在 {src_dir} 中没有找到 {'/'.join('.'+e for e in exts)} 文件，无需操作")
        sys.exit(0)

    print(f"目标目录: {src_dir}")
    print(f"查找类型: {', '.join('.'+e for e in sorted(exts))}")
    print(f"共匹配 {len(matched)} 个文件:\n")
    for p in matched:
        size = os.path.getsize(p)
        print(f"  [{size/1024:.1f} KB] {os.path.relpath(p, src_dir)}")

    # ---------- 第二步：确认 ----------
    if not args.confirm:
        answer = input(f"\n确定删除以上 {len(matched)} 个文件吗? (y/N): ").strip().lower()
        if answer not in ("y", "yes"):
            print("已取消，未删除任何文件。")
            sys.exit(0)

    # ---------- 第三步：执行 ----------
    trash_dir = None
    if not args.permanent:
        trash_dir = os.path.join(src_dir, f"_回收站_{datetime.now():%Y%m%d_%H%M%S}")
        os.makedirs(trash_dir, exist_ok=True)

    ok, fail = 0, 0
    for src in matched:
        try:
            if trash_dir:
                # 移入回收站，保留相对目录结构，方便反悔时找回
                dst = os.path.join(trash_dir, os.path.relpath(src, src_dir))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)
            else:
                os.remove(src)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"  [失败] {os.path.relpath(src, src_dir)}: {e}")

    print(f"\n完成: 处理 {ok} 个，失败 {fail} 个")
    if trash_dir:
        print(f"文件已移入回收站（确认无误后可手动删除）: {trash_dir}")
        log = os.path.join(trash_dir, "删除清单.txt")
        with open(log, "w", encoding="utf-8") as fp:
            fp.write(f"删除时间: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
            fp.write(f"来源目录: {src_dir}\n共 {ok} 个文件:\n")
            for src in matched:
                fp.write(os.path.relpath(src, src_dir) + "\n")
        print(f"删除清单: {log}")

if __name__ == "__main__":
    main()
