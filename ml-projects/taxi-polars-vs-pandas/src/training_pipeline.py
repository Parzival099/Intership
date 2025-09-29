# src/training_pipeline.py
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error

# Importar nuestra función de preprocesamiento
from preprocessing import process_data

# --- CONSTANTES ---
DATA_PATH = "data/yellow_tripdata_2025-01.parquet" # Ajusta el nombre de tu archivo
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "lgbm_duration_model.joblib")

def train_model():
    """
    Orquesta el preprocesamiento, entrenamiento y guardado del modelo.
    """
    # 1. Cargar y procesar los datos
    model_df = process_data(DATA_PATH)

    # 2. Separar features (X) y objetivo (y)
    features = [col for col in model_df.columns if col != "trip_duration"]
    target = "trip_duration"

    X = model_df.select(features).to_pandas()
    y = model_df.select(target).to_pandas()

    # 3. Dividir datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Entrenar el modelo (con manejo de categóricas)
    print("Entrenando modelo LightGBM...")
    model = LGBMRegressor(random_state=42)

    categorical_features = ["PULocationID", "DOLocationID", "payment_type", "day_of_week", "is_weekend"]
    X_train[categorical_features] = X_train[categorical_features].astype("category")
    X_test[categorical_features] = X_test[categorical_features].astype("category")

    model.fit(X_train, y_train)

    # 5. Evaluar el modelo
    predictions = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    print(f"✅ Evaluación completada. RMSE: {rmse:.2f} minutos.")

    # 6. Guardar el modelo
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Modelo guardado en: {MODEL_PATH}")

if __name__ == "__main__":
    train_model()