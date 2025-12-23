# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:02
# @Author  : fzf
# @FileName: __init__.py
# @Software: PyCharm
from __future__ import annotations
from typing import Dict
from ..enums import LoginStrategyType
from .BaijiahaoLogin import BaijiahaoLogin
from ..base import LoginStrategy


class LoginStrategyFactory:
    registry: Dict[str, LoginStrategy] = {
        LoginStrategyType.BAIJIAHAO: BaijiahaoLogin(),
    }

    @classmethod
    def get(cls, platform: str) -> LoginStrategy:
        try:
            return cls.registry[platform]
        except KeyError:
            raise KeyError(f"Unknown platform={platform}. Registered={list(cls.registry.keys())}")
