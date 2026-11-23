#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reading 每日一篇格式檢查器 — 出題品質把關

檢查每篇 .md：
  1. 每題有 4 個選項（A/B/C/D）
  2. 選項順序必須 A→B→C→D（唔可以亂序）
  3. 答案字母存在於選項
  4. 必須有「文中依據」引原文
  5. 必須有 💡技巧 同 ⚠️陷阱
  6. 題數 = 8
"""
import glob
import re
import sys

OPT_RE = re.compile(r"^-\s*([A-D])[.、]\s*(.+)$")
Q_RE = re.compile(r"^###\s*Q(\d+)\s*[（(]([^）)]+)[）)]")
ANS_RE = re.compile(r"\*\*答案：?\*\*\s*([A-D])")


def parse_block(lines):
    opts, ans, basis, tip, trap = [], None, "", "", ""
    for ln in lines:
        m = OPT_RE.match(ln.strip())
        if m:
            opts.append((m.group(1), m.group(2).strip()))
        if "答案" in ln and ans is None:
            a = ANS_RE.search(ln)
            if a:
                ans = a.group(1)
        if "文中依據" in ln:
            basis = ln.split("**文中依據：**")[-1].strip()
        if "技巧" in ln:
            tip = ln
        if "陷阱" in ln:
            trap = ln
    return opts, ans, basis, tip, trap


def check_file(path):
    text = open(path, encoding="utf-8").read()
    errors, warns = [], []
    # 切題
    parts = re.split(r"(?m)^###\s*Q", text)
    blocks = []
    for p in parts[1:]:
        header, _, body = p.partition("\n")
        blocks.append(("Q" + header.strip(), body.splitlines()))
    if len(blocks) != 8:
        errors.append(f"題數 {len(blocks)}，應為 8")
    for name, lines in blocks:
        opts, ans, basis, tip, trap = parse_block(lines)
        if len(opts) != 4:
            errors.append(f"{name}: 選項 {len(opts)} 個（應 4 個）")
            continue
        letters = [o[0] for o in opts]
        if letters != ["A", "B", "C", "D"]:
            errors.append(f"{name}: 選項亂序 {letters}（應 A,B,C,D）")
        if not ans:
            errors.append(f"{name}: 搵唔到答案字母")
        elif ans not in letters:
            errors.append(f"{name}: 答案 {ans} 唔喺選項內 {letters}")
        if not basis:
            errors.append(f"{name}: 缺「文中依據」")
        if not tip:
            warns.append(f"{name}: 缺 💡技巧")
        if not trap:
            warns.append(f"{name}: 缺 ⚠️陷阱")
        # 重複選項
        vals = [o[1] for o in opts]
        if len(set(vals)) != len(vals):
            errors.append(f"{name}: 有重複選項")
    return errors, warns, len(blocks)


def main(paths):
    total_err = 0
    for p in sorted(paths):
        errs, warns, n = check_file(p)
        name = p.split("/")[-1]
        if errs:
            total_err += len(errs)
            print(f"\n❌ {name}（{n} 題）")
            for e in errs:
                print("   •", e)
        else:
            print(f"\n✅ {name}（{n} 題）結構 OK")
        for w in warns:
            print("   ⚠️", w)
    print(f"\n總錯誤：{total_err}")
    return 1 if total_err else 0


if __name__ == "__main__":
    args = sys.argv[1:] or glob.glob("Reading/*.md")
    sys.exit(main([a for a in args if not a.endswith("README.md")]))
