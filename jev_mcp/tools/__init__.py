"""MewCP Jev tool registration."""

from fastmcp import FastMCP

from .evaluations_tools import register_evaluations_tools
from .models_tools import register_models_tools


def register_tools(mcp: FastMCP) -> None:
    register_evaluations_tools(mcp)
    register_models_tools(mcp)
