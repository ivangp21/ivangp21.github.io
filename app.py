from flask import Flask, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración de Flask-Mail para usar Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ivangp21@gmail.com'
app.config['MAIL_PASSWORD'] = 'gomezpas21'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form['mensaje']

    msg = Message("Nuevo mensaje de contacto",
                  sender='ivangp21@gmail.com',  # Remitente del mensaje
                  recipients=['ivangp21@gmail.com'])  # Destinatario del mensaje
    msg.body = f"De: {nombre}\nEmail: {email}\nMensaje: {mensaje}"
    mail.send(msg)

    return 'Formulario enviado con éxito'

if __name__ == '__main__':
    app.run(debug=True)
