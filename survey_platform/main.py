from modelos.encuesta import (
    ESTADO_BORRADOR,
    ESTADO_PUBLICADA,
    PRIVACIDAD_ELIGE,
    PRIVACIDAD_NOMBRE,
)
from patrones.encuesta_builder import EncuestaBuilder
from patrones.formato_factory import FORMATOS_DISPONIBLES
from patrones.pregunta_creator import (
    CreadorEscala,
    CreadorOpcionMultiple,
    CreadorSeleccionUnica,
    CreadorTextoLibre,
)
from servicios.plataforma import Plataforma


class MenuConsola:
    """Gestiona la interfaz de usuario en consola bajo el paradigma orientado a objetos."""

    def __init__(self, plataforma):
        self.plataforma = plataforma
        self.tipos_de_pregunta = {
            "1": ("Selección única", CreadorSeleccionUnica(), True),
            "2": ("Opción múltiple", CreadorOpcionMultiple(), True),
            "3": ("Escala 1-5", CreadorEscala(), False),
            "4": ("Texto libre", CreadorTextoLibre(), False),
        }
        self.opciones = [
            ("Crear encuesta", self.crear_encuesta),
            ("Crear encuesta desde un formato", self.crear_desde_formato),
            ("Agregar preguntas", self.agregar_preguntas),
            ("Duplicar encuesta", self.duplicar_encuesta),
            ("Publicar encuesta", self.publicar_encuesta),
            ("Responder encuesta", self.responder_encuesta),
            ("Analizar resultados", self.analizar_resultados),
        ]

    #Ayuda para pedir datos

    def pedir_obligatorio(self, mensaje):
        while True:
            texto = input(mensaje).strip()
            if texto:
                return texto
            print("  Este dato es obligatorio.")

    def pedir_privacidad(self):
        print("Privacidad de las respuestas:")
        print("  1. El participante elige si responde anónimo o con nombre")
        print("  2. El nombre es obligatorio")
        while True:
            opcion = input("Elige (1-2): ").strip()
            if opcion == "1":
                return PRIVACIDAD_ELIGE
            if opcion == "2":
                return PRIVACIDAD_NOMBRE
            print("  Opción no válida.")

    def elegir_encuesta(self, estado=None):
        candidatas = [
            e for e in self.plataforma.encuestas if estado is None or e.estado == estado
        ]
        if not candidatas:
            detalle = " en estado {}".format(estado) if estado else ""
            print("No hay encuestas{} para esta opción.".format(detalle))
            return None
        for i, e in enumerate(candidatas, 1):
            print("  {}. {} [{}] - {} pregunta(s)".format(i, e.titulo, e.estado, len(e.preguntas)))
        entrada = input("Elige una encuesta (Enter para cancelar): ").strip()
        if not entrada:
            return None
        if entrada.isdigit() and 1 <= int(entrada) <= len(candidatas):
            return candidatas[int(entrada) - 1]
        print("Opción no válida.")
        return None

    #Opciones del menú

    def crear_encuesta(self):
        builder = EncuestaBuilder(creador="Admin")
        while True:
            try:
                builder.set_titulo(input("Título: "))
                break
            except ValueError as error:
                print("  Error: {}".format(error))
        builder.set_descripcion(input("Descripción (opcional): "))
        builder.set_privacidad(self.pedir_privacidad())
        encuesta = self.plataforma.registrar(builder.build())
        print("[Builder] Encuesta '{}' construida paso a paso. ID: {} | Estado: {}".format(
            encuesta.titulo, encuesta.id, encuesta.estado))

    def crear_desde_formato(self):
        print("Formatos disponibles:")
        for i, formato in enumerate(FORMATOS_DISPONIBLES, 1):
            print("  {}. {}".format(i, formato.nombre))
        opcion = input("Elige un formato: ").strip()
        if not (opcion.isdigit() and 1 <= int(opcion) <= len(FORMATOS_DISPONIBLES)):
            print("Formato no válido.")
            return
        formato = FORMATOS_DISPONIBLES[int(opcion) - 1]
        while True:
            titulo = input("Título: ")
            try:
                encuesta = self.plataforma.crear_desde_formato(
                    formato, titulo, privacidad=PRIVACIDAD_ELIGE
                )
                break
            except ValueError as error:
                print("  Error: {}".format(error))
        print("[Abstract Factory] Formato {} creó la encuesta '{}' con {} pregunta(s) base y su reporte.".format(
            formato.nombre, encuesta.titulo, len(encuesta.preguntas)))

    def agregar_preguntas(self):
        encuesta = self.elegir_encuesta(ESTADO_BORRADOR)
        if encuesta is None:
            return
        while True:
            print("\nTipo de pregunta (Enter para terminar):")
            for clave, (nombre, _, _) in self.tipos_de_pregunta.items():
                print("  {}. {}".format(clave, nombre))
            clave = input("Elige: ").strip()
            if not clave:
                return
            if clave not in self.tipos_de_pregunta:
                print("  Opción no válida.")
                continue
            nombre, creador, lleva_opciones = self.tipos_de_pregunta[clave]
            enunciado = input("Enunciado: ")
            opciones = None
            if lleva_opciones:
                opciones = input("Opciones separadas por coma (mínimo 2): ").split(",")
            try:
                pregunta = creador.crear_pregunta(enunciado, opciones)
                encuesta.agregar_pregunta(pregunta)
            except ValueError as error:
                print("  Error: {}".format(error))
                continue
            print("[Factory Method] {} creó una pregunta de tipo '{}'. La encuesta ya tiene {}.".format(
                type(creador).__name__, pregunta.tipo, len(encuesta.preguntas)))

    def duplicar_encuesta(self):
        original = self.elegir_encuesta()
        if original is None:
            return
        copia = self.plataforma.duplicar(original)
        print("[Prototype] Copia creada: '{}' | ID {} (original: {}) | Estado: {}".format(
            copia.titulo, copia.id, original.id, copia.estado))

    def publicar_encuesta(self):
        encuesta = self.elegir_encuesta(ESTADO_BORRADOR)
        if encuesta is None:
            return
        try:
            token = self.plataforma.publicar(encuesta)
        except ValueError as error:
            print("  Error: {}".format(error))
            return
        print("[Singleton] Encuesta publicada. Token de acceso (enlace) único: {}".format(token))

    def responder_encuesta(self):
        token = input("Token de la encuesta (el enlace que recibiste): ").strip()
        encuesta = self.plataforma.buscar_por_token(token)
        if encuesta is None or encuesta.estado != ESTADO_PUBLICADA:
            print("  No existe una encuesta publicada con ese token.")
            return

        print("\n{}\n{}".format(encuesta.titulo, encuesta.descripcion))
        valores = []
        for i, pregunta in enumerate(encuesta.preguntas, 1):
            print("\nP{}. {}".format(i, pregunta.describir()))
            if hasattr(pregunta, "opciones"):
                print("  (escribe el número de la opción; si son varias, sepáralas con coma)")
            while True:
                try:
                    valores.append(pregunta.validar_respuesta(input("Tu respuesta: ")))
                    break
                except ValueError as error:
                    print("  {}".format(error))

        nombre = None
        anonimo = False
        if encuesta.privacidad == PRIVACIDAD_NOMBRE:
            nombre = self.pedir_obligatorio("Tu nombre (obligatorio en esta encuesta): ")
        else:
            anonimo = input("¿Responder de forma anónima? (s/n): ").strip().lower().startswith("s")
            if not anonimo:
                nombre = self.pedir_obligatorio("Tu nombre: ")
        try:
            self.plataforma.responder(encuesta, valores, nombre, anonimo)
        except ValueError as error:
            print("  Error: {}".format(error))
            return
        print("Respuesta registrada. ¡Gracias por participar!")

    def analizar_resultados(self):
        encuesta = self.elegir_encuesta(ESTADO_PUBLICADA)
        if encuesta is None:
            return
        print()
        print(self.plataforma.analizar(encuesta))

    def ejecutar(self):
        while True:
            print("\nPLATAFORMA DE ENCUESTAS")
            for i, (nombre, _) in enumerate(self.opciones, 1):
                print("{}. {}".format(i, nombre))
            print("{}. Salir".format(len(self.opciones) + 1))
            try:
                opcion = input("Elige una opción: ").strip()
                if opcion == str(len(self.opciones) + 1):
                    break
                if opcion.isdigit() and 1 <= int(opcion) <= len(self.opciones):
                    print()
                    self.opciones[int(opcion) - 1][1]()
                else:
                    print("Opción no válida.")
            except (EOFError, KeyboardInterrupt):
                print()
                break
        print("¡Hasta luego!")


if __name__ == "__main__":
    plataforma = Plataforma()
    menu = MenuConsola(plataforma)
    menu.ejecutar()