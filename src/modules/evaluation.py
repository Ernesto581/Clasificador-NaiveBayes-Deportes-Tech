import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def evaluate(model, vectorizer, X_test, y_test, parent_frame=None):
    X_vec = vectorizer.transform(X_test)
    y_pred = model.predict(X_vec)

    # Métricas
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)

    if parent_frame is not None:
        show_confusion_matrix(cm, model.classes_, parent_frame)

    return report, cm


def show_confusion_matrix(cm, classes, parent):
    fig, ax = plt.subplots(figsize=(4, 4))
    im = ax.imshow(cm)

    ax.set_xticks(range(len(classes)))
    ax.set_yticks(range(len(classes)))
    ax.set_xticklabels(classes)
    ax.set_yticklabels(classes)

    ax.set_xlabel("Predicción")
    ax.set_ylabel("Real")
    ax.set_title("Matriz de Confusión")

    for i in range(len(classes)):
        for j in range(len(classes)):
            ax.text(j, i, cm[i, j], ha="center", va="center")

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack()
