
from datetime import datetime


class ReporteDecorator:
    def __init__(self, reporte):
        self._reporte = reporte

    def generar(self, encuesta, respuestas):
        return self._reporte.generar(encuesta, respuestas)

    def construir_datos(self, encuesta, respuestas):
        return self._reporte.construir_datos(encuesta, respuestas)


class ReporteConFecha(ReporteDecorator):

    def generar(self, encuesta, respuestas):
        reporte = self._reporte.generar(encuesta, respuestas)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return "{}\nFecha de generacion: {}".format(reporte, fecha)

    def construir_datos(self, encuesta, respuestas):
        datos = self._reporte.construir_datos(
            encuesta, respuestas
        ).copy()

        datos["fecha_generacion"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return datos
