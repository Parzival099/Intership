# src/preprocessing.py
import polars as pl

def process_data(file_path: str) -> pl.DataFrame:
    """
    Carga, limpia y crea features para el dataset de taxis.
    Retorna un DataFrame listo para el entrenamiento del modelo.
    """
    # Cargar los datos
    df = pl.read_parquet(file_path)

    # Crear 'trip_duration'
    df = df.with_columns(
        trip_duration = (
            (pl.col("tpep_dropoff_datetime") - pl.col("tpep_pickup_datetime")).dt.total_seconds() / 60
        )
    )

    # Ingeniería de Características (Feature Engineering)
    df = df.with_columns(
        pickup_hour = pl.col("tpep_pickup_datetime").dt.hour(),
        day_of_week = pl.col("tpep_pickup_datetime").dt.weekday(),
    ).with_columns(
        is_weekend = pl.when(pl.col("day_of_week").is_in([6, 7])).then(1).otherwise(0)
    )

    # Aplicar filtros para eliminar outliers y datos inconsistentes
    df_clean = df.filter(
        (pl.col("trip_duration").is_between(1, 120)) &
        (pl.col("trip_distance") > 0) &
        (pl.col("passenger_count") > 0)
    )

    # Seleccionar solo las columnas necesarias para el modelo
    features = [
        "passenger_count", "trip_distance", "PULocationID", "DOLocationID",
        "payment_type", "pickup_hour", "day_of_week", "is_weekend"
    ]
    target = "trip_duration"

    final_df = df_clean.select(features + [target])

    print("✅ Preprocesamiento completado.")
    return final_df