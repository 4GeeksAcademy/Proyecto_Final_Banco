from flask_mail import Mail

mail = Mail()

def get_mail():
    return mail