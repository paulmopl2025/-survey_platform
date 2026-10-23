from abc import ABC, abstractmethod


# ==========================================
# 1. PRODUCTOS ABSTRACTOS (Interfaces)
# ==========================================
class Boton(ABC):
    @abstractmethod
    def renderizar(self) -> None:
        pass


class TextBox(ABC):
    @abstractmethod
    def renderizar(self) -> None:
        pass


# ==========================================
# 2. PRODUCTOS CONCRETOS DE WINDOWS
# ==========================================
class BotonWindows(Boton):
    def renderizar(self) -> None:
        print("[Windows] Rendering a flat rectangular button with Fluent UI style.")


class TextBoxWindows(TextBox):
    def renderizar(self) -> None:
        print("[Windows] Rendering a square border text box with Windows font.")


# ==========================================
# 3. PRODUCTOS CONCRETOS DE MAC
# ==========================================
class BotonMac(Boton):
    def renderizar(self) -> None:
        print("[Mac] Rendering a rounded button with Aqua OS style.")


class TextBoxMac(TextBox):
    def renderizar(self) -> None:
        print("[Mac] Rendering a smooth rounded text box with SF Pro font.")


# ==========================================
# 4. FÁBRICA ABSTRACTA (Abstract Factory)
# ==========================================
class GUIFactory(ABC):
    @abstractmethod
    def crear_boton(self) -> Boton:
        pass

    @abstractmethod
    def crear_textbox(self) -> TextBox:
        pass


# ==========================================
# 5. FÁBRICAS CONCRETAS
# ==========================================
class WindowsFactory(GUIFactory):
    def crear_boton(self) -> Boton:
        return BotonWindows()

    def crear_textbox(self) -> TextBox:
        return TextBoxWindows()


class MacFactory(GUIFactory):
    def crear_boton(self) -> Boton:
        return BotonMac()

    def crear_textbox(self) -> TextBox:
        return TextBoxMac()


# ==========================================
# 6. CÓDIGO CLIENTE Y DEMOSTRACIÓN
# ==========================================
class AplicacionUI:
    def __init__(self, factory: GUIFactory):
        self.boton = factory.crear_boton()
        self.textbox = factory.crear_textbox()

    def dibujar_interfaz(self):
        self.textbox.renderizar()
        self.boton.renderizar()


if __name__ == "__main__":
    import platform

    print("=== RETO OPCIONAL: ABSTRACT FACTORY PARA GUI MULTIPLATAFORMA ===\n")

    # Detección automática del sistema operativo o selección manual
    sistema_actual = platform.system()
    print(f"Sistema detectado en la máquina: {sistema_actual}\n")

    # 1. Probar componentes con la fábrica de Windows
    print("--- Generando interfaz para Windows ---")
    factory_win = WindowsFactory()
    app_win = AplicacionUI(factory_win)
    app_win.dibujar_interfaz()

    print("\n---------------------------------------\n")

    # 2. Probar componentes con la fábrica de Mac
    print("--- Generando interfaz para macOS ---")
    factory_mac = MacFactory()
    app_mac = AplicacionUI(factory_mac)
    app_mac.dibujar_interfaz()
