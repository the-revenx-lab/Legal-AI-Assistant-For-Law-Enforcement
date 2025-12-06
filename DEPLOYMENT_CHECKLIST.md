# ✅ Coolify Deployment Checklist

Use this checklist to ensure a smooth deployment to Coolify.

## 📋 Pre-Deployment Checklist

### 1. Code Preparation
- [ ] All code changes committed to Git
- [ ] All files pushed to repository
- [ ] Rasa model trained and committed (or will train during deployment)
- [ ] No hardcoded credentials in code
- [ ] All environment variables documented

### 2. Rasa Model Training
- [ ] Navigate to `chat/` directory
- [ ] Run `rasa train` to generate latest model
- [ ] Verify model exists in `models/` directory
- [ ] Commit model files to Git
- [ ] Push to repository

**Note:** If you skip this, the Dockerfile will need to train the model during build (slower).

### 3. Environment Variables Preparation
- [ ] Review `ENV_VARIABLES.md`
- [ ] Generate secure passwords for:
  - [ ] `MYSQL_ROOT_PASSWORD`
  - [ ] `MYSQL_PASSWORD`
  - [ ] `API_KEY`
- [ ] Document all values (keep secure!)
- [ ] Prepare environment variable list for Coolify

### 4. Database Schema Files
- [ ] Verify `schema.sql` exists
- [ ] Verify `fir_schema.sql` exists
- [ ] Verify `chathistory.sql` exists
- [ ] All SQL files are valid

### 5. Docker Files Verification
- [ ] `Dockerfile.rasa` exists and is correct
- [ ] `Dockerfile.actions` exists and is correct
- [ ] `Dockerfile.fastapi` exists and is correct
- [ ] `docker-compose.coolify.yml` exists
- [ ] All Dockerfiles tested locally (optional)

---

## 🚀 Deployment Steps

### Step 1: Create Coolify Project
- [ ] Login to Coolify dashboard
- [ ] Create new project: "Legal AI Assistant"
- [ ] Project created successfully

### Step 2: Deploy MySQL Database
- [ ] Add MySQL database resource
- [ ] Configure:
  - [ ] Name: `legal-ai-mysql`
  - [ ] Database: `legal_ai`
  - [ ] Root password: [Generated secure password]
  - [ ] User: `legal_ai_user`
  - [ ] Password: [Generated secure password]
- [ ] Deploy MySQL
- [ ] Wait for MySQL to be healthy
- [ ] Initialize database schema:
  - [ ] Import `schema.sql`
  - [ ] Import `fir_schema.sql`
  - [ ] Import `chathistory.sql`
- [ ] Verify tables created

### Step 3: Deploy Rasa Action Server
- [ ] Add new service/resource
- [ ] Configure:
  - [ ] Name: `rasa-actions`
  - [ ] Dockerfile: `Dockerfile.actions`
  - [ ] Port: `5055`
  - [ ] Build context: Root of repository
- [ ] Set environment variables:
  - [ ] `DB_HOST=legal-ai-mysql` (or service name)
  - [ ] `DB_USER=legal_ai_user`
  - [ ] `DB_PASSWORD=[your password]`
  - [ ] `DB_NAME=legal_ai`
  - [ ] `PYTHONUNBUFFERED=1`
- [ ] Deploy service
- [ ] Verify health check passes: `http://service-url:5055/health`

### Step 4: Deploy Rasa Server
- [ ] Add new service/resource
- [ ] Configure:
  - [ ] Name: `rasa`
  - [ ] Dockerfile: `Dockerfile.rasa`
  - [ ] Port: `5005`
  - [ ] Build context: Root of repository
- [ ] Set environment variables:
  - [ ] `RASA_ACTION_ENDPOINT=http://rasa-actions:5055/webhook`
  - [ ] `DB_HOST=legal-ai-mysql`
  - [ ] `DB_USER=legal_ai_user`
  - [ ] `DB_PASSWORD=[your password]`
  - [ ] `DB_NAME=legal_ai`
  - [ ] `PYTHONUNBUFFERED=1`
- [ ] Deploy service
- [ ] Verify health check passes: `http://service-url:5005/health`
- [ ] If model missing, add build step: `rasa train`

### Step 5: Deploy FastAPI Backend
- [ ] Add new service/resource
- [ ] Configure:
  - [ ] Name: `fastapi` or `legal-ai-backend`
  - [ ] Dockerfile: `Dockerfile.fastapi`
  - [ ] Port: `8080`
  - [ ] Build context: Root of repository
- [ ] Set environment variables:
  - [ ] `DB_HOST=legal-ai-mysql`
  - [ ] `DB_USER=legal_ai_user`
  - [ ] `DB_PASSWORD=[your password]`
  - [ ] `DB_NAME=legal_ai`
  - [ ] `RASA_SERVER_URL=http://rasa:5005`
  - [ ] `PORT=8080`
  - [ ] `HOST=0.0.0.0`
  - [ ] `ALLOWED_ORIGINS=*` (or your domain)
  - [ ] `API_KEY=[your secure API key]`
  - [ ] `PYTHONUNBUFFERED=1`
- [ ] Enable public access (if needed)
- [ ] Deploy service
- [ ] Verify health check: `http://service-url:8080/api/health`

### Step 6: Configure Networking
- [ ] Verify all services are in same network
- [ ] Services can communicate using service names
- [ ] External ports are accessible (if needed)

---

## ✅ Post-Deployment Verification

### Health Checks
- [ ] FastAPI health: `GET /api/health` returns 200
- [ ] Rasa health: `GET /health` returns 200
- [ ] Actions health: `GET /health` returns 200
- [ ] MySQL is accessible from all services

### Functional Tests
- [ ] Chat interface loads: `http://your-url:8080/chat`
- [ ] Can send message to bot
- [ ] Bot responds correctly
- [ ] FIR form loads: `http://your-url:8080/fir`
- [ ] Can submit FIR
- [ ] FIR appears in admin dashboard
- [ ] IPC section queries work
- [ ] Chat history saves

### Database Verification
- [ ] All tables exist
- [ ] Can query IPC sections
- [ ] Can query crimes
- [ ] FIR data persists
- [ ] Chat history saves

### Security Checks
- [ ] Default passwords changed
- [ ] API_KEY is secure
- [ ] CORS configured (if needed)
- [ ] Database not publicly accessible
- [ ] HTTPS enabled (if using custom domain)

---

## 🔧 Troubleshooting

### If services can't connect:
- [ ] Verify service names match in environment variables
- [ ] Check all services are in same network
- [ ] Verify MySQL is healthy before other services start
- [ ] Check logs for connection errors

### If Rasa model not found:
- [ ] Train model: `rasa train`
- [ ] Commit models directory
- [ ] Rebuild Docker image
- [ ] Or add training step to Dockerfile

### If database errors:
- [ ] Verify schema files imported correctly
- [ ] Check database credentials
- [ ] Verify database is initialized
- [ ] Check MySQL logs

### If health checks fail:
- [ ] Verify ports are correct
- [ ] Check service is running
- [ ] Review service logs
- [ ] Verify dependencies are installed

---

## 📝 Notes

- Keep all passwords secure and documented
- Test locally with Docker Compose first (optional)
- Monitor logs during deployment
- Have backup plan for database
- Document your deployment URLs

---

**Last Updated:** Generated for deployment
**Status:** Ready for Coolify deployment

