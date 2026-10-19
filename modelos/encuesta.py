import uuid

ESTADO_BORRADOR = "Borrador"
ESTADO_PUBLICADA = "Publicada"
PRIVACIDAD_ELIGE = "participante_elige"
PRIVACIDAD_NOMBRE = "nombre_obligatorio"

class Encuesta:
    def __init__(self):
        self.id = uuid.uuid4().hex[:8]
        self.titulo = ""
        self.descripcion = ""
        self.privacidad = PRIVACIDAD_ELIGE
        self.estado = ESTADO_BORRADOR
        self.creador = "Admin"
        self.preguntas = []
        self.token = None

    def agregar_pregunta(self, pregunta):
        if self.estado != ESTADO_BORRADOR:
            raise ValueError("Solo se pueden agregar preguntas en estado Borrador.")
        self.preguntas.append(pregunta)