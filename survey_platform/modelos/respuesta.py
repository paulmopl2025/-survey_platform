from datetime import datetime


class RespuestaEncuesta:
    # Almacena las respuestas enviadas por un participante en una encuesta (RF-06)

    def __init__(self, encuesta_id, valores, participante=None):
        self.encuesta_id = encuesta_id
        self.valores = valores
        self.participante = participante
        self.fecha_hora = datetime.now()