from __future__ import annotations

from abc import ABC, abstractmethod

from survey_platform.exceptions import EnunciadoRequeridoError
from survey_platform.models.enums import QuestionType
from survey_platform.models.question import Question


class QuestionCreator(ABC):
    """Creador abstracto del Factory Method (RF-02)."""

    def create(self, statement: str) -> Question:
        if statement is None or not str(statement).strip():
            raise EnunciadoRequeridoError()
        return self._factory_method(statement.strip())

    @abstractmethod
    def _factory_method(self, statement: str) -> Question:
        raise NotImplementedError


class SingleChoiceQuestionCreator(QuestionCreator):
    def _factory_method(self, statement: str) -> Question:
        return Question(statement=statement, question_type=QuestionType.SINGLE_CHOICE)


class MultipleChoiceQuestionCreator(QuestionCreator):
    def _factory_method(self, statement: str) -> Question:
        return Question(statement=statement, question_type=QuestionType.MULTIPLE_CHOICE)


class FreeTextQuestionCreator(QuestionCreator):
    def _factory_method(self, statement: str) -> Question:
        return Question(statement=statement, question_type=QuestionType.FREE_TEXT)


class ScaleQuestionCreator(QuestionCreator):
    def _factory_method(self, statement: str) -> Question:
        return Question(statement=statement, question_type=QuestionType.SCALE_1_5)


class QuestionFactory:
    """Punto de entrada que delega en el creador concreto según el tipo."""

    _creators: dict[QuestionType, QuestionCreator] = {
        QuestionType.SINGLE_CHOICE: SingleChoiceQuestionCreator(),
        QuestionType.MULTIPLE_CHOICE: MultipleChoiceQuestionCreator(),
        QuestionType.FREE_TEXT: FreeTextQuestionCreator(),
        QuestionType.SCALE_1_5: ScaleQuestionCreator(),
    }

    @classmethod
    def create(cls, question_type: QuestionType, statement: str) -> Question:
        try:
            creator = cls._creators[question_type]
        except KeyError as exc:
            raise ValueError(f"Tipo de pregunta no soportado: {question_type}") from exc
        return creator.create(statement)
