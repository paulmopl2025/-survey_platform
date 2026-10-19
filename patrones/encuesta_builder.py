from modelos.encuesta import Encuesta, PRIVACIDAD_ELIGE, PRIVACIDAD_NOMBRE


class EncuestaBuilder:
    """Patrón Builder (RF-01): construye la encuesta paso a paso."""

    def __init__(self, creador="Admin"):
        self.reset()
        self.encuesta.creador = creador

    def reset(self):
        self.encuesta = Encuesta()
        return self

    def set_titulo(self, titulo):
        if not titulo or not titulo.strip():
            raise ValueError("El título de la encuesta es obligatorio.")
        self.encuesta.titulo = titulo.strip()
        return self

    def set_descripcion(self, descripcion):
        self.encuesta.descripcion = descripcion.strip() if descripcion else ""
        return self

    def set_privacidad(self, privacidad):
        if privacidad not in (PRIVACIDAD_ELIGE, PRIVACIDAD_NOMBRE):
            raise ValueError("Configuración de privacidad no válida.")
        self.encuesta.privacidad = privacidad
        return self

    def build(self):
        if not self.encuesta.titulo:
            raise ValueError("No se puede crear una encuesta sin título.")
        resultado = self.encuesta
        self.reset()
        return resultado