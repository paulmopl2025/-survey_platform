# Plataforma de Encuestas con Análisis de Resultados

Sistema en Python desarrollado bajo el enfoque de Programación Orientada a Objetos y Patrones de Diseño Creacionales.

## 🚀 Requerimientos Funcionales y Patrones de Diseño

| Requerimiento | Descripción | Patrón Aplicado |
|---|---|---|
| **RF-01** | Crear encuestas con título obligatorio y descripción. | **Builder** |
| **RF-02** | Agregar preguntas de selección única y respuesta abierta. | **Factory Method** |
| **RF-03** | Configurar mínimo 2 opciones para preguntas de selección. | **Factory Method** |
| **RF-04** | Duplicar encuestas existentes con sus preguntas sin modificar la original. | **Prototype** |
| **RF-05** | Construir la encuesta paso a paso antes de su publicación. | **Builder** |
| **RF-06** | Registrar respuestas de participantes y generar token único. | **Singleton** (Generador de Tokens) |
| **RF-07** | Calcular y mostrar estadísticas de respuestas y totales. | **Template Method** |
| **RF-08** | Validar que la encuesta no se publique sin título o sin preguntas. | Validación en Servicio |

---

## 🛠️ Estructura del Proyecto

```text
-survey_platform/
│── modelos/          # Entidades base (Encuesta, Pregunta, Reporte)
│── patrones/         # Patrones Creacionales (Builder, Factory, Prototype, Singleton)
│── servicios/        # Lógica de plataforma y gestión de estado
└── main.py           # Menú interactivo en consola
