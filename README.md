<div align="center">

# nonebot-plugin-tempfile

_✨ 适用于 NoneBot2 插件的临时文件/IO 依赖注入支持 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/NCBM/nonebot-plugin-tempfile.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-tempfile">
  <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/nonebot-plugin-tempfile">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-tempfile">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-tempfile.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 介绍

`nonebot-plugin-tempfile` 是帮助**开发者**利用依赖注入特性辅助管理临时文件/IO 的库插件，支持结束会话时自动清理临时文件（夹）。

## 安装

通过 `nb-cli`:

```console
nb plugin install nonebot-plugin-tempfile
```

## 使用

### 加载模块

```python
from nonebot import require

require("nonebot_plugin_tempfile")
```

### 简单管理临时文件（夹）

```python
from nonebot_plugin_tempfile import SimpleTempFile, SimpleTempDir

@some_matcher.handle()
async def some_handler(tmpfile: SimpleTempFile):
    # tmp is a `pathlib.Path` in function
    ...

@some_matcher.handle()
async def some_handler(tmpdir: SimpleTempDir):
    # tmp is a `pathlib.Path` in function
    ...
```

> 注意：`Simple` 开头的依赖类型无法同时使用多个，注入值在同一上下文内相同。
>
> 如有管理多个临时文件的需求，请另行声明自有依赖。

### 自定义临时文件（夹）

```python
from nonebot_plugin_tempfile import TempFile, TempDir

@some_matcher.handle()
async def some_handler(tmp1: Path = TempFile(".png"), tmp2: Path = TempFile(".txt", "tmp-someplugin-")):
    ...

tmpdir = TempDir(prefix="tmp-kazoo-")
tmpdir2 = TempDir(dir=tmpdir)
# 支持目录嵌套

@some_matcher.handle()
async def some_handler(
    tmp1: Path = TempFile(".png", dir=tmpdir),
    tmp2: Path = TempFile(".txt", "tmp-someplugin-", dir=tmpdir2)
):
    ...
```

### 注入虚拟 IO

```python
from io import StringIO, BytesIO
from nonebot_plugin_tempfile import TempStringIO, TempBytesIO

@some_matcher.handle()
async def some_handler(tmp1: StringIO = TempStringIO(), tmp2: BytesIO = TempBytesIO()):
    ...

@some_matcher.handle()
async def some_handler(tmp1: BytesIO = TempBytesIO(), tmp2: BytesIO = TempBytesIO()):
    ...
```

## 配置

本插件增加了下列可选配置项，有需要的用户请自行在 `.env` 或选用的以 `.env` 开头的文件中配置：

```python
# 下列配置项请按需解除注释并配置

# 临时文件默认前缀（字符串）
# tempfile_default_prefix=tmpnonebot
```
