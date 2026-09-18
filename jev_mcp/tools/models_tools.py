"""Models group: list_models"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.models import ModelInfo, ModelListData, ModelListResult  # noqa: F401
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("jev-mcp.tools.models")


def register_models_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_models",
        description=(
            "Lists the model names and aliases this account can pass in the evaluate-state "
            "`model` field, with a description and release date for each. This list currently "
            "only surfaces aliases such as `jev-latest` and `jev-preview` — a versioned model "
            "ID (e.g. `jev-1.13.0`) is still accepted by the evaluate-state `model` field even "
            "when it does not appear here."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_models() -> ModelListResult:
        tlog = ToolLogger(logger, "list_models")

        try:
            data, status, retry_after = service.api_request(
                "GET", "/models",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return ModelListResult(success=True, statusCode=status, data=ModelListData(**data))
            return _upstream_err(ModelListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ModelListResult, tlog, exc)
