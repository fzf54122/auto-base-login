# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:03
# @Author  : fzf
# @FileName: base.py
# @Software: PyCharm
from __future__ import annotations
from abc import ABC, abstractmethod
import os

from playwright.async_api import Page

from ...schemas import LoginOptions, LoginResponse
from ...enums import LoginReasonType, LoginStrategyType
from .playwright_base import BasePlaywrightStrategy


class LoginStrategy(ABC,
                    BasePlaywrightStrategy):
    """每个平台实现：生成cookie、校验cookie。"""

    async def login_and_save(self, account_file: str, options: LoginOptions) -> LoginResponse:
        try:
            return await self.execute(account_file, options, mode=LoginStrategyType.LOGIN)
        except Exception as e:
            return LoginResponse(False, LoginReasonType.UNKNOWN_ERROR, path=account_file, extra={"err": str(e)})

    async def auth(self, account_file: str, options: LoginOptions) -> LoginResponse:
        if not os.path.exists(account_file):
            return LoginResponse(False, LoginReasonType.COOKIE_FILE_MISSING, path=account_file)

        try:
            return await self.execute(account_file, options, mode=LoginStrategyType.AUTH)
        except Exception as e:
            return LoginResponse(False, LoginReasonType.PLAYWRIGHT_ERROR, path=account_file, extra={"err": str(e)})

    async def setup(self, account_file: str, options: LoginOptions, handle: bool = False) -> LoginResponse:
        """不存在/失效则（可选）触发登录生成。"""

        if not os.path.exists(account_file):
            if not handle:
                return LoginResponse(False, LoginReasonType.COOKIE_FILE_MISSING, path=account_file)
            return await self.login_and_save(account_file, options)
        auth_res = await self.auth(account_file, options)

        if auth_res.ok:
            return auth_res
        if not handle:
            return LoginResponse(False, LoginReasonType.COOKIE_INVALID, path=account_file)
        return await self.login_and_save(account_file, options)
