import unittest

from survey_platform.builders.survey_builder import SurveyBuilder
from survey_platform.exceptions import EnunciadoRequeridoError
from survey_platform.factories.question_factory import QuestionFactory
from survey_platform.models.enums import PrivacySetting, QuestionType, SurveyStatus
from survey_platform.models.user import User


def _encuesta_borrador():
    return (
        SurveyBuilder()
        .with_title("Hábitos")
        .with_description("")
        .with_privacy(PrivacySetting.PARTICIPANT_CHOOSES)
        .with_creator(User(name="Ana"))
        .build()
    )


class TestRF02AgregarPreguntas(unittest.TestCase):
    def test_agregar_pregunta_seleccion_unica_a_encuesta_en_borrador(self):
        encuesta = _encuesta_borrador()
        self.assertEqual(encuesta.status, SurveyStatus.DRAFT)

        pregunta = QuestionFactory.create(QuestionType.SINGLE_CHOICE, "¿x?")
        encuesta.add_question(pregunta)

        self.assertEqual(pregunta.question_type, QuestionType.SINGLE_CHOICE)
        self.assertEqual(pregunta.statement, "¿x?")
        self.assertEqual(encuesta.questions, [pregunta])

    def test_factory_crea_todos_los_tipos_soportados(self):
        tipos = (
            QuestionType.SINGLE_CHOICE,
            QuestionType.MULTIPLE_CHOICE,
            QuestionType.FREE_TEXT,
            QuestionType.SCALE_1_5,
        )
        for question_type in tipos:
            with self.subTest(question_type=question_type):
                pregunta = QuestionFactory.create(
                    question_type, "¿Estudia en las noches?"
                )
                self.assertEqual(pregunta.question_type, question_type)
                self.assertEqual(pregunta.statement, "¿Estudia en las noches?")

    def test_rechaza_pregunta_sin_enunciado(self):
        encuesta = _encuesta_borrador()

        with self.assertRaises(EnunciadoRequeridoError) as ctx:
            QuestionFactory.create(QuestionType.SINGLE_CHOICE, "")
        self.assertEqual(str(ctx.exception), "El enunciado es obligatorio")
        self.assertEqual(encuesta.questions, [])


if __name__ == "__main__":
    unittest.main()
