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

## 📖 Sobre el Proyecto

**¿Alguna vez te has preguntado cómo una máquina entiende el significado de un texto?** 🤔

Este proyecto es una implementación práctica y visual de esa capacidad. Utilizando el algoritmo **Multinomial Naive Bayes**, hemos desarrollado un sistema inteligente capaz de analizar el contenido semántico de cualquier documento y clasificarlo instantáneamente entre **Deportes** ⚽ y **Tecnología** 💻.

**Lo que hace diferente a este proyecto:**
Más allá de un simple script, hemos construido una **herramienta completa de análisis**:
*   🧠 **Aprendizaje Profundo (pero simple):** Transforma palabras en vectores matemáticos (TF-IDF) para encontrar patrones ocultos.
*   ⚡ **Rendimiento Visual:** No es una caja negra. A través de nuestra interfaz web, puedes ver exactamente *por qué* el modelo toma sus decisiones (Matriz de Confusión y Feature Importance).
*   🛠️ **Flexibilidad Total:** Entrena con nuestros generadores sintéticos o pon a prueba el sistema con tus propios datos reales.

> *Un puente entre la teoría de Recuperación de Información y la aplicación práctica moderna.*

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
├── data/                # 💾 Archivos .txt de ejemplo y dataset generado
├── src/
│   ├── gui/             # 🖥️ Interfaz de Escritorio (Componentes Tkinter)
│   ├── modules/         # 🧠 Cerebro: Algoritmo Bayes, Preprocesamiento y Generadores
│   ├── utils/           # 🛠️ Utilidades: Manejo de errores y guardado de modelos
│   ├── streamlit_app.py # 🌐 Punto de entrada Web (Streamlit)
│   └── main.py          # 🚪 Punto de entrada Escritorio
               

```

---
<div align="center">
    <sub>Desarrollado para la asignatura de Sistemas de Información - 2025</sub>
</div>
