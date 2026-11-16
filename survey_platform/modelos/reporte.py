import statistics
from abc import ABC, abstractmethod
from collections import Counter

from modelos.pregunta import PreguntaConOpciones, PreguntaEscala


class ReporteAnalitico(ABC):
    # Clase base para generar el análisis de resultados de una encuesta (RF-07)

    titulo = "Reporte"

    def generar(self, encuesta, respuestas):
        total = len(respuestas)
        lineas = [
            "Reporte: {} ({})".format(encuesta.titulo, self.titulo),
            "Total de participantes: {}".format(total),
        ]
        if total == 0:
            lineas.append("Aún no hay respuestas para analizar.")
            return "\n".join(lineas)

        for i, pregunta in enumerate(encuesta.preguntas):
            valores = [r.valores[i] for r in respuestas]
            lineas.append("")
            lineas.append("P{}. {} [{}]".format(i + 1, pregunta.enunciado, pregunta.tipo))
            lineas.extend(self._analizar_pregunta(pregunta, valores, total))
        return "\n".join(lineas)

    def construir_datos(self, encuesta, respuestas):
        # Se agrega esta funcion para exponer los datos del reporte al adaptador
        total = len(respuestas)
        datos = {
            "encuesta_id": encuesta.id,
            "titulo": encuesta.titulo,
            "reporte": self.titulo,
            "total_participantes": total,
            "preguntas": [],
        }
        if total == 0:
            return datos

        for i, pregunta in enumerate(encuesta.preguntas):
            valores = [r.valores[i] for r in respuestas]
            entrada = {
                "numero": i + 1,
                "enunciado": pregunta.enunciado,
                "tipo": pregunta.tipo,
            }
            if isinstance(pregunta, PreguntaConOpciones):
                entrada["analisis"] = "opciones"
                entrada["opciones"] = [
                    {
                        "opcion": opcion,
                        "cantidad": cantidad,
                        "porcentaje": round(cantidad * 100.0 / total, 1),
                    }
                    for opcion, cantidad in self._contar_opciones(pregunta, valores)
                ]
            elif isinstance(pregunta, PreguntaEscala):
                entrada["analisis"] = "escala"
                entrada["estadisticas"] = self._resumen_estadistico(valores)
            else:
                entrada["analisis"] = "texto"
                entrada["respuestas"] = list(valores)
            datos["preguntas"].append(entrada)
        return datos

    def _contar_opciones(self, pregunta, valores):
        # Se agrega esta funcion para reutilizar el conteo de opciones
        elegidas = []
        for v in valores:
            elegidas.extend(v if isinstance(v, list) else [v])
        conteo = Counter(elegidas)
        return [(o, conteo.get(o, 0)) for o in pregunta.opciones]

    def _analizar_pregunta(self, pregunta, valores, total):
        if isinstance(pregunta, PreguntaConOpciones):
            return self._generar_barras(self._contar_opciones(pregunta, valores), total)
        if isinstance(pregunta, PreguntaEscala):
            return self._analizar_escala(valores, total)
        return ["  * {}".format(v) for v in valores]

    def _generar_barras(self, conteos, total):
        ancho = max(len(etiqueta) for etiqueta, _ in conteos)
        lineas = []
        for etiqueta, cantidad in conteos:
            porcentaje = cantidad * 100.0 / total
            barra = "#" * int(round(porcentaje / 5))
            lineas.append("  {:<{w}} | {:<20} {} ({:.1f}%)".format(
                etiqueta, barra, cantidad, porcentaje, w=ancho))
        return lineas

    def _resumen_estadistico(self, valores):
        # Se agrega esta funcion para reutilizar los calculos estadisticos
        media = statistics.mean(valores)
        mediana = statistics.median(valores)
        conteo = Counter(valores)
        mayor = max(conteo.values())
        moda = sorted(v for v, c in conteo.items() if c == mayor)
        return {
            "media": round(media, 2),
            "mediana": mediana,
            "moda": moda,
        }

    def _calcular_estadisticas(self, valores):
        resumen = self._resumen_estadistico(valores)
        return [
            "  Media:   {:g}".format(resumen["media"]),
            "  Mediana: {:g}".format(resumen["mediana"]),
            "  Moda:    {}".format(", ".join(str(m) for m in resumen["moda"])),
        ]

    def _distribucion_escala(self, valores, total):
        conteo = Counter(valores)
        conteos = [(str(n), conteo.get(n, 0)) for n in range(PreguntaEscala.MINIMO, PreguntaEscala.MAXIMO + 1)]
        return self._generar_barras(conteos, total)

    @abstractmethod
    def _analizar_escala(self, valores, total):
        pass


class ReporteGeneral(ReporteAnalitico):
    # Reporte estándar que adapta el cálculo según el tipo de pregunta

    titulo = "Reporte de resultados"

    def _analizar_escala(self, valores, total):
        return self._calcular_estadisticas(valores)
