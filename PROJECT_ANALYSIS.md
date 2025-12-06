# 📋 Legal AI Assistant - Complete Project Analysis

## 🏗️ Architecture Overview

This is a **multi-service AI-powered legal assistant** for law enforcement with the following components:

```
┌─────────────────┐
│   Web Browser   │
└────────┬────────┘
         │ HTTP/WebSocket
         ▼
┌─────────────────────────────────────┐
│      FastAPI Backend (chat.py)      │
│         Port: 8080                  │
│  - Web UI (HTML/CSS/JS)              │
│  - FIR Management API               │
│  - IPC Section Management           │
│  - WebSocket Chat Interface         │
└────────┬────────────────────────────┘
         │ HTTP REST API
         ▼
┌─────────────────────────────────────┐
│      Rasa Server                    │
│      Port: 5005/10000               │
│  - NLU Processing                   │
│  - Dialogue Management              │
│  - Intent Classification            │
└────────┬────────────────────────────┘
         │ Action Webhook
         ▼
┌─────────────────────────────────────┐
│   Rasa Action Server                │
│   Port: 5055                        │
│  - Custom Actions                   │
│  - Database Queries                 │
│  - IPC/Crime Information Retrieval  │
└────────┬────────────────────────────┘
         │ MySQL Connection
         ▼
┌─────────────────────────────────────┐
│      MySQL Database                 │
│      Port: 3306                     │
│  - ipc_sections                     │
│  - crimes                           │
│  - crime_ipc_mapping                │
│  - fir_reports                      │
│  - fir_complainants                 │
│  - chat_sessions                    │
│  - chat_messages                    │
└─────────────────────────────────────┘
```

---

## 📁 Complete Directory Structure

```
chat/
├── actions/                    # Rasa Custom Actions
│   ├── __init__.py
│   └── actions.py              # Main action handlers (IPC, crimes, confessions)
│
├── data/                       # Rasa Training Data
│   ├── nlu.yml                # NLU training examples (intents, entities, synonyms)
│   ├── stories.yml            # Conversation stories
│   └── rules.yml              # Conversation rules
│
├── docs/                       # Documentation
│   ├── api.md                 # API documentation
│   ├── deployment.md          # Deployment guide
│   ├── development.md         # Development guide
│   ├── schema.md              # Database schema
│   └── user_guide.md          # User guide
│
├── models/                     # Trained Rasa models (generated)
│
├── rasa/                       # Alternative Rasa config
│   ├── actions/
│   ├── config.yml             # Rasa pipeline configuration
│   └── data/
│
├── rasa_data/                  # Legacy Rasa data
│
├── static/                     # Web UI Assets
│   ├── about.html
│   ├── chat.html              # Main chat interface
│   ├── chat_history.html      # Chat history viewer
│   ├── fir.html               # FIR form
│   ├── fir_admin.html         # FIR admin dashboard
│   ├── ipc_admin.html         # IPC admin dashboard
│   ├── login.html             # Login page
│   ├── saverate.html          # FIR details view
│   ├── styles.css             # CSS styles
│   ├── index.js               # Frontend JavaScript
│   └── *.svg, *.png           # Images
│
├── tests/                      # Test files
│   └── test_stories.yml
│
├── *.py                        # Python Scripts
│   ├── chat.py                # ⭐ MAIN FastAPI Application
│   ├── fir_api.py             # FIR API endpoints
│   ├── api_client.py          # Rasa HTTP client
│   ├── actions.py             # (duplicate/legacy)
│   ├── config.py              # Database configuration
│   ├── train_rasa_model.py    # Model training script
│   └── [many utility scripts]
│
├── *.yml                       # Configuration Files
│   ├── domain.yml             # Rasa domain (intents, entities, responses, actions)
│   ├── endpoints.yml          # Rasa endpoints (action server, tracker store)
│   ├── credentials.yml        # Rasa credentials
│   └── config.yml             # General config
│
├── *.sql                       # Database Schemas
│   ├── schema.sql             # Main database schema (IPC, crimes, mappings)
│   ├── fir_schema.sql         # FIR tables schema
│   └── chathistory.sql        # Chat history tables
│
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Current Dockerfile (needs update)
├── docker-compose.yml          # Current docker-compose (needs update)
└── README.md                   # Project documentation
```

---

## 🔧 Service Details

### 1. FastAPI Backend (`chat.py`)

**Purpose**: Main web application server

**Responsibilities**:
- Serve HTML/CSS/JS frontend
- Handle WebSocket connections for chat
- Provide REST API for FIR management
- Provide REST API for IPC section management
- Manage chat history
- User authentication (simple in-memory)

**Key Endpoints**:
- `GET /` - Login page
- `GET /chat` - Chat interface
- `GET /fir` - FIR form
- `GET /fir/admin` - FIR admin dashboard
- `GET /ipc/admin` - IPC admin dashboard
- `GET /chat/history` - Chat history viewer
- `WebSocket /ws` - Real-time chat
- `POST /api/fir` - Submit FIR
- `GET /api/fir/search` - Search FIRs
- `GET /api/ipc` - Get IPC sections
- `GET /api/chat/history` - Get chat sessions

**Port**: 8080 (configurable via `PORT` env var)

**Dependencies**:
- FastAPI
- Uvicorn
- WebSockets
- MySQL connector
- Jinja2 templates

**Database Connections**:
- Uses `config.py` for FIR/IPC database
- Hardcoded config for chat history (needs fix)

---

### 2. Rasa Server

**Purpose**: Natural Language Understanding and Dialogue Management

**Responsibilities**:
- Process user messages
- Classify intents
- Extract entities
- Manage conversation flow
- Call action server for custom actions

**Configuration**:
- `domain.yml` - Defines intents, entities, responses, actions
- `endpoints.yml` - Points to action server at `http://localhost:5055/webhook`
- `data/nlu.yml` - Training examples
- `data/stories.yml` - Conversation flows
- `data/rules.yml` - Conversation rules

**Port**: 5005 (default) or 10000 (configurable)

**Commands**:
```bash
rasa run --enable-api --cors "*" --port 5005
```

**Tracker Store**: SQLite (configured in `endpoints.yml`)

---

### 3. Rasa Action Server (`actions/actions.py`)

**Purpose**: Execute custom actions triggered by Rasa

**Custom Actions**:
1. `action_query_ipc_section` - Query IPC section details
2. `action_query_crime` - Query crime information
3. `action_query_ipc_punishment` - Query IPC punishment details
4. `action_handle_crime_confession` - Handle crime confessions
5. `action_suggest_ipc_from_description` - ⚠️ **MISSING** (referenced in domain.yml but not implemented)

**Port**: 5055

**Commands**:
```bash
rasa run actions --cors "*" --port 5055
```

**Database Connection**: 
- ⚠️ **ISSUE**: Hardcoded MySQL credentials in `actions.py`
- Uses: `host="localhost"`, `user="root"`, `password="pass"`, `database="legal_ai"`
- **NEEDS FIX**: Should use environment variables

---

### 4. MySQL Database

**Database Name**: `legal_ai`

**Tables**:

1. **`ipc_sections`**
   - `id`, `section_number`, `title`, `description`, `punishment`, `category`, `is_active`, `created_at`, `updated_at`

2. **`crimes`**
   - `id`, `name`, `description`, `severity`, `category`, `bailable`, `cognizable`, `compoundable`, `created_at`, `updated_at`

3. **`crime_ipc_mapping`**
   - `id`, `crime_id`, `ipc_section_id`, `is_primary`, `created_at`

