import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from modules.model import NaiveBayesClassifier
from modules.advanced_txt_generator import generate_txt
from modules.data_generator import generate_dataset
from modules.text_preprocessing import preprocess
from modules.evaluation import evaluate
from sklearn.model_selection import train_test_split
from gui.metrics_table import MetricsTable
from utils.errors import show_error
from utils.persistence import save_model_versioned, load_latest_model


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Clasificador Naive Bayes")
        self.root.geometry("950x820")

        self.classifier = NaiveBayesClassifier()

        # ================= TEXTO =================
        tk.Label(root, text="Texto a clasificar", font=("Arial", 12, "bold")).pack()
        self.text_input = tk.Text(root, height=5, width=90)
        self.text_input.pack(pady=5)

        # ================= BOTONES =================
        btns = tk.Frame(root)
        btns.pack(pady=5)

        tk.Button(btns, text="Entrenar con dataset interno", command=self.train_default)\
            .grid(row=0, column=0, padx=5)

        tk.Button(btns, text="Entrenar desde TXT", command=self.load_txt)\
            .grid(row=0, column=1, padx=5)

        tk.Button(btns, text="Clasificar texto", command=self.classify)\
            .grid(row=0, column=2, padx=5)

        tk.Button(btns, text="Guardar modelo", command=self.save_model)\
            .grid(row=0, column=3, padx=5)

        # ================= GENERADOR TXT =================
        gen_frame = tk.LabelFrame(root, text="Generar dataset TXT")
        gen_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(gen_frame, text="Cantidad de ejemplos:").grid(row=0, column=0)
        self.samples_var = tk.IntVar(value=500)
        tk.Entry(gen_frame, textvariable=self.samples_var, width=10)\
            .grid(row=0, column=1)

        tk.Label(gen_frame, text="Ratio Deportes (0-1):").grid(row=0, column=2)
        self.ratio_var = tk.DoubleVar(value=0.5)
        tk.Entry(gen_frame, textvariable=self.ratio_var, width=10)\
            .grid(row=0, column=3)

        tk.Button(gen_frame, text="Generar TXT", command=self.generate_txt_ui)\
            .grid(row=0, column=4, padx=10)

        # ================= PROGRESO =================
        self.progress = ttk.Progressbar(root, maximum=100, length=400)
        self.progress.pack(pady=5)

        # ================= RESULTADO =================
        self.result_label = tk.Label(
            root,
            text="",
            font=("Arial", 12),
            justify="left"
        )
        self.result_label.pack(pady=10)

        # ================= MÉTRICAS =================
        eval_box = tk.LabelFrame(root, text="Evaluación del modelo")
        eval_box.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(eval_box)
        scrollbar = ttk.Scrollbar(eval_box, orient="vertical", command=canvas.yview)
        self.eval_frame = tk.Frame(canvas)

        self.eval_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.eval_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_model()

    # ======================================================
    # ENTRENAR Y EVALUAR (COMÚN)
    # ======================================================
    def train_and_evaluate(self, X, y):
        for w in self.eval_frame.winfo_children():
            w.destroy()

        X = [preprocess(x) for x in X]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, stratify=y, random_state=42
        )

        self.progress["value"] = 30
        self.root.update()

        self.classifier.train(X_train, y_train)

        self.progress["value"] = 70
        self.root.update()

        report, _ = evaluate(
            self.classifier.get_model(),
            self.classifier.get_vectorizer(),
            X_test,
            y_test,
            parent_frame=self.eval_frame
        )

        MetricsTable(self.eval_frame, report)

        self.progress["value"] = 100

    # ======================================================
    def train_default(self):
        try:
            X, y = generate_dataset()
            self.train_and_evaluate(X, y)
            messagebox.showinfo("Entrenamiento", "Modelo entrenado con dataset interno")
        except Exception as e:
            show_error("Error al entrenar", e)

    # ======================================================
    def load_txt(self):
        try:
            path = filedialog.askopenfilename(filetypes=[("TXT", "*.txt")])
            if not path:
                return

            X, y = [], []
            with open(path, encoding="utf-8") as f:
                for line in f:
                    label, text = line.strip().split("|", 1)
                    X.append(text)
                    y.append(label)

            self.train_and_evaluate(X, y)
            messagebox.showinfo(
                "Entrenamiento",
                "Modelo entrenado y evaluado desde TXT"
            )

        except Exception as e:
            show_error("Error TXT", e)

    # ======================================================
    # 🔧 CLASIFICACIÓN (FIX DEFINITIVO)
    # ======================================================
    def classify(self):
        try:
            raw_text = self.text_input.get("1.0", tk.END).strip()
            if not raw_text:
                messagebox.showwarning("Aviso", "Ingrese un texto para clasificar")
                return

            text = preprocess(raw_text)

            proba_matrix = self.classifier.predict_proba(text)

            if proba_matrix is None or len(proba_matrix) == 0:
                raise ValueError("El modelo no devolvió probabilidades")

            proba = proba_matrix[0]        # ndarray 1D
            classes = self.classifier.get_model().classes_

            idx = int(proba.argmax())
            label = classes[idx]
            confidence = float(proba[idx])

            if confidence >= 0.75:
                color = "green"
            elif confidence >= 0.55:
                color = "orange"
            else:
                color = "red"

            probs_text = "\n".join(
                f"{cls}: {round(p * 100, 2)}%"
                for cls, p in zip(classes, proba)
            )

            self.result_label.config(
                text=(
                    f"Clase predicha: {label}\n"
                    f"Confianza: {round(confidence * 100, 2)}%\n\n"
                    f"Probabilidades:\n{probs_text}"
                ),
                fg=color
            )

        except Exception as e:
            show_error("Error al clasificar", e)

    # ======================================================
    def generate_txt_ui(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".txt")
            if not path:
                return

            generate_txt(
                output_path=path,
                total_samples=self.samples_var.get(),
                sports_ratio=self.ratio_var.get()
            )

            messagebox.showinfo("TXT generado", f"Archivo creado:\n{path}")

        except Exception as e:
            show_error("Error al generar TXT", e)

    # ======================================================
    def save_model(self):
        try:
            save_model_versioned(self.classifier)
            messagebox.showinfo("Modelo", "Modelo guardado")
        except Exception as e:
            show_error("Error", e)

    # ======================================================
    def load_model(self):
        model, _ = load_latest_model()
        if model:
            self.classifier = model
