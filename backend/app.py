"""
MultiOficios Microservice Backend
Framework: Flask + SQLAlchemy (SQLite) + Flask-CORS
Author: MultiOficios Engineering Team
"""

import os
import math
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Colaborador, ObraContratada, MensajeChat, PagoCustodia, Valoracion

def seed_initial_data():
    """Siembra perfiles verificados de Bogotá para iniciar la base de datos"""
    colaboradores_iniciales = [
        Colaborador(
            nombre="Hernán Darío Velásquez",
            avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&auto=format&fit=crop&q=80",
            especialidad="Maestro Carpintero, Ebanista y Muebles Modulares",
            categoria="carpinteria",
            lat=4.6295, lng=-74.1520,
            barrio="Kennedy / Castilla",
            ciudad="Bogotá D.C.",
            calificacion=4.9,
            total_resenas=31,
            anos_experiencia=14,
            obras_completadas=39,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=125000,
            tarifa_hora=25000,
            bio="14 años de experiencia fabricando, armando e instalando cocinas integrales, closets empotrados y cerraduras de seguridad.",
            arl_nivel="Riesgo III",
            herramientas_json=json.dumps(["Sierra circular DeWalt", "Taladro percutor", "Router", "Nivel láser autonivelante"]),
            telefono="3124567890"
        ),
        Colaborador(
            nombre="Javier Orlando Mora",
            avatar_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80",
            especialidad="Maestro de Obra Blanca, Albañilería y Enchapes",
            categoria="albanileria",
            lat=4.6380, lng=-74.1410,
            barrio="Mandalay / Kennedy",
            ciudad="Bogotá D.C.",
            calificacion=4.8,
            total_resenas=42,
            anos_experiencia=18,
            obras_completadas=58,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=140000,
            tarifa_hora=28000,
            bio="Especialista en instalación de porcelanato de gran formato, revoque liso, muros en drywall y remodelaciones integrales.",
            arl_nivel="Riesgo V",
            herramientas_json=json.dumps(["Cortadora de baldosa Rubi 120cm", "Bailarina compactadora", "Andamios certificados", "Taladro demoledor"]),
            telefono="3139876543"
        ),
        Colaborador(
            nombre="Carlos Eduardo Pineda",
            avatar_url="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&auto=format&fit=crop&q=80",
            especialidad="Técnico Plomero Hidrosanitario y Destapes",
            categoria="plomeria",
            lat=4.6410, lng=-74.1350,
            barrio="Américas Occidental",
            ciudad="Bogotá D.C.",
            calificacion=4.95,
            total_resenas=53,
            anos_experiencia=11,
            obras_completadas=74,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=130000,
            tarifa_hora=26000,
            bio="Especialista en termofusión PPR, detección de fugas no visibles con geófono ultrasónico y destapes sin romper.",
            arl_nivel="Riesgo III",
            herramientas_json=json.dumps(["Termofusora digital", "Sonda eléctrica Ridgid K-45", "Detector geófono de fugas"]),
            telefono="3102345678"
        ),
        Colaborador(
            nombre="Nelson Enrique Fajardo",
            avatar_url="https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=300&auto=format&fit=crop&q=80",
            especialidad="Técnico Electricista Certificado Contec / Retie",
            categoria="electricidad",
            lat=4.6490, lng=-74.1200,
            barrio="Puente Aranda / Ciudad Montes",
            ciudad="Bogotá D.C.",
            calificacion=4.9,
            total_resenas=29,
            anos_experiencia=9,
            obras_completadas=41,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=135000,
            tarifa_hora=27000,
            bio="Instalaciones eléctricas residenciales y comerciales bajo norma RETIE. Cuadros de breakers, balanceo de cargas y cableado estructurado.",
            arl_nivel="Riesgo IV",
            herramientas_json=json.dumps(["Multímetro Fluke profesional", "Pinza voltiamperimétrica", "Probador de aislamiento Megger", "Ponchadora hidráulica"]),
            telefono="3158765432"
        ),
        Colaborador(
            nombre="Luz Marina Cárdenas",
            avatar_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80",
            especialidad="Especialista en Pintura Airless, Estuco y Resinas Epóxicas",
            categoria="pintura",
            lat=4.6210, lng=-74.1600,
            barrio="Timiza / Kennedy",
            ciudad="Bogotá D.C.",
            calificacion=4.85,
            total_resenas=24,
            anos_experiencia=8,
            obras_completadas=33,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=120000,
            tarifa_hora=24000,
            bio="Acabados estéticos de alta gama para fachadas, apartamentos y oficinas. Manejo de turbina Airless para aplicación uniforme y sin goteos.",
            arl_nivel="Riesgo III",
            herramientas_json=json.dumps(["Equipo de pulverización Airless Wagner", "Lijadora de paredes con aspiradora HEPA", "Pistola de calor"]),
            telefono="3171234567"
        ),
        Colaborador(
            nombre="Gustavo Adolfo Rincón",
            avatar_url="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&auto=format&fit=crop&q=80",
            especialidad="Técnico Especialista en Cerrajería Residencial y Digital",
            categoria="cerrajeria",
            lat=4.6550, lng=-74.1100,
            barrio="Salitre / Teusaquillo",
            ciudad="Bogotá D.C.",
            calificacion=4.92,
            total_resenas=37,
            anos_experiencia=12,
            obras_completadas=52,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=125000,
            tarifa_hora=25000,
            bio="Aperturas de emergencia sin daño, instalación de cerraduras digitales Yale, Samsung y de seguridad multipunto con cilindros antibumping.",
            arl_nivel="Riesgo II",
            herramientas_json=json.dumps(["Máquina duplicadora computarizada", "Ganzúas profesionales", "Taladro angular para cerrajería"]),
            telefono="3186543210"
        ),
        Colaborador(
            nombre="Brayan Camilo Suárez",
            avatar_url="https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=300&auto=format&fit=crop&q=80",
            especialidad="Técnico de Soporte, Redes y Mantenimiento de Computadores",
            categoria="computadores",
            lat=4.6620, lng=-74.1380,
            barrio="Modelia / Fontibón",
            ciudad="Bogotá D.C.",
            calificacion=4.9,
            total_resenas=28,
            anos_experiencia=7,
            obras_completadas=45,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=110000,
            tarifa_hora=22000,
            bio="Mantenimiento preventivo y correctivo de PC torre y portátiles. Cambio de pastas térmicas, optimización SSD, cableado estructurado Cat 6A y Wi-Fi Mesh.",
            arl_nivel="Riesgo I",
            herramientas_json=json.dumps(["Tester de red Fluke", "Estación de soldadura SMD", "Soplador antiestático", "Herramientas iFixit Pro"]),
            telefono="3163456789"
        ),
        Colaborador(
            nombre="Wilson Alirio Cárdenas",
            avatar_url="https://images.unsplash.com/photo-1540569014015-19a7be504e3a?w=300&auto=format&fit=crop&q=80",
            especialidad="Soldador Calificado 3G/4G SMAW & MIG Estructuras Metálicas",
            categoria="soldadura",
            lat=4.6050, lng=-74.1800,
            barrio="Bosa Carbonell",
            ciudad="Bogotá D.C.",
            calificacion=4.88,
            total_resenas=22,
            anos_experiencia=15,
            obras_completadas=36,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=145000,
            tarifa_hora=29000,
            bio="Fabricación y montaje de barandas, cerramientos, portones corredizos, vigas y pérgolas con acabados anticorrosivos de alta durabilidad.",
            arl_nivel="Riesgo V",
            herramientas_json=json.dumps(["Inversor de soldadura 250A Bi-voltaje", "Pulidora DeWalt 9 pulgadas", "Careta fotosensible 4 sensores"]),
            telefono="3147890123"
        ),
        Colaborador(
            nombre="Rodrigo Alberto Salamanca",
            avatar_url="https://images.unsplash.com/photo-1560250097-0b93528c311a?w=300&auto=format&fit=crop&q=80",
            especialidad="Técnico Especialista en Lavadoras, Secadoras y Centros de Lavado",
            categoria="lavadoras",
            lat=4.6390, lng=-74.1480,
            barrio="Kennedy / Castilla",
            ciudad="Bogotá D.C.",
            calificacion=4.95,
            total_resenas=46,
            anos_experiencia=13,
            obras_completadas=84,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=110000,
            tarifa_hora=25000,
            bio="13 años reparando lavadoras inverter y tradicionales Whirlpool, Haceb, LG y Samsung. Diagnóstico de tarjetas electrónicas, cambio de transmisiones y bombas de desagüe.",
            arl_nivel="Riesgo III",
            herramientas_json=json.dumps(["Extractor de poleas", "Multímetro inverter", "Manómetro hidrostático", "Juego de llaves de copa"]),
            telefono="3112345678"
        ),
        Colaborador(
            nombre="Edgar Mauricio Peñuela",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&auto=format&fit=crop&q=80",
            especialidad="Técnico Frigorista Certificado - Neveras y Nevecones",
            categoria="neveras",
            lat=4.6520, lng=-74.1120,
            barrio="Teusaquillo / Salitre",
            ciudad="Bogotá D.C.",
            calificacion=4.9,
            total_resenas=39,
            anos_experiencia=16,
            obras_completadas=72,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=130000,
            tarifa_hora=30000,
            bio="Refrigeración doméstica y comercial: neveras No Frost, Nevecones Side by Side Samsung, LG, Mabe y Haceb. Recarga de gas ecológico R600a/R134a y cambio de compresores.",
            arl_nivel="Riesgo III",
            herramientas_json=json.dumps(["Bomba de vacío Robinair", "Manifold 4 vías", "Detector fugas halogenadas", "Equipo de soldadura oxi-gas"]),
            telefono="3145678901"
        ),
        Colaborador(
            nombre="Diego Armando Cifuentes",
            avatar_url="https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=300&auto=format&fit=crop&q=80",
            especialidad="Mecánico Automotriz a Domicilio - Mecánica Rápida y Scanner",
            categoria="mecanica_rapida",
            lat=4.6720, lng=-74.1450,
            barrio="Fontibón / Modelia",
            ciudad="Bogotá D.C.",
            calificacion=4.92,
            total_resenas=51,
            anos_experiencia=11,
            obras_completadas=95,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=140000,
            tarifa_hora=35000,
            bio="Mecánica preventiva y rápida en tu parqueadero o domicilio. Diagnóstico por escáner OBD2, cambio de pastillas y discos de freno, aceite y filtros, bujías y correas.",
            arl_nivel="Riesgo IV",
            herramientas_json=json.dumps(["Escáner OBD2 Launch X431", "Torquímetro de precisión", "Gato caimán 3T", "Compresor portátil"]),
            telefono="3208901234"
        ),
        Colaborador(
            nombre="Valeria Sofía Restrepo",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&auto=format&fit=crop&q=80",
            especialidad="Estilista Profesional & Barbería - Corte, Color y Tratamientos",
            categoria="corte_belleza",
            lat=4.6460, lng=-74.0620,
            barrio="Chapinero Central",
            ciudad="Bogotá D.C.",
            calificacion=4.98,
            total_resenas=64,
            anos_experiencia=10,
            obras_completadas=120,
            es_verificado=True,
            disponibilidad="disponible_hoy",
            tarifa_jornal=110000,
            tarifa_hora=30000,
            bio="Estilista integral y barbera profesional a domicilio. Cortes modernos para dama, caballero y niños, diseño de barba con toalla caliente, cepillados y keratina orgánica.",
            arl_nivel="Riesgo I",
            herramientas_json=json.dumps(["Máquinas Wahl y BaByliss Pro", "Tijeras cobalto 440C", "Secador iónico Parlux", "Esterilizador UV portátil"]),
            telefono="3017654321"
        )
    ]

    for colab in colaboradores_iniciales:
        db.session.add(colab)
    db.session.commit()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Base de datos SQLite alojada en la carpeta /datos persistida por volumen Docker
    db_path = os.environ.get('DATABASE_URL', 'sqlite:////app/datos/multioficios.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'multioficios-secret-key-2026')

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
            # Sembrar datos iniciales si la tabla de colaboradores está vacía
            if Colaborador.query.count() == 0:
                seed_initial_data()
        except Exception as e:
            # En SQLite con múltiples workers gunicorn concurrentes, si ya existe o está bloqueada, continuar
            app.logger.warning(f"Aviso inicialización DB SQLite: {e}")

    # --------------------------------------------------------------------------
    # Health Check & API Discovery
    # --------------------------------------------------------------------------
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "microservice": "MultiOficios Core Engine",
            "database": "SQLite 3.45 (WAL Mode)",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat()
        })

    # --------------------------------------------------------------------------
    # Colaboradores & Geolocalización (Fórmula de Haversine)
    # --------------------------------------------------------------------------
    @app.route('/api/colaboradores', methods=['GET'])
    def get_colaboradores():
        lat = float(request.args.get('lat', 4.6345))
        lng = float(request.args.get('lng', -74.1458))
        radius_km = float(request.args.get('radius_km', 25.0))
        category = request.args.get('category', None)
        query = request.args.get('q', '').lower()

        all_colabs = Colaborador.query.all()
        results = []

        for c in all_colabs:
            # Cálculo de distancia Haversine
            dlat = math.radians(c.lat - lat)
            dlng = math.radians(c.lng - lng)
            a = (math.sin(dlat / 2) ** 2 +
                 math.cos(math.radians(lat)) * math.cos(math.radians(c.lat)) *
                 math.sin(dlng / 2) ** 2)
            c_dist = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            dist_km = round(6371 * c_dist, 1)

            if dist_km <= radius_km:
                if category and category != 'todos' and c.categoria != category:
                    continue
                if query and (query not in c.nombre.lower() and query not in c.especialidad.lower()):
                    continue

                colab_dict = c.to_dict()
                colab_dict['distancia_km'] = dist_km
                results.append(colab_dict)

        results.sort(key=lambda x: x['distancia_km'])
        return jsonify({
            "total": len(results),
            "radio_km": radius_km,
            "colaboradores": results
        })

    @app.route('/api/colaboradores/<int:colaborador_id>', methods=['GET'])
    def get_colaborador_detail(colaborador_id):
        colab = Colaborador.query.get_or_404(colaborador_id)
        return jsonify(colab.to_dict(include_reviews=True))

    # --------------------------------------------------------------------------
    # Obras, Contratos por Obra o Labor & Custodia Segura (Escrow)
    # --------------------------------------------------------------------------
    @app.route('/api/obras', methods=['GET'])
    def get_obras():
        cliente_id = request.args.get('cliente_id', 'user-me')
        obras = ObraContratada.query.filter_by(cliente_id=cliente_id).all()
        return jsonify([o.to_dict() for o in obras])

    @app.route('/api/obras/contratar', methods=['POST'])
    def contratar_obra():
        data = request.get_json()
        if not data:
            return jsonify({"error": "Payload inválido"}), 400

        nueva_obra = ObraContratada(
            cliente_id=data.get('cliente_id', 'user-me'),
            cliente_nombre=data.get('cliente_nombre', 'Cliente MultiOficios'),
            colaborador_id=data['colaborador_id'],
            tipo_servicio=data.get('tipo_servicio', 'jornal'),
            descripcion=data['descripcion'],
            direccion=data.get('direccion', 'Bogotá D.C.'),
            lat=data.get('lat', 4.6345),
            lng=data.get('lng', -74.1458),
            monto_base=data['monto_base'],
            tarifa_arl=data.get('tarifa_arl', 12000),
            tarifa_custodia=data.get('tarifa_custodia', 8000),
            monto_total=data['monto_total'],
            estado='fondos_en_custodia'
        )

        pago = PagoCustodia(
            obra=nueva_obra,
            monto=data['monto_total'],
            metodo=data.get('metodo_pago', 'pse'),
            estado_custodia='fondos_retenidos'
        )

        db.session.add(nueva_obra)
        db.session.add(pago)
        db.session.commit()

        return jsonify({
            "mensaje": "Contrato creado con éxito. Fondos retenidos bajo custodia fiduciaria.",
            "obra": nueva_obra.to_dict()
        }), 201

    @app.route('/api/obras/<int:obra_id>/actualizar-estado', methods=['PATCH'])
    def actualizar_estado_obra(obra_id):
        obra = ObraContratada.query.get_or_404(obra_id)
        data = request.get_json()
        nuevo_estado = data.get('estado')
        nota = data.get('nota', '')

        obra.estado = nuevo_estado
        obra.agregar_actualizacion(nuevo_estado, nota)
        db.session.commit()

        return jsonify({
            "mensaje": f"Estado de la obra actualizado a {nuevo_estado}",
            "obra": obra.to_dict()
        })

    @app.route('/api/obras/<int:obra_id>/liberar-fondos', methods=['POST'])
    def liberar_fondos_obra(obra_id):
        obra = ObraContratada.query.get_or_404(obra_id)
        obra.estado = 'finalizado'
        if obra.pago:
            obra.pago.estado_custodia = 'liberado_al_colaborador'
            obra.pago.fecha_liberacion = datetime.utcnow()

        obra.agregar_actualizacion('finalizado', 'Acta de entrega digital firmada a satisfacción por el cliente. Fondos dispersados al colaborador.')
        db.session.commit()

        return jsonify({
            "mensaje": "Fondos en custodia liberados exitosamente.",
            "obra": obra.to_dict()
        })

    # --------------------------------------------------------------------------
    # Chat Privado E2EE
    # --------------------------------------------------------------------------
    @app.route('/api/chat/<int:obra_id>/mensajes', methods=['GET', 'POST'])
    def chat_mensajes(obra_id):
        if request.method == 'GET':
            mensajes = MensajeChat.query.filter_by(obra_id=obra_id).order_by(MensajeChat.timestamp.asc()).all()
            return jsonify([m.to_dict() for m in mensajes])
        else:
            data = request.get_json()
            nuevo_msg = MensajeChat(
                obra_id=obra_id,
                remitente_id=data['remitente_id'],
                remitente_rol=data['remitente_rol'],
                texto=data['texto'],
                es_cifrado=True
            )
            db.session.add(nuevo_msg)
            db.session.commit()
            return jsonify(nuevo_msg.to_dict()), 201

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
