from tkinter import messagebox

def show_error(msg: str, exc: Exception = None) -> None:
    """Muestra mensaje de error gráfico en Tkinter"""
    detail = f"\n\nDetalle: {exc}" if exc else ""
    messagebox.showerror("Error", msg + detail)
