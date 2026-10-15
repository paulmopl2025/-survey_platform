from enum import Enum


class SurveyStatus(Enum):
    DRAFT = "Borrador"
    PUBLISHED = "Publicada"


class PrivacySetting(Enum):
    PARTICIPANT_CHOOSES = "el participante elige"
    NAME_REQUIRED = "nombre obligatorio"
    ANONYMOUS_ONLY = "anónimo obligatorio"


class QuestionType(Enum):
    SINGLE_CHOICE = "selección única"
    MULTIPLE_CHOICE = "opción múltiple"
    FREE_TEXT = "texto libre"
    SCALE_1_5 = "escala 1–5"
