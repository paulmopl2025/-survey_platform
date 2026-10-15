from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from survey_platform.models.enums import PrivacySetting, SurveyStatus
from survey_platform.models.question import Question
from survey_platform.models.user import User


@dataclass
class Survey:
    title: str
    creator: User
    description: str = ""
    privacy: PrivacySetting = PrivacySetting.PARTICIPANT_CHOOSES
    id: str = field(default_factory=lambda: str(uuid4()))
    status: SurveyStatus = SurveyStatus.DRAFT
    admin: User = field(init=False)
    questions: list[Question] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.admin = self.creator

    def add_question(self, question: Question) -> None:
        self.questions.append(question)
