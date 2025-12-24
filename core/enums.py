# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:15
# @Author  : fzf
# @FileName: emums.py
# @Software: PyCharm
from enum import StrEnum


class LoginReasonType(StrEnum):
    # 通用
    OK = "ok"
    COOKIE_SAVED = "cookie_saved"
    COOKIE_VALID = "cookie_valid"
    COOKIE_INVALID = "cookie_invalid"
    COOKIE_FILE_MISSING = "cookie_file_missing"

    # 流程/超时
    LOGIN_TIMEOUT = "login_timeout"
    NAVIGATION_TIMEOUT = "navigation_timeout"
    ELEMENT_TIMEOUT = "element_timeout"
    RETRY_EXHAUSTED = "retry_exhausted"

    # 浏览器/环境
    BROWSER_LAUNCH_FAILED = "browser_launch_failed"
    PLAYWRIGHT_ERROR = "playwright_error"

    # 未知
    UNKNOWN_ERROR = "unknown_error"


class StrategyModeType(object):
    AUTH = "auth"
    LOGIN = "login_and_save"


class LoginStrategyType(StrategyModeType):
    BAIJIAHAO = "baijiahao"
    TOUTIAO = "toutiao"
    NETEASE = "netease"
    SOHU = "sohu"
    DAYU = "dayu"
    PENGUIN = "penguin"
    YIDIAN = "yidian"



if __name__ == '__main__':
    print(LoginStrategyType.AUTH)