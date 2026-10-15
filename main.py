import copy
import uuid
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


# ==========================================
# 1. PATRÓN SINGLETON (RF-06: Generador de Tokens)
# ==========================================
class TokenGeneratorSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenGeneratorSingleton, cls).__new__(cls)
            cls._instance.tokens_emitidos = set()
        return cls._instance

    def generar_token(self) -> str:
        token = str(uuid.uuid4())[:8]
        while token in self.tokens_emitidos:
            token = str(uuid.uuid4())[:8]
        self.tokens_emitidos.add(token)
        return token


# ==========================================
# MODELOS DE PREGUNTAS Y FACTORY METHOD (RF-02)
# ==========================================
class Pregunta(ABC):
    def __init__(self, enunciado: str):
        if not enunciado or not enunciado.strip():
            raise ValueError("El enunciado de la pregunta no puede estar vacío.")
        self.enunciado = enunciado

    @abstractmethod
    def obtener_tipo(self) -> str:
        pass


class PreguntaSeleccionUnica(Pregunta):
    def __init__(self, enunciado: str, opciones: Optional[List[str]] = None):
        super().__init__(enunciado)
        self.opciones = opciones if opciones is not None else []

    def agregar_opcion(self, opcion: str):
        if not opcion or not opcion.strip():
            raise ValueError("La opción no puede estar vacía.")
        self.opciones.append(opcion)

    def obtener_tipo(self) -> str:
        return "Selección Única"


class PreguntaEscala(Pregunta):
    def __init__(self, enunciado: str, min_val: int = 1, max_val: int = 5):
        super().__init__(enunciado)
        self.min_val = min_val
        self.max_val = max_val

    def obtener_tipo(self) -> str:
        return f"Escala ({self.min_val}-{self.max_val})"


class PreguntaTextoLibre(Pregunta):
    def obtener_tipo(self) -> str:
        return "Texto Libre"


# FACTORY METHOD (RF-02)
class PreguntaFactory:
    @staticmethod
    def crear_pregunta(tipo: str, enunciado: str, **kwargs) -> Pregunta:
        tipo_lower = tipo.lower()
        if tipo_lower in ("seleccion_unica", "seleccion unica"):
            return PreguntaSeleccionUnica(enunciado, kwargs.get("opciones", []))
        elif tipo_lower == "escala":
            return PreguntaEscala(enunciado, kwargs.get("min_val", 1), kwargs.get("max_val", 5))
        elif tipo_lower in ("texto", "texto_libre"):
            return PreguntaTextoLibre(enunciado)
        else:
            raise ValueError(f"Tipo de pregunta desconocido: {tipo}")


# ==========================================
# 2. PATRÓN PROTOTYPE Y MODELO ENCUESTA (RF-04)
# ==========================================
class Encuesta:
    def __init__(self):
        self.id: str = str(uuid.uuid4())[:8]
        self.titulo: str = ""
        self.descripcion: str = ""
        self.privacidad: str = "el participante elige"
        self.estado: str = "Borrador"
        self.creador: str = "Admin"
        self.preguntas: List[Pregunta] = []
        self.token_acceso: Optional[str] = None

    # Implementación de PROTOTYPE (Copia profunda)
    def clone(self) -> 'Encuesta':
        copia = copy.deepcopy(self)
        copia.id = str(uuid.uuid4())[:8]
        copia.estado = "Borrador"
        copia.token_acceso = None
        return copia


# ==========================================
# 3. PATRÓN BUILDER (RF-01: Crear Encuesta)
# ==========================================
class EncuestaBuilder:
    def __init__(self, creador: str = "Admin"):
        self.reset()
        self.encuesta.creador = creador

    def reset(self):
        self.encuesta = Encuesta()
        return self

    def set_titulo(self, titulo: str):
        if not titulo or not titulo.strip():
            raise ValueError("El título de la encuesta es obligatorio.")
        self.encuesta.titulo = titulo
        return self

    def set_descripcion(self, descripcion: str):
        self.encuesta.descripcion = descripcion
        return self

    def set_privacidad(self, privacidad: str):
        self.encuesta.privacidad = privacidad
        return self

    def add_pregunta(self, pregunta: Pregunta):
        self.encuesta.preguntas.append(pregunta)
        return self

    def build(self) -> Encuesta:
        if not self.encuesta.titulo:
            raise ValueError("No se puede construir una encuesta sin título.")
        resultado = self.encuesta
        self.reset()
        return resultado


