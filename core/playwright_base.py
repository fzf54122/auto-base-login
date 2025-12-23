# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:38
# @Author  : fzf
# @FileName: playwright_base.py
# @Software: PyCharm
from __future__ import annotations
import asyncio
import os
from typing import Any, Callable, Coroutine, TypeVar

from playwright.async_api import async_playwright, Browser, BrowserContext, Page, TimeoutError as PWTimeout
from core.types import LoginOptions

T = TypeVar("T")


class BasePlaywrightStrategy:
    """
    给策略继承：
    - 统一 launch / context / page
    - 统一 goto 超时
    - 统一重试
    - 统一错误截图/trace
    """

    async def set_init_script(self, context: BrowserContext) -> BrowserContext:
        # 子类按需覆盖：UA/注入脚本/viewport等
        return context

    def _ensure_artifacts_dir(self, options: LoginOptions) -> str:
        os.makedirs(options.artifacts_dir, exist_ok=True)
        return options.artifacts_dir

    async def _launch_browser(self, options: LoginOptions) -> Browser:
        async with async_playwright() as p:
            # 注意：这里不能直接 return browser，否则 playwright 上下文会退出。
            # 所以我们不在这里启动；改用下面的 _with_playwright() 包装。
            raise RuntimeError("Use _with_playwright wrapper")  # 防误用

    async def _with_playwright(self, fn: Callable[[Any], Coroutine[Any, Any, T]]) -> T:
        async with async_playwright() as p:
            return await fn(p)

    async def _new_context(self, p: Any, options: LoginOptions) -> BrowserContext:
        browser = await p.chromium.launch(
            headless=options.headless,
            args=options.browser_args,
            executable_path=options.executable_path,
            channel=options.channel,
        )
        context = await browser.new_context()
        context.set_default_navigation_timeout(options.nav_timeout_ms)
        context.set_default_timeout(options.nav_timeout_ms)
        context = await self.set_init_script(context)
        # 把 browser 绑到 context 方便统一关闭
        context._browser = browser  # type: ignore[attr-defined]
        return context

    async def _close_context(self, context: BrowserContext) -> None:
        browser = getattr(context, "_browser", None)
        try:
            await context.close()
        finally:
            if browser:
                await browser.close()

    async def safe_goto(self, page: Page, url: str, options: LoginOptions, wait_until: str = "domcontentloaded") -> None:
        try:
            await page.goto(url, wait_until=wait_until, timeout=options.nav_timeout_ms)
        except PWTimeout as e:
            raise PWTimeout(f"goto timeout url={url}") from e

    async def _capture_on_error(self, page: Page | None, options: LoginOptions, name: str) -> None:
        if not options.enable_screenshot_on_error or page is None:
            return
        out_dir = self._ensure_artifacts_dir(options)
        path = os.path.join(out_dir, f"{name}.png")
        try:
            await page.screenshot(path=path, full_page=True)
        except Exception:
            pass

    async def _trace_start(self, context: BrowserContext, options: LoginOptions) -> None:
        if not options.enable_trace:
            return
        # trace 需要明确启动
        await context.tracing.start(screenshots=True, snapshots=True, sources=False)

    async def _trace_stop(self, context: BrowserContext, options: LoginOptions, name: str) -> None:
        if not options.enable_trace:
            return
        out_dir = self._ensure_artifacts_dir(options)
        path = os.path.join(out_dir, f"{name}.zip")
        try:
            await context.tracing.stop(path=path)
        except Exception:
            pass

    async def run_with_retry(
        self,
        options: LoginOptions,
        action_name: str,
        action: Callable[[BrowserContext], Coroutine[Any, Any, T]],
    ) -> T:
        last_exc: Exception | None = None

        for attempt in range(options.retries + 1):
            trace_name = f"{action_name}_attempt{attempt}"
            page_for_shot: Page | None = None

            try:
                async def _runner(p: Any) -> T:
                    context = await self._new_context(p, options)
                    await self._trace_start(context, options)
                    try:
                        # 给子 action 机会返回/管理 page
                        result = await action(context)
                        return result
                    finally:
                        await self._trace_stop(context, options, trace_name)
                        await self._close_context(context)

                return await self._with_playwright(_runner)

            except Exception as e:
                last_exc = e
                # 这里拿不到 page（由 action 内部创建），所以推荐 action 内部把 page 传给 capture
                # 或者你把 action 封装为创建 page 后返回 page，让 base 统一截图
                await asyncio.sleep(options.retry_backoff_ms / 1000.0)

        assert last_exc is not None
        raise last_exc
