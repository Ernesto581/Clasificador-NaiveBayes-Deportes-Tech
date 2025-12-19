import tkinter as tk
from tkinter import ttk


class MetricsTable:
    def __init__(self, parent, report):
        self.tree = ttk.Treeview(
            parent,
            columns=("precision", "recall", "f1"),
            show="headings"
        )

        self.tree.heading("precision", text="Precisión")
        self.tree.heading("recall", text="Recall")
        self.tree.heading("f1", text="F1-score")

        for label, values in report.items():
            if label in ["accuracy", "macro avg", "weighted avg"]:
                continue
            self.tree.insert(
                "",
                tk.END,
                values=(
                    round(values["precision"], 2),
                    round(values["recall"], 2),
                    round(values["f1-score"], 2)
                ),
                text=label
            )

        self.tree.pack()
