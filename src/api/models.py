from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))  # Asumimos que será en texto plano o hasheado
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.String(200))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_nacimiento = db.Column(db.Date)
    tipo_documento = db.Column(db.String(20))
    numero_documento = db.Column(db.String(50), unique=True)
    cuentas = db.relationship("Cuenta", back_populates="cliente")
    asesor = db.relationship("Asesor", back_populates="cliente", uselist=False)
    configuracion = db.relationship("ConfiguracionUsuario", back_populates="cliente", uselist=False)

    def __repr__(self):
        return f'<Cliente {self.nombre}, Email: {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "fecha_creacion": self.fecha_creacion,
            "fecha_nacimiento": self.fecha_nacimiento,
            "tipo_documento": self.tipo_documento,
            "numero_documento": self.numero_documento,
        }


class ConfiguracionUsuario(db.Model):
    __tablename__ = 'configuracion_usuario'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    modo_oscuro = db.Column(db.Boolean, default=False)
    idioma = db.Column(db.String(5))
    componentesSave = db.Column(db.String(50))

    # Relación con Cliente
    cliente = db.relationship("Cliente", back_populates="configuracion")

    def __repr__(self):
        return f'<ConfiguracionUsuario Cliente ID: {self.id_usuario}>'

    def serialize(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "modo_oscuro": self.modo_oscuro,
            "idioma": self.idioma,
            "componentesSave": self.componentesSave,
        }


class Cuenta(db.Model):
    __tablename__ = 'cuenta'

    id = db.Column(db.Integer, primary_key=True)
    numero_cuenta = db.Column(db.String(20), unique=True)
    tipo_cuenta = db.Column(db.String(50))
    saldo = db.Column(db.Float)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    estado = db.Column(db.Integer)
    cliente = db.relationship("Cliente", back_populates="cuentas")
    transacciones = db.relationship("Transaccion", back_populates="cuenta")
    seguro_id = db.Column(db.Integer, db.ForeignKey('seguro.id'))
    seguro = db.relationship("Seguro", back_populates="cuentas")

    def __repr__(self):
        return f'<Cuenta {self.numero_cuenta}, Tipo: {self.tipo_cuenta}, Saldo: {self.saldo}>'

    def serialize(self):
        return {
            "id": self.id,
            "numero_cuenta": self.numero_cuenta,
            "tipo_cuenta": self.tipo_cuenta,
            "saldo": self.saldo,
            "estado": self.estado,
            "cliente_id": self.cliente_id,
            "seguro_id": self.seguro_id,
        }


class Transaccion(db.Model):
    __tablename__ = 'transaccion'

    id = db.Column(db.Integer, primary_key=True)
    cuenta_id = db.Column(db.Integer, db.ForeignKey('cuenta.id'))
    tipo = db.Column(db.String(50))
    monto = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.String(200))
    cuenta = db.relationship("Cuenta", back_populates="transacciones")
    tipo_transaccion_id = db.Column(db.Integer, db.ForeignKey('tipo_transaccion.id'))
    tipo_transaccion = db.relationship("TipoTransaccion", back_populates="transacciones")

    def __repr__(self):
        return f'<Transaccion {self.tipo}, Monto: {self.monto}, Fecha: {self.fecha}>'

    def serialize(self):
        return {
            "id": self.id,
            "cuenta_id": self.cuenta_id,
            "tipo": self.tipo,
            "monto": self.monto,
            "fecha": self.fecha,
            "descripcion": self.descripcion,
            "tipo_transaccion_id": self.tipo_transaccion_id,
        }


class TipoTransaccion(db.Model):
    __tablename__ = 'tipo_transaccion'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(200))
    transacciones = db.relationship("Transaccion", back_populates="tipo_transaccion")

    def __repr__(self):
        return f'<TipoTransaccion {self.nombre}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
        }


class Asesor(db.Model):
    __tablename__ = 'asesor'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    puesto = db.Column(db.String(50))
    fecha_contratacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    cliente = db.relationship("Cliente", back_populates="asesor")

    def __repr__(self):
        return f'<Asesor {self.nombre}, Puesto: {self.puesto}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "puesto": self.puesto,
            "fecha_contratacion": self.fecha_contratacion,
            "activo": self.activo,
            "cliente_id": self.cliente_id,
        }


class Seguro(db.Model):
    __tablename__ = 'seguro'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Integer)
    cuentas = db.relationship("Cuenta", back_populates="seguro")

    def __repr__(self):
        return f'<Seguro {self.tipo}>'

    def serialize(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
        }
