# -*- coding: utf-8 -*-
"""无依赖校验 registry plugins.json（镜像 schema 关键约束）。用法：python validate_index.py"""
import json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
idx = json.load(open(os.path.join(BASE, "plugins.json"), encoding="utf-8"))
REQ = ["id", "name", "description", "author", "version", "apiVersion",
       "repository", "permissions", "publishedAt"]
ALLOW = set(REQ + ["status", "license", "icon", "homepage", "releaseUrl",
                   "downloadUrl", "requires", "tags"])
errs = []

if not re.fullmatch(r"\d+\.\d+\.\d+", idx["registryVersion"]):
    errs.append("registryVersion pattern")
for p in idx["plugins"]:
    pid = p.get("id", "?")
    for k in REQ:
        if k not in p:
            errs.append(f"{pid}: missing {k}")
    extra = set(p) - ALLOW
    if extra:
        errs.append(f"{pid}: extra keys {sorted(extra)}")
    if p["status"] not in ("active", "pending"):
        errs.append(f"{pid}: bad status {p['status']}")
    if p["status"] == "active":
        if "releaseUrl" not in p or "downloadUrl" not in p:
            errs.append(f"{pid}: active missing releaseUrl/downloadUrl")
    if not re.fullmatch(r"[a-z][a-z0-9-]*(\.[a-z0-9-]+)+", pid):
        errs.append(f"{pid}: id pattern fail")
    if not re.fullmatch(r"\d+\.\d+\.\d+", p["version"]):
        errs.append(f"{pid}: version pattern fail")
    for u in ("releaseUrl", "downloadUrl"):
        if u in p and not p[u].startswith("https://"):
            errs.append(f"{pid}: {u} not https")

active = sum(1 for p in idx["plugins"] if p["status"] == "active")
if errs:
    print("ERRORS:", *errs, sep="\n  ")
    sys.exit(1)
print(f"VALID: {len(idx['plugins'])} entries, {active} active, 0 errors")
