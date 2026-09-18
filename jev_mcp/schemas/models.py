from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class ModelInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    description: str
    release_date: str


class ModelListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    models: list[ModelInfo]


class ModelListResult(ToolResult):
    data: ModelListData | None = None
