import copy
import uuid

ESTADO_BORRADOR = "Borrador"
ESTADO_PUBLICADA = "Publicada"

PRIVACIDAD_ELIGE = "participante_elige"
PRIVACIDAD_NOMBRE = "nombre_obligatorio"


class Encuesta:
    """Representa una encuesta dentro de la plataforma e implementa Prototype."""

    def __init__(self):
        self.id = uuid.uuid4().hex[:8]
        self.titulo = ""
        self.descripcion = ""
        self.privacidad = PRIVACIDAD_ELIGE
        self.estado = ESTADO_BORRADOR
        self.creador = "Admin"
        self.preguntas = []
        self.token = None
        self.reporte = None

    def agregar_pregunta(self, pregunta):
        if self.estado != ESTADO_BORRADOR:
            raise ValueError("Solo se pueden agregar preguntas a una encuesta en Borrador.")
        self.preguntas.append(pregunta)

    def clone(self):
        """Patrón Prototype (RF-04): crea una copia profunda e independiente."""
        copia = copy.deepcopy(self)
        copia.id = uuid.uuid4().hex[:8]
        copia.titulo = f"{self.titulo} (copia)"
        copia.estado = ESTADO_BORRADOR
        copia.token = None
        return copia
