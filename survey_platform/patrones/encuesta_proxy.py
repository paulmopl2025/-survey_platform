from abc import ABC, abstractmethod


class GestionEncuesta(ABC):
    # Patrón Proxy: interfaz común (Sujeto) para las operaciones protegidas de una encuesta

    @abstractmethod
    def agregar_seccion(self, seccion, padre=None):
        pass

    @abstractmethod
    def agregar_pregunta(self, pregunta, seccion=None):
        pass

    @abstractmethod
    def publicar(self):
        pass

    @abstractmethod
    def analizar(self):
        pass

    @abstractmethod
    def exportar_reporte(self, exportador):
        pass


class EncuestaReal(GestionEncuesta):
    # Sujeto real: ejecuta las operaciones sobre la encuesta sin ninguna restricción

    def __init__(self, encuesta, plataforma):
        self._encuesta = encuesta
        self._plataforma = plataforma

    def agregar_seccion(self, seccion, padre=None):
        self._encuesta.agregar_seccion(seccion, padre)

    def agregar_pregunta(self, pregunta, seccion=None):
        self._encuesta.agregar_pregunta(pregunta, seccion)

    def publicar(self):
        return self._plataforma.publicar(self._encuesta)

    def analizar(self):
        return self._plataforma.analizar(self._encuesta)

    def exportar_reporte(self, exportador):
        return self._plataforma.exportar_reporte(self._encuesta, exportador)


class EncuestaProxy(GestionEncuesta):
    # Patrón Proxy de protección: controla el acceso a la encuesta real.
    # Solo el creador puede modificarla, publicarla y analizar o exportar sus resultados.

    def __init__(self, encuesta, plataforma, usuario):
        self._encuesta = encuesta
        self._usuario = (usuario or "").strip()
        self._real = EncuestaReal(encuesta, plataforma)

    @property
    def usuario(self):
        return self._usuario

    def tiene_acceso(self):
        return bool(self._usuario) and self._usuario == self._encuesta.creador

    def verificar_acceso(self, accion):
        if not self.tiene_acceso():
            raise PermissionError(
                "'{}' no puede {} la encuesta '{}': solo su creador ('{}') tiene permiso.".format(
                    self._usuario, accion, self._encuesta.titulo, self._encuesta.creador))

    def agregar_seccion(self, seccion, padre=None):
        # Protege la creacion de secciones verificando que sea el creador
        self.verificar_acceso("modificar")
        self._real.agregar_seccion(seccion, padre)

    def agregar_pregunta(self, pregunta, seccion=None):
        self.verificar_acceso("modificar")
        self._real.agregar_pregunta(pregunta, seccion)

    def publicar(self):
        self.verificar_acceso("publicar")
        return self._real.publicar()

    def analizar(self):
        self.verificar_acceso("analizar los resultados de")
        return self._real.analizar()

    def exportar_reporte(self, exportador):
        self.verificar_acceso("exportar los resultados de")
        return self._real.exportar_reporte(exportador)
