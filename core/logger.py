# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:37
# @Author  : fzf
# @FileName: logger.py
# @Software: PyCharm
from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Any, Dict
from rich.logging import RichHandler

from config import settings

default_level = settings.LOGGER_LEVEL


def get_logger(name, level=default_level):
    return _get_rich_logger(name, level)


def _get_standard_logger(name, level=default_level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s][line %(lineno)s][%(funcName)5s()]: %(message)s"
    formatter = logging.Formatter(FORMAT)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def _get_rich_logger(name, level=default_level):
    logger = logging.getLogger('login.' + name)
    logger.setLevel(level)
    FORMAT = "[%(filename)s][line %(lineno)s][%(funcName)5s()]: %(message)s"
    formatter = logging.Formatter(FORMAT)
    console_handler = RichHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


@dataclass(slots=True)
class LogCtx:
    platform: str
    account_file: str

    def as_dict(self) -> Dict[str, Any]:
        return {"platform": self.platform, "account_file": self.account_file}


def log_kv(logger: logging.Logger, level: int, msg: str, **kv: Any) -> None:
    # 简单结构化：message + key=value
    suffix = " ".join([f"{k}={repr(v)}" for k, v in kv.items()])
    logger.log(level, f"{msg} {suffix}".rstrip())


if __name__ == "__main__":
    logger = get_logger()
    ctx = LogCtx(platform="baijiahao", account_file="/tmp/bjh.json")
    log_kv(logger, logging.INFO, "cookie auth start", **ctx.as_dict())
