"""Configuration for MewCP Jev MCP Server."""

import logging
import os

SERVER_VERSION = "v1.0.0"
BREAKING_CHANGES: list[dict] = []

JEV_API_BASE = "https://api.typesafe.ai/v1"

CONNECT_TIMEOUT = 5    # TCP connection — fixed across all servers
# The evaluate-state endpoint is a single-call LLM-backed request with no
# documented SLA beyond standard rate-limit guidance, so use a generous but
# bounded read timeout to accommodate slower model/question-set combinations
# without hanging indefinitely.
READ_TIMEOUT = 60
# No async job endpoints are documented for this API, so no POLL_TIMEOUT.


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
