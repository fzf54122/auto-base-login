# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:02
# @Author  : fzf
# @FileName: baijiahao.py
# @Software: PyCharm
from __future__ import annotations
import os
import time
import logging

from core.base import LoginStrategy
from core.types import LoginOptions,LoginResponse
from core.playwright_base import BasePlaywrightStrategy
from core.enums import (LoginReasonType,LoginStrategyType)
from core.logger import (get_logger,
                         LogCtx,
                         log_kv)
from config import settings


class BaijiahaoLogin(LoginStrategy,
                     BasePlaywrightStrategy):
    name = LoginStrategyType.BAIJIAHAO

    def __init__(self) -> None:
        self.logger = get_logger(LoginStrategyType.BAIJIAHAO)

    async def login_and_save(self, account_file: str, options: LoginOptions) -> LoginResponse:
        os.makedirs(os.path.dirname(account_file) or ".", exist_ok=True)
        ctx = LogCtx(self.name, account_file)

        async def _action(context):
            log_kv(self.logger, logging.INFO, "login start", **ctx.as_dict(), headless=options.headless)

            login_page = await context.new_page()
            await self.safe_goto(login_page, settings.BAIJIAHAO_LOGIN_URL, options)

            probe = await context.new_page()
            start = time.monotonic()

            while True:
                if (time.monotonic() - start) * 1000 > options.timeout_ms:
                    await self._capture_on_error(login_page, options, "bjh_login_timeout")
                    return LoginResponse(False, LoginReasonType.LOGIN_TIMEOUT, path=account_file)

                try:
                    await self.safe_goto(probe, settings.BAIJIAHAO_HOME_URL, options)
                    await probe.wait_for_timeout(1500)

                    need_login = await probe.get_by_text("注册/登录百家号").count()
                    if need_login == 0:
                        await context.storage_state(path=account_file)
                        log_kv(self.logger, logging.INFO, "cookie saved", **ctx.as_dict())
                        return LoginResponse(True, LoginReasonType.COOKIE_SAVED, path=account_file)
                except Exception as e:
                    # 页面偶发异常继续轮询
                    await probe.wait_for_timeout(1500)

        try:
            return await self.run_with_retry(options, "bjh_login_and_save", _action)
        except Exception as e:
            log_kv(self.logger, logging.ERROR, "login failed", **ctx.as_dict(), err=str(e))
            return LoginResponse(False, LoginReasonType.UNKNOWN_ERROR, path=account_file,
                                 extra={"err": str(e)})

    async def auth(self, account_file: str, options: LoginOptions) -> LoginResponse:
        ctx = LogCtx(self.name, account_file)
        if not os.path.exists(account_file):
            return LoginResponse(False, LoginReasonType.COOKIE_FILE_MISSING, path=account_file)

        async def _action(context):
            page = await context.new_page()
            await self.safe_goto(page, settings.BAIJIAHAO_HOME_URL, options)
            await page.wait_for_timeout(options.auth_wait_ms)

            need_login = await page.get_by_text("注册/登录百家号").count()
            if need_login:
                return LoginResponse(False, LoginReasonType.COOKIE_INVALID, path=account_file)
            return LoginResponse(True, LoginReasonType.COOKIE_VALID, path=account_file)

        try:
            return await self.run_with_retry(options, "bjh_auth", _action)
        except Exception as e:
            log_kv(self.logger, logging.ERROR, "auth failed", **ctx.as_dict(), err=str(e))
            return LoginResponse(False, LoginReasonType.PLAYWRIGHT_ERROR, path=account_file,
                                 extra={"err": str(e)})
