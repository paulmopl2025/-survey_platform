Survey Platform - Plataforma de encuestas con análisis de resultados

Una plataforma interactiva en Python diseñada para la creación, gestión, publicación y análisis de encuestas. El proyecto aplica principios sólidos de Programación Orientada a Objetos (POO) y varios Patrones de Diseño de Software para garantizar una arquitectura extensible, mantenible y desacoplada.

🛠️ Arquitectura y Patrones de Diseño

El sistema está estructurado modularmente para resolver problemas comunes en el ciclo de vida de una encuesta:

- **Builder (`patrones/encuesta_builder.py`):** Permite la construcción paso a paso de la encuesta (título, descripción y privacidad), dejándola en estado Borrador. Las preguntas se agregan después, creadas con el Factory Method.
- **Factory Method (`patrones/pregunta_creator.py`):** Delega la creación de los distintos tipos de preguntas (selección única, opción múltiple, texto libre y escala 1–5) a creadores específicos, facilitando la incorporación de nuevos tipos en el futuro.
- **Prototype (`modelos/encuesta.py`):** Implementa la clonación profunda (*deep copy*) de encuestas existentes con todas sus preguntas y opciones asociadas, garantizando copias totalmente independientes de la original.
- **Singleton (`patrones/token_generator.py`):** Centraliza la generación de tokens únicos para las encuestas publicadas, asegurando una única instancia global para evitar duplicados en los enlaces.
- **Composite (`patrones/seccion_composite.py`):** Organiza la encuesta como una estructura de árbol (`Encuesta -> Sección -> Subsección / Pregunta`) mediante la interfaz común `ElementoEncuesta`, permitiendo agrupar preguntas en secciones temáticas que responden de forma uniforme a mostrar, contar y validar.
- **Decorator (`patrones/pregunta_decorator.py`):** Permite envolver cualquier `Pregunta` con comportamientos combinables en tiempo de ejecución (`Obligatoria`, `ConAyuda` y `ConValidacion`) sin crear múltiples subclases por combinación, habilitando también preguntas opcionales.
- **Proxy (`patrones/encuesta_proxy.py`):** `EncuestaProxy` es un proxy de protección que se interpone entre el menú y la encuesta real. Solo deja pasar al creador de la encuesta para modificarla (agregar secciones o preguntas), publicarla y analizar o exportar sus resultados; a cualquier otro usuario le niega el acceso. Desde el menú se puede usar la opción "Cambiar usuario" para probarlo.
- **Adapter (`patrones/exportador_adapter.py`):** Adapta el reporte de resultados a formatos externos (CSV y JSON) mediante `ExportadorCSV` y `ExportadorJSON`, sin modificar el cálculo del reporte.

### 📁 Estructura del proyecto

- `modelos/`: Clases de dominio de la plataforma (`encuesta`, `pregunta`, `respuesta`, `reporte`).
- `patrones/`: Implementaciones desacopladas de los patrones de diseño (creacionales y estructurales).
- `servicios/`: Lógica del sistema y control de la consola (`plataforma.py`).
- `main.py`: Punto de entrada interactivo para ejecutar la aplicación.

### ▶️ Cómo ejecutar

Requiere Python 3.8 o superior y no tiene dependencias externas.

```bash
git clone https://github.com/paulmopl2025/-survey_platform
cd ./-survey_platform
python survey_platform/main.py
```

Esto abre el menú interactivo en consola (crear, organizar en secciones, configurar preguntas, duplicar, publicar, responder, analizar, exportar encuestas a CSV/JSON y cambiar de usuario).