# ==========================================
# 4. PATRÓN ABSTRACT FACTORY (RF-05)
# ==========================================
class ReporteAnalitico(ABC):
    @abstractmethod
    def generar_resumen(self, respuestas: List[Dict]) -> str:
        pass


class ReporteSatisfaccion(ReporteAnalitico):
    def generar_resumen(self, respuestas: List[Dict]) -> str:
        return "Reporte de Satisfacción: Calculando Media, Mediana y Moda para escalas."


class ReporteOpinion(ReporteAnalitico):
    def generar_resumen(self, respuestas: List[Dict]) -> str:
        return "Reporte de Opinión: Generando gráfico de barras porcentual."


class FormatoEncuestaFactory(ABC):
    @abstractmethod
    def crear_preguntas_base(self) -> List[Pregunta]:
        pass

    @abstractmethod
    def crear_reporte(self) -> ReporteAnalitico:
        pass


class FormatoSatisfaccionFactory(FormatoEncuestaFactory):
    def crear_preguntas_base(self) -> List[Pregunta]:
        return [PreguntaFactory.crear_pregunta("escala", "¿Qué tan satisfecho está con el servicio?")]

    def crear_reporte(self) -> ReporteAnalitico:
        return ReporteSatisfaccion()


class FormatoOpinionFactory(FormatoEncuestaFactory):
    def crear_preguntas_base(self) -> List[Pregunta]:
        p = PreguntaFactory.crear_pregunta("seleccion_unica", "¿Recomendaría el servicio?", opciones=["Sí", "No"])
        return [p]

    def crear_reporte(self) -> ReporteAnalitico:
        return ReporteOpinion()


# ==========================================
# SERVICIO PRINCIPAL Y PUBLICACIÓN (RF-06)
# ==========================================
class ServicioEncuesta:
    @staticmethod
    def publicar_encuesta(encuesta: Encuesta) -> str:
        if not encuesta.preguntas:
            raise ValueError("No se puede publicar una encuesta sin preguntas.")

        encuesta.estado = "Publicada"
        token_gen = TokenGeneratorSingleton()
        encuesta.token_acceso = token_gen.generar_token()
        return encuesta.token_acceso


# ==========================================
# DEMOSTRACIÓN DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE PATRONES CREACIONALES Y BDD ===")

    # 1. Builder (RF-01)
    builder = EncuestaBuilder(creador="Docente")
    encuesta_original = (builder.set_titulo("Hábitos de estudio")
                         .set_descripcion("Encuesta sobre rutinas nocturnas")
                         .set_privacidad("el participante elige")
                         .build())
    print(f"\n[Builder] Encuesta Creada: '{encuesta_original.titulo}' | ID: {encuesta_original.id} | Estado: {encuesta_original.estado}")

    # 2. Factory Method (RF-02)
    preg1 = PreguntaFactory.crear_pregunta("seleccion_unica", "¿Estudia en las noches?", opciones=["Sí", "No"])
    preg2 = PreguntaFactory.crear_pregunta("escala", "Nivel de concentración (1 a 5)")
    encuesta_original.preguntas.extend([preg1, preg2])
    print(f"[Factory Method] Preguntas agregadas: {len(encuesta_original.preguntas)}")

    # 3. Prototype (RF-04)
    encuesta_copia = encuesta_original.clone()
    print(f"\n[Prototype] Copia Creada | ID Copia: {encuesta_copia.id} (Original: {encuesta_original.id})")

    # Prueba de independencia de la copia
    encuesta_original.preguntas.pop()
    print(f"[Prototype Test] Preguntas en Original tras eliminar 1: {len(encuesta_original.preguntas)}")
    print(f"[Prototype Test] Preguntas en Copia (conserva 2): {len(encuesta_copia.preguntas)}")

    # 4. Singleton (RF-06)
    token = ServicioEncuesta.publicar_encuesta(encuesta_copia)
    print(f"\n[Singleton] Encuesta Publicada con Token de Acceso Único: {token}")

    # 5. Abstract Factory (RF-05)
    factory_sat = FormatoSatisfaccionFactory()
    preguntas_sat = factory_sat.crear_preguntas_base()
    reporte_sat = factory_sat.crear_reporte()
    print(f"\n[Abstract Factory] Formato Satisfacción creado:")
    print(f" - Pregunta base: {preguntas_sat[0].enunciado}")
    print(f" - Tipo de Reporte: {reporte_sat.generar_resumen([])}")
    