"""
Modelos de Datos para MultiOficios (Flask + SQLAlchemy + SQLite)
"""

from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Colaborador(db.Model):
    __tablename__ = 'colaboradores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True)
    especialidad = db.Column(db.String(150), nullable=False)
    categoria = db.Column(db.String(60), nullable=False) # albanileria, plomeria, carpinteria, etc.
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    barrio = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(60), default='Bogotá D.C.')
    calificacion = db.Column(db.Float, default=5.0)
    total_resenas = db.Column(db.Integer, default=0)
    anos_experiencia = db.Column(db.Integer, default=5)
    obras_completadas = db.Column(db.Integer, default=0)
    es_verificado = db.Column(db.Boolean, default=True)
    disponibilidad = db.Column(db.String(40), default='disponible_hoy')
    tarifa_jornal = db.Column(db.Integer, nullable=False) # COP
    tarifa_hora = db.Column(db.Integer, default=25000)
    bio = db.Column(db.Text, nullable=True)
    arl_nivel = db.Column(db.String(20), default='Riesgo III')
    herramientas_json = db.Column(db.Text, default='[]')
    telefono = db.Column(db.String(30), nullable=True)

    obras = db.relationship('ObraContratada', backref='colaborador', lazy=True)
    valoraciones = db.relationship('Valoracion', backref='colaborador', lazy=True)

    def to_dict(self, include_reviews=False):
        data = {
            "id": self.id,
            "nombre": self.nombre,
            "avatar": self.avatar_url,
            "especialidad": self.especialidad,
            "categoria": self.categoria,
            "ubicacion": {
                "lat": self.lat,
                "lng": self.lng,
                "barrio": self.barrio,
                "ciudad": self.ciudad
            },
            "calificacion": self.calificacion,
            "total_resenas": self.total_resenas,
            "anos_experiencia": self.anos_experiencia,
            "obras_completadas": self.obras_completadas,
            "es_verificado": self.es_verificado,
            "disponibilidad": self.disponibilidad,
            "tarifa_jornal": self.tarifa_jornal,
            "tarifa_hora": self.tarifa_hora,
            "bio": self.bio,
            "arl_nivel": self.arl_nivel,
            "herramientas": json.loads(self.herramientas_json) if self.herramientas_json else [],
            "telefono": self.telefono
        }
        if include_reviews:
            data["valoraciones"] = [v.to_dict() for v in self.valoraciones]
        return data

class ObraContratada(db.Model):
    __tablename__ = 'obras_contratadas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.String(80), nullable=False)
    cliente_nombre = db.Column(db.String(120), nullable=False)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaboradores.id'), nullable=False)
    tipo_servicio = db.Column(db.String(40), default='jornal') # jornal, por_obra, horas
    descripcion = db.Column(db.Text, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    monto_base = db.Column(db.Integer, nullable=False)
    tarifa_arl = db.Column(db.Integer, default=12000)
    tarifa_custodia = db.Column(db.Integer, default=8000)
    monto_total = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), default='fondos_en_custodia')
    bitacora_json = db.Column(db.Text, default='[]')
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    pago = db.relationship('PagoCustodia', backref='obra', uselist=False, lazy=True)
    mensajes = db.relationship('MensajeChat', backref='obra', lazy=True)

    def agregar_actualizacion(self, estado, nota, foto_url=None):
        bitacora = json.loads(self.bitacora_json) if self.bitacora_json else []
        bitacora.append({
            "timestamp": datetime.utcnow().strftime('%H:%M %p'),
            "estado": estado,
            "nota": nota,
            "foto_url": foto_url
        })
        self.bitacora_json = json.dumps(bitacora)

    def to_dict(self):
        return {
            "id": self.id,
            "numero_orden": f"#MO-{self.id + 10000}",
            "cliente_id": self.cliente_id,
            "cliente_nombre": self.cliente_nombre,
            "colaborador_id": self.colaborador_id,
            "tipo_servicio": self.tipo_servicio,
            "descripcion": self.descripcion,
            "direccion": self.direccion,
            "monto_total": self.monto_total,
            "estado": self.estado,
            "bitacora": json.loads(self.bitacora_json) if self.bitacora_json else [],
            "creado_en": self.creado_en.isoformat(),
            "custodia": self.pago.to_dict() if self.pago else None
        }

class PagoCustodia(db.Model):
    __tablename__ = 'pagos_custodia'

    id = db.Column(db.Integer, primary_key=True)
    obra_id = db.Column(db.Integer, db.ForeignKey('obras_contratadas.id'), nullable=False)
    monto = db.Column(db.Integer, nullable=False)
    metodo = db.Column(db.String(40), default='pse')
    estado_custodia = db.Column(db.String(50), default='fondos_retenidos') # fondos_retenidos, liberado_al_colaborador, disputa
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_liberacion = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "monto": self.monto,
            "metodo": self.metodo,
            "estado": self.estado_custodia,
            "fecha_pago": self.fecha_pago.isoformat(),
            "fecha_liberacion": self.fecha_liberacion.isoformat() if self.fecha_liberacion else None
        }

class MensajeChat(db.Model):
    __tablename__ = 'mensajes_chat'

    id = db.Column(db.Integer, primary_key=True)
    obra_id = db.Column(db.Integer, db.ForeignKey('obras_contratadas.id'), nullable=False)
    remitente_id = db.Column(db.String(80), nullable=False)
    remitente_rol = db.Column(db.String(30), nullable=False) # cliente, colaborador
    texto = db.Column(db.Text, nullable=False)
    foto_url = db.Column(db.String(255), nullable=True)
    es_cifrado = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "obra_id": self.obra_id,
            "remitente_id": self.remitente_id,
            "remitente_rol": self.remitente_rol,
            "texto": self.texto,
            "foto_url": self.foto_url,
            "es_cifrado": self.es_cifrado,
            "timestamp": self.timestamp.strftime('%H:%M %p')
        }

class Valoracion(db.Model):
    __tablename__ = 'valoraciones'

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaboradores.id'), nullable=False)
    cliente_id = db.Column(db.String(80), nullable=False)
    cliente_nombre = db.Column(db.String(120), nullable=False)
    estrellas = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_nombre": self.cliente_nombre,
            "estrellas": self.estrellas,
            "comentario": self.comentario,
            "fecha": self.fecha.strftime('%d/%m/%Y')
        }