4. **`fir_reports`**
   - `id`, `fir_number`, `police_station`, `district`, `fir_date`, `complainant_id`, `info_type`, `place_of_occurrence`, `date_time_of_occurrence`, `accused_details`, `property_details`, `property_value`, `complaint`, `sections_acts`, `status`, `created_at`, `updated_at`

5. **`fir_complainants`**
   - `id`, `name`, `parent_name`, `age`, `gender`, `nationality`, `occupation`, `address`, `contact`, `created_at`

6. **`chat_sessions`**
   - `id`, `session_name`, `created_at`

7. **`chat_messages`**
   - `id`, `session_id`, `sender`, `content`, `timestamp`

8. **`user_interactions`** (optional, for analytics)
   - `id`, `user_query`, `bot_response`, `confidence_score`, `created_at`

**Views**:
- `fir_report_details` - Joined view of FIR reports and complainants

**Port**: 3306

**Default Credentials** (local):
- Host: `localhost`
- User: `root1` (config.py) or `root` (actions.py) ⚠️ **INCONSISTENCY**
- Password: `pass`
- Database: `legal_ai`

---

## 🔗 Service Interactions

### Chat Flow:
1. User sends message via WebSocket → `chat.py`
2. `chat.py` forwards to Rasa via HTTP → `RasaClient.send_message()`
3. Rasa processes message → Intent classification, entity extraction
4. Rasa calls action server → `http://localhost:5055/webhook`
5. Action server queries MySQL → IPC/crime data
6. Action server returns response → Rasa
7. Rasa returns formatted response → `chat.py`
8. `chat.py` sends to user via WebSocket

### FIR Flow:
1. User submits FIR form → `POST /api/fir`
2. `fir_api.py` validates data → Pydantic models
3. `fir_api.py` inserts into MySQL → `fir_complainants` + `fir_reports`
4. Returns success response

### IPC Query Flow:
1. User asks about IPC section → Chat interface
2. Rasa identifies `ask_about_ipc` intent
3. Rasa calls `action_query_ipc_section`
4. Action queries `ipc_sections` table
5. Returns formatted response

---

## ⚠️ Issues & Inconsistencies Found

### 1. **Database Credentials Hardcoded**
   - **Location**: `actions/actions.py` (lines 45-49, 142-146, 381-385, 503-507)
   - **Issue**: Hardcoded `localhost`, `root`, `pass`
   - **Fix**: Use environment variables via `config.py`

### 2. **Database User Inconsistency**
   - `config.py` uses: `root1`
   - `actions.py` uses: `root`
   - **Fix**: Standardize on one user or use env vars

### 3. **Chat History DB Config Hardcoded**
   - **Location**: `chat.py` (lines 57-62)
   - **Issue**: Hardcoded credentials
   - **Fix**: Use `config.py` or environment variables

### 4. **Missing Action Implementation**
   - `action_suggest_ipc_from_description` referenced in `domain.yml` but not implemented
   - **Fix**: Implement or remove from domain

### 5. **Docker Compose Uses PostgreSQL**
   - **Location**: `docker-compose.yml`
   - **Issue**: Project uses MySQL, but docker-compose.yml has PostgreSQL
   - **Fix**: Update to MySQL

### 6. **Dockerfile Runs Wrong Command**
   - **Location**: `Dockerfile` (line 43)
   - **Issue**: Runs `chat.py` but should be for Rasa
   - **Fix**: Create separate Dockerfiles for each service

### 7. **Rasa Client URL Hardcoded**
   - **Location**: `api_client.py` (line 9)
   - **Issue**: Defaults to `http://localhost:5005`
   - **Fix**: Use environment variable

### 8. **Rasa Action Endpoint Hardcoded**
   - **Location**: `endpoints.yml` (line 14)
   - **Issue**: Hardcoded `http://localhost:5055/webhook`
   - **Fix**: Use environment variable or Docker service name

---

## 📦 Dependencies

