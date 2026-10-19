from modelos.encuesta import ESTADO_BORRADOR, ESTADO_PUBLICADA
from patrones.generador_token import GeneradorTokenSingleton


class PlataformaEncuestas:
    """Gestor principal del sistema para administrar encuestas y respuestas."""

    def __init__(self):
        self.encuestas = {}  # {id_encuesta: encuesta_obj}
        self.respuestas = {} # {id_encuesta: [respuestas]}
        self.tokens_activos = {} # {token: id_encuesta}
        self.generador_token = GeneradorTokenSingleton()

    def registrar_encuesta(self, encuesta):
        self.encuestas[encuesta.id] = encuesta
        self.respuestas[encuesta.id] = []

    def publicar_encuesta(self, id_encuesta):
        encuesta = self.encuestas.get(id_encuesta)
        if not encuesta:
            raise ValueError("Encuesta no encontrada.")
        if not encuesta.preguntas:
            raise ValueError("No se puede publicar una encuesta sin preguntas.")
        
        token = self.generador_token.generar_token()
        encuesta.token = token
        encuesta.estado = ESTADO_PUBLICADA
        self.tokens_activos[token] = id_encuesta
        return token

    def obtener_por_token(self, token):
        id_encuesta = self.tokens_activos.get(token)
        if not id_encuesta:
            return None
        return self.encuestas.get(id_encuesta)

    def guardar_respuesta(self, id_encuesta, respuesta):
        if id_encuesta not in self.respuestas:
            self.respuestas[id_encuesta] = []
        self.respuestas[id_encuesta].append(respuesta)