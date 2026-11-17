import csv
import io
import json
from abc import ABC, abstractmethod

from modelos.reporte import ReporteGeneral


class ExportadorReporte(ABC):
    # Patron Adapter interfaz objetivo comun para exportar reportes a distintos formatos

    def __init__(self, reporte=None):
        self._reporte = reporte

    def _obtener_datos(self, encuesta, respuestas):
        reporte = self._reporte or encuesta.reporte or ReporteGeneral()
        return reporte.construir_datos(encuesta, respuestas)

    @abstractmethod
    def exportar(self, encuesta, respuestas):
        pass


class ExportadorCSV(ExportadorReporte):
    # Adaptador que convierte los datos del reporte a formato CSV

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
                media = "" if est["media"] is None else est["media"]
                mediana = "" if est["mediana"] is None else est["mediana"]
                escritor.writerow(base + ["Media", media, ""])
                escritor.writerow(base + ["Mediana", mediana, ""])
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
    # Adaptador que convierte los datos del reporte a formato JSON

    def exportar(self, encuesta, respuestas):
        datos = self._obtener_datos(encuesta, respuestas)
        return json.dumps(datos, indent=2, ensure_ascii=False)
