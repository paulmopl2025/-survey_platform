import csv
import io
import json
from abc import ABC, abstractmethod

from modelos.reporte import ReporteGeneral
from patrones.reporte_decorator import ReporteConFecha

class ExportadorReporte(ABC):
    # Se agrega el patron adapter para exportar reportes a distintos formatos

    def __init__(self, reporte=None):
        self._reporte = reporte

    def _obtener_datos(self, encuesta, respuestas):
        reporte = self._reporte or encuesta.reporte or ReporteGeneral()
        reporte = ReporteConFecha(reporte)
        return reporte.construir_datos(encuesta, respuestas)

    @abstractmethod
    def exportar(self, encuesta, respuestas):
        pass


class ExportadorCSV(ExportadorReporte):
    # Se agrega adaptador para exportar resultados en formato CSV

    def exportar(self, encuesta, respuestas):
        datos = self._obtener_datos(encuesta, respuestas)
        buffer = io.StringIO()
        escritor = csv.writer(buffer, lineterminator="\n")
        escritor.writerow([
            "encuesta",
            "total_participantes",
            "numero_pregunta",
            "pregunta",
            "tipo",
            "detalle",
            "valor",
            "porcentaje",
            "fecha_generacion",
        ])

        if datos["total_participantes"] == 0:
            escritor.writerow([
                datos["titulo"],
                0,
                "",
                "",
                "",
                "Sin respuestas",
                "",
                "",
                datos["fecha_generacion"],
            ])
            return buffer.getvalue().rstrip("\n")

        for pregunta in datos["preguntas"]:
            base = [
                datos["titulo"],
                datos["total_participantes"],
                pregunta["numero"],
                pregunta["enunciado"],
                pregunta["tipo"],
            ]
            if pregunta["analisis"] == "opciones":
                for item in pregunta["opciones"]:
                    escritor.writerow(base + [
                        item["opcion"],
                        item["cantidad"],
                        "{:.1f}%".format(item["porcentaje"]),
                    ])
            elif pregunta["analisis"] == "escala":
                est = pregunta["estadisticas"]
                escritor.writerow(base + ["Media", est["media"], ""])
                escritor.writerow(base + ["Mediana", est["mediana"], ""])
                escritor.writerow(base + [
                    "Moda",
                    ", ".join(str(m) for m in est["moda"]),
                    "",
                ])
            else:
                for respuesta_texto in pregunta["respuestas"]:
                    escritor.writerow(base + ["Respuesta", respuesta_texto, ""])

        return buffer.getvalue().rstrip("\n")


class ExportadorJSON(ExportadorReporte):
    # Se agrega adaptador para exportar resultados en formato JSON

    def exportar(self, encuesta, respuestas):
        datos = self._obtener_datos(encuesta, respuestas)
        return json.dumps(datos, indent=2, ensure_ascii=False)
