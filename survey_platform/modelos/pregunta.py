from abc import ABC, abstractmethod


class Pregunta(ABC):
    """Clase base abstracta para todos los tipos de pregunta."""

    def __init__(self, enunciado):
        if not enunciado or not enunciado.strip():
            raise ValueError("La pregunta necesita un enunciado.")
        self.enunciado = enunciado.strip()

    @property
    @abstractmethod
    def tipo(self):
        pass

    @abstractmethod
    def validar_respuesta(self, entrada):
        """Valida y transforma la respuesta ingresada por el participante."""
        pass

    def describir(self):
        return "[{}] {}".format(self.tipo, self.enunciado)


class PreguntaConOpciones(Pregunta):
    """Clase base para preguntas que requieren configurar mínimo 2 opciones (RF-03)."""

    def __init__(self, enunciado, opciones):
        super().__init__(enunciado)
        limpias = [o.strip() for o in (opciones or []) if o and o.strip()]
        if len(limpias) < 2:
            raise ValueError("Una pregunta de selección necesita al menos 2 opciones.")
        self.opciones = limpias

    def describir(self):
        lista = "  ".join("({}) {}".format(i, o) for i, o in enumerate(self.opciones, 1))
        return "{}  {}".format(super().describir(), lista)

    def _opcion_por_numero(self, texto):
        try:
            numero = int(texto.strip())
        except ValueError:
            raise ValueError("Escribe el número de la opción.")
        if not 1 <= numero <= len(self.opciones):
            raise ValueError("Elige un número entre 1 y {}.".format(len(self.opciones)))
        return self.opciones[numero - 1]


class PreguntaSeleccionUnica(PreguntaConOpciones):
    @property
    def tipo(self):
        return "Selección única"

    def validar_respuesta(self, entrada):
        return self._opcion_por_numero(entrada)


class PreguntaOpcionMultiple(PreguntaConOpciones):
    @property
    def tipo(self):
        return "Opción múltiple"

    def validar_respuesta(self, entrada):
        if not entrada.strip():
            raise ValueError("Elige al menos una opción (separadas por coma).")
        elegidas = []
        for parte in entrada.split(","):
            opcion = self._opcion_por_numero(parte)
            if opcion not in elegidas:
                elegidas.append(opcion)
        return elegidas


class PreguntaEscala(Pregunta):
    MINIMO = 1
    MAXIMO = 5

    @property
    def tipo(self):
        return "Escala {}-{}".format(self.MINIMO, self.MAXIMO)

    def validar_respuesta(self, entrada):
        try:
            valor = int(entrada.strip())
        except ValueError:
            raise ValueError("Escribe un número entre {} y {}.".format(self.MINIMO, self.MAXIMO))
        if not self.MINIMO <= valor <= self.MAXIMO:
            raise ValueError("El valor debe estar entre {} y {}.".format(self.MINIMO, self.MAXIMO))
        return valor


class PreguntaTextoLibre(Pregunta):
    @property
    def tipo(self):
        return "Texto libre"

    def validar_respuesta(self, entrada):
        if not entrada.strip():
            raise ValueError("Escribe una respuesta.")
        return entrada.strip()