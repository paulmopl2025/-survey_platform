from modelos.encuesta import PRIVACIDAD_ELIGE, PRIVACIDAD_NOMBRE, Encuesta


class EncuestaBuilder:
    """Patrón Builder (RF-01): construye una encuesta paso a paso."""

    def __init__(self, creador="Admin"):
        self._creador = creador
        self.reset()

    def reset(self):
        self._encuesta = Encuesta()
        self._encuesta.creador = self._creador
        return self

    def set_titulo(self, titulo):
        if not titulo or not titulo.strip():
            raise ValueError("El título es obligatorio.")
        self._encuesta.titulo = titulo.strip()
        return self

    def set_descripcion(self, descripcion):
        self._encuesta.descripcion = (descripcion or "").strip()
        return self

    def set_privacidad(self, privacidad):
        if privacidad not in (PRIVACIDAD_ELIGE, PRIVACIDAD_NOMBRE):
            raise ValueError("Privacidad no válida.")
        self._encuesta.privacidad = privacidad
        return self

    def build(self):
        if not self._encuesta.titulo:
            raise ValueError("No se puede crear una encuesta sin título.")
        resultado = self._encuesta
        self.reset()
        return resultado