import statistics
from abc import ABC, abstractmethod
from collections import Counter


class ReporteAnalitico(ABC):
    """Patrón Template Method (RF-08): plantilla para generar reportes analíticos."""

    def generar(self, encuesta, respuestas):
        lineas = [
            "=" * 50,
            f"REPORTE ANALÍTICO: {encuesta.titulo.upper()}",
            f"ID Encuesta: {encuesta.id}",
            f"Total de respuestas recibidas: {len(respuestas)}",
            "=" * 50,
        ]

        if not respuestas:
            lineas.append("\nNo hay respuestas registradas para esta encuesta.")
            return "\n".join(lineas)

        for i, pregunta in enumerate(encuesta.preguntas):
            valores_pregunta = [r[i] for r in respuestas if i < len(r)]
            lineas.append(f"\nPregunta {i+1}: {pregunta.enunciado} [{pregunta.tipo}]")
            lineas.extend(self._analizar_pregunta(pregunta, valores_pregunta))

        return "\n".join(lineas)

    def _analizar_pregunta(self, pregunta, valores):
        if not valores:
            return ["  Sin datos registrados."]

        # Preguntas de Selección (Única / Múltiple)
        if hasattr(pregunta, "opciones"):
            # Aplanar si vienen listas dentro de listas (Opción múltiple)
            flat_vals = []
            for v in valores:
                if isinstance(v, list):
                    flat_vals.extend(v)
                else:
                    flat_vals.append(v)

            conteo = Counter(flat_vals)
            total = len(valores)
            resultado = []
            for opcion in pregunta.opciones:
                cant = conteo.get(opcion, 0)
                porcentaje = (cant / total) * 100 if total > 0 else 0
                resultado.append(f"  - {opcion}: {cant} votos ({porcentaje:.1f}%)")
            return resultado

        # Preguntas de Escala
        elif pregunta.tipo.startswith("Escala"):
            nums = [v for v in valores if isinstance(v, (int, float))]
            if not nums:
                return ["  No hay respuestas numéricas válidas."]
            
            promedio = statistics.mean(nums)
            mediana = statistics.median(nums)
            try:
                moda = statistics.mode(nums)
            except statistics.StatisticsError:
                moda = "N/A (Empate u homogéneo)"

            return [
                f"  - Promedio: {promedio:.2f}",
                f"  - Mediana: {mediana}",
                f"  - Moda: {moda}",
            ]

        # Preguntas de Texto libre
        return [f"  - \"{v}\"" for v in valores]


class ReporteEstandar(ReporteAnalitico):
    """Implementación concreta del reporte estándar."""
    pass