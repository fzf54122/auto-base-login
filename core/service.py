# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:03
# @Author  : fzf
# @FileName: service.py
# @Software: PyCharm
from __future__ import annotations
from .strategies import LoginStrategyFactory
from .types import LoginOptions, LoginResponse


class LoginService:

    @staticmethod
    async def setup(platform: str, account_file: str, *, handle: bool = False, options: LoginOptions | None = None) -> LoginResponse:
        options = options or LoginOptions()
        strategy = LoginStrategyFactory.get(platform)
        return await strategy.setup(account_file, options, handle=handle)

    @staticmethod
    async def auth(platform: str, account_file: str, *, options: LoginOptions | None = None) -> LoginResponse:
        options = options or LoginOptions()
        strategy = LoginStrategyFactory.get(platform)
        return await strategy.auth(account_file, options)

    @staticmethod
    async def login_and_save(platform: str, account_file: str, *, options: LoginOptions | None = None) -> LoginResponse:
        options = options or LoginOptions()
        strategy = LoginStrategyFactory.get(platform)
        return await strategy.login_and_save(account_file, options)