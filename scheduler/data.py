from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Task:
    """A project task."""

    id: str
    duration: int
    demands: Dict[str, int] = field(default_factory=dict)
    predecessors: List[str] = field(default_factory=list)


@dataclass
class Resource:
    """A renewable resource with limited capacity."""

    id: str
    capacity: int


@dataclass
class Calendar:
    """Simple working calendar."""

    id: str
    working_hours: int = 8
