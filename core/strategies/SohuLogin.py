# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:02
# @Author  : fzf
# @FileName: sohu.py
# @Software: PyCharm
from __future__ import annotations
import os
from playwright.async_api import Page

from .utils.base import LoginStrategy
from ..schemas import LoginOptions, LoginResponse
from ..enums import LoginReasonType, LoginStrategyType
from ..utils.logger import get_logger, LogCtx
from ..config import settings

logger = get_logger(LoginStrategyType.SOHU)


class SohuLogin(LoginStrategy):
    name = LoginStrategyType.SOHU

    async def handler_auth_cookie(self, page: Page, account_file: str, options: LoginOptions) -> LoginResponse:
        # 使用统一的优化认证检查方法，提高所有策略的性能一致性
        return await self._optimized_auth_check(page, account_file, options,
                                                url=settings.SOHU_HOME_URL,
                                                need_login_text=settings.SOHU_NEED_LOGIN_TEXT)

    async def handler_login_and_save(self, page: Page, account_file: str, options: LoginOptions) -> LoginResponse:
        os.makedirs(os.path.dirname(account_file) or ".", exist_ok=True)
        # 打开登录页
        await self.safe_goto(page, settings.SOHU_LOGIN_URL, options)
        try:
            # ✅ 等到登录成功自动跳到 home（最多等 timeout_ms）
            await page.wait_for_url(settings.SOHU_HOME_URL, timeout=options.timeout_ms)
            # 保存 cookie
            # await page.context.storage_state(path=account_file)
            state = await page.context.storage_state()
            return LoginResponse(True, LoginReasonType.COOKIE_SAVED, path=account_file, data=state)

        except Exception as e:
            return LoginResponse(False, LoginReasonType.LOGIN_TIMEOUT, path=account_file, extra={"err": str(e)})
