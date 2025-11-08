import os # Necesario para leer variables de entorno
from flask import Flask, render_template, request, redirect, url_for
from email.message import EmailMessage 
import smtplib 
from email.mime.text import MIMEText # Se añade para manejo de texto plano
from email.mime.multipart import MIMEMultipart # Se añade para manejo de estructura de correo

app = Flask(__name__)

# --- Configuración de Correo ---
# Correo al que deben llegar los mensajes del formulario
RECIPIENT_EMAIL = 'juanmanuelcastro011@gmail.com'

# Servidor SMTP de Gmail
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# El correo que usas para ENVIAR los mensajes (debe ser un correo real con App Password)
# Por seguridad, el código lee el email y la contraseña de VARIABLES DE ENTORNO.
# Reemplaza 'tu_correo_de_envio@gmail.com' con el email desde donde enviarás.
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'notificaciones.cotizaciones@gmail.com')
SENDER_PASS = os.environ.get('GMAIL_PASS', 'wujq fhkf kbdd kyjv') # ¡Usar variable de entorno!
# -----------------------------


# RUTA PRINCIPAL
@app.route('/')
@app.route('/index') 
def index():
    """Ruta principal que renderiza el index.html."""
    return render_template('index.html')

# RUTA DE INGENIERÍA
@app.route('/ingenieria')
def ingenieria():
    """Ruta de detalle para la página de Ingeniería."""
    return render_template('ingenieria.html') 

# RUTA DE MONTAJES
@app.route('/montajes')
def montajes():
    """Ruta de detalle para la página de Montajes."""
    return render_template('montajes.html') 

# RUTA DE MECANICA
@app.route('/mecanica')
def mecanica():
    """Ruta de detalle para la página de Mecánica."""
    return render_template('mecanica.html')

# RUTA DE METALMECANICA
@app.route('/metalmecanica')
def metalmecanica():
    """Ruta de detalle para la página de Metalmecánica."""
    return render_template('metalmecanica.html')

# RUTA DE ENERGIA 
@app.route('/energia')
def energia():
    """Ruta de detalle para la página de Energía."""
    return render_template('energia.html')

# RUTA DE CONSTRUCCION 
@app.route('/construccion')
def construccion():
    """Ruta de detalle para la página de Construcción."""
    return render_template('construccion.html')

# FUNCIÓN DE ENVÍO DE CORREO
def send_email(name, user_email, subject, message, quote_request):
    """
    Intenta enviar un correo electrónico usando las credenciales de Gmail.
    Requiere una 'App Password' de Google.
    """
    if SENDER_PASS == 'TU_PASSWORD_AQUI':
        print("\n❌ ERROR DE CONFIGURACIÓN: Reemplaza 'TU_PASSWORD_AQUI' en el código o configura la variable de entorno GMAIL_PASS. ❌")
        return False

    # 1. Construir el cuerpo del mensaje
    cuerpo_mensaje_texto = f"""
    --- FORMULARIO DE CONTACTO WEB ---
    Enviado por: {name}
    Email de Contacto: {user_email}
    Asunto: {subject}
    Solicita Cotización: {quote_request}
    
    Mensaje:
    {message}
    """
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = f"CONTACTO WEB: {subject}"
    
    # Agregar el cuerpo del mensaje
    msg.attach(MIMEText(cuerpo_mensaje_texto, 'plain'))
    
    # 2. Enviar el correo
    try:
        # Se conecta al servidor SMTP de Gmail (TLS)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()  # Iniciar conexión cifrada TLS
            server.ehlo()
            server.login(SENDER_EMAIL, SENDER_PASS) # Autenticación
            server.send_message(msg)
        
        print(f"\n✅ Correo de '{name}' enviado con éxito a {RECIPIENT_EMAIL} ✅\n")
        return True
        
    except smtplib.AuthenticationError:
        print("\n❌ ERROR DE AUTENTICACIÓN: La contraseña o el email son incorrectos. ¿Usaste una App Password de Google? ❌")
        return False
    except Exception as e:
        print(f"\n❌ ERROR DE ENVÍO (General): {e} ❌")
        return False


# RUTA DE CONTACTO (Solo acepta peticiones POST del formulario)
@app.route('/contactanos', methods=['POST'])
def contactanos():
    """Ruta para manejar el envío del formulario de contacto."""
    
    # Captura y procesamiento de datos del formulario
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    asunto = request.form.get('asunto')
    mensaje = request.form.get('mensaje')
    cotizacion = request.form.get('cotizacion', 'off')
    
    cotizacion_str = 'Sí' if cotizacion == 'on' else 'No'

    # Intenta enviar el correo
    envio_exitoso = send_email(nombre, email, asunto, mensaje, cotizacion_str)
    
    if not envio_exitoso:
        # Si el envío falla, aún redirecciona, pero el error se muestra en la consola
        print("El envío falló. Revisar los logs de error.")

    # Redireccionar a la página principal tras procesar el envío
    return redirect(url_for('index'))

# Bloque de ejecución principal
if __name__ == '__main__':
    # Ejecuta el servidor en modo debug para desarrollo
    app.run(debug=True)