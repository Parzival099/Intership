from flask import Flask, render_template
import datetime
import os  # Importa la librería 'os' para leer variables de entorno

# Crea la instancia de la aplicación Flask
app = Flask(__name__)

@app.route('/')
def index():
    # Define datos dinámicos para pasar a la plantilla
    page_title = "¡App Integrada con Key Vault y Storage!"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- INICIO DE CAMBIOS ---
    # Lee las variables de entorno que Azure inyecta desde Key Vault
    # os.environ.get() es la forma segura de leerlas.
    # Si la variable no existe, devolverá "No Encontrado".
    db_user_val = os.environ.get('DB_USER', 'No Encontrado')
    
    # Para la contraseña, es una buena práctica no mostrarla.
    # Aquí la reemplazamos con asteriscos si la encuentra.
    db_pass_raw = os.environ.get('DB_PASS')
    if db_pass_raw:
        db_pass_val = "********"
    else:
        db_pass_val = "No Encontrado (¡Bien!)"
    # --- FIN DE CAMBIOS ---

    # Renderiza el archivo 'index.html'
    return render_template('index.html',
                           titulo="¡App Integrada con Key Vault y Storage!",
                           server_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           db_user=db_user_val,
                           db_pass=db_pass_val) # Pasa las variables a la plantilla

if __name__ == '__main__':
    # Esto es solo para pruebas locales
    app.run(debug=True)