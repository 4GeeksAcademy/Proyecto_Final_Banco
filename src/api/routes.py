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
from datetime import datetime, timezone, timedelta




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

#                                  REGISTRO, LOGIN, IFORMACION DE USUARIO Y MODIFICACION DE USUARIO

@api.route('/User/Register', methods=['POST'])
def addUser():
    data = request.get_json()
    print('desde routes', data)

    # Datos del usuario
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    is_active = data.get("is_active", True)

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
        db.session.flush()  
        print("Usuario creado:", new_user)

        # Crear cliente asociado al usuario
        print("Creando cliente...")
        nuevo_cliente = Cliente(
            nombre=name,
            apellidos="Introduzca apellido",
            telefono="Introduzca numero",
            direccion="Introduzca direccion",
        )
        db.session.add(nuevo_cliente)
        db.session.flush() 
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
            saldo=0,  # Saldo inicial en 0
            saldo_retenido=0,
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
            {"tipo": "retiro", "monto": -200.00, "descripcion": "Retiro en cajero"},
            {"tipo": "transferencia", "monto": -300.00, "descripcion": "Transferencia a otro usuario"},
            {"tipo": "depósito", "monto": 500.00, "descripcion": "Depósito de salario"},
            {"tipo": "retiro", "monto": -100.00, "descripcion": "Compra en tienda"},
        ]

        for transaccion_data in tipos_transacciones:
            # Guardamos el saldo anterior
            saldo_anterior = nueva_cuenta.saldo

            # Actualizamos el saldo de la cuenta según el tipo de transacción
            if transaccion_data["tipo"] == "depósito":
                nueva_cuenta.saldo += transaccion_data["monto"]
            elif transaccion_data["tipo"] == "retiro":
                if nueva_cuenta.saldo >= abs(transaccion_data["monto"]):  # Verificar saldo suficiente
                    nueva_cuenta.saldo += transaccion_data["monto"] 
                else:
                    raise ValueError("Saldo insuficiente para realizar el retiro")
            elif transaccion_data["tipo"] == "transferencia":
                if nueva_cuenta.saldo >= abs(transaccion_data["monto"]):  # Verificar saldo suficiente
                    nueva_cuenta.saldo += transaccion_data["monto"]
                else:
                    raise ValueError("Saldo insuficiente para realizar la transferencia")
            else:
                raise ValueError("Tipo de transacción no válido")

            # Guardar el saldo posterior
            saldo_posterior = nueva_cuenta.saldo

            # Crear la transacción
            nueva_transaccion = Transaccion(
                cuenta_id=nueva_cuenta.id,
                tipo=transaccion_data["tipo"],
                monto=transaccion_data["monto"],
                descripcion=transaccion_data["descripcion"],
                fecha=datetime.now(timezone.utc),
                saldo_anterior=saldo_anterior,
                saldo_posterior=saldo_posterior
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
        
        cuenta = cliente.cuentas[0] 

        # Obtener transacciones de la cuenta
        transacciones_data = [
            {
                "id": transaccion.id,
                "tipo": transaccion.tipo,
                "monto": float(transaccion.monto),
                "fecha": transaccion.fecha.isoformat(),
                "descripcion": transaccion.descripcion,
                "saldo_anterior": float(transaccion.saldo_anterior),
                "saldo_posterior": float(transaccion.saldo_posterior)
            }
            for transaccion in cuenta.transacciones
        ]

        tarjeta_coordenadas_data = [
            {
                "posicion": coord.posicion,
                "valor": coord.valor 
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
                "nombre": cliente.nombre,
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
    nombre = perfil.get("nombre")
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
    if nombre:
        cliente.nombre = nombre
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

#                                                             CONFIGURACION DEL USUARIO

@api.route('/update_config', methods=['POST'])
def update_config():
    data = request.get_json()
    user_id = data.get('user_id')  # ID del User
    modo_oscuro = data.get('modo_oscuro')
    ocultar_saldo = data.get('ocultar_saldo')

    config = ConfiguracionUsuario.query.filter_by(id_usuario=user_id).first()
    if config:
        config.modo_oscuro = modo_oscuro
        config.ocultar_saldo = ocultar_saldo
        db.session.commit()
        return jsonify({"message": "Configuración actualizada correctamente"}), 200
    else:
        return jsonify({"error": "Configuración no encontrada"}), 404
    
@api.route('/api/get_config', methods=['GET'])
def get_config():
    user_id = request.args.get('user_id')  # ID del User
    config = ConfiguracionUsuario.query.filter_by(id_usuario=user_id).first()
    if config:
        return jsonify(config.serialize()), 200
    else:
        return jsonify({"error": "Configuración no encontrada"}), 404

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
    monto = abs(data.get("monto"))  # Asegurarse de que el monto sea positivo
    descripcion = data.get("descripcion", "Depósito")

    # Validaciones básicas
    if not cuenta_id or not monto:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        # Obtener la cuenta
        cuenta = Cuenta.query.get(cuenta_id)
        if not cuenta:
            return jsonify({"error": "Cuenta no encontrada"}), 404

        # Guardar el saldo anterior
        saldo_anterior = cuenta.saldo

        # Actualizar el saldo de la cuenta
        cuenta.saldo += monto

        # Guardar el saldo posterior
        saldo_posterior = cuenta.saldo

        # Crear la transacción de depósito
        transaccion = Transaccion(
            cuenta_id=cuenta_id,
            tipo="depósito",
            monto=monto,  # Monto positivo
            descripcion=descripcion,
            fecha=datetime.now(timezone.utc),
            saldo_anterior=saldo_anterior,  # Saldo antes de la transacción
            saldo_posterior=saldo_posterior  # Saldo después de la transacción
        )
        db.session.add(transaccion)

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
    monto = -abs(data.get("monto"))  # Asegurarse de que el monto sea negativo
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
        if cuenta.saldo < abs(monto):
            return jsonify({"error": "Saldo insuficiente"}), 400

        # Guardar el saldo anterior
        saldo_anterior = cuenta.saldo

        # Actualizar el saldo de la cuenta (sumar el monto negativo)
        cuenta.saldo += monto  # Aquí se suma el monto negativo

        # Guardar el saldo posterior
        saldo_posterior = cuenta.saldo

        # Crear la transacción de retiro
        transaccion = Transaccion(
            cuenta_id=cuenta_id,
            tipo="retiro",
            monto=monto,  # Monto negativo
            descripcion=descripcion,
            fecha=datetime.now(timezone.utc),
            saldo_anterior=saldo_anterior,  # Saldo antes de la transacción
            saldo_posterior=saldo_posterior  # Saldo después de la transacción
        )
        db.session.add(transaccion)

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
    numero_cuenta_destino = data.get("numero_cuenta_destino")
    monto = abs(data.get("monto"))
    descripcion = data.get("descripcion", "Transferencia entre cuentas")

    try:
        # Obtener cuentas
        cuenta_origen = Cuenta.query.get(cuenta_origen_id)
        cuenta_destino = Cuenta.query.filter_by(numero_cuenta=numero_cuenta_destino).first()

        # Validaciones
        if not cuenta_origen or not cuenta_destino:
            return jsonify({"error": "Cuenta no encontrada"}), 404

        if cuenta_origen.saldo < monto:
            return jsonify({"error": "Saldo insuficiente"}), 400

        # Realizar transferencia
        cuenta_origen.saldo -= monto
        cuenta_destino.saldo += monto

        # Crear transacciones
        transaccion_origen = Transaccion(
            cuenta_id=cuenta_origen.id,
            tipo="transferencia",
            monto=-monto,
            descripcion=f"Transferencia a cuenta {cuenta_destino.numero_cuenta}",
            saldo_anterior=cuenta_origen.saldo + monto,
            saldo_posterior=cuenta_origen.saldo
        )

        transaccion_destino = Transaccion(
            cuenta_id=cuenta_destino.id,
            tipo="depósito",
            monto=monto,
            descripcion=f"Transferencia desde cuenta {cuenta_origen.numero_cuenta}",
            saldo_anterior=cuenta_destino.saldo - monto,
            saldo_posterior=cuenta_destino.saldo
        )

        # Crear notificaciones
        notificacion_remitente = Notificacion(
            mensaje=f"Transferencia enviada de {monto}€ a cuenta {cuenta_destino.numero_cuenta}",
            cliente_id=cuenta_origen.cliente_id
        )

        notificacion_destinatario = Notificacion(
            mensaje=f"Transferencia recibida de {monto}€ desde cuenta {cuenta_origen.numero_cuenta}",
            cliente_id=cuenta_destino.cliente_id
        )

        # Guardar todo en la base de datos
        db.session.add_all([
            transaccion_origen,
            transaccion_destino,
            notificacion_remitente,
            notificacion_destinatario
        ])
        
        db.session.commit()

        return jsonify({
            "mensaje": "Transferencia exitosa",
            "saldo_origen": cuenta_origen.saldo,
            "saldo_destino": cuenta_destino.saldo,
            "notificaciones": {
                "remitente": notificacion_remitente.serialize(),
                "destinatario": notificacion_destinatario.serialize()
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# @api.route('/transaccion/transferencia', methods=['POST'])
# def realizar_transferencia():
#     data = request.get_json()

#     # Datos de la transferencia
#     cuenta_origen_id = data.get("cuenta_origen_id")
#     cuenta_destino_id = data.get("cuenta_destino_id")
#     monto = abs(data.get("monto"))  # Asegurarse de que el monto sea positivo
#     descripcion = data.get("descripcion", "Transferencia entre cuentas")

#     # Validaciones básicas
#     if not cuenta_origen_id or not cuenta_destino_id or not monto:
#         return jsonify({"error": "Faltan datos obligatorios"}), 400

#     try:
#         # Obtener las cuentas
#         cuenta_origen = Cuenta.query.get(cuenta_origen_id)
#         cuenta_destino = Cuenta.query.get(cuenta_destino_id)

#         if not cuenta_origen or not cuenta_destino:
#             return jsonify({"error": "Cuenta no encontrada"}), 404

#         # Verificar que haya saldo suficiente en la cuenta origen
#         if cuenta_origen.saldo < monto:
#             return jsonify({"error": "Saldo insuficiente en la cuenta origen"}), 400

#         # Guardar los saldos anteriores
#         saldo_anterior_origen = cuenta_origen.saldo
#         saldo_anterior_destino = cuenta_destino.saldo

#         # Actualizar los saldos de las cuentas
#         cuenta_origen.saldo -= monto
#         cuenta_destino.saldo += monto

#         # Guardar los saldos posteriores
#         saldo_posterior_origen = cuenta_origen.saldo
#         saldo_posterior_destino = cuenta_destino.saldo

#         # Crear transacción de retiro en la cuenta origen (monto negativo)
#         transaccion_origen = Transaccion(
#             cuenta_id=cuenta_origen_id,
#             tipo="transferencia",
#             monto=-monto,  # Monto negativo
#             descripcion=f"Transferencia a cuenta {cuenta_destino.numero_cuenta}",
#             fecha=datetime.now(timezone.utc),
#             saldo_anterior=saldo_anterior_origen,  # Saldo antes de la transacción
#             saldo_posterior=saldo_posterior_origen  # Saldo después de la transacción
            
#         )
#         db.session.add(transaccion_origen)

#         # Crear transacción de depósito en la cuenta destino (monto positivo)
#         transaccion_destino = Transaccion(
#             cuenta_id=cuenta_destino_id,
#             tipo="depósito",
#             monto=monto,  # Monto positivo
#             descripcion=f"Transferencia desde cuenta {cuenta_origen.numero_cuenta}",
#             fecha=datetime.now(timezone.utc),
#             saldo_anterior=saldo_anterior_destino,  # Saldo antes de la transacción
#             saldo_posterior=saldo_posterior_destino  # Saldo después de la transacción
#         )
#         db.session.add(transaccion_destino)

#         # Guardar los cambios en la base de datos
#         db.session.commit()

#         return jsonify({
#             "mensaje": "Transferencia realizada exitosamente",
#             "saldo_origen": cuenta_origen.saldo,
#             "saldo_destino": cuenta_destino.saldo,
#             "transaccion_origen": transaccion_origen.serialize(),
#             "transaccion_destino": transaccion_destino.serialize()
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

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

    #                                                             CODIGO PARA TARJETAS DE COORDENADAS

@api.route('/send-coordinates-code', methods=['POST'])
def send_coordinates_code():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email es requerido'}), 400

    # Buscar el usuario por email
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Generar un código de seguridad
    code = f"{random.randint(100000, 999999)}"
    user.coordinates_code = code  # Asignar el código al usuario
    user.code_expires = datetime.now(timezone.utc) + timedelta(minutes=10)  # Código válido por 10 minutos

    # Guardar cambios en la base de datos
    db.session.commit()

    # Enviar correo electrónico con el código
    msg = Message('Código para obtener tu tarjeta de coordenadas en Geek-Bank',
                  recipients=[email])
    msg.body = (
        f"Hola {user.name},\n\n"
        f"Hemos recibido una solicitud para obtener tu tarjeta de coordenadas en Geek-Bank.\n\n"
        f"Tu código de seguridad es:\n\n"
        f"🔑 **{code}** 🔑\n\n"
        f"Por favor, introduce este código en nuestra página web para acceder a tu tarjeta de coordenadas.\n\n"
        f"Este código es válido por 10 minutos.\n\n"
        f"⚠️ *Nota importante:* Si no solicitaste este código, es posible que alguien haya intentado acceder a tu cuenta. "
        f"Te recomendamos ignorar este mensaje y, si tienes alguna duda, contacta con nuestro equipo de soporte a la brevedad.\n\n"
        f"¡Gracias por confiar en Geek-Bank!\n\n"
        f"Atentamente,\n"
        f"El equipo de Geek-Bank")

    get_mail().send(msg)

    return jsonify({'message': 'Código enviado exitosamente', 'code': code}), 200

@api.route('/verify-coordinates-code', methods=['POST'])
def verify_coordinates_code():
    data = request.json
    email = data.get('email')
    code = data.get('code')

    if not email or not code:
        return jsonify({'error': 'Email y código son requeridos'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Asegúrate de que user.code_expires sea offset-aware
    if user.code_expires.tzinfo is None:
        user.code_expires = user.code_expires.replace(tzinfo=timezone.utc)

    # Compara con un datetime offset-aware
    current_time = datetime.now(timezone.utc)

    if user.coordinates_code != code or user.code_expires < current_time:
        return jsonify({'error': 'Código inválido o expirado'}), 400

    # Acceder a la cuenta a través del cliente
    if not user.cliente or not user.cliente.cuentas:
        return jsonify({'error': 'El usuario no tiene una cuenta asociada'}), 404

    # Suponiendo que un cliente tiene solo una cuenta
    cuenta = user.cliente.cuentas[0]

    # Obtener las tarjetas de coordenadas de la cuenta
    tarjeta_coordenadas = [
        {"posicion": coord.posicion, "valor": coord.valor}
        for coord in cuenta.tarjetas_coordenadas
    ]

    return jsonify({
        'message': 'Código verificado exitosamente',
        'tarjeta_coordenadas': tarjeta_coordenadas
    }), 200

@api.route('/send-coordinates-card/<int:user_id>', methods=['POST'])
def send_coordinates_card(user_id):
    try:
        # Buscar el usuario por ID
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Obtener el cliente asociado al usuario
        cliente = user.cliente
        if not cliente:
            return jsonify({"error": "El usuario no tiene un cliente asociado"}), 404

        # Obtener la única cuenta del cliente
        if not cliente.cuentas:
            return jsonify({"error": "El cliente no tiene cuentas"}), 404
        
        cuenta = cliente.cuentas[0]

        # Obtener la tarjeta de coordenadas
        tarjeta_coordenadas_data = [
            {
                "posicion": coord.posicion,
                "valor": coord.valor 
            }
            for coord in cuenta.tarjetas_coordenadas
        ]

        # Formatear la tarjeta de coordenadas para el correo electrónico
        coordenadas_formateadas = "\n".join([f"Posición {coord['posicion']}: {coord['valor']}" for coord in tarjeta_coordenadas_data])

        # Enviar correo electrónico con la tarjeta de coordenadas
        msg = Message('Tu tarjeta de coordenadas en Geek-Bank',
                      recipients=[user.email])
        msg.body = (
            f"Hola {user.name},\n\n"
            f"A continuación encontrarás tu tarjeta de coordenadas para tu cuenta en Geek-Bank:\n\n"
            f"{coordenadas_formateadas}\n\n"
            f"Guarda esta información en un lugar seguro y no la compartas con nadie.\n\n"
            f"Atentamente,\n"
            f"El equipo de Geek-Bank")

        get_mail().send(msg)
        return jsonify({'message': 'Tarjeta de coordenadas enviada exitosamente'}), 200

    except Exception as e:
        return jsonify({"error": "Ha ocurrido un error", "details": str(e)}), 500
    
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