<div align="center">

# 🚀 Auto Back Login

**一个强大、优雅的自动化登录服务框架，支持多平台登录策略**

**简体中文** | [English](README.en.md)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)](https://playwright.dev/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[📖 快速开始](#-快速开始) • [🏗️ 核心功能](#-核心功能) • [📚 API参考](#-api参考) • [🔧 配置选项](#-配置选项) • [🤝 贡献](#-贡献)

</div>

## 🌟 项目简介

Auto Back Login 是一个专为自动化登录场景设计的服务框架，采用策略模式实现多平台登录支持，使用 Playwright 进行浏览器自动化操作，提供简洁优雅的 API 接口。

<div align="center">
  <img src="https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1332&q=80" alt="自动化服务架构" width="600" style="border-radius: 8px; margin-bottom: 20px;">
</div>

<div align="center">

| 🎯 **策略模式** | ⚡ **自动登录** | 🛡️ **类型安全** | 📦 **多平台支持** |
|:---:|:---:|:---:|:---:|
| 灵活扩展不同平台登录策略 | 自动化处理登录流程 | 基于Python类型注解 | 轻松添加新平台支持 |

</div>

## ✨ 核心功能

### 🔧 多平台登录支持
- **策略模式** - 灵活扩展不同平台的登录策略
- **百家号(Baijiahao)** - 已实现的登录策略
- **易于扩展** - 可快速添加新平台支持

### 🚀 自动化登录流程
- **自动检测登录状态** - 智能判断是否需要登录
- **浏览器自动化** - 使用Playwright处理复杂登录流程
- **Cookie管理** - 自动保存和验证登录状态

### 📦 优雅的API设计

<div align="center">
  <img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1740&q=80" alt="API设计" width="500" style="border-radius: 8px; margin-bottom: 20px;">
</div>

- **LoginService** - 统一的服务入口
- **异步支持** - 基于async/await的异步API
- **类型安全** - 完整的Python类型注解

### 🌐 配置选项
- **无头模式** - 支持无头浏览器运行
- **超时控制** - 灵活的超时配置
- **重试机制** - 自动重试失败的操作
- **排障功能** - 支持截图和Trace输出

## 🛠️ 技术栈

| 组件 | 技术选型 | 版本要求 |
|------|----------|----------|
| **编程语言** | Python | 3.11+ |
| **浏览器自动化** | Playwright | 1.40+ |
| **设计模式** | 策略模式 | - |
| **类型注解** | Python Typing | - |
| **异步支持** | asyncio | - |

## 📁 项目结构

```
auto-back-login/
├── __init__.py                 # 包初始化
├── main.py                     # 示例入口
├── core/                       # 核心模块
│   ├── __init__.py            # 核心模块初始化
│   ├── config.py              # 配置文件
│   ├── enums.py               # 枚举定义
│   ├── schemas.py             # 类型定义
│   ├── service.py             # 登录服务
│   ├── strategies/            # 登录策略
│   │   ├── __init__.py        # 策略模块初始化
│   │   ├── BaijiahaoLogin.py  # 百家号登录策略
│   │   └── utils/             # 策略工具
│   │       ├── base.py        # 基础策略类
│   │       └── playwright_base.py  # Playwright基础策略
│   └── utils/                 # 通用工具
│       └── logger.py          # 日志系统
├── data/                      # 数据目录
│   └── fzf/                   # 用户数据示例
├── artifacts/                 # 排障文件目录
└── README.md                  # 项目文档
```

## 🚀 快速开始

### ⚡ 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd auto-back-login

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install
```

### 💻 基础使用

#### 1. 配置文件

配置现已集成到`core/config.py`中，可根据需要进行修改。

#### 2. 登录示例

```python
# main.py
import asyncio
from core.service import LoginService
from core.schemas import LoginOptions

async def main():
    # 配置登录选项
    opts = LoginOptions(headless=False, timeout_ms=180_000)
    
    # 登录百家号并保存cookie
    res = await LoginService.setup(
        "baijiahao",
        account_file="/tmp/bjh.json",
        handle=True,  # 是否自动处理登录
        options=opts,
    )
    print(res.data)

asyncio.run(main())
```

#### 3. 验证登录状态

```python
async def verify_login():
    opts = LoginOptions(headless=True)
    res = await LoginService.auth(
        "baijiahao",
        account_file="/tmp/bjh.json",
        options=opts,
    )
    print("登录状态:", "有效" if res.ok else "无效")
    print(res.data)
```

#### 4. 仅登录并保存

```python
async def login_and_save():
    opts = LoginOptions(headless=False)
    res = await LoginService.login_and_save(
        "baijiahao",
        account_file="/tmp/bjh.json",
        options=opts,
    )
    print("登录结果:", "成功" if res.ok else "失败")
    print(res.data)
```

## 📚 API参考

### LoginService

#### setup
```python
@staticmethod
async def setup(platform: str, account_file: str, *, handle: bool = False, options: LoginOptions | None = None) -> LoginResponse:
    """
    设置并登录指定平台
    
    Args:
        platform: 平台名称（如 "baijiahao"）
        account_file: Cookie保存路径
        handle: 是否自动处理登录
        options: 登录选项（可选，默认使用LoginOptions.default）
        
    Returns:
        LoginResponse: 登录结果响应
    """
```

#### auth
```python
@staticmethod
async def auth(platform: str, account_file: str, *, options: LoginOptions | None = None) -> LoginResponse:
    """
    验证登录状态
    
    Args:
        platform: 平台名称
        account_file: Cookie文件路径
        options: 登录选项（可选，默认使用LoginOptions.default）
        
    Returns:
        LoginResponse: 验证结果响应
    """
```

#### login_and_save
```python
@staticmethod
async def login_and_save(platform: str, account_file: str, *, options: LoginOptions | None = None) -> LoginResponse:
    """
    登录并保存Cookie
    
    Args:
        platform: 平台名称
        account_file: Cookie保存路径
        options: 登录选项（可选，默认使用LoginOptions.default）
        
    Returns:
        LoginResponse: 登录结果响应
    """
```

### LoginOptions

| 属性 | 类型 | 描述 | 默认值 |
|------|------|------|--------|
| `headless` | bool | 是否使用无头浏览器 | False |
| `timeout_ms` | int | 登录总超时时间（毫秒） | 300000 |
| `nav_timeout_ms` | int | 单次导航超时（毫秒） | 30000 |
| `auth_wait_ms` | int | 验证等待时间（毫秒） | 150000 |
| `browser_args` | list[str] | 浏览器启动参数 | ["--lang=en-GB"] |
| `executable_path` | str | 自定义浏览器路径 | None |
| `channel` | str | 浏览器渠道 | None |
| `artifacts_dir` | str | 排障文件输出目录 | "./artifacts" |
| `enable_trace` | bool | 是否启用Trace | False |
| `enable_screenshot_on_error` | bool | 错误时是否截图 | True |
| `retries` | int | 重试次数 | 2 |
| `retry_backoff_ms` | int | 重试间隔（毫秒） | 800 |
| `default` | property | 返回默认配置 | - |
| `data` | property | 返回字典形式的数据 | - |

### LoginResponse

| 属性 | 类型 | 描述 |
|------|------|------|
| `ok` | bool | 操作是否成功 |
| `reason` | str | 操作结果原因 |
| `path` | str | Cookie文件路径 |
| `extra` | dict | 额外信息 |
| `data` | dict | 响应数据字典 |

## 🔧 高级配置

### 自定义LoginOptions

```python
from core.schemas import LoginOptions

# 创建自定义登录选项
opts = LoginOptions(
    headless=True,              # 使用无头浏览器
    timeout_ms=300_000,         # 延长超时时间到5分钟
    auth_wait_ms=10_000,        # 增加验证等待时间
    enable_screenshot_on_error=True,  # 错误时截图
    artifacts_dir="./logs",    # 自定义排障文件目录
)
```

### 扩展新平台

```python
# 1. 创建新的登录策略类
from playwright.async_api import Page
from core.strategies.utils.base import LoginStrategy
from core.strategies.utils.playwright_base import BasePlaywrightStrategy
from core.schemas import LoginOptions, LoginResponse
from core.enums import LoginReasonType
from core.service import LoginService

class NewPlatformLogin(LoginStrategy, BasePlaywrightStrategy):
    name = "new_platform"
    
    async def handler_auth_cookie(self, page: Page, account_file: str, options: LoginOptions) -> LoginResponse:
        # 实现登录逻辑
        pass
    
    async def handler_login_and_save(self, page: Page, account_file: str, options: LoginOptions) -> LoginResponse:
        # 实现验证逻辑
        pass

# 2. 注册到策略工厂
from core.strategies import LoginStrategyFactory
LoginStrategyFactory.registry["new_platform"] = NewPlatformLogin()

# 3. 使用新平台
res = await LoginService.setup("new_platform", "/tmp/new_platform.json")
```

## 🤝 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目！

### 贡献流程

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详情请查看 [LICENSE](LICENSE) 文件

## 💖 致谢

- 感谢 [Playwright](https://playwright.dev/) 提供优秀的浏览器自动化工具
- 感谢所有使用和支持这个项目的开发者！

> 🚀 **开始使用**：按照快速开始指南，5分钟内即可体验自动化登录功能！