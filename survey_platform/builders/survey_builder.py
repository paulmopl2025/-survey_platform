from __future__ import annotations

from survey_platform.exceptions import TituloRequeridoError
from survey_platform.models.enums import PrivacySetting
from survey_platform.models.survey import Survey
from survey_platform.models.user import User


class SurveyBuilder:
    """Builder para crear una encuesta paso a paso (RF-01)."""

    def __init__(self) -> None:
        self._title: str | None = None
        self._description: str = ""
        self._privacy: PrivacySetting | None = None
        self._creator: User | None = None

    def with_title(self, title: str) -> SurveyBuilder:
        self._title = title
        return self

    def with_description(self, description: str) -> SurveyBuilder:
        self._description = description
        return self

    def with_privacy(self, privacy: PrivacySetting) -> SurveyBuilder:
        self._privacy = privacy
        return self

    def with_creator(self, creator: User) -> SurveyBuilder:
        self._creator = creator
        return self

    def build(self) -> Survey:
        if self._title is None or not str(self._title).strip():
            raise TituloRequeridoError()
        if self._creator is None:
            raise ValueError("El creador es obligatorio")
        if self._privacy is None:
            raise ValueError("La privacidad es obligatoria")

        return Survey(
            title=self._title.strip(),
            description=self._description,
            privacy=self._privacy,
            creator=self._creator,
        )
