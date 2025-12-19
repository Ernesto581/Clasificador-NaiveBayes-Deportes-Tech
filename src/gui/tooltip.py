import tkinter as tk

class ToolTip:
    """Muestra tooltip al pasar el mouse sobre un widget"""
    def __init__(self, widget, text):
        self.tip = None
        widget.bind("<Enter>", lambda e: self.show(text, widget))
        widget.bind("<Leave>", lambda e: self.hide())

    def show(self, text, widget):
        self.tip = tk.Toplevel(widget)
        self.tip.overrideredirect(True)
        tk.Label(self.tip, text=text, bg="#ffffe0").pack()
        x = widget.winfo_rootx()
        y = widget.winfo_rooty() + 25
        self.tip.geometry(f"+{x}+{y}")

    def hide(self):
        if self.tip:
            self.tip.destroy()
            self.tip = None
