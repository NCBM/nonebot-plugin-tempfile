from pydantic import BaseModel


class Config(BaseModel, extra="ignore"):
    tempfile_default_prefix: str = "tmpnonebot"
    """临时文件默认前缀"""