import copy
import uuid

from patrones.seccion_composite import Seccion

ESTADO_BORRADOR = "Borrador"
ESTADO_PUBLICADA = "Publicada"

PRIVACIDAD_ELIGE = "participante_elige"
PRIVACIDAD_NOMBRE = "nombre_obligatorio"


class Encuesta:
    # Representa una encuesta dentro de la plataforma e implementa Prototype

    def __init__(self):
        self.id = uuid.uuid4().hex[:8]
        self.titulo = ""
        self.descripcion = ""
        self.privacidad = PRIVACIDAD_ELIGE
        self.estado = ESTADO_BORRADOR
        self.creador = "Admin"
        self.elementos = []
        self.token = None
        self.reporte = None

    @property
    def preguntas(self):
        # Obtiene la lista plana de todas las preguntas hoja en orden de recorrido
        lista = []
        for elemento in self.elementos:
            lista.extend(elemento.obtener_preguntas())
        return lista

    @property
    def secciones(self):
        # Lista todas las secciones y subsecciones registradas en la encuesta
        return [s for s, _ in self.obtener_secciones_con_nivel()]

    def obtener_secciones_con_nivel(self):
        # Recorre el arbol de secciones junto con su nivel de anidacion
        resultado = []
        for elemento in self.elementos:
            if isinstance(elemento, Seccion):
                resultado.extend(elemento.obtener_secciones(0))
        return resultado

    def _contiene_seccion(self, seccion):
        return any(s is seccion for s in self.secciones)

    def agregar_seccion(self, seccion, padre=None):
        # Incorpora una seccion principal o subseccion dentro del arbol Composite
        if self.estado != ESTADO_BORRADOR:
            raise ValueError("Solo se pueden agregar secciones a una encuesta en Borrador.")
        if not isinstance(seccion, Seccion):
            raise TypeError("Debe proporcionar una Seccion valida.")
        if padre is not None:
            if not self._contiene_seccion(padre):
                raise ValueError("La sección padre no pertenece a esta encuesta.")
            padre.agregar(seccion)
        else:
            self.elementos.append(seccion)

    def agregar_pregunta(self, pregunta, seccion=None):
        if self.estado != ESTADO_BORRADOR:
            raise ValueError("Solo se pueden agregar preguntas a una encuesta en Borrador.")
        if seccion is not None:
            if not self._contiene_seccion(seccion):
                raise ValueError("La sección no pertenece a esta encuesta.")
            seccion.agregar(pregunta)
        else:
            self.elementos.append(pregunta)

    def contar_preguntas(self):
        return sum(elemento.contar() for elemento in self.elementos)

    def mostrar_estructura(self):
        return "\n".join(elemento.mostrar() for elemento in self.elementos)

    def validar_estructura(self):
        # Valida recursivamente todas las secciones y preguntas antes de publicar
        for elemento in self.elementos:
            elemento.validar()
        return True

    def clone(self):
        # Patrón Prototype (RF-04): crea una copia profunda e independiente
        copia = copy.deepcopy(self)
        copia.id = uuid.uuid4().hex[:8]
        copia.titulo = f"{self.titulo} (copia)"
        copia.estado = ESTADO_BORRADOR
        copia.token = None
        return copia
