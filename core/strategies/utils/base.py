# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:03
# @Author  : fzf
# @FileName: base.py
# @Software: PyCharm
# mcplogin/base.py
from __future__ import annotations
from abc import ABC, abstractmethod
from ...schemas import LoginOptions, LoginResponse
from ...enums import LoginReasonType
import os


class LoginStrategy(ABC):
    """每个平台实现：生成cookie、校验cookie。"""

    name: str  # platform key，如 "baijiahao"

    @abstractmethod
    async def login_and_save(self, account_file: str, options: LoginOptions) -> LoginResponse:
        """打开登录页（扫码/账号登录）并保存 storage_state 到 account_file。"""
        ...

    @abstractmethod
    async def auth(self, account_file: str, options: LoginOptions) -> LoginResponse:
        """校验 account_file 是否仍有效。"""
        ...

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
