# dashboard/app.py
import streamlit as st
import joblib
import pandas as pd
import numpy as np

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Predicción de Viajes en Taxi NYC",
    page_icon="🚖",
    layout="wide"
)

# --- Cargar el Modelo ---
# Usamos un bloque try-except para manejar el caso en que el modelo no se encuentre
try:
    model = joblib.load("models/lgbm_duration_model.joblib")
except FileNotFoundError:
    st.error("Error: Archivo del modelo no encontrado. Asegúrate de que 'lgbm_duration_model.joblib' esté en la carpeta 'models/'.")
    st.stop()

# --- Título y Descripción ---
st.title("Predicción de Duración de Viajes en Taxi de NYC 🚕")
# Reemplaza el st.write original con este:

st.write(
    """
    Esta aplicación utiliza un modelo de Machine Learning (LightGBM) para predecir la duración 
    de un viaje en taxi en Nueva York.

    El modelo basa su predicción en factores clave: la **distancia** y las **zonas de recogida/destino** son los más 
    importantes, mientras que la **hora** y el **día de la semana** le ayudan a considerar el impacto del tráfico. 
    Introduce los detalles en el panel de la izquierda para obtener una estimación.
    """
)

# --- Panel Lateral de Entradas (Inputs) ---
st.sidebar.header("Parámetros del Viaje")

def get_user_inputs():
    """Recoge los inputs del usuario desde el panel lateral."""
    trip_distance = st.sidebar.slider("Distancia del Viaje (millas)", 0.1, 50.0, 5.0)
    pickup_hour = st.sidebar.slider("Hora de Recogida (0-23)", 0, 23, 18)
    day_of_week = st.sidebar.selectbox("Día de la Semana", options=range(1, 8), format_func=lambda x: ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][x-1])
    passenger_count = st.sidebar.selectbox("Número de Pasajeros", [1, 2, 3, 4, 5, 6])
    pu_location = st.sidebar.number_input("ID de Zona de Recogida (PULocationID)", 1, 265, 132)
    do_location = st.sidebar.number_input("ID de Zona de Destino (DOLocationID)", 1, 265, 239)
    payment_type = st.sidebar.selectbox("Método de Pago", options=[1, 2], format_func=lambda x: "Tarjeta" if x==1 else "Efectivo")

    # Crear el feature 'is_weekend' basado en 'day_of_week'
    is_weekend = 1 if day_of_week in [6, 7] else 0

    # Crear un DataFrame con los datos para la predicción
    features = pd.DataFrame({
        'passenger_count': [passenger_count],
        'trip_distance': [trip_distance],
        'PULocationID': [pu_location],
        'DOLocationID': [do_location],
        'payment_type': [payment_type],
        'pickup_hour': [pickup_hour],
        'day_of_week': [day_of_week],
        'is_weekend': [is_weekend]
    })
    return features

input_df = get_user_inputs()

# --- Predicción y Resultados ---
st.header("Resultado de la Predicción")

if st.sidebar.button("Predecir Duración"):
    # Convertir las columnas categóricas al tipo correcto para LightGBM
    categorical_features = ["PULocationID", "DOLocationID", "payment_type", "day_of_week", "is_weekend"]
    input_df[categorical_features] = input_df[categorical_features].astype("category")

    # Realizar la predicción
    prediction = model.predict(input_df)

    st.metric(
        label="Duración Estimada del Viaje",
        value=f"{prediction[0]:.2f} minutos"
    )
else:
    st.info("Ajusta los parámetros en el panel de la izquierda y haz clic en 'Predecir Duración'.")

# --- Mostrar los datos de entrada ---
st.subheader("Datos de Entrada para la Predicción")
st.dataframe(input_df)

# --- Mostrar Feature Importance (Opcional pero recomendado) ---
st.subheader("¿Qué considera importante el modelo?")
st.image("feature_importance.png", caption="Importancia de Features del Modelo")
st.write(
    "Como se ve en el gráfico, la **distancia del viaje** y las **zonas de recogida/destino** "
    "son los factores más determinantes para la predicción."
)
# (Para que esto funcione, guarda el gráfico de feature importance como 'feature_importance.png' en la raíz del proyecto)