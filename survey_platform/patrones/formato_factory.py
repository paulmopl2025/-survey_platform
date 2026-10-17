from abc import ABC, abstractmethod

from modelos.reporte import ReporteOpinion, ReporteSatisfaccion
from patrones.pregunta_creator import CreadorEscala, CreadorSeleccionUnica


class FormatoEncuestaFactory(ABC):
    """Patrón Abstract Factory (RF-05): crea familias de preguntas base y reportes compatibles."""

    nombre = ""

    @abstractmethod
    def crear_preguntas_base(self):
        pass

    @abstractmethod
    def crear_reporte(self):
        pass


class FormatoSatisfaccionFactory(FormatoEncuestaFactory):
    nombre = "Satisfacción"

    def crear_preguntas_base(self):
        return [CreadorEscala().crear_pregunta("¿Qué tan satisfecho está con el servicio?")]

    def crear_reporte(self):
        return ReporteSatisfaccion()


class FormatoOpinionFactory(FormatoEncuestaFactory):
    nombre = "Opinión"

    def crear_preguntas_base(self):
        return [CreadorSeleccionUnica().crear_pregunta("¿Recomendaría el servicio?", ["Sí", "No"])]

    def crear_reporte(self):
        return ReporteOpinion()


FORMATOS_DISPONIBLES = [FormatoSatisfaccionFactory(), FormatoOpinionFactory()]