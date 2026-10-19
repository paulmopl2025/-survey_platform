from abc import ABC, abstractmethod
from modelos.pregunta import (
    PreguntaEscala,
    PreguntaOpcionMultiple,
    PreguntaSeleccionUnica,
    PreguntaTextoLibre,
)


class CreadorPregunta(ABC):
    """Clase base abstracta para el patrón Factory Method (RF-02)."""

    @abstractmethod
    def crear_pregunta(self, enunciado, opciones=None):
        pass


class CreadorSeleccionUnica(CreadorPregunta):
    def crear_pregunta(self, enunciado, opciones=None):
        return PreguntaSeleccionUnica(enunciado, opciones)


class CreadorOpcionMultiple(CreadorPregunta):
    def crear_pregunta(self, enunciado, opciones=None):
        return PreguntaOpcionMultiple(enunciado, opciones)


class CreadorEscala(CreadorPregunta):
    def crear_pregunta(self, enunciado, opciones=None):
        return PreguntaEscala(enunciado)


class CreadorTextoLibre(CreadorPregunta):
    def crear_pregunta(self, enunciado, opciones=None):
        return PreguntaTextoLibre(enunciado)