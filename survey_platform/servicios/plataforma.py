from modelos.encuesta import (
    ESTADO_BORRADOR,
    ESTADO_PUBLICADA,
    PRIVACIDAD_ELIGE,
    PRIVACIDAD_NOMBRE,
)
from modelos.reporte import ReporteGeneral
from modelos.respuesta import RespuestaEncuesta
from patrones.encuesta_builder import EncuestaBuilder
from patrones.token_generator import TokenGenerator


class Plataforma:
    """Gestiona las encuestas, respuestas y operaciones principales del sistema."""

    def __init__(self):
        self.encuestas = []
        self._respuestas = {}

    def registrar(self, encuesta):
        self.encuestas.append(encuesta)
        return encuesta

    def crear_desde_formato(self, formato, titulo, descripcion="", privacidad=PRIVACIDAD_ELIGE):
        encuesta = (
            EncuestaBuilder()
            .set_titulo(titulo)
            .set_descripcion(descripcion)
            .set_privacidad(privacidad)
            .build()
        )
        for pregunta in formato.crear_preguntas_base():
            encuesta.agregar_pregunta(pregunta)
        encuesta.reporte = formato.crear_reporte()
        return self.registrar(encuesta)

    def duplicar(self, encuesta):
        return self.registrar(encuesta.clone())

    def publicar(self, encuesta):
        if encuesta.estado == ESTADO_PUBLICADA:
            raise ValueError("La encuesta ya está publicada.")
        if not encuesta.titulo.strip():
            raise ValueError("No se puede publicar una encuesta sin título.")
        if not encuesta.preguntas:
            raise ValueError("No se puede publicar: agrega al menos una pregunta.")
        encuesta.estado = ESTADO_PUBLICADA
        encuesta.token = TokenGenerator().generar_token()
        return encuesta.token

    def buscar_por_token(self, token):
        for encuesta in self.encuestas:
            if encuesta.token and encuesta.token == token.strip():
                return encuesta
        return None

    def responder(self, encuesta, valores, nombre=None, anonimo=False):
        if encuesta.estado != ESTADO_PUBLICADA:
            raise ValueError("La encuesta no está publicada.")
        if len(valores) != len(encuesta.preguntas):
            raise ValueError("Faltan respuestas.")

        nombre = (nombre or "").strip() or None
        if encuesta.privacidad == PRIVACIDAD_NOMBRE:
            if nombre is None:
                raise ValueError("Esta encuesta requiere tu nombre.")
            participante = nombre
        elif anonimo:
            participante = None
        else:
            if nombre is None:
                raise ValueError("Escribe tu nombre o elige responder de forma anónima.")
            participante = nombre

        respuesta = RespuestaEncuesta(encuesta.id, valores, participante)
        self._respuestas.setdefault(encuesta.id, []).append(respuesta)
        return respuesta

    def respuestas_de(self, encuesta):
        return self._respuestas.get(encuesta.id, [])

    def analizar(self, encuesta):
        reporte = encuesta.reporte or ReporteGeneral()
        return reporte.generar(encuesta, self.respuestas_de(encuesta))