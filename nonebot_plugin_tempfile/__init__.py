from functools import wraps
from io import BytesIO, StringIO
import os
from pathlib import Path
from tempfile import TemporaryDirectory as _TemporaryDirectory, mkstemp
from typing import Callable, Generator, Optional, TypeVar
from typing_extensions import Annotated, ParamSpec

from nonebot import get_driver, logger
from nonebot.params import Depends
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    "方寸狭间",
    "临时文件/IO 依赖注入支持",
    "[详见插件主页]",
    "library",
    "https://github.com/NCBM/nonebot-plugin-tempfile",
    Config
)

_config = Config.parse_obj(get_driver().config)

_T = TypeVar("_T")
_P = ParamSpec("_P")


def TempDir(
    suffix: str = "",
    prefix: Optional[str] = None,
    dir: Optional[Path] = None,
    *,
    cache: bool = True
) -> Path:
    """
    临时目录的依赖构造函数。

    参数：
    - suffix: 临时文件夹后缀名；
    - prefix: 临时文件夹前缀名；
    - dir: 创建位置；
    - cache: 是否启用依赖注入缓存。

    返回值：用于依赖注入的对象。

    注入值：临时目录路径。
    """
    _prefix = _config.tempfile_default_prefix if prefix is None else prefix
    def _temp_dir(_dir: Optional[Path] = dir) -> Generator[Path, None, None]:
        with _TemporaryDirectory(suffix, _prefix, _dir) as tmpdir:
            logger.debug(f"Successfully created temp directory {tmpdir!r}")
            yield Path(tmpdir)
        logger.debug(f"Successfully removed temp directory {tmpdir!r}")

    return Depends(_temp_dir, use_cache=cache)


def TempFile(
    suffix: str = "",
    prefix: Optional[str] = None,
    dir: Optional[Path] = None,
    *,
    cache: bool = True
) -> Path:
    """
    临时文件的依赖构造函数。

    参数：
    - suffix: 临时文件后缀名；
    - prefix: 临时文件前缀名；
    - dir: 创建位置；
    - cache: 是否启用依赖注入缓存。

    返回值：用于依赖注入的对象。

    注入值：临时文件路径。
    """
    _prefix = _config.tempfile_default_prefix if prefix is None else prefix
    def _temp_file(_dir: Optional[Path] = dir) -> Generator[Path, None, None]:
        fd, fp = mkstemp(suffix, _prefix, _dir)
        logger.debug(f"Successfully created temp file {fp!r}")
        try:
            path = Path(fp)
            os.close(fd)
            yield path
        finally:
            os.remove(fp)
            logger.debug(f"Successfully removed temp file {fp!r}")

    return Depends(_temp_file, use_cache=cache)


def nestwrap(t: Callable[_P, _T], *, cache: bool = True) -> Callable[_P, _T]:
    """用于依赖注入的简单依赖构造器。"""
    @wraps(t)
    def _nestwrap(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        def _nest_inject() -> _T:
            return t(*args, **kwargs)
        
        return Depends(_nest_inject, use_cache=cache)
    
    return _nestwrap


SimpleTempDir = Annotated[Path, TempDir()]
"""
临时目录的快捷依赖。

此快捷依赖可在整个会话中保持值不变，但同时也无法在一次会话中使用多个此依赖。
如有此需求请自行构造 `TempDir` 依赖。
"""
SimpleTempFile = Annotated[Path, TempFile()]
"""
临时文件的快捷依赖。

此快捷依赖可在整个会话中保持值不变，但同时也无法在一次会话中使用多个此依赖。
如有此需求请自行构造 `TempFile` 依赖。
"""

TempStringIO = nestwrap(StringIO)
"""
临时 `StringIO` 的依赖构造函数，参数与 `io.StringIO` 初始化参数一致。

返回值：用于依赖注入的对象（不可用于其它位置）。

注入值：临时 `StringIO`。
"""
TempBytesIO = nestwrap(BytesIO)
"""
临时 `BytesIO` 的依赖构造函数，参数与 `io.BytesIO` 初始化参数一致。

返回值：用于依赖注入的对象（不可用于其它位置）。

注入值：临时 `BytesIO`。
"""