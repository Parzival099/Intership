# 1. Usar una imagen base oficial de Python (slim es ligera)
FROM python:3.9-slim

# 2. Establecer un directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar primero el archivo de requisitos e instalar dependencias
# (Esto se hace separado para aprovechar la caché de Docker)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Copiar el resto de tu aplicación (app.py y la carpeta templates)
COPY . .

# 5. Exponer el puerto en el que Gunicorn se ejecutará
EXPOSE 9000

# 6. El comando para iniciar la aplicación cuando se ejecute el contenedor
# Usa Gunicorn (que está en requirements.txt) para servir la app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]