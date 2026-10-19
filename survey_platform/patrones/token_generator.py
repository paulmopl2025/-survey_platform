import uuid


class TokenGenerator:
    # Patrón Singleton (RF-06): garantiza una única instancia para emitir tokens sin repetición

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._emitidos = set()
        return cls._instancia

    def generar_token(self):
        token = uuid.uuid4().hex[:8]
        while token in self._emitidos:
            token = uuid.uuid4().hex[:8]
        self._emitidos.add(token)
        return token