"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
import requests
import os
from api.models import db, User, Cliente, Cuenta, ConfiguracionUsuario, Transaccion, Notificacion, TarjetaCoordenadas
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.mail_config import get_mail




# Para Flask-Mail, codigo de seguridad
from flask_mail import Message
import random


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/test')
def test():
    es_divisible_por_dos = lambda numero: True if numero % 2 == 0 else False
    for i in range(1, 101):
        new_user = User(
            email= f"ejemplo{i}",
            password= f"ejemplo{i}",
            is_active= es_divisible_por_dos(i)
        )
        db.session.add(new_user)
    db.session.commit() 
    
    Users = User.query.all()
    return jsonify([user.serialize() for user in Users]), 201


@api.route('/Users')
def getUsers():
    Users = User.query.all()
    return jsonify([user.serialize() for user in Users]), 201

from datetime import datetime  # Asegúrate de importar datetime

#                                               REGISTRO, LOGIN, IFORMACION DE USUARIO Y MODIFICACION DE USUARIO

@api.route('/User/Register', methods=['POST'])
def addUser():
    data = request.get_json()
    print('desde routes', data)

    # Datos del usuario
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    is_active = data.get("is_active", True)  # Default: activo

    # Validaciones básicas
    if not email or not name or not password:
        return jsonify({"mensaje": "Faltan datos obligatorios del usuario"}), 400

    try:
        # Crear usuario
        print("Creando usuario...")
        new_user = User(
            name=name,
            email=email,
            password=password,
            is_active=is_active
        )
        db.session.add(new_user)
        db.session.flush()  # Esto asegura que new_user.id esté disponible
        print("Usuario creado:", new_user)

        # Crear cliente asociado al usuario
        print("Creando cliente...")
        nuevo_cliente = Cliente(
            nombre_completo=name,
            apellidos="Introduzca apellido",
            telefono="Introduzca numero",
            direccion="Introduzca direccion",
        )
        db.session.add(nuevo_cliente)
        db.session.flush()  # Esto asegura que nuevo_cliente.id esté disponible
        print("Cliente creado:", nuevo_cliente)

        # Asociar el cliente al usuario
        new_user.cliente_id = nuevo_cliente.id
        db.session.add(new_user)  # Actualizar el usuario con el cliente asociado

        # Crear cuenta asociada al cliente
        print("Creando cuenta...")
        nueva_cuenta = Cuenta(
            numero_cuenta=f"GEEK-ES24{random.randint(10000000, 99990000)}",
            numero_tarjeta=f"{random.randint(1000000000000000, 9999999999999999)}",
            cvv=f"{random.randint(100, 999)}",
            caducidad="12/30",
            tipo_cuenta="Debito",
            saldo=1500,
            saldo_retenido=50,
            cliente_id=nuevo_cliente.id,
            estado=1,
        )
        db.session.add(nueva_cuenta)
        db.session.flush()
        print("Cuenta creada:", nueva_cuenta)

        print("Generando tarjeta de coordenadas...")
        posiciones = [f"{fila}{columna}" for fila in "ABCD" for columna in range(1, 5)]  # de A1 a D4
        for pos in posiciones:
            codigo = f"{random.randint(0, 9999):04d}"  # 4 dígitos
            coordenada = TarjetaCoordenadas(
                cuenta_id=nueva_cuenta.id,
                posicion=pos,
                valor=codigo,
            )
            db.session.add(coordenada)
        print("Tarjeta de coordenadas generada")

        # Notificaciones por defecto
        notificaciones_por_defecto = [
            "Bienvenido a Geek-Bank!",
            "Configura tu perfil para una mejor experiencia y desbloquear las funcionalidades al completo.",
            "Revisa nuestras nuevas funcionalidades.",
            "No te olvides de solicitar tu tarjeta de coordenadas"
        ]

        for mensaje in notificaciones_por_defecto:
            nueva_notificacion = Notificacion(
                mensaje=mensaje,
                cliente_id=nuevo_cliente.id
            )
            db.session.add(nueva_notificacion)
            print(f"Notificación creada: {mensaje}")

        # Generar transacciones automáticas
        print("Generando transacciones...")
        tipos_transacciones = [
            {"tipo": "depósito", "monto": 1000.00, "descripcion": "Depósito inicial"},
            {"tipo": "retiro", "monto": 200.00, "descripcion": "Retiro en cajero"},
            {"tipo": "transferencia", "monto": 300.00, "descripcion": "Transferencia a otro usuario"},
            {"tipo": "depósito", "monto": 500.00, "descripcion": "Depósito de salario"},
            {"tipo": "retiro", "monto": 100.00, "descripcion": "Compra en tienda"},
        ]

        for transaccion_data in tipos_transacciones:
            nueva_transaccion = Transaccion(
                cuenta_id=nueva_cuenta.id,
                tipo=transaccion_data["tipo"],
                monto=transaccion_data["monto"],
                descripcion=transaccion_data["descripcion"],
                fecha=datetime.utcnow(),  # Fecha y hora actual
            )
            db.session.add(nueva_transaccion)
            print(f"Transacción creada: {nueva_transaccion}")

        # Confirmar los cambios
        db.session.commit()
        print("Cambios confirmados")

        # Generar un token para el usuario
        access_token = create_access_token(identity=new_user.id)
        return jsonify({
            "mensaje": "Usuario, cliente, cuenta y transacciones creados exitosamente",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            },
            "Notificacion": notificaciones_por_defecto,
            "token": access_token
        }), 201

    except Exception as e:
        db.session.rollback()  # Revertir cambios si hay un error
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 400
       
@api.route('/User/Login', methods=['POST'])
# @jwt_required()
def user_autentication():
    # Obtener datos del cliente
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    print("Datos recibidos:", data)  # Log para depuración

    # Validaciones
    if not email:
        return jsonify({"Mensaje": "The email is missing"}), 400
    if not password:
        return jsonify({"Mensaje": "The password is missing"}), 400
    if not name:
        return jsonify({"Mensaje": "The name is missing"}), 400

    try:
        # Buscar usuario en la base de datos
        user = User.query.filter_by(name=name, email=email, password=password).first()

        if user is None:
            return jsonify({"mensaje": "Invalid password or email"}), 400
        
        # Crear token de acceso
        access_token = create_access_token(identity=user.name)

        # Responder con el usuario y el token
        return jsonify({
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
    },
    "token": access_token
        }), 200  # 200 para indicar éxito en login

    except Exception as e:
        print("Error en el backend:", str(e))  # Log para debugging
        return jsonify({"error": "An error occurred during login"}), 500

@api.route('/User/<int:id>')
# @jwt_required()
def get_user_details(id):
    try:
        # Buscar el usuario por ID
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Obtener el cliente asociado al usuario
        cliente = user.cliente
        if not cliente:
            return jsonify({"error": "El usuario no tiene un cliente asociado"}), 404

        # Obtener la única cuenta del cliente
        if not cliente.cuentas:
            return jsonify({"error": "El cliente no tiene cuentas"}), 404
        
        cuenta = cliente.cuentas[0]  # Tomamos la primera (y única) cuenta

        # Obtener transacciones de la cuenta
        transacciones_data = [
            {
                "id": transaccion.id,
                "tipo": transaccion.tipo,
                "monto": float(transaccion.monto),  # Convertir a float para JSON
                "fecha": transaccion.fecha.isoformat(),  # Formato ISO
                "descripcion": transaccion.descripcion
            }
            for transaccion in cuenta.transacciones
        ]

        # Obtener coordenadas (¡expone datos sensibles!)
        tarjeta_coordenadas_data = [
            {
                "posicion": coord.posicion,
                "valor": coord.valor  # En producción, enmascara esto
            }
            for coord in cuenta.tarjetas_coordenadas
        ]

        # Construir la respuesta
        response = {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            },
            "cliente": {
                "id": cliente.id,
                "nombre": cliente.nombre_completo,
                "apellidos": cliente.apellidos,
                "telefono": cliente.telefono,
                "direccion": cliente.direccion,
                "Tipo_de_documento": cliente.tipo_documento,
                "Numero_de_documento": cliente.numero_documento,
            },
            "cuentas": {
                "id": cuenta.id,
                "numero_cuenta": cuenta.numero_cuenta,
                "numero_tarjeta": cuenta.numero_tarjeta,
                "cvv": cuenta.cvv,
                "caducidad": cuenta.caducidad,
                "tipo_cuenta": cuenta.tipo_cuenta,
                "saldo": float(cuenta.saldo), 
                "saldo_retenido": float(cuenta.saldo_retenido),
                "transacciones": transacciones_data,
            },
            "notificaciones": [notificacion.serialize() for notificacion in cliente.notificaciones],
            "tarjeta_coordenadas": tarjeta_coordenadas_data
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Ha ocurrido un error", "details": str(e)}), 500

@api.route('/User/<int:id>/Perfil', methods=['PUT'])
# @jwt_required()
def update_cliente_profile(id):
    perfil = request.get_json()  # Obtener los datos enviados en la solicitud

    # Buscar el usuario por ID
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Verificar si el usuario tiene un cliente asociado
    cliente = user.cliente
    if not cliente:
        return jsonify({"error": "El usuario no tiene un cliente asociado"}), 404

    # Obtener los datos enviados en la solicitud
    nombre_completo = perfil.get("nombre_completo")
    apellidos = perfil.get("apellidos")
    direccion = perfil.get("direccion")
    telefono = perfil.get("telefono")
    tipo_documento = perfil.get("tipo_documento")
    numero_documento = perfil.get("numero_documento")

    # Validar el número de documento si es único
    if numero_documento:
        existing_cliente = cliente.query.filter_by(numero_documento=numero_documento).first()
        if existing_cliente and existing_cliente.id != cliente.id:
            return jsonify({"error": "El número de documento ya está en uso por otro cliente"}), 400

    # Actualizar solo los campos enviados
    if nombre_completo:
        cliente.nombre_completo = nombre_completo
    if apellidos:
        cliente.apellidos = apellidos
    if telefono:
        cliente.telefono = telefono
    if direccion:
        cliente.direccion = direccion
    if tipo_documento:
        cliente.tipo_documento = tipo_documento
    if numero_documento:
        cliente.numero_documento = numero_documento

    # Guardar cambios en la base de datos
    db.session.commit()

    return jsonify({"mensaje": "Perfil del cliente actualizado exitosamente", "cliente": cliente.serialize()}), 200

#                                                                  PRIVADO PARA JWT
    
@api.route('/private', methods=['POST'])
@jwt_required()
def private():
    current_user = get_jwt_identity()
    return jsonify({"ok" : True, "current_user" : current_user}), 200

#                                                                   NOTIFICACIONES

@api.route('/notificaciones/<int:cliente_id>', methods=['GET'])
# @jwt_required()
def get_notificaciones(cliente_id):
    try:
        # Buscar el cliente por ID
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return jsonify({"error": "Cliente no encontrado"}), 404

        # Obtener las notificaciones del cliente
        notificaciones = cliente.notificaciones

        # Serializar las notificaciones
        notificaciones_data = [notificacion.serialize() for notificacion in notificaciones]

        return jsonify(notificaciones_data), 200

    except Exception as e:
        return jsonify({"error": "Ha ocurrido un error", "details": str(e)}), 500

@api.route('/notificaciones/<int:cliente_id>/agregar', methods=['POST'])
# @jwt_required()
def agregar_notificacion(cliente_id):
    try:
        # Buscar el cliente por ID
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return jsonify({"error": "Cliente no encontrado"}), 404

        # Obtener el mensaje de la notificación desde el cuerpo de la solicitud
        data = request.get_json()
        mensaje = data.get("mensaje")

        if not mensaje:
            return jsonify({"error": "El mensaje es requerido"}), 400

        # Crear la nueva notificación
        nueva_notificacion = Notificacion(
            mensaje=mensaje,
            cliente_id=cliente_id
        )

        # Guardar la notificación en la base de datos
        db.session.add(nueva_notificacion)
        db.session.commit()

        return jsonify({"mensaje": "Notificación agregada exitosamente", "notificacion": nueva_notificacion.serialize()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Ha ocurrido un error", "details": str(e)}), 500

@api.route('/notificaciones/<int:notificacion_id>/marcar-leida', methods=['PUT'])
# @jwt_required()
def marcar_notificacion_leida(notificacion_id):
    try:
        # Buscar la notificación por ID
        notificacion = Notificacion.query.get(notificacion_id)
        if not notificacion:
            return jsonify({"error": "Notificación no encontrada"}), 404

        # Marcar la notificación como leída
        notificacion.leida = True

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({"mensaje": "Notificación marcada como leída", "notificacion": notificacion.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Ha ocurrido un error", "details": str(e)}), 500
    
#                                                       DEPOSITOS RETIROS Y TRANSFERENCIAS

@api.route('/transaccion/deposito', methods=['POST'])
def realizar_deposito():
    data = request.get_json()

    # Datos de la transacción
    cuenta_id = data.get("cuenta_id")
    monto = data.get("monto")
    descripcion = data.get("descripcion", "Depósito")

    # Validaciones básicas
    if not cuenta_id or not monto:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        # Obtener la cuenta
        cuenta = Cuenta.query.get(cuenta_id)
        if not cuenta:
            return jsonify({"error": "Cuenta no encontrada"}), 404

        # Crear la transacción de depósito
        transaccion = Transaccion(
            cuenta_id=cuenta_id,
            tipo="depósito",
            monto=monto,
            descripcion=descripcion,
            fecha=datetime.utcnow()
        )
        db.session.add(transaccion)

        # Actualizar el saldo de la cuenta
        cuenta.saldo += monto

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({
            "mensaje": "Depósito realizado exitosamente",
            "saldo_actual": cuenta.saldo,
            "transaccion": transaccion.serialize()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@api.route('/transaccion/retiro', methods=['POST'])
def realizar_retiro():
    data = request.get_json()

    # Datos de la transacción
    cuenta_id = data.get("cuenta_id")
    monto = data.get("monto")
    descripcion = data.get("descripcion", "Retiro")

    # Validaciones básicas
    if not cuenta_id or not monto:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        # Obtener la cuenta
        cuenta = Cuenta.query.get(cuenta_id)
        if not cuenta:
            return jsonify({"error": "Cuenta no encontrada"}), 404

        # Verificar que haya saldo suficiente
        if cuenta.saldo < monto:
            return jsonify({"error": "Saldo insuficiente"}), 400

        # Crear la transacción de retiro
        transaccion = Transaccion(
            cuenta_id=cuenta_id,
            tipo="retiro",
            monto=monto,
            descripcion=descripcion,
            fecha=datetime.utcnow()
        )
        db.session.add(transaccion)

        # Actualizar el saldo de la cuenta
        cuenta.saldo -= monto

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({
            "mensaje": "Retiro realizado exitosamente",
            "saldo_actual": cuenta.saldo,
            "transaccion": transaccion.serialize()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/transaccion/transferencia', methods=['POST'])
def realizar_transferencia():
    data = request.get_json()

    # Datos de la transferencia
    cuenta_origen_id = data.get("cuenta_origen_id")
    cuenta_destino_id = data.get("cuenta_destino_id")
    monto = data.get("monto")
    descripcion = data.get("descripcion", "Transferencia entre cuentas")

    # Validaciones básicas
    if not cuenta_origen_id or not cuenta_destino_id or not monto:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        # Obtener las cuentas
        cuenta_origen = Cuenta.query.get(cuenta_origen_id)
        cuenta_destino = Cuenta.query.get(cuenta_destino_id)

        if not cuenta_origen or not cuenta_destino:
            return jsonify({"error": "Cuenta no encontrada"}), 404

        # Verificar que haya saldo suficiente en la cuenta origen
        if cuenta_origen.saldo < monto:
            return jsonify({"error": "Saldo insuficiente en la cuenta origen"}), 400

        # Crear transacción de retiro en la cuenta origen
        transaccion_origen = Transaccion(
            cuenta_id=cuenta_origen_id,
            tipo="transferencia",
            monto=monto,
            descripcion=f"Transferencia a cuenta {cuenta_destino.numero_cuenta}"
        )
        db.session.add(transaccion_origen)

        # Crear transacción de depósito en la cuenta destino
        transaccion_destino = Transaccion(
            cuenta_id=cuenta_destino_id,
            tipo="depósito",
            monto=monto,
            descripcion=f"Transferencia desde cuenta {cuenta_origen.numero_cuenta}"
        )
        db.session.add(transaccion_destino)

        # Actualizar los saldos de las cuentas
        cuenta_origen.saldo -= monto
        cuenta_destino.saldo += monto

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({
            "mensaje": "Transferencia realizada exitosamente",
            "saldo_origen": cuenta_origen.saldo,
            "saldo_destino": cuenta_destino.saldo,
            "transaccion_origen": transaccion_origen.serialize(),
            "transaccion_destino": transaccion_destino.serialize()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500   

#                                                   ENVIO DE CODIGO Y VERIFICACIONES POR EMAIL

# Endpoint para codigo de seguridad
@api.route('/send-code', methods=['POST'])
def send_code():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email es requerido'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Generar código de seguridad
    code = f"{random.randint(100000, 999999)}"
    user.reset_code = code
    # user.code_expires = datetime.now(timezone.utc) + timedelta(minutes=10)  # Código válido por 10 minutos

    # Guardar cambios en la base de datos
    db.session.commit()

    # Enviar correo
    msg = Message('Código de seguridad para restablecer tu contraseña en Geek-Bank',
                  recipients=[email])
    msg.body = (
        f"Hola,\n\n"
        f"Hemos recibido una solicitud para restablecer tu contraseña en Geek-Bank.\n\n"
        f"Tu código de seguridad es:\n\n"
        f"🔑 **{code}** 🔑\n\n" 
        f"Por favor, introduce este código en nuestra página web para completar el proceso de recuperación de tu cuenta.\n\n"
        f"Este código es válido por 10 minutos.\n\n"
        f"⚠️ *Nota importante:* Si no solicitaste este código, es posible que alguien haya intentado acceder a tu cuenta. "
        f"Te recomendamos ignorar este mensaje y, si tienes alguna duda, contacta con nuestro equipo de soporte a la brevedad.\n\n"
        f"¡Gracias por confiar en Geek-Bank!\n\n"
        f"Atentamente,\n"
        f"El equipo de Geek-Bank")

    get_mail().send(msg)
    return jsonify({'message': 'Código enviado exitosamente', 'code': code}), 200
    
@api.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    email = data.get('email')
    code = data.get('code')

    if not email or not code:
        return jsonify({'error': 'Email y código son requeridos'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    if user.reset_code != code:
        return jsonify({'error': 'Código incorrecto'}), 400
    return jsonify({'message': 'Código verificado correctamente'}), 200

@api.route('/data', methods=['GET'])
def get_data():
    # Ejemplo de datos
    data = [
    {"date": "2023-01-01", "price": 100},
    {"date": "2023-01-02", "price": 102},
    {"date": "2023-01-03", "price": 101},
    {"date": "2023-01-04", "price": 105},
    {"date": "2023-01-05", "price": 98},
    {"date": "2023-01-06", "price": 99},
    {"date": "2023-01-07", "price": 103},
    {"date": "2023-01-08", "price": 104},
    {"date": "2023-01-09", "price": 98},
    {"date": "2023-01-10", "price": 100},
    {"date": "2023-01-11", "price": 107},
    {"date": "2023-01-12", "price": 101},
    {"date": "2023-01-13", "price": 102},
    {"date": "2023-01-14", "price": 106},
    {"date": "2023-01-15", "price": 103},
    {"date": "2023-01-16", "price": 107},
    {"date": "2023-01-17", "price": 108},
    {"date": "2023-01-18", "price": 105},
    {"date": "2023-01-19", "price": 106},
    {"date": "2023-01-20", "price": 109},
    {"date": "2023-01-21", "price": 104},
    {"date": "2023-01-22", "price": 103},
    {"date": "2023-01-23", "price": 108},
    {"date": "2023-01-24", "price": 110},
    {"date": "2023-01-25", "price": 111},
    {"date": "2023-01-26", "price": 112},
    {"date": "2023-01-27", "price": 109},
    {"date": "2023-01-28", "price": 107},
    {"date": "2023-01-29", "price": 106},
    {"date": "2023-01-30", "price": 108},
    {"date": "2023-01-31", "price": 111},
    {"date": "2023-02-01", "price": 113},
    {"date": "2023-02-02", "price": 115},
    {"date": "2023-02-03", "price": 112},
    {"date": "2023-02-04", "price": 111},
    {"date": "2023-02-05", "price": 113},
    {"date": "2023-02-06", "price": 116},
    {"date": "2023-02-07", "price": 114},
    {"date": "2023-02-08", "price": 115},
    {"date": "2023-02-09", "price": 113}
]
    return jsonify(data)

@api.route('/market-data', methods=['GET'])
def get_market_data():
    try:
        # Parámetros desde el cliente
        symbol = request.args.get('symbol', default='AAPL', type=str)
        resolution = request.args.get('resolution', default='D', type=str)
        from_date = request.args.get('from', type=int)
        to_date = request.args.get('to', type=int)
        
        # Verifica si los parámetros necesarios están presentes
        if not from_date or not to_date:
            return jsonify({"error": "Faltan parámetros 'from' y 'to'"}), 400

        # URL de la API de Finnhub
        url = f"https://finnhub.io/api/v1/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": resolution,
            "from": from_date,
            "to": to_date,
            "token": os.getenv("FINNHUB_API_KEY"),  # Tu clave de la API
        }

        # Solicitud a Finnhub
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return jsonify({"error": "Error al obtener datos de Finnhub", "details": response.json()}), response.status_code
        
        # Devuelve los datos al frontend
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": "Ocurrió un error", "details": str(e)}), 500