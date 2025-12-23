# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:02
# @Author  : fzf
# @FileName: __init__.py
import asyncio
from core.service import LoginService
from core.types import LoginOptions


async def main():
    opts = LoginOptions(headless=False, timeout_ms=180_000)
    res = await LoginService.setup(
        "baijiahao",
        account_file="/tmp/bjh.json",
        handle=True,
        options=opts,
    )
    print(res.data)


asyncio.run(main())
