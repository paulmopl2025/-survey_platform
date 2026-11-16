from patrones.seccion_composite import ElementoEncuesta


class PreguntaDecorator(ElementoEncuesta):
    # Se agrega el patron decorator como base para envolver preguntas

    def __init__(self, pregunta):
        if not isinstance(pregunta, ElementoEncuesta) or not hasattr(pregunta, "validar_respuesta"):
            raise TypeError("El decorador debe envolver una Pregunta valida.")
        self._pregunta = pregunta

    @property
    def pregunta_base(self):
        return getattr(self._pregunta, "pregunta_base", self._pregunta)

    @property
    def tipo(self):
        return self._pregunta.tipo

    @property
    def enunciado(self):
        return self._pregunta.enunciado

    @property
    def es_obligatoria(self):
        return getattr(self._pregunta, "es_obligatoria", False)

    def describir(self):
        return self._pregunta.describir()

    def validar_respuesta(self, entrada):
        return self._pregunta.validar_respuesta(entrada)

    def mostrar(self, nivel=0):
        sangria = "  " * nivel
        return "{}{}".format(sangria, self.describir().replace("\n", "\n" + sangria))

    def contar(self):
        return self._pregunta.contar()

    def obtener_preguntas(self):
        return [self]

    def validar(self):
        return self._pregunta.validar()

    def __getattr__(self, nombre):
        if nombre.startswith("_"):
            raise AttributeError(nombre)
        return getattr(self._pregunta, nombre)


class Obligatoria(PreguntaDecorator):
    # Se agrega decorador para exigir respuesta obligatoria

    @property
    def es_obligatoria(self):
        return True

    def describir(self):
        texto = self._pregunta.describir()
        if "\n" in texto:
            primera, resto = texto.split("\n", 1)
            return "{} [Obligatoria]\n{}".format(primera, resto)
        return "{} [Obligatoria]".format(texto)

    def validar_respuesta(self, entrada):
        if not entrada or not entrada.strip():
            raise ValueError("Esta pregunta es obligatoria.")
        return self._pregunta.validar_respuesta(entrada)


class ConAyuda(PreguntaDecorator):
    # Se agrega decorador para mostrar texto de ayuda en la pregunta

    def __init__(self, pregunta, ayuda):
        super().__init__(pregunta)
        if not ayuda or not ayuda.strip():
            raise ValueError("El texto de ayuda no puede estar vacío.")
        self.ayuda = ayuda.strip()

    def describir(self):
        return "{}\n  Ayuda: {}".format(self._pregunta.describir(), self.ayuda)


class ConValidacion(PreguntaDecorator):
    # Se agrega decorador para agregar validaciones configurables

    def __init__(self, pregunta, min_caracteres=None, min_opciones=None):
        super().__init__(pregunta)
        if min_caracteres is None and min_opciones is None:
            raise ValueError("Debes indicar al menos una regla de validación.")
        if min_caracteres is not None and min_caracteres <= 0:
            raise ValueError("El mínimo de caracteres debe ser mayor a 0.")
        if min_opciones is not None and min_opciones <= 0:
            raise ValueError("El mínimo de opciones debe ser mayor a 0.")
        self.min_caracteres = min_caracteres
        self.min_opciones = min_opciones

    def describir(self):
        reglas = []
        if self.min_caracteres is not None:
            reglas.append("mínimo {} caracteres".format(self.min_caracteres))
        if self.min_opciones is not None:
            reglas.append("mínimo {} opciones".format(self.min_opciones))
        return "{}\n  Validación: {}".format(
            self._pregunta.describir(), ", ".join(reglas))

    def validar_respuesta(self, entrada):
        valor = self._pregunta.validar_respuesta(entrada)
        if valor is None:
            return None
        if self.min_caracteres is not None and isinstance(valor, str):
            if len(valor) < self.min_caracteres:
                raise ValueError("La respuesta debe tener al menos {} caracteres.".format(
                    self.min_caracteres))
        if self.min_opciones is not None and isinstance(valor, list):
            if len(valor) < self.min_opciones:
                raise ValueError("Debes elegir al menos {} opciones.".format(
                    self.min_opciones))
        return valor
