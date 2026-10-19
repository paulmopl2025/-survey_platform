import uuid


class GeneradorTokenSingleton:
    """Patrón Singleton (RF-06): garantiza una única instancia para generador de tokens."""

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.tokens_generados = set()
        return cls._instancia

    def generar_token(self):
        """Genera un token único de 8 caracteres y valida que no esté repetido."""
        while True:
            token = uuid.uuid4().hex[:8]
            if token not in self.tokens_generados:
                self.tokens_generados.add(token)
                return token