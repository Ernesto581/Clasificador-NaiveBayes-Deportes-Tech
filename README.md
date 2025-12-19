<div align="center">

# 🧠 Clasificador de Documentos Inteligente
## Tarea 9: Naive Bayes - Sistemas de Información

<img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit"/>
<img src="https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit Learn"/>

### 👥 Equipo Desarrollador
| **Carlos Miguel Vázquez** | **Ernesto Linares Toledo** |
|:---:|:---:|
| Backend & Algoritmos | Frontend & Integración |

> *"Clasificando el mundo entre Deportes ⚽ y Tecnología 💻 con el poder de la probabilidad."*

</div>

---

## 📋 Descripción del Proyecto
Este sistema implementa un **Clasificador Naive Bayes Multinomial** capaz de distinguir automáticamente documentos e informes basándose en su contenido semántico. Combina una arquitectura de Machine Learning robusta con una interfaz visual moderna.

## ✨ Características Principales
*   **Doble Interfaz:**
    *   🌐 **Web (Streamlit):** Gráficos interactivos, matrices en tiempo real y explioración de datos.
    *   🖥️ **Escritorio (Tkinter):** Versión clásica ligera y funcional.
*   **Entrenamiento Flexible:** 
    *   Generador automático de datos sintéticos.
    *   Carga de datasets propios (`.txt`).
*   **Analíticas:** Visualización de la Matriz de Confusión y métricas de desempeño (F1-Score, Accuracy).
*   **Explicabilidad:** Descubre qué palabras (Features) pesan más para cada categoría.

## 🚀 Inicio Rápido

### Requisitos Previos
```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

### ▶️ Ejecutar Interfaz Web (Recomendado)
```bash
streamlit run src/streamlit_app.py
```
*Accede a:* `http://localhost:8501`

### ▶️ Ejecutar Versión de Escritorio
```bash
python src/main.py
```

## 📂 Estructura del repositorio
```text
proyecto/
├── src/
│   ├── modules/         # Lógica de ML (Algoritmo y Preprocesamiento)
│   ├── streamlit_app.py # App Web Visual
│   └── main.py          # App de Escritorio
├── data/                # Datasets de ejemplo
├── INFORME.md           # Informe Académico Detallado
└── GUIA_EXPOSICION.md   # Guion de presentación
```

---
<div align="center">
    <sub>Desarrollado para la asignatura de Recuperación de Información - 2024</sub>
</div>
