import os
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# --- Configuración de Correo ---
RECIPIENT_EMAIL = 'juanmanuelcastro011@gmail.com'
SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587

# Variables de entorno o valores por defecto
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'notificaciones.cotizaciones@gmail.com')
# Tu App Password de 16 caracteres de Gmail
SENDER_PASS = os.environ.get('GMAIL_PASS', 'wujq fhkf kbdd kyjv') 
# -----------------------------

@app.route('/')
@app.route('/index') 
def index():
    return render_template('index.html')

@app.route('/ingenieria')
def ingenieria():
    return render_template('ingenieria.html') 

@app.route('/montajes')
def montajes():
    return render_template('montajes.html') 

@app.route('/mecanica')
def mecanica():
    return render_template('mecanica.html')

@app.route('/metalmecanica')
def metalmecanica():
    return render_template('metalmecanica.html')

@app.route('/energia')
def energia():
    return render_template('energia.html')

@app.route('/construccion')
def construccion():
    return render_template('construccion.html')

def send_email(name, user_email, subject, message, quote_request):
    """
    Envía un correo usando TLS en el puerto 587.
    Se agregó un timeout para evitar que Gunicorn bloquee el worker.
    """
    
    # 1. Construir el mensaje
    cuerpo_mensaje_texto = f"""
    --- FORMULARIO DE CONTACTO WEB - W&D INGENIERÍA ---
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
    msg.attach(MIMEText(cuerpo_mensaje_texto, 'plain'))
    
    # 2. Intentar el envío
    try:
        # Añadimos timeout=10 para que no se quede colgado si falla la conexión
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()  # Cifrado obligatorio para Gmail
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.send_message(msg)
        
        print(f"✅ Correo enviado con éxito a {RECIPIENT_EMAIL}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ ERROR: Autenticación fallida. Revisa el App Password.")
        return False
    except Exception as e:
        print(f"❌ ERROR DE ENVÍO: {e}")
        return False

@app.route('/contactanos', methods=['POST'])
def contactanos():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    asunto = request.form.get('asunto')
    mensaje = request.form.get('mensaje')
    cotizacion = request.form.get('cotizacion', 'off')
    
    cotizacion_str = 'Sí' if cotizacion == 'on' else 'No'

    # Ejecutar envío
    envio_exitoso = send_email(nombre, email, asunto, mensaje, cotizacion_str)
    
    # Redireccionamos siempre al index para evitar errores visuales al usuario
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)