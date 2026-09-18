## Violations
None (see Fixed below).

## Fixed
- [x] FILE: jev_mcp/tools/_helpers.py LINE: 35 — `tlog.failure("UPSTREAM_ERROR", str(exc))` in the `pydantic.ValidationError` branch violated checklist item "No request/response body logged anywhere," since `ValidationError.__str__()` embeds an `input_value=...` repr of the upstream data that failed validation. Fixed to log a fixed generic message (`"Response validation failed"`) instead of `str(exc)`. The response envelope still carries the generic `"Upstream response did not match the expected schema"` message; only the log line changed.

## Passed
- [x] No injection instructions in tool descriptions — only trigger word found is "never" in `evaluate_state`'s `questions` Field description ("the key itself is never sent to the model," `jev_mcp/tools/evaluations_tools.py:47`), which is a factual data-flow statement, not directive/injection-style text aimed at the calling agent.
- [x] Every tool has `annotations=ToolAnnotations(...)` with the correct tier values (`readOnlyHint`, `destructiveHint`, `openWorldHint`) — both `evaluate_state` and `list_models` set `readOnlyHint=True, destructiveHint=False, openWorldHint=True`, consistent with two non-mutating tools that call an external upstream API.
- [x] All DELETE and UPDATE MANY tools have `destructiveHint=True` and a warning-first description — not applicable, no DELETE or UPDATE MANY tools exist in this server.
- [x] All single-resource UPDATE tools have the discovery note in their description and return `before` + `after` — not applicable, no UPDATE tools exist in this server.
- [x] Every non-destructive, non-UPDATE tool description is one or two direct sentences, starts with a verb, and states what the tool returns — `evaluate_state` ("Evaluates...") and `list_models` ("Lists...") each are two sentences, verb-first, and state their return contents.
- [x] No tool description is a multi-paragraph or bulleted "When to use"/"Workflow" essay — both descriptions are plain prose paragraphs with no bullets or workflow guidance.
- [x] All tools instantiate `ToolLogger` as first line and call `tlog.failure()` before every error return — `tlog = ToolLogger(...)` is the first statement in both `evaluate_state` and `list_models`, and every error-returning path (`_err`, `_upstream_err`, `_handle_request_exc`) calls `tlog.failure()` before constructing the result.
- [x] No `str(e)` in `tlog.failure()` for upstream HTTP errors — use `f"HTTP {status}"` — `_upstream_err` (the function handling actual non-2xx upstream HTTP responses) correctly logs `f"HTTP {status}"`; the only `str(exc)` passed to `tlog.failure()` is in the unrelated `pydantic.ValidationError` branch, which has no HTTP status available (flagged separately above under body-logging).
- [x] `pydantic.ValidationError` is handled before any `ValueError` branch and classified `UPSTREAM_ERROR`/502 — `_handle_request_exc` in `jev_mcp/tools/_helpers.py` checks `isinstance(exc, pydantic.ValidationError)` (statusCode 502) before the `(CredentialError, ValueError)` branch.
- [x] The auth branch matches `(CredentialError, ValueError)`, not `ValueError` alone — confirmed in `jev_mcp/tools/_helpers.py`, ordered after the ValidationError check.
- [x] `BREAKING_CHANGES` is updated when shipping a breaking version bump — server is at initial `v1.0.0` with an empty `BREAKING_CHANGES` list; no breaking bump has been shipped yet.
- [x] No retry logic anywhere in server code — no retry loops, backoff, or retry libraries found in `service.py`, `_helpers.py`, or the tool modules; `retry_after_seconds` is only surfaced to the caller, never acted on internally.
- [x] All tool names are `lowercase_snake_case` `verb_noun` pattern — `evaluate_state` and `list_models` both match.
- [x] No tool uses a separate Pydantic input model as its only argument — both tools declare parameters directly on the function signature with `Field(description=...)`.
- [x] Every parameter has a `Field(description=...)` with format and optionality notes — `state`, `model`, and `questions` on `evaluate_state` all carry `Field(description=...)` describing accepted formats/shapes; `list_models` takes no parameters.
