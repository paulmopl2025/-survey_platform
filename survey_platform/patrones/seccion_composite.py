from abc import ABC, abstractmethod


class ElementoEncuesta(ABC):
    # Patron Composite interfaz comun para secciones y preguntas

    @abstractmethod
    def mostrar(self, nivel=0):
        pass

    @abstractmethod
    def contar(self):
        pass

    @abstractmethod
    def obtener_preguntas(self):
        pass

    @abstractmethod
    def validar(self):
        pass


class Seccion(ElementoEncuesta):
    # Componente compuesto que agrupa preguntas y subsecciones

    def __init__(self, titulo):
        if not titulo or not titulo.strip():
            raise ValueError("La sección necesita un título.")
        self.titulo = titulo.strip()
        self.elementos = []

    def agregar(self, elemento):
        # Incorpora una pregunta o subseccion dentro de la seccion actual
        if elemento is self:
            raise ValueError("Una sección no puede contenerse a sí misma.")
        if not isinstance(elemento, ElementoEncuesta):
            raise TypeError("El elemento debe heredar de ElementoEncuesta.")
        self.elementos.append(elemento)

    def contar(self):
        return sum(elemento.contar() for elemento in self.elementos)

    def contar_directas(self):
        # Cuenta unicamente las preguntas directas de esta seccion
        return sum(
            1 for elemento in self.elementos if not isinstance(elemento, Seccion)
        )

    def obtener_preguntas(self):
        preguntas = []
        for elemento in self.elementos:
            preguntas.extend(elemento.obtener_preguntas())
        return preguntas

    def obtener_secciones(self, nivel=0):
        # Lista recursivamente las secciones y subsecciones con su nivel de profundidad
        resultado = [(self, nivel)]
        for elemento in self.elementos:
            if isinstance(elemento, Seccion):
                resultado.extend(elemento.obtener_secciones(nivel + 1))
        return resultado

    def mostrar(self, nivel=0):
        sangria = "  " * nivel
        etiqueta = "Subsección" if nivel > 0 else "Sección"
        lineas = ["{}{}: {} ({} pregunta(s))".format(
            sangria, etiqueta, self.titulo, self.contar_directas())]
        for elemento in self.elementos:
            lineas.append(elemento.mostrar(nivel + 1))
        return "\n".join(lineas)

    def validar(self):
        if self.contar() == 0:
            raise ValueError("La sección '{}' no tiene preguntas.".format(self.titulo))
        for elemento in self.elementos:
            elemento.validar()
        return True
