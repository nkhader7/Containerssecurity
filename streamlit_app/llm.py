"""Helper utilities for generating remediation suggestions using an LLM provider."""

from __future__ import annotations

import os
from typing import Any, Dict

import openai

_SYSTEM_PROMPT = (
    "You are an infrastructure-as-code security assistant. Given a failing Checkov check, "
    "explain the issue and propose a safe remediation patch. Provide the answer in markdown with a short summary, "
    "a bullet list of risks, and a code block showing the suggested fix."
)


def _client_from_env() -> openai.OpenAI | None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    client = openai.OpenAI(api_key=api_key)
    return client


def generate_fix_suggestion(check: Dict[str, Any]) -> str:
    """Generate a fix suggestion for a Checkov failing check.

    If an OpenAI API key is not provided, a deterministic fallback message is returned so that
    the interface remains usable in offline environments.
    """

    client = _client_from_env()
    description = check.get("description", "No description provided")
    check_id = check.get("check_id", "unknown")
    resource = check.get("resource", "resource")
    file_path = check.get("file_path", "file")
    code_block = check.get("code_block") or "Code block unavailable"

    user_prompt = (
        f"Check ID: {check_id}\n"
        f"Resource: {resource}\n"
        f"File: {file_path}\n"
        f"Description: {description}\n"
        "Problematic code snippet:\n"
        f"{code_block}\n"
        "Please propose an actionable remediation."
    )

    if client is None:
        return (
            "OpenAI credentials are not configured.\n\n"
            "Review the failing check and update the infrastructure code based on the guideline provided."
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or "The model did not return any content."
