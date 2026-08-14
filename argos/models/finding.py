"""Shared security and diagnostic finding models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Severity(StrEnum):
    """Severity assigned to an ArgOS finding."""

    SUCCESS = "success"
    INFORMATION = "information"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class Finding:
    """A normalized observation produced by an ArgOS module."""

    severity: Severity
    title: str
    description: str
    evidence: dict[str, Any] = field(default_factory=dict)
    source: str | None = None
    recommendation: str | None = None

    def __post_init__(self) -> None:
        """Validate required finding fields"""
        if not self.title.strip():
            raise ValueError("Finding title cannot be empty.")

        if not self.description.strip():
            raise ValueError("Finding description cannot be empty.")

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation of the finding."""

        return {
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence,
            "source": self.source,
            "recommendation": self.recommendation,
        }
