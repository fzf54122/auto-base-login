# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:03
# @Author  : fzf
# @FileName: types.py
# @Software: PyCharm
from __future__ import annotations
from dataclasses import dataclass, field, asdict, is_dataclass
from typing import Any, Dict

from .config import settings


class DataMixin:
    @property
    def data(self) -> Dict[str, Any]:
        if not is_dataclass(self):
            raise TypeError(f"{type(self)!r} is not a dataclass")
        return asdict(self)


# 业务层
@dataclass(slots=True)
class LoginOptions(DataMixin):
    headless: bool = False
    timeout_ms: int = 300_000  # 登录等待总超时
    nav_timeout_ms: int = 30_000  # 单次 goto 超时
    auth_wait_ms: int = 150_000

    browser_args: list[str] = field(default_factory=lambda: ["--lang=en-GB"])

    # 使用系统 Chrome 时可填；否则默认 Playwright 管理的 chromium
    executable_path: str | None = None
    channel: str | None = None  # 例如 "chrome"（可选）

    # 排障
    artifacts_dir: str = "./artifacts"  # 截图/trace 输出目录
    enable_trace: bool = False  # 需要时打开
    enable_screenshot_on_error: bool = True

    # 重试
    retries: int = 2
    retry_backoff_ms: int = 800

    @property
    def default(self) -> LoginOptions:
        return LoginOptions(
            headless=settings.PW_HEADLESS,
            timeout_ms=settings.PW_TIMEOUT_MS,
            nav_timeout_ms=settings.PW_NAV_TIMEOUT_MS,
            auth_wait_ms=settings.PW_AUTH_WAIT_MS,
            browser_args=settings.PW_BROWSER_ARGS,
            executable_path=settings.PW_EXECUTABLE_PATH,
            channel=settings.PW_CHANNEL,
            artifacts_dir=settings.ARTIFACTS_DIR,
            enable_trace=settings.PW_ENABLE_TRACE,
            enable_screenshot_on_error=settings.PW_ENABLE_SCREENSHOT_ON_ERROR,
            retries=settings.PW_RETRIES,
            retry_backoff_ms=settings.PW_RETRY_BACKOFF_MS,
        )


@dataclass(slots=True)
class LoginResponse(DataMixin):
    ok: bool | None = None
    reason: str | None = None
    path: str | None = None
    extra: Dict[str, Any] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)


if __name__ == "__main__":
    opts = LoginOptions()
    login = LoginResponse()
    print(opts.data)
    print(login.data)
