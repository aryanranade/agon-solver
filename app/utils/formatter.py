def format_output(answer: str) -> str:
    """Formatter to ensure concise and deterministic outputs."""
    if not answer:
        return ""
    # Strip any extra conversational fluff or whitespace
    return answer.strip()
