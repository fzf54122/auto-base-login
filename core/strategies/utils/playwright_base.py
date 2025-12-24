# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:38
# @Author  : fzf
# @FileName: playwright_base.py
# @Software: PyCharm
from __future__ import annotations
import asyncio
import os
from abc import ABC, abstractmethod
from typing import Optional

from playwright.async_api import async_playwright, Browser, BrowserContext, Page, TimeoutError as PWTimeout

from ...enums import LoginStrategyType, LoginReasonType
from ...schemas import LoginOptions, LoginResponse


class BasePlaywrightStrategy:
    """
    给策略继承：
    - 统一 launch / context / page
    - 统一 goto 超时
    - 统一重试
    - 统一错误截图/trace
    """

    name: str  # platform key，如 "baijiahao"

    @abstractmethod
    async def handler_login_and_save(self, page: Page, account_file: str, options: LoginOptions) -> LoginResponse:
        """登录并保存cookie。"""
        ...

    @abstractmethod
    async def handler_auth_cookie(self, page: Page, account_file: str, options: LoginOptions) -> LoginResponse:
        """校验cookie是否有效。"""
        ...

    async def run(self, page: Page, account_file: str, options: LoginOptions,
                  mode: str | LoginStrategyType) -> LoginResponse:
        if mode == LoginStrategyType.AUTH:
            return await self.handler_auth_cookie(page, account_file, options)
        elif mode == LoginStrategyType.LOGIN:
            return await self.handler_login_and_save(page, account_file, options)
        else:
            return LoginResponse(False, LoginReasonType.UNKNOWN_ERROR, path=account_file)

    @staticmethod
    async def set_init_script(context: BrowserContext) -> BrowserContext:
        return context

    @staticmethod
    def _ensure_dir(path: str) -> None:
        os.makedirs(path, exist_ok=True)

    @staticmethod
    async def safe_goto(page: Page, url: str, options: LoginOptions,
                        wait_until: str = "domcontentloaded") -> None:
        await page.goto(url, wait_until=wait_until, timeout=options.nav_timeout_ms)

    async def _screenshot(self, page: Optional[Page], options: LoginOptions, name: str) -> None:
        if not options.enable_screenshot_on_error or page is None:
            return
        self._ensure_dir(options.artifacts_dir)
        out = os.path.join(options.artifacts_dir, f"{name}.png")
        try:
            await page.screenshot(path=out, full_page=True)
        except Exception:
            pass

    async def _trace_start(self, context: BrowserContext, options: LoginOptions) -> None:
        if options.enable_trace:
            self._ensure_dir(options.artifacts_dir)
            await context.tracing.start(screenshots=True, snapshots=True, sources=False)

    async def _trace_stop(self, context: BrowserContext, options: LoginOptions, name: str) -> None:
        if options.enable_trace:
            self._ensure_dir(options.artifacts_dir)
            out = os.path.join(options.artifacts_dir, f"{name}.zip")
            try:
                await context.tracing.stop(path=out)
            except Exception:
                pass

    @staticmethod
    def is_user_abort_error(e: Exception) -> bool:
        # Ctrl+C / task cancel
        if isinstance(e, asyncio.CancelledError):
            return True

        msg = str(e).lower()
        # Playwright 常见关闭异常文本（不同版本略有差异）
        keywords = [
            "target closed",
            "browser has been closed",
            "browser closed",
            "page closed",
            "context closed",
            "closed",
            "connection closed",
            "websocket connection closed",
        ]
        return any(k in msg for k in keywords)

    async def execute(self, account_file: str, options: LoginOptions, mode: LoginStrategyType | str) -> LoginResponse:
        last_exc: Exception | None = None
        headless = True if mode == LoginStrategyType.AUTH else False

        async with async_playwright() as p:
            for attempt in range(options.retries):
                browser: Browser | None = None
                context: BrowserContext | None = None
                page: Page | None = None
                trace_name = f"{self.name}_{mode}_attempt{attempt}"

                try:
                    browser = await p.chromium.launch(
                        headless=headless,
                        args=options.browser_args,
                        executable_path=options.executable_path,
                        channel=options.channel,
                    )
                    if mode == LoginStrategyType.AUTH:
                        context = await browser.new_context(storage_state=account_file)
                    elif mode == LoginStrategyType.LOGIN:
                        context = await browser.new_context()

                    context.set_default_navigation_timeout(options.nav_timeout_ms)
                    context.set_default_timeout(options.nav_timeout_ms)
                    context = await self.set_init_script(context)

                    await self._trace_start(context, options)

                    page = await context.new_page()
                    return await self.run(page, account_file, options, mode)

                except PWTimeout as e:
                    last_exc = e
                    await self._screenshot(page, options, f"{trace_name}_timeout")
                    await asyncio.sleep(options.retry_backoff_ms / 1000.0)

                except Exception as e:
                    # ✅ 用户主动关闭窗口/中止：不重试，直接退出
                    if self.is_user_abort_error(e):
                        return LoginResponse(
                            False,
                            "user_aborted",
                            path=account_file,
                            extra={"err": str(e), "mode": mode, "attempt": attempt},
                        )
                    last_exc = e
                    await self._screenshot(page, options, f"{trace_name}_error")
                    await asyncio.sleep(options.retry_backoff_ms / 1000.0)

                finally:
                    if context is not None:
                        await self._trace_stop(context, options, trace_name)
                        try:
                            await context.close()
                        except Exception:
                            pass
                    if browser is not None:
                        try:
                            await browser.close()
                        except Exception:
                            pass

        # 重试耗尽，返回失败（或抛异常都行，你选）
        return LoginResponse(False, "retry_exhausted",
                             path=account_file,
                             extra={"err": str(last_exc) if last_exc else None})
