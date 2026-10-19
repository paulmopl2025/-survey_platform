from modelos.encuesta import ESTADO_BORRADOR, PRIVACIDAD_ELIGE, PRIVACIDAD_NOMBRE
from modelos.reporte import ReporteEstandar
from patrones.encuesta_builder import EncuestaBuilder
from patrones.pregunta_creator import (
    CreadorEscala,
    CreadorOpcionMultiple,
    CreadorSeleccionUnica,
    CreadorTextoLibre,
)
from servicios.plataforma import PlataformaEncuestas


def main():
    plataforma = PlataformaEncuestas()
    builder = EncuestaBuilder()

    print("=" * 50)
    print("   BIENVENIDO A PLATAFORMA DE ENCUESTAS")
    print("=" * 50)

    # --- DEMOSTRACIÓN DE FUNCIONALIDAD ---
    # 1. Crear una encuesta con el Builder (RF-01)
    encuesta1 = (
        builder.set_titulo("Encuesta de Satisfacción Laboral")
        .set_descripcion("Medición de clima organizacional 2026")
        .set_privacidad(PRIVACIDAD_ELIGE)
        .build()
    )

    # 2. Agregar preguntas usando los Creadores Factory Method (RF-02 y RF-03)
    creador_su = CreadorSeleccionUnica()
    creador_escala = CreadorEscala()
    creador_texto = CreadorTextoLibre()

    p1 = creador_su.crear_pregunta(
        "¿Cómo evalúas el ambiente de trabajo?", ["Excelente", "Bueno", "Regular", "Malo"]
    )
    p2 = creador_escala.crear_pregunta("¿Qué tan satisfecho estás con tus herramientas?")
    p3 = creador_texto.crear_pregunta("¿Qué sugerencia tienes para mejorar?")

    encuesta1.agregar_pregunta(p1)
    encuesta1.agregar_pregunta(p2)
    encuesta1.agregar_pregunta(p3)

    plataforma.registrar_encuesta(encuesta1)

    # 3. Publicar y generar Token Singleton (RF-06)
    token = plataforma.publicar_encuesta(encuesta1.id)
    print(f"\nEncuesta '{encuesta1.titulo}' creada y publicada exitosamente.")
    print(f"Token de acceso único: {token}")

    # 4. Probar clonación con Prototype (RF-04)
    encuesta_clonada = encuesta1.clone()
    plataforma.registrar_encuesta(encuesta_clonada)
    print(f"\nEncuesta clonada correctamente: '{encuesta_clonada.titulo}' (ID: {encuesta_clonada.id})")

    # 5. Simular respuestas
    plataforma.guardar_respuesta(encuesta1.id, ["Excelente", 5, "Todo marcha excelente."])
    plataforma.guardar_respuesta(encuesta1.id, ["Bueno", 4, "Más capacitación."])
    plataforma.guardar_respuesta(encuesta1.id, ["Excelente", 4, "Sillas ergonómicas."])

    # 6. Generar Reporte Analítico con Template Method (RF-08)
    reporte = ReporteEstandar()
    resultado_reporte = reporte.generar(encuesta1, plataforma.respuestas[encuesta1.id])

    print("\n" + resultado_reporte)


if __name__ == "__main__":
    main()