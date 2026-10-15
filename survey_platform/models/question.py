from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from survey_platform.models.enums import QuestionType


@dataclass
class Question:
    statement: str
    question_type: QuestionType
    id: str = field(default_factory=lambda: str(uuid4()))
    options: list[str] = field(default_factory=list)
