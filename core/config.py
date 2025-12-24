# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:16
# @Author  : fzf
# @FileName: config.py
# @Software: PyCharm
from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing import List


def _env(key: str, default: str) -> str:
    return os.getenv(key, default)


def _env_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default


def _env_bool(key: str, default: bool) -> bool:
    v = os.getenv(key)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


class URLConfig:
    # 平台 URL / 关键文案
    # 百家号
    BAIJIAHAO_LOGIN_URL: str = "https://baijiahao.baidu.com/builder/theme/bjh/login"
    BAIJIAHAO_HOME_URL: str = "https://baijiahao.baidu.com/builder/rc/home"
    BAIJIAHAO_NEED_LOGIN_TEXT: str = "注册/登录百家号"

    # 头条号
    TOUTIAO_LOGIN_URL: str = "https://sso.toutiao.com/login/"
    TOUTIAO_HOME_URL: str = "https://mp.toutiao.com/profile_v4/index"
    TOUTIAO_NEED_LOGIN_TEXT: str = "登录"

    # 网易号
    NETEASE_LOGIN_URL: str = "https://mp.163.com/login.html"
    NETEASE_HOME_URL: str = "https://mp.163.com/writer#/"
    NETEASE_NEED_LOGIN_TEXT: str = "登录"

    # 搜狐号
    SOHU_LOGIN_URL: str = "https://mp.sohu.com/mpfe/v3/login"
    SOHU_HOME_URL: str = "https://mp.sohu.com/main.html"
    SOHU_NEED_LOGIN_TEXT: str = "登录"

    # 大鱼号
    DAYU_LOGIN_URL: str = "https://mp.dayu.com/account/login"
    DAYU_HOME_URL: str = "https://mp.dayu.com/dashboard"
    DAYU_NEED_LOGIN_TEXT: str = "登录"

    # 企鹅号
    PENGUIN_LOGIN_URL: str = "https://om.qq.com/user/auth/login"
    PENGUIN_HOME_URL: str = "https://om.qq.com/user/home"
    PENGUIN_NEED_LOGIN_TEXT: str = "登录"

    # 一点号
    YIDIAN_LOGIN_URL: str = "https://mp.yidianzixun.com/login"
    YIDIAN_HOME_URL: str = "https://mp.yidianzixun.com/dashboard"
    YIDIAN_NEED_LOGIN_TEXT: str = "登录"


@dataclass(slots=True)
class Config(URLConfig):
    # 日志
    LOGGER_LEVEL: str = _env("LOGIN_LOG_LEVEL", "INFO")

    # 目录（强烈建议统一）
    DATA_DIR: str = _env("LOGIN_DATA_DIR", "./data")
    COOKIE_DIR: str = _env("LOGIN_COOKIE_DIR", "./data/cookies")
    ARTIFACTS_DIR: str = _env("LOGIN_ARTIFACTS_DIR", "./data/artifacts")

    # Playwright 默认参数
    PW_HEADLESS: bool = _env_bool("PW_HEADLESS", False)
    PW_TIMEOUT_MS: int = _env_int("PW_TIMEOUT_MS", 180_000)
    PW_NAV_TIMEOUT_MS: int = _env_int("PW_NAV_TIMEOUT_MS", 30_000)
    PW_AUTH_WAIT_MS: int = _env_int("PW_AUTH_WAIT_MS", 5_000)

    PW_RETRIES: int = _env_int("PW_RETRIES", 2)
    PW_RETRY_BACKOFF_MS: int = _env_int("PW_RETRY_BACKOFF_MS", 800)

    PW_ENABLE_TRACE: bool = _env_bool("PW_ENABLE_TRACE", False)
    PW_ENABLE_SCREENSHOT_ON_ERROR: bool = _env_bool("PW_ENABLE_SCREENSHOT_ON_ERROR", True)

    PW_EXECUTABLE_PATH: str | None = os.getenv("PW_EXECUTABLE_PATH")  # /usr/bin/google-chrome-stable
    PW_CHANNEL: str | None = os.getenv("PW_CHANNEL")  # "chrome"
    PW_BROWSER_ARGS: List[str] = field(
        default_factory=lambda: _env("PW_BROWSER_ARGS", "--lang=en-GB").split())

settings = Config()
