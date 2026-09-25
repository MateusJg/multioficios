import React, { useState } from 'react';
import { 
  X, 
  FolderGit2, 
  Server, 
  Database, 
  FileCode, 
  Terminal, 
  Globe, 
  CheckCircle2, 
  Copy, 
  Download,
  Layers,
  Cloud
} from 'lucide-react';

interface DockerArchitectureModalProps {
  onClose: () => void;
}

export const DockerArchitectureModal: React.FC<DockerArchitectureModalProps> = ({ onClose }) => {
  const [activeTab, setActiveTab] = useState<'estructura' | 'docker' | 'backend' | 'migraciones' | 'hostinger'>('estructura');
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const dockerComposeSnippet = `version: '3.8'

services:
  # 1. Frontend Web (React + Vite + Tailwind CSS / Nginx)
  frontend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: multioficios_frontend
    restart: always
    ports:
      - "80:80"
    networks:
      - multioficios_network

  # 2. Backend API Microservicio (Python Flask + SQLAlchemy)
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: multioficios_backend
    restart: always
    ports:
      - "5000:5000"
    volumes:
      - ./datos:/app/datos
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:////app/datos/multioficios.db
      - SECRET_KEY=MultiOficios_SuperSecret_JwtKey_2026
      - ESCROW_GATEWAY=epayco_sandbox
    networks:
      - multioficios_network

networks:
  multioficios_network:
    driver: bridge

volumes:
  datos_volume:
    driver: local`;

  const flaskAppSnippet = `from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Colaborador, ObraContratada, MensajeChat, PagoCustodia
import os

app = Flask(__name__)
CORS(app)

# Configuración de base de datos SQLite ligera y escalable
DB_PATH = os.environ.get('DATABASE_URL', 'sqlite:////app/datos/multioficios.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-key')

db.init_app(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "MultiOficios Microservice", "version": "1.0.0"})

# 1. Obtener colaboradores por geolocalización y radio (Haversine)
@app.route('/api/colaboradores', methods=['GET'])
def get_colaboradores():
    lat = float(request.args.get('lat', 4.6345))
    lng = float(request.args.get('lng', -74.1458))
    radius_km = float(request.args.get('radius_km', 25.0))
    category = request.args.get('category', None)
    
    colabs = Colaborador.query_within_radius(lat, lng, radius_km, category)
    return jsonify({"count": len(colabs), "colaboradores": [c.to_dict() for c in colabs]})

# 2. Crear contrato de obra o labor con pago en custodia (Escrow)
@app.route('/api/obras/contratar', methods=['POST'])
def contratar_obra():
    data = request.get_json()
    obra = ObraContratada(
        cliente_id=data['cliente_id'],
        colaborador_id=data['colaborador_id'],
        tipo_servicio=data['tipo_servicio'],
        descripcion=data['descripcion'],
        monto_total=data['monto_total'],
        estado='fondos_en_custodia'
    )
    pago = PagoCustodia(obra=obra, monto=data['monto_total'], metodo=data['metodo_pago'])
    db.session.add(obra)
    db.session.add(pago)
    db.session.commit()
    return jsonify({"mensaje": "Contrato creado con éxito. Fondos retenidos en custodia.", "obra_id": obra.id}), 201

# 3. Acta de entrega y liberación de fondos en custodia
@app.route('/api/obras/<int:obra_id>/liberar-pago', methods=['POST'])
def liberar_pago(obra_id):
    obra = ObraContratada.query.get_or_404(obra_id)
    obra.estado = 'finalizado'
    obra.pago.estado_custodia = 'liberado_al_colaborador'
    db.session.commit()
    return jsonify({"mensaje": "Acta de entrega aprobada. Pago dispersado al técnico.", "status": "liberado"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)`;

  const migrationsSnippet = `# =======================================================
# MultiOficios: Gestión de Migraciones de Base de Datos (SQLite)
# =======================================================

# Método 1: Utilizando Flask-Migrate (Alembic)
# -------------------------------------------------------
export FLASK_APP=backend/app.py

# 1. Inicializar el directorio de migraciones (primera vez)
flask db init

# 2. Generar migración automática tras cambiar modelos en models.py
flask db migrate -m "Agregar columnas de clasificacion ARL y huella digital"

# 3. Aplicar las migraciones a la base de datos SQLite en producción
flask db upgrade

# 4. En caso de necesitar revertir una versión anterior
flask db downgrade

# -------------------------------------------------------
# Método 2: Backup manual antes de cada migración
# -------------------------------------------------------
cp datos/multioficios.db datos/backups/multioficios_\$(date +%Y%m%d_%H%M%S).db`;

  const hostingerSnippet = `# =======================================================
# Guía Paso a Paso para Desplegar MultiOficios en Hostinger VPS
# =======================================================

# Paso 1: Conectarse por SSH a tu servidor Hostinger VPS
ssh root@tu-ip-hostinger.com

# Paso 2: Instalar Docker y Docker Compose en Ubuntu/Debian
apt update && apt upgrade -y
apt install -y docker.io docker-compose git nginx certbot python3-certbot-nginx
systemctl enable --now docker

# Paso 3: Clonar el repositorio del proyecto
git clone https://github.com/tu-usuario/multioficios-app.git /var/www/multioficios
cd /var/www/multioficios

# Paso 4: Levantar los contenedores de Microservicios con Docker Compose
docker-compose up -d --build

# Paso 5: Verificar que los contenedores estén corriendo
docker-compose ps
# multioficios_frontend   Up   0.0.0.0:80->80/tcp
# multioficios_backend    Up   0.0.0.0:5000->5000/tcp

# Paso 6: Configurar Dominio y Certificado SSL Gratuito (HTTPS con Let's Encrypt)
certbot --nginx -d tu-dominio-multioficios.com`;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-stone-900/60 backdrop-blur-xs flex items-center justify-center p-3 sm:p-6 animate-in fade-in duration-200">
      <div 
        className="relative w-full max-w-5xl bg-white rounded-3xl shadow-2xl border border-stone-200 overflow-hidden my-6 flex flex-col max-h-[90vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-stone-900 text-white p-5 sm:p-6 flex items-center justify-between border-b border-stone-800">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-2xl bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-600/30">
              <FolderGit2 className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-lg sm:text-xl font-black text-white">
                  Arquitectura Docker • Microservicios & Hostinger
                </h3>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30">
                  DOCKER READY
                </span>
              </div>
              <p className="text-xs text-stone-400">
                Estructura modular en 3 carpetas: <code className="text-amber-400">frontend/</code>, <code className="text-blue-400">backend/</code> y <code className="text-emerald-400">datos/</code> (Flask + SQLite)
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Tab switcher */}
        <div className="flex border-b border-stone-200 px-6 bg-stone-50 overflow-x-auto">
          <button
            onClick={() => setActiveTab('estructura')}
            className={`py-3.5 px-4 text-xs font-bold border-b-2 cursor-pointer transition whitespace-nowrap ${
              activeTab === 'estructura'
                ? 'border-blue-600 text-blue-600 bg-white'
                : 'border-transparent text-stone-600 hover:text-stone-900'
            }`}
          >
            Estructura de 3 Carpetas
          </button>
          <button
            onClick={() => setActiveTab('docker')}
            className={`py-3.5 px-4 text-xs font-bold border-b-2 cursor-pointer transition whitespace-nowrap ${
              activeTab === 'docker'
                ? 'border-blue-600 text-blue-600 bg-white'
                : 'border-transparent text-stone-600 hover:text-stone-900'
            }`}
          >
            docker-compose.yml
          </button>
          <button
            onClick={() => setActiveTab('backend')}
            className={`py-3.5 px-4 text-xs font-bold border-b-2 cursor-pointer transition whitespace-nowrap ${
              activeTab === 'backend'
                ? 'border-blue-600 text-blue-600 bg-white'
                : 'border-transparent text-stone-600 hover:text-stone-900'
            }`}
          >
            Backend Flask REST API
          </button>
          <button
            onClick={() => setActiveTab('migraciones')}
            className={`py-3.5 px-4 text-xs font-bold border-b-2 cursor-pointer transition whitespace-nowrap ${
              activeTab === 'migraciones'
                ? 'border-blue-600 text-blue-600 bg-white'
                : 'border-transparent text-stone-600 hover:text-stone-900'
            }`}
          >
            Migraciones SQLite
          </button>
          <button
            onClick={() => setActiveTab('hostinger')}
            className={`py-3.5 px-4 text-xs font-bold border-b-2 cursor-pointer transition whitespace-nowrap ${
              activeTab === 'hostinger'
                ? 'border-blue-600 text-blue-600 bg-white'
                : 'border-transparent text-stone-600 hover:text-stone-900'
            }`}
          >
            Despliegue en Hostinger VPS
          </button>
        </div>

        {/* Tab Content */}
        <div className="p-6 overflow-y-auto flex-1 space-y-5 bg-stone-50/50">
          {activeTab === 'estructura' && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* 1. Frontend */}
                <div className="p-5 rounded-2xl bg-white border border-stone-200 shadow-xs space-y-3">
                  <div className="flex items-center gap-2.5 text-amber-600">
                    <Globe className="w-5 h-5" />
                    <h4 className="font-extrabold text-stone-900 text-sm">/frontend</h4>
                  </div>
                  <p className="text-xs text-stone-600 leading-relaxed">
                    Interfaz de usuario responsive construida con HTML5 semántico, CSS moderno y JavaScript modular.
                  </p>
                  <ul className="text-xs text-stone-700 space-y-1 font-mono bg-stone-50 p-3 rounded-xl border border-stone-200">
                    <li>├── index.html</li>
                    <li>├── css/style.css</li>
                    <li>├── js/app.js</li>
                    <li>├── js/api_client.js</li>
                    <li>└── Dockerfile (Nginx)</li>
                  </ul>
                </div>

                {/* 2. Backend */}
                <div className="p-5 rounded-2xl bg-white border border-stone-200 shadow-xs space-y-3">
                  <div className="flex items-center gap-2.5 text-blue-600">
                    <Server className="w-5 h-5" />
                    <h4 className="font-extrabold text-stone-900 text-sm">/backend</h4>
                  </div>
                  <p className="text-xs text-stone-600 leading-relaxed">
                    Microservicio en Python Flask con API RESTful documentada, JWT auth, geocálculos y pasarela Escrow.
                  </p>
                  <ul className="text-xs text-stone-700 space-y-1 font-mono bg-stone-50 p-3 rounded-xl border border-stone-200">
                    <li>├── app.py</li>
                    <li>├── models.py</li>
                    <li>├── routes/</li>
                    <li>├── requirements.txt</li>
                    <li>└── Dockerfile (Gunicorn)</li>
                  </ul>
                </div>

                {/* 3. Datos */}
                <div className="p-5 rounded-2xl bg-white border border-stone-200 shadow-xs space-y-3">
                  <div className="flex items-center gap-2.5 text-emerald-600">
                    <Database className="w-5 h-5" />
                    <h4 className="font-extrabold text-stone-900 text-sm">/datos</h4>
                  </div>
                  <p className="text-xs text-stone-600 leading-relaxed">
                    Persistencia relacional en SQLite, esquemas DDL, scripts de migración de versiones y utilitarios de backup.
                  </p>
                  <ul className="text-xs text-stone-700 space-y-1 font-mono bg-stone-50 p-3 rounded-xl border border-stone-200">
                    <li>├── multioficios.db</li>
                    <li>├── schema.sql</li>
                    <li>├── init_db.py</li>
                    <li>├── migrations/</li>
                    <li>└── backup_util.py</li>
                  </ul>
                </div>
              </div>

              {/* Architecture benefits */}
              <div className="p-4 rounded-2xl bg-white border border-stone-200 flex items-center justify-between text-xs">
                <div className="flex items-center gap-2 text-stone-800">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>Separación limpia de responsabilidades, listo para empaquetado en contenedores Docker estándar.</span>
                </div>
                <span className="font-bold text-blue-600">Hostinger & VPS Ready</span>
              </div>
            </div>
          )}

          {activeTab === 'docker' && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-stone-700">docker-compose.yml (Orquestación de Microservicios)</span>
                <button
                  onClick={() => copyToClipboard(dockerComposeSnippet, 'docker')}
                  className="flex items-center gap-1.5 text-xs font-bold text-blue-600 hover:text-blue-700 bg-white px-3 py-1.5 rounded-xl border border-stone-200 cursor-pointer"
                >
                  <Copy className="w-3.5 h-3.5" />
                  <span>{copiedKey === 'docker' ? '¡Copiado!' : 'Copiar Archivo'}</span>
                </button>
              </div>

              <pre className="p-4 bg-stone-950 text-stone-200 rounded-2xl text-xs font-mono overflow-x-auto leading-relaxed border border-stone-800">
                {dockerComposeSnippet}
              </pre>
            </div>
          )}

          {activeTab === 'backend' && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-stone-700">backend/app.py (Flask REST API Endpoints)</span>
                <button
                  onClick={() => copyToClipboard(flaskAppSnippet, 'flask')}
                  className="flex items-center gap-1.5 text-xs font-bold text-blue-600 hover:text-blue-700 bg-white px-3 py-1.5 rounded-xl border border-stone-200 cursor-pointer"
                >
                  <Copy className="w-3.5 h-3.5" />
                  <span>{copiedKey === 'flask' ? '¡Copiado!' : 'Copiar Código'}</span>
                </button>
              </div>

              <pre className="p-4 bg-stone-950 text-stone-200 rounded-2xl text-xs font-mono overflow-x-auto leading-relaxed border border-stone-800">
                {flaskAppSnippet}
              </pre>
            </div>
          )}

          {activeTab === 'migraciones' && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-stone-700">Guía de Migraciones de Base de Datos SQLite</span>
                <button
                  onClick={() => copyToClipboard(migrationsSnippet, 'migraciones')}
                  className="flex items-center gap-1.5 text-xs font-bold text-blue-600 hover:text-blue-700 bg-white px-3 py-1.5 rounded-xl border border-stone-200 cursor-pointer"
                >
                  <Copy className="w-3.5 h-3.5" />
                  <span>{copiedKey === 'migraciones' ? '¡Copiado!' : 'Copiar Comandos'}</span>
                </button>
              </div>

              <pre className="p-4 bg-stone-950 text-emerald-300 rounded-2xl text-xs font-mono overflow-x-auto leading-relaxed border border-stone-800">
                {migrationsSnippet}
              </pre>
            </div>
          )}

          {activeTab === 'hostinger' && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-stone-700">Instrucciones de Despliegue en Hostinger VPS</span>
                <button
                  onClick={() => copyToClipboard(hostingerSnippet, 'hostinger')}
                  className="flex items-center gap-1.5 text-xs font-bold text-blue-600 hover:text-blue-700 bg-white px-3 py-1.5 rounded-xl border border-stone-200 cursor-pointer"
                >
                  <Copy className="w-3.5 h-3.5" />
                  <span>{copiedKey === 'hostinger' ? '¡Copiado!' : 'Copiar Guía'}</span>
                </button>
              </div>

              <pre className="p-4 bg-stone-950 text-amber-200 rounded-2xl text-xs font-mono overflow-x-auto leading-relaxed border border-stone-800">
                {hostingerSnippet}
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
