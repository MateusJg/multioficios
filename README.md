# 👷 MultiOficios - Plataforma de Contratación de Oficios Varios por Obra o Labor

Plataforma web para conectar clientes y técnicos independientes de oficios varios (albañilería, plomería, electricidad, pintura, carpintería, cerrajería, refrigeración, mantenimiento de lavadoras, cómputo y belleza) con geolocalización en tiempo real, perfiles auditados, pago seguro en custodia (Escrow), seguimiento de obra en vivo, chat privado cifrado con notificaciones emergentes en pantalla, y consola de administración.

Diseñado bajo una arquitectura modular y escalable con **Docker**, estructurado con el frontend en la raíz (`React 19 + TypeScript + Vite + Nginx`), microservicio de backend en Python (`backend/`) y persistencia relacional en SQLite (`datos/`), listo para producción en servidores VPS como **Hostinger**.

---

## 📁 1. Estructura Actualizada del Proyecto

```text
├── Dockerfile             # Multi-stage build (Node 20 Alpine -> Nginx) para el Frontend
├── nginx.conf             # Configuración del servidor Nginx de producción
├── docker-compose.yml     # Orquestación multi-contenedor (Frontend + Backend + Datos)
├── package.json           # Dependencias y scripts de Vite / React / Tailwind
├── tsconfig.json          # Configuración TypeScript del proyecto
├── vite.config.ts         # Configuración del empaquetador Vite
├── index.html             # Punto de entrada HTML5 para React
│
├── src/                   # Aplicación Frontend React 19 + TypeScript + Tailwind
│   ├── components/        # Componentes UI modulares (Tarjetas, Chat, Modal de Perfil, Contratos, etc.)
│   ├── data/              # Modelos y catálogo de categorías de oficios varios
│   ├── types.ts           # Definiciones de tipos TypeScript de la plataforma
│   ├── App.tsx            # Componente raíz con estado global y vistas
│   └── main.tsx           # Montaje de la aplicación React
│
├── backend/               # Microservicio API REST (Python Flask + SQLAlchemy)
│   ├── app.py             # API RESTful con geocálculos Haversine y pasarela Escrow
│   ├── models.py          # Modelos de datos de Colaborador, Obra, Pago y Chat
│   ├── requirements.txt   # Dependencias Python (Flask, Flask-CORS, SQLAlchemy, Gunicorn)
│   └── Dockerfile         # Imagen Docker con Python 3.11-slim y Gunicorn
│
├── datos/                 # Persistencia Relacional y Gestión de Datos (SQLite)
│   ├── multioficios.db    # Base de datos SQLite ligera y de alto rendimiento (modo WAL)
│   ├── schema.sql         # Esquema DDL con tablas, llaves foráneas e índices
│   ├── init_db.py         # Script de inicialización y datos de prueba
│   ├── backup_util.py     # Script para copias de seguridad atómicas
│   └── migrations/        # Versionado y control de migraciones de base de datos
│       ├── 001_initial_schema.sql
│       └── MIGRATION_GUIDE.md
│
├── public/                # Recursos estáticos públicos (favicons, íconos, logos)
└── README.md              # Documentación técnica del proyecto
```

---

## 🔄 2. Cambios Recientes en la Arquitectura y Código

1. **Unificación y Limpieza de Raíz (Eliminación de `/frontend`):**
   - Se eliminó la carpeta redundante `/frontend` que solo contenía configuraciones aisladas.
   - El `Dockerfile` y `nginx.conf` se trasladaron a la raíz del repositorio, alineándose con el estándar de proyectos SPA modernos en React + Vite.
   - `docker-compose.yml` ahora construye el servicio frontend directamente desde la raíz (`dockerfile: Dockerfile`).

2. **Simplificación de la Interfaz de Contacto:**
   - Se consolidó un **único botón de Chat Privado** en las tarjetas de colaboradores y en sus perfiles modales, eliminando la duplicidad visual que causaba confusión entre WhatsApp y el chat interno.

3. **Notificaciones Emergentes en Pantalla (Push/Web Notification API):**
   - Se retiró la dependencia de envíos manuales de WhatsApp / SMS desde el chat.
   - Se implementó el sistema de **Notificaciones Emergentes en Pantalla** directamente conectado al navegador y teléfono mediante la **Web Notification API** nativa acompañada de aviso sonoro (Web Audio API) y alerta visual en tiempo real.

4. **Base de Datos Limpia para Producción:**
   - Se limpiaron los registros hardcodeados de prueba en `mockData.ts` para permitir el ingreso limpio de colaboradores y contratos reales a través del portal de registro y la base de datos SQLite.

---

## 🚀 3. Puesta en Marcha

### Opción A: Desarrollo Local con Node.js / Vite
```bash
# 1. Instalar dependencias
npm install

# 2. Iniciar servidor de desarrollo
npm run dev
```
La aplicación estará disponible en `http://localhost:3000` (o el puerto asignado por Vite).

---

### Opción B: Ejecución con Docker Compose (Producción)

#### Requisitos previos:
- **Docker Engine** (v20+)
- **Docker Compose** (v2+)

#### Comandos:
```bash
# Iniciar todos los contenedores en segundo plano
docker-compose up -d --build

# Verificar estado de los contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f
```
* **Frontend Web**: `http://localhost:80`
* **Backend API**: `http://localhost:5001/api/health` (o puerto configurado en `.env`)

---

## 🌐 4. Guía de Despliegue en Hostinger VPS (Ubuntu 22.04 / 24.04 LTS)

### Paso 1: Conectarse por SSH al servidor
```bash
ssh root@tu-servidor-hostinger.com
```

### Paso 2: Instalar Docker y utilidades
```bash
apt update && apt upgrade -y
apt install -y docker.io docker-compose git nginx certbot python3-certbot-nginx
systemctl enable --now docker
```

### Paso 3: Clonar el proyecto
```bash
git clone https://github.com/tu-usuario/multioficios.git /var/www/multioficios
cd /var/www/multioficios
```

### Paso 4: Levantar los contenedores
```bash
docker-compose up -d --build
```

### Paso 5: Configurar Dominio y Certificado SSL (HTTPS Let's Encrypt)
```bash
certbot --nginx -d tu-dominio-multioficios.com
```

---

## 🗄️ 5. Gestión de Base de Datos y Migraciones (SQLite)

La persistencia se maneja en `./datos/multioficios.db`. Para consultar la guía detallada de migraciones, revise `datos/migrations/MIGRATION_GUIDE.md`.

```bash
# 1. Crear respaldo preventivo antes de cualquier cambio
python3 datos/backup_util.py

# 2. Generar migración tras editar backend/models.py
export FLASK_APP=backend/app.py
flask db migrate -m "Descripcion de la migracion"

# 3. Aplicar migración en el contenedor de producción
docker exec -it multioficios_backend flask db upgrade
```

---

## 🔒 6. Seguridad y Cumplimiento Normativo

- **Cifrado en Plataforma**: Los mensajes y cotizaciones entre clientes y técnicos viajan cifrados.
- **Habeas Data**: Cumplimiento de la Ley 1581 de 2012 (Colombia) para la protección y tratamiento de datos personales.
- **Pago Seguro en Custodia (Escrow)**: El valor del servicio se retiene y únicamente se dispersa cuando el cliente aprueba y firma digitalmente el acta de entrega de la labor.
- **Póliza ARL**: Verificación de cobertura de riesgos laborales para trabajos de obra civil, instalaciones y mantenimiento.