### Python Dependencies (`requirements.txt`):
```
rasa==3.6.2
mysql-connector-python==8.0.33
fastapi==0.68.1
uvicorn==0.15.0
python-multipart==0.0.5
jinja2==3.0.1
python-socketio==5.10.0
websockets>=10.0,<11.0
selenium==4.18.1
webdriver-manager==4.0.1
python-jose==3.3.0
passlib==1.7.4
bcrypt==3.2.0
reportlab==3.6.12
python-dotenv==0.19.0
```

### System Dependencies:
- Python 3.8+
- MySQL 5.7+ or 8.0+
- Docker & Docker Compose (for deployment)

---

## 🔐 Environment Variables Required

### FastAPI Backend:
- `DB_HOST` - MySQL host (default: `localhost`)
- `DB_USER` - MySQL user (default: `root1`)
- `DB_PASSWORD` - MySQL password (default: `pass`)
- `DB_NAME` - MySQL database (default: `legal_ai`)
- `PORT` - FastAPI port (default: `8080`)
- `ALLOWED_ORIGINS` - CORS origins (default: `http://localhost:8080`)
- `API_KEY` - API key for protected endpoints (default: `changeme`)
- `RASA_SERVER_URL` - Rasa server URL (default: `http://localhost:5005`)

### Rasa Server:
- `RASA_ACTION_ENDPOINT` - Action server URL (default: `http://localhost:5055/webhook`)
- `DB_HOST` - MySQL host (for tracker store if using MySQL)
- `DB_USER` - MySQL user
- `DB_PASSWORD` - MySQL password
- `DB_NAME` - MySQL database

### Rasa Action Server:
- `DB_HOST` - MySQL host (default: `localhost`)
- `DB_USER` - MySQL user (default: `root`)
- `DB_PASSWORD` - MySQL password (default: `pass`)
- `DB_NAME` - MySQL database (default: `legal_ai`)

### MySQL:
- `MYSQL_ROOT_PASSWORD` - Root password
- `MYSQL_DATABASE` - Database name (default: `legal_ai`)
- `MYSQL_USER` - Application user
- `MYSQL_PASSWORD` - Application password

---

## 🚀 Deployment Requirements

### For Coolify Deployment:

1. **Separate Dockerfiles** for each service:
   - `Dockerfile.rasa` - Rasa server
   - `Dockerfile.actions` - Rasa action server
   - `Dockerfile.fastapi` - FastAPI backend

2. **Docker Compose v3** compatible configuration

3. **Environment Variables** properly configured

4. **Database Initialization**:
   - Run `schema.sql`
   - Run `fir_schema.sql`
   - Run `chathistory.sql`
   - Optionally run `populate_database.py`

5. **Rasa Model Training**:
   - Train model before deployment: `rasa train`
   - Model should be included in Docker image or volume

6. **Network Configuration**:
   - All services in same Docker network
   - Services communicate via service names

7. **Volume Mounts**:
   - MySQL data persistence
   - Rasa models (optional)
   - Chat logs (optional)

---

## 📝 Next Steps

1. ✅ **Project Analysis Complete** (this document)
2. ⏳ Fix hardcoded credentials in `actions.py`
3. ⏳ Create separate Dockerfiles for each service
4. ⏳ Create production-ready `docker-compose.yml`
5. ⏳ Create environment variable template
6. ⏳ Implement missing `action_suggest_ipc_from_description`
7. ⏳ Test deployment locally
8. ⏳ Deploy to Coolify

---

## 📞 Service Ports Summary

| Service | Port | Protocol | Notes |
|---------|------|----------|-------|
| FastAPI Backend | 8080 | HTTP/WebSocket | Main web interface |
| Rasa Server | 5005/10000 | HTTP | NLU & Dialogue |
| Rasa Action Server | 5055 | HTTP | Custom actions |
| MySQL | 3306 | TCP | Database |

---

**Document Generated**: $(date)
**Project Version**: Based on current codebase analysis

