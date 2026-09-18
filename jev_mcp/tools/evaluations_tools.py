"""Evaluations group: evaluate_state"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.evaluations import EvaluateStateData, EvaluateStateResult
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("jev-mcp.tools.evaluations")


def register_evaluations_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="evaluate_state",
        description=(
            "Evaluates the given state against a map of typed questions and returns one "
            "structured answer per question, keyed by the same ids used in the request. "
            "Every question is evaluated independently and in parallel against the same "
            "state, and noul (yes/no), choice (single-select), and score (rubric) questions "
            "can be freely mixed within a single call."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def evaluate_state(
        state: str | dict | list = Field(
            description=(
                "The content to evaluate: a plain string for text, or structured data "
                "(object/array) for chat logs, records, or app state."
            )
        ),
        model: str = Field(
            description=(
                "The model that handles the request, e.g. 'jev-latest' (alias) or a pinned "
                "version like 'jev-1.13.0'. See the models group."
            )
        ),
        questions: dict[str, dict] = Field(
            description=(
                "A map of typed Question objects, keyed by a caller-chosen id — answers come "
                "back under the same keys, and the key itself is never sent to the model. Each "
                "Question is a discriminated union on its required 'type' field, one of "
                "'noul', 'choice', or 'score'; all three also accept 'instructions' (required, "
                "string | object | array | null — arbitrary JSON is accepted for clarity or to "
                "pass supporting data verbatim). Noul ('type': 'noul') is a yes/no question with "
                "an optional 'criteria' object holding optional 'true'/'false' descriptions "
                "(string, object, or array) of what a yes/no answer means. Choice "
                "('type': 'choice') picks one option from a set and requires 'criteria': a map "
                "of option name to an optional rubric description (string, object, array, or "
                "null when the option needs no extra detail) — one entry per option. Score "
                "('type': 'score') rates the state on a rubric and requires 'criteria': an "
                "ordered array of at least two level descriptions (each a string, or an object/"
                "array for structured rubric detail). Any mix of the three types is allowed in "
                "the same map."
            )
        ),
    ) -> EvaluateStateResult:
        tlog = ToolLogger(logger, "evaluate_state")

        if not questions:
            return _err(EvaluateStateResult, tlog, "VALIDATION_ERROR",
                        "questions must contain at least one entry", 400)

        try:
            data, status, retry_after = service.api_request(
                "POST", "/systemone",
                body={"state": state, "model": model, "questions": questions},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return EvaluateStateResult(success=True, statusCode=status, data=EvaluateStateData(**data))
            return _upstream_err(EvaluateStateResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(EvaluateStateResult, tlog, exc)
