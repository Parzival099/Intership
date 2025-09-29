# 🚖 Taxi Trip Data – Pandas vs Polars Benchmark

Este proyecto compara el rendimiento de **Pandas** y **Polars** en un flujo completo de **ciencia de datos** usando el dataset de **NYC Taxi Trips**.
El objetivo es demostrar cómo **Polars optimiza memoria y velocidad**, integrándolo dentro de un pipeline de **EDA → Feature Engineering → Modelado Predictivo → Dashboard**.

---

## 🎯 Objetivos

* 🧹 Realizar **limpieza y preprocesamiento** del dataset de taxis.
* 📊 Comparar **tiempos de ejecución** y **uso de memoria** entre **Pandas** y **Polars**.
* 🔎 Desarrollar un **EDA interactivo** para entender mejor los viajes en taxi.
* ⚙️ Construir un **pipeline de features y modelo de predicción** (ej. duración o tarifa).
* 📈 Implementar un **dashboard en Streamlit** para visualizar resultados.
* ☁️ Desplegar el proyecto en la nube (**Streamlit Cloud / Hugging Face / Render**).

---

## 📂 Estructura del proyecto

```bash
📦 taxi-polars-vs-pandas
 ┣ 📁 data/                   # Dataset parquet (NYC Taxi)
 ┣ 📁 notebooks/              # Notebooks de exploración y prototipos
 ┣ 📁 src/                    # Código fuente organizado en módulos
 ┃ ┣ 📄 eda.py                # Exploratory Data Analysis
 ┃ ┣ 📄 preprocessing.py      # Limpieza y feature engineering
 ┃ ┣ 📄 training_pipeline.py  # Entrenamiento del modelo
 ┃ ┣ 📄 inference_pipeline.py # Inferencia y predicciones
 ┃ ┗ 📄 benchmarking.py       # Comparación Pandas vs Polars
 ┣ 📁 dashboard/              # Código para el dashboard en Streamlit
 ┣ 📄 requirements.txt        # Dependencias del proyecto
 ┗ 📄 README.md               # Documentación de este proyecto
```

---

## ⚡ Benchmarking Pandas vs Polars

Ejemplo de comparación (lectura + limpieza de 1M registros):

| Librería | Tiempo (s) | Memoria (MB) |
| -------- | ---------- | ------------ |
| Pandas   | 12.5       | 480          |
| Polars   | 4.2        | 210          |

✅ Polars mostró ser **3x más rápido** y **2x más eficiente en memoria**.

---

## 🛠️ Tecnologías utilizadas

* **Python** 🐍
* **Pandas** y **Polars**
* **Scikit-learn** para el modelado predictivo
* **Matplotlib / Seaborn / Plotly** para visualización
* **Streamlit** para el dashboard
* **Docker** (opcional para despliegue reproducible)

---

## 🚀 Ejecución del proyecto

1. **Clonar repositorio**

   ```bash
   git clone https://github.com/tu-usuario/portfolio-data-ml.git
   cd portfolio-data-ml/ml-projects/taxi-polars-vs-pandas
   ```

2. **Crear entorno virtual e instalar dependencias**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. **Ejecutar el benchmarking**

   ```bash
   python src/benchmarking.py
   ```

4. **Ejecutar dashboard en Streamlit**

   ```bash
   streamlit run dashboard/app.py
   ```

---

## ☁️ Despliegue en la nube

El proyecto puede ser desplegado en:

* 🌐 **Streamlit Cloud** → simple y rápido.
* 🤗 **Hugging Face Spaces** → ideal para modelos ML.
* 🚀 **Render / Railway** → despliegue backend + frontend.

---
