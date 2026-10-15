class TituloRequeridoError(ValueError):
    """Se lanza cuando se intenta crear una encuesta sin título."""

    def __init__(self) -> None:
        super().__init__("El título es obligatorio")


class EnunciadoRequeridoError(ValueError):
    """Se lanza cuando se intenta agregar una pregunta sin enunciado."""

    def __init__(self) -> None:
        super().__init__("El enunciado es obligatorio")
