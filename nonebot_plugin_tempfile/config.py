from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    tempfile_default_prefix: str = "tmpnonebot"
    """临时文件默认前缀"""