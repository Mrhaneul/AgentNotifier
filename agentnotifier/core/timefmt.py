"""Time formatting utilities."""

from __future__ import annotations


def format_duration(seconds: float) -> str:
    """Convert raw seconds into a short human-readable duration."""

    seconds = max(0.0, seconds)
    if seconds < 1:
        return f"{seconds:.2f}s"

    total_seconds = int(round(seconds))
    hours, rem = divmod(total_seconds, 3600)
    minutes, secs = divmod(rem, 60)

    parts: list[str] = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if secs or not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)
