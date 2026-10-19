from abc import ABC, abstractmethod

from modelos.pregunta import (
    PreguntaEscala,
    PreguntaOpcionMultiple,
    PreguntaSeleccionUnica,
    PreguntaTextoLibre,
)


class PreguntaCreator(ABC):
    # Patrón Factory Method (RF-02): creador abstracto de preguntas

    @abstractmethod
    def crear_pregunta(self, enunciado, opciones=None):
        pass


class CreadorSeleccionUnica(PreguntaCreator):
    def crear_pregunta(self, enunciado, opciones=None):
        return PreguntaSeleccionUnica(enunciado, opciones)


class CreadorOpcionMultiple(PreguntaCreator):
    def crear_pregunta(self, enunciado, opciones=None):
        return PreguntaOpcionMultiple(enunciado, opciones)


class CreadorEscala(PreguntaCreator):
    def crear_pregunta(self, enunciado, opciones=None):
        return PreguntaEscala(enunciado)


class CreadorTextoLibre(PreguntaCreator):
    def crear_pregunta(self, enunciado, opciones=None):
        return PreguntaTextoLibre(enunciado)