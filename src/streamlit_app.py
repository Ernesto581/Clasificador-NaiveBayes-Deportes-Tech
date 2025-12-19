import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add current directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.model import NaiveBayesClassifier
from modules.data_generator import generate_dataset
from modules.text_preprocessing import preprocess
from modules.evaluation import evaluate
from modules.advanced_txt_generator import generate_sports_sentence, generate_tech_sentence
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import joblib

# Page Config
st.set_page_config(
    page_title="Clasificador Naive Bayes - Tarea 9",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Estado de la sesión
if 'classifier' not in st.session_state:
    st.session_state.classifier = NaiveBayesClassifier()
if 'trained' not in st.session_state:
    st.session_state.trained = False
if 'metrics' not in st.session_state:
    st.session_state.metrics = None
if 'confusion_matrix' not in st.session_state:
    st.session_state.confusion_matrix = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Configuración")
    st.info("Tarea 9: Clasificador de Documentos\n\n**Equipo**: Carlos Miguel, Ernesto Linares, Carlos Rolando")
    
    st.markdown("---")
    st.subheader("Generación de Datos (Sintéticos)")
    num_samples = st.slider("Cantidad de Muestras", 100, 5000, 1000, 100)
    ratio = st.slider("Ratio Deportes/Tecnología", 0.1, 0.9, 0.5, 0.1)
    
    if st.button("Re-Generar Dataset Interno y Entrenar"):
        with st.spinner('Generando datos y entrenando...'):
            X, y = generate_dataset(num_samples, ratio)
            
            # Preprocessing
            X_proc = [preprocess(x) for x in X]
            
            # Split
            X_train, X_test, y_train, y_test = train_test_split(
                X_proc, y, test_size=0.3, stratify=y, random_state=42
            )
            
            # Train
            st.session_state.classifier.train(X_train, y_train)
            
            # Evaluate
            model = st.session_state.classifier.get_model()
            vec = st.session_state.classifier.get_vectorizer()
            
            # Predictions for metrics
            X_test_vec = vec.transform(X_test)
            y_pred = model.predict(X_test_vec)
            
            # Store metrics
            from sklearn.metrics import classification_report
            st.session_state.metrics = classification_report(y_test, y_pred, output_dict=True)
            st.session_state.confusion_matrix = confusion_matrix(y_test, y_pred)
            st.session_state.classes = model.classes_
            st.session_state.trained = True
            
            st.success("¡Modelo Entrenado Exitosamente!")

    st.markdown("---")
    st.subheader("Cargar Dataset Propio (TXT)")
    uploaded_file = st.file_uploader("Sube un archivo .txt (Formato: Etiqueta|Texto)", type="txt")
    
    if uploaded_file is not None:
        if st.button("Entrenar con Archivo Subido"):
            try:
                # Same training logic as before...
                # Read file
                stringio = uploaded_file.getvalue().decode("utf-8")
                
                X_custom, y_custom = [], []
                lines = stringio.splitlines()
                
                for line in lines:
                    if "|" in line:
                        label, text = line.strip().split("|", 1)
                        X_custom.append(text)
                        y_custom.append(label)
                
                if len(X_custom) < 10:
                    st.error("El archivo debe tener al menos 10 ejemplos.")
                else:
                    with st.spinner('Entrenando con datos personalizados...'):
                         # Preprocessing
                        X_proc = [preprocess(x) for x in X_custom]
                        X_train, X_test, y_train, y_test = train_test_split(
                            X_proc, y_custom, test_size=0.3, stratify=y_custom, random_state=42
                        )
                        st.session_state.classifier.train(X_train, y_train)
                        model = st.session_state.classifier.get_model()
                        vec = st.session_state.classifier.get_vectorizer()
                        X_test_vec = vec.transform(X_test)
                        y_pred = model.predict(X_test_vec)
                        st.session_state.metrics = classification_report(y_test, y_pred, output_dict=True)
                        st.session_state.confusion_matrix = confusion_matrix(y_test, y_pred)
                        st.session_state.classes = model.classes_
                        st.session_state.trained = True
                        st.success(f"Modelo re-entrenado con {len(X_custom)} ejemplos del archivo.")
            except Exception as e:
                st.error(f"Error al procesar el archivo: {e}")

    st.markdown("---")
    st.subheader("🛠️ Generar Archivo TXT")
    st.markdown("Crea un archivo nuevo para descargar y compartir.")
    
    gen_samples = st.number_input("Cantidad a generar", 10, 10000, 500)
    gen_ratio = st.slider("Proporción Deportes/Tech", 0.1, 0.9, 0.5)
    
    if st.button("Generar Archivo"):
        # Logic adapted from advanced_txt_generator.py but for memory buffer
        import random
        sports_c = int(gen_samples * gen_ratio)
        tech_c = gen_samples - sports_c
        sentences = []
        
        # Sports
        for _ in range(sports_c):
             sentences.append(f"Deportes|{generate_sports_sentence()}")
        # Tech
        for _ in range(tech_c):
             sentences.append(f"Tecnologia|{generate_tech_sentence()}")
             
        random.shuffle(sentences)
        final_txt = "\n".join(sentences)
        
        st.download_button(
            label="⬇️ Descargar dataset.txt",
            data=final_txt,
            file_name="dataset_generado.txt",
            mime="text/plain"
        )
        st.success(f"¡Generados {len(sentences)} ejemplos listos para descargar!")

# --- MAIN PAGE ---
st.title("🧠 Clasificador de Documentos Naive Bayes")
st.markdown("Sistema inteligente para clasificar textos entre **Deportes** y **Tecnología**.")

tab1, tab2, tab3 = st.tabs(["📊 Evaluación del Modelo", "🧪 Prueba en Tiempo Real", "🔍 Explicabilidad (Top Features)"])

# TAB 1: EVALUACIÓN
with tab1:
    if not st.session_state.trained:
        st.warning("⚠️ El modelo aún no ha sido entrenado. Usa el panel lateral para iniciar el entrenamiento.")
    else:
        # Métricas Clave
        c1, c2, c3 = st.columns(3)
        metrics = st.session_state.metrics
        accuracy = metrics['accuracy']
        macro_f1 = metrics['macro avg']['f1-score']
        weighted_f1 = metrics['weighted avg']['f1-score']
        
        c1.metric("Exactitud (Accuracy)", f"{accuracy:.2%}", delta="Global")
        c2.metric("F1-Score (Macro)", f"{macro_f1:.2%}")
        c3.metric("F1-Score (Weighted)", f"{weighted_f1:.2%}")
        
        st.divider()
        
        col_cm, col_det = st.columns([1, 1])
        
        with col_cm:
            st.subheader("Matriz de Confusión")
            cm = st.session_state.confusion_matrix
            classes = st.session_state.classes
            
            # Plot Confusion Matrix using Matplotlib
            fig, ax = plt.subplots(figsize=(5, 4))
            im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
            ax.figure.colorbar(im, ax=ax)
            
            ax.set(xticks=np.arange(cm.shape[1]),
                   yticks=np.arange(cm.shape[0]),
                   xticklabels=classes, yticklabels=classes,
                   ylabel='Etiqueta Real',
                   xlabel='Predicción')
            
            # Loop over data dimensions and create text annotations.
            thresh = cm.max() / 2.
            for i in range(cm.shape[0]):
                for j in range(cm.shape[1]):
                    ax.text(j, i, format(cm[i, j], 'd'),
                            ha="center", va="center",
                            color="white" if cm[i, j] > thresh else "black")
            
            st.pyplot(fig)
            
        with col_det:
            st.subheader("Detalle por Clase")
            df_metrics = pd.DataFrame(metrics).transpose()
            st.dataframe(df_metrics.style.format("{:.2%}").highlight_max(axis=0))

# TAB 2: PRUEBA EN TIEMPO REAL
with tab2:
    st.header("Clasificación en Vivo")
    
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        user_input = st.text_area("Ingresa un texto para clasificar:", height=200, placeholder="Ejemplo: El delantero marcó un gol increíble en el último minuto...")
        classify_btn = st.button("Clasificar Texto", type="primary")
        
    with col_result:
        if classify_btn and user_input:
            if not st.session_state.trained:
                st.error("Primero debes entrenar el modelo.")
            else:
                processed_text = preprocess(user_input)
                proba = st.session_state.classifier.predict_proba(processed_text)[0]
                classes = st.session_state.classifier.get_model().classes_
                
                # Get max prediction
                idx = np.argmax(proba)
                label = classes[idx]
                confidence = proba[idx]
                
                # Colors
                color = "#28a745" if label == "Deportes" else "#007bff"
                if label == "Deportes": bg_color = "#d4edda"; text_color = "#155724"
                else: bg_color = "#cce5ff"; text_color = "#004085"
                
                st.markdown(f"""
                <div style="background-color: {bg_color}; color: {text_color};" class="prediction-box">
                    Predicción: {label.upper()}<br>
                    <span style="font-size: 16px">Confianza: {confidence:.2%}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Bar chart for probabilities
                chart_data = pd.DataFrame({
                    "Clase": classes,
                    "Probabilidad": proba
                })
                st.bar_chart(chart_data, x="Clase", y="Probabilidad", color="#007bff")

# TAB 3: EXPLICABILIDAD
with tab3:
    st.header("¿Qué palabras definen cada categoría?")
    
    if st.session_state.trained:
        model = st.session_state.classifier.get_model()
        vec = st.session_state.classifier.get_vectorizer()
        
        feature_names = vec.get_feature_names_out()
        
        # MultinomialNB has feature_log_prob_ (n_classes, n_features)
        # We can simulate "importance" by looking at the diff or raw probabilities
        
        for i, class_label in enumerate(model.classes_):
            st.subheader(f"Top palabras para: {class_label}")
            
            # Get log probs for this class
            log_prob = model.feature_log_prob_[i]
            
            # Sort indices
            top10_idx = log_prob.argsort()[-10:][::-1]
            
            top_features = [feature_names[j] for j in top10_idx]
            top_scores = [np.exp(log_prob[j]) for j in top10_idx] # convert back from log for intuitive view
            
            df_feat = pd.DataFrame({"Palabra": top_features, "Score (Probabilidad)": top_scores})
            
            st.table(df_feat)
            
    else:
        st.info("Entrena el modelo para ver las características más importantes.")

