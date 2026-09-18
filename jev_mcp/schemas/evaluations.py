from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class EvaluateStateUsage(BaseModel):
    model_config = ConfigDict(extra="allow")

    input_tokens: int
    output_tokens: int


class EvaluateStateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str
    # Each answer's shape varies by its own `type` (noul/choice/score), so it
    # is kept as a raw dict rather than forced into one fixed Answer schema.
    answers: dict[str, dict]
    usage: EvaluateStateUsage


class EvaluateStateResult(ToolResult):
    data: EvaluateStateData | None = None
