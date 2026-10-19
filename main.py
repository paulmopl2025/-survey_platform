from modelos.encuesta import Encuesta
from modelos.pregunta import PreguntaSeleccionUnica, PreguntaTextoLibre
from patrones.encuesta_builder import EncuestaBuilder
from patrones.pregunta_creator import CreadorSeleccionUnica, CreadorTextoLibre
from servicios.plataforma import PlataformaEncuestas


def main():
    plataforma = PlataformaEncuestas()
    builder = EncuestaBuilder()

    print("=" * 60)
    print("   SISTEMA DE PLATAFORMA DE ENCUESTAS (RF-01 a RF-08)")
    print("=" * 60)

    # 1. RF-01 / RF-05: Crear y construir encuesta progresivamente (Builder)
    encuesta_original = (
        builder.set_titulo("Encuesta de Evaluación Académica")
        .set_descripcion("Evaluación del curso de Programación Orientada a Objetos")
        .build()
    )

    # 2. RF-02 / RF-03: Crear preguntas y configurar opciones (Factory Method)
    creador_su = CreadorSeleccionUnica()
    creador_texto = CreadorTextoLibre()

    p1 = creador_su.crear_pregunta(
        "¿Cómo califica el contenido de la asignatura?",
        ["Excelente", "Aceptable", "Insuficiente"]
    )
    p2 = creador_texto.crear_pregunta("¿Qué temas sugiere incluir para el próximo semestre?")

    encuesta_original.agregar_pregunta(p1)
    encuesta_original.agregar_pregunta(p2)

    plataforma.registrar_encuesta(encuesta_original)

    # 3. RF-08: Validar y publicar encuesta
    token = plataforma.publicar_encuesta(encuesta_original.id)
    print(f"\nEncuesta '{encuesta_original.titulo}' creada y validada correctamente.")
    print(f"Token de acceso generado: {token}")

    # 4. RF-04: Duplicar encuesta (Prototype)
    encuesta_copia = encuesta_original.clone()
    plataforma.registrar_encuesta(encuesta_copia)
    print(f"\nEncuesta duplicada (Prototype): '{encuesta_copia.titulo}' (ID: {encuesta_copia.id})")

    # 5. RF-06: Registrar respuestas de participantes
    plataforma.guardar_respuesta(encuesta_original.id, ["Excelente", "Incluir más patrones de diseño."])
    plataforma.guardar_respuesta(encuesta_original.id, ["Excelente", "Más ejercicios prácticos."])
    plataforma.guardar_respuesta(encuesta_original.id, ["Aceptable", "Profundizar en Python avanzado."])

    # 6. RF-07: Analizar resultados
    from modelos.reporte import ReporteEstandar
    reporte = ReporteEstandar()
    analisis = reporte.generar(encuesta_original, plataforma.respuestas[encuesta_original.id])

    print("\n" + analisis)


if __name__ == "__main__":
    main()