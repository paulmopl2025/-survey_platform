import unittest

from survey_platform.builders.survey_builder import SurveyBuilder
from survey_platform.exceptions import TituloRequeridoError
from survey_platform.models.enums import PrivacySetting, SurveyStatus
from survey_platform.models.user import User


class TestRF01CrearEncuesta(unittest.TestCase):
    def test_crear_encuesta_paso_a_paso_en_borrador_con_admin(self):
        creador = User(name="Ana")

        encuesta = (
            SurveyBuilder()
            .with_title("x")
            .with_description("Descripción de la encuesta")
            .with_privacy(PrivacySetting.PARTICIPANT_CHOOSES)
            .with_creator(creador)
            .build()
        )

        self.assertEqual(encuesta.title, "x")
        self.assertEqual(encuesta.description, "Descripción de la encuesta")
        self.assertEqual(encuesta.privacy, PrivacySetting.PARTICIPANT_CHOOSES)
        self.assertEqual(encuesta.status, SurveyStatus.DRAFT)
        self.assertTrue(encuesta.id)
        self.assertEqual(encuesta.admin, creador)
        self.assertEqual(encuesta.creator, creador)

    def test_rechaza_creacion_sin_titulo(self):
        creador = User(name="Ana")
        builder = (
            SurveyBuilder()
            .with_description("Sin título")
            .with_privacy(PrivacySetting.PARTICIPANT_CHOOSES)
            .with_creator(creador)
        )

        with self.assertRaises(TituloRequeridoError) as ctx:
            builder.build()
        self.assertEqual(str(ctx.exception), "El título es obligatorio")


if __name__ == "__main__":
    unittest.main()
