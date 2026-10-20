Survey Platform - Plataforma de encuestas con análisis de resultados

Una plataforma interactiva en Python diseñada para la creación, gestión, publicación y análisis de encuestas. El proyecto aplica principios sólidos de Programación Orientada a Objetos (POO) y varios Patrones de Diseño de Software para garantizar una arquitectura extensible, mantenible y desacoplada.

🛠️ Arquitectura y Patrones de Diseño

El sistema está estructurado modularmente para resolver problemas comunes en el ciclo de vida de una encuesta:

- **Builder (`patrones/encuesta_builder.py`):** Permite la construcción paso a paso de la encuesta (título, descripción y privacidad), dejándola en estado Borrador. Las preguntas se agregan después, creadas con el Factory Method.
- **Factory Method (`patrones/pregunta_creator.py`):** Delega la creación de los distintos tipos de preguntas (selección única, opción múltiple, texto libre y escala 1–5) a creadores específicos, facilitando la incorporación de nuevos tipos en el futuro.
- **Prototype (`modelos/encuesta.py`):** Implementa la clonación profunda (*deep copy*) de encuestas existentes con todas sus preguntas y opciones asociadas, garantizando copias totalmente independientes de la original.
- **Singleton (`patrones/token_generator.py`):** Centraliza la generación de tokens únicos para las encuestas publicadas, asegurando una única instancia global para evitar duplicados en los enlaces.

### 📁 Estructura del proyecto

- `modelos/`: Clases de dominio de la plataforma (`encuesta`, `pregunta`, `respuesta`, `reporte`).
- `patrones/`: Implementaciones desacopladas de los patrones creacionales.
- `servicios/`: Lógica del sistema y control de la consola (`plataforma.py`).
- `main.py`: Punto de entrada interactivo para ejecutar la aplicación.

### ▶️ Cómo ejecutar

Requiere Python 3.8 o superior y no tiene dependencias externas.

```bash
git clone https://github.com/paulmopl2025/-survey_platform
cd -survey_platform
python survey_platform/main.py
```

Esto abre el menú interactivo en consola (crear, duplicar, publicar, responder y analizar encuestas).
