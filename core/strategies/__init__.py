# -*- coding: utf-8 -*-
# @Time    : 2025/12/23 下午2:02
# @Author  : fzf
# @FileName: __init__.py
# @Software: PyCharm
from __future__ import annotations
from typing import Dict
from ..enums import LoginStrategyType
from .BaijiahaoLogin import BaijiahaoLogin
from .ToutiaoLogin import ToutiaoLogin
from .NeteaseLogin import NeteaseLogin
from .SohuLogin import SohuLogin
from .DayuLogin import DayuLogin
from .PenguinLogin import PenguinLogin
from .YidianLogin import YidianLogin
from .utils.base import LoginStrategy


class LoginStrategyFactory:
    registry: Dict[str, LoginStrategy] = {
        LoginStrategyType.BAIJIAHAO: BaijiahaoLogin(),
        LoginStrategyType.TOUTIAO: ToutiaoLogin(),
        LoginStrategyType.NETEASE: NeteaseLogin(),
        LoginStrategyType.SOHU: SohuLogin(),
        LoginStrategyType.DAYU: DayuLogin(),
        LoginStrategyType.PENGUIN: PenguinLogin(),
        LoginStrategyType.YIDIAN: YidianLogin(),
    }

    @classmethod
    def get(cls, platform: str) -> LoginStrategy:
        try:
            return cls.registry[platform]
        except KeyError:
            raise KeyError(f"Unknown platform={platform}. Registered={list(cls.registry.keys())}")