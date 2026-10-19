import sys
from modelos.encuesta import ESTADO_BORRADOR, ESTADO_PUBLICADA
from modelos.reporte import ReporteEstandar
from patrones.encuesta_builder import EncuestaBuilder
from patrones.pregunta_creator import CreadorSeleccionUnica, CreadorTextoLibre
from servicios.plataforma import PlataformaEncuestas


def mostrar_menu():
    print("\n" + "=" * 55)
    print("      PLATAFORMA DE ENCUESTAS - MENÚ PRINCIPAL")
    print("=" * 55)
    print("1. Crear nueva encuesta (RF-01 / RF-05: Builder)")
    print("2. Agregar pregunta a encuesta borrador (RF-02 / RF-03: Factory)")
    print("3. Validar y Publicar encuesta (RF-08 / RF-06: Token)")
    print("4. Duplicar encuesta existente (RF-04: Prototype)")
    print("5. Responder encuesta (RF-06)")
    print("6. Ver reporte de resultados (RF-07: Analizador)")
    print("7. Listar todas las encuestas")
    print("0. Salir")
    print("=" * 55)


def main():
    plataforma = PlataformaEncuestas()
    builder = EncuestaBuilder()
    reporte_analitico = ReporteEstandar()

    creador_su = CreadorSeleccionUnica()
    creador_texto = CreadorTextoLibre()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        # ----------------------------------------------------
        # 1. CREAR NUEVA ENCUESTA (RF-01, RF-05)
        # ----------------------------------------------------
        if opcion == "1":
            print("\n--- NUEVA ENCUESTA (Builder) ---")
            titulo = input("Ingrese el título de la encuesta (obligatorio): ").strip()
            if not titulo:
                print("❌ ERROR (RF-01/RF-08): El título es obligatorio.")
                continue

            descripcion = input("Ingrese la descripción de la encuesta: ").strip()

            try:
                encuesta = (
                    builder.set_titulo(titulo)
                    .set_descripcion(descripcion)
                    .build()
                )
                plataforma.registrar_encuesta(encuesta)
                print(f"✅ Encuesta '{encuesta.titulo}' creada en Borrador (ID: {encuesta.id}).")
            except Exception as e:
                print(f"❌ Error al crear encuesta: {e}")

        # ----------------------------------------------------
        # 2. AGREGAR PREGUNTA (RF-02, RF-03)
        # ----------------------------------------------------
        elif opcion == "2":
            borradores = [e for e in plataforma.encuestas.values() if e.estado == ESTADO_BORRADOR]
            if not borradores:
                print("⚠️ No hay encuestas en estado 'Borrador' para agregar preguntas.")
                continue

            print("\nEncuestas en Borrador disponibles:")
            for idx, enc in enumerate(borradores, 1):
                print(f"  {idx}. [{enc.id}] {enc.titulo} ({len(enc.preguntas)} preguntas)")

            try:
                sel = int(input("Seleccione el número de encuesta: ")) - 1
                enc_seleccionada = borradores[sel]
            except (ValueError, IndexError):
                print("❌ Selección inválida.")
                continue

            print("\nTipos de pregunta:")
            print("  1. Selección Única")
            print("  2. Respuesta Abierta (Texto Libre)")
            tipo_p = input("Elija el tipo de pregunta (1 o 2): ").strip()

            enunciado = input("Ingrese el enunciado de la pregunta: ").strip()
            if not enunciado:
                print("❌ ERROR (RF-02): El enunciado de la pregunta no puede estar vacío.")
                continue

            try:
                if tipo_p == "1":
                    print("Ingrese las opciones de respuesta separadas por coma (mínimo 2):")
                    raw_opciones = input("Opciones (ej. Opción A, Opción B): ").split(",")
                    opciones = [o.strip() for o in raw_opciones if o.strip()]

                    if len(opciones) < 2:
                        print("❌ ERROR (RF-03): Se requieren al menos 2 opciones de respuesta.")
                        continue

                    pregunta = creador_su.crear_pregunta(enunciado, opciones)
                elif tipo_p == "2":
                    pregunta = creador_texto.crear_pregunta(enunciado)
                else:
                    print("❌ Tipo de pregunta no válido.")
                    continue

                enc_seleccionada.agregar_pregunta(pregunta)
                print(f"✅ Pregunta agregada exitosamente a '{enc_seleccionada.titulo}'.")

            except Exception as e:
                print(f"❌ Error al agregar pregunta: {e}")

        # ----------------------------------------------------
        # 3. PUBLICAR ENCUESTA (RF-08)
        # ----------------------------------------------------
        elif opcion == "3":
            borradores = [e for e in plataforma.encuestas.values() if e.estado == ESTADO_BORRADOR]
            if not borradores:
                print("⚠️ No hay encuestas en Borrador listas para publicar.")
                continue

            print("\nEncuestas en Borrador:")
            for idx, enc in enumerate(borradores, 1):
                print(f"  {idx}. [{enc.id}] {enc.titulo} ({len(enc.preguntas)} preguntas)")

            try:
                sel = int(input("Seleccione la encuesta a publicar: ")) - 1
                enc_sel = borradores[sel]

                # Validación RF-08
                token = plataforma.publicar_encuesta(enc_sel.id)
                print(f"✅ Encuesta '{enc_sel.titulo}' publicada con éxito.")
                print(f"🔑 Token único asignado (Singleton): {token}")
            except ValueError as ve:
                print(f"❌ ERROR DE VALIDACIÓN (RF-08): {ve}")
            except (IndexError, TypeError):
                print("❌ Selección inválida.")

        # ----------------------------------------------------
        # 4. DUPLICAR ENCUESTA (RF-04: Prototype)
        # ----------------------------------------------------
        elif opcion == "4":
            if not plataforma.encuestas:
                print("⚠️ No hay encuestas registradas para duplicar.")
                continue

            print("\nEncuestas existentes:")
            lista_enc = list(plataforma.encuestas.values())
            for idx, enc in enumerate(lista_enc, 1):
                print(f"  {idx}. [{enc.id}] {enc.titulo} ({enc.estado})")

            try:
                sel = int(input("Seleccione el número de encuesta a duplicar: ")) - 1
                enc_origen = lista_enc[sel]

                enc_copia = enc_origen.clone()
                plataforma.registrar_encuesta(enc_copia)
                print(f"✅ Encuesta duplicada con éxito (Prototype).")
                print(f"   Nueva Encuesta ID: {enc_copia.id} | Título: '{enc_copia.titulo}'")
            except (ValueError, IndexError):
                print("❌ Selección inválida.")

        # ----------------------------------------------------
        # 5. RESPONDER ENCUESTA (RF-06)
        # ----------------------------------------------------
        elif opcion == "5":
            publicadas = [e for e in plataforma.encuestas.values() if e.estado == ESTADO_PUBLICADA]
            if not publicadas:
                print("⚠️ No hay encuestas publicadas disponibles para responder.")
                continue

            print("\nEncuestas Publicadas:")
            for idx, enc in enumerate(publicadas, 1):
                print(f"  {idx}. [{enc.id}] {enc.titulo}")

            try:
                sel = int(input("Seleccione la encuesta a responder: ")) - 1
                enc_sel = publicadas[sel]
            except (ValueError, IndexError):
                print("❌ Selección inválida.")
                continue

            print(f"\n--- RESPONDIENDO: {enc_sel.titulo} ---")
            respuestas_usuario = []

            for i, preg in enumerate(enc_sel.preguntas, 1):
                print(f"\nPregunta {i}: {preg.enunciado}")
                if hasattr(preg, "opciones"):
                    for op_idx, op in enumerate(preg.opciones, 1):
                        print(f"  {op_idx}. {op}")
                    
                    while True:
                        try:
                            o_sel = int(input("Elija el número de opción: ")) - 1
                            if 0 <= o_sel < len(preg.opciones):
                                respuestas_usuario.append(preg.opciones[o_sel])
                                break
                            print("❌ Opción fuera de rango.")
                        except ValueError:
                            print("❌ Ingrese un número válido.")
                else:
                    ans = input("Respuesta: ").strip()
                    respuestas_usuario.append(ans)

            plataforma.guardar_respuesta(enc_sel.id, respuestas_usuario)
            print("✅ ¡Muchas gracias! Sus respuestas han sido registradas exitosamente (RF-06).")

        # ----------------------------------------------------
        # 6. VER ANALISIS / REPORTES (RF-07)
        # ----------------------------------------------------
        elif opcion == "6":
            if not plataforma.encuestas:
                print("⚠️ No hay encuestas creadas en el sistema.")
                continue

            print("\nEncuestas disponibles:")
            lista_enc = list(plataforma.encuestas.values())
            for idx, enc in enumerate(lista_enc, 1):
                num_resp = len(plataforma.respuestas.get(enc.id, []))
                print(f"  {idx}. [{enc.id}] {enc.titulo} - Respuestas recibidas: {num_resp}")

            try:
                sel = int(input("Seleccione la encuesta para ver el análisis: ")) - 1
                enc_sel = lista_enc[sel]

                resps = plataforma.respuestas.get(enc_sel.id, [])
                reporte_resultado = reporte_analitico.generar(enc_sel, resps)
                print("\n" + reporte_resultado)
            except (ValueError, IndexError):
                print("❌ Selección inválida.")

        # ----------------------------------------------------
        # 7. LISTAR ENCUESTAS
        # ----------------------------------------------------
        elif opcion == "7":
            if not plataforma.encuestas:
                print("⚠️ No hay encuestas registradas en el sistema.")
                continue

            print("\n--- LISTADO GENERAL DE ENCUESTAS ---")
            for enc in plataforma.encuestas.values():
                num_p = len(enc.preguntas)
                num_r = len(plataforma.respuestas.get(enc.id, []))
                print(f"• ID: {enc.id} | Título: '{enc.titulo}' | Estado: {enc.estado} | Preguntas: {num_p} | Respuestas: {num_r}")

        # ----------------------------------------------------
        # 0. SALIR
        # ----------------------------------------------------
        elif opcion == "0":
            print("\n¡Gracias por utilizar la Plataforma de Encuestas! Hasta luego.")
            sys.exit(0)

        else:
            print("❌ Opción inválida. Elija un número entre 0 y 7.")


if __name__ == "__main__":
    main()