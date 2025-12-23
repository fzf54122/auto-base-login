# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:03
# @Author  : fzf
# @FileName: types.py
# @Software: PyCharm
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(slots=True)
class LoginOptions:
    headless: bool = False
    timeout_ms: int = 180_000          # 登录等待总超时
    nav_timeout_ms: int = 30_000       # 单次 goto 超时
    auth_wait_ms: int = 5_000

    browser_args: list[str] = field(default_factory=lambda: ["--lang=en-GB"])

    # 使用系统 Chrome 时可填；否则默认 Playwright 管理的 chromium
    executable_path: str | None = None
    channel: str | None = None         # 例如 "chrome"（可选）

    # 排障
    artifacts_dir: str = "./artifacts" # 截图/trace 输出目录
    enable_trace: bool = False         # 需要时打开
    enable_screenshot_on_error: bool = True

    # 重试
    retries: int = 2
    retry_backoff_ms: int = 800


@dataclass(slots=True)
class LoginResponse:
    ok: bool
    reason: str
    path: str | None = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def data(self) -> Dict[str, Any]:
        return {"ok": self.ok, "reason": self.reason, "path": self.path, "extra": self.extra}
