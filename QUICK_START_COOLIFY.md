# 🚀 Quick Start Guide - Coolify Deployment

This is a condensed guide for deploying to Coolify. For detailed instructions, see `COOLIFY_DEPLOYMENT.md`.

## ⚡ Quick Steps

### 1. Prepare Repository
```bash
cd chat
rasa train  # Train model (if not already done)
git add .
git commit -m "Ready for Coolify deployment"
git push
```

### 2. Create Coolify Project
1. Login to Coolify
2. Create project: **"Legal AI Assistant"**

### 3. Deploy MySQL (First!)
1. **New Resource** → **Database** → **MySQL**
2. Configure:
   - Name: `legal-ai-mysql`
   - Database: `legal_ai`
   - Root Password: `[Generate strong password]`
   - User: `legal_ai_user`
   - Password: `[Generate strong password]`
3. Deploy and wait for healthy status
4. Initialize schema via Database Console:
   - Import `schema.sql`
   - Import `fir_schema.sql`
   - Import `chathistory.sql`

### 4. Deploy Rasa Action Server
1. **New Resource** → **Service** → **Dockerfile**
2. Configure:
   - Name: `rasa-actions`
   - Dockerfile: `Dockerfile.actions`
   - Port: `5055`
3. Environment Variables:
   ```
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=[your MySQL password]
   DB_NAME=legal_ai
   PYTHONUNBUFFERED=1
   ```
4. Deploy

### 5. Deploy Rasa Server
1. **New Resource** → **Service** → **Dockerfile**
2. Configure:
   - Name: `rasa`
   - Dockerfile: `Dockerfile.rasa`
   - Port: `5005`
3. Environment Variables:
   ```
   RASA_ACTION_ENDPOINT=http://rasa-actions:5055/webhook
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=[your MySQL password]
   DB_NAME=legal_ai
   PYTHONUNBUFFERED=1
   ```
4. Deploy

### 6. Deploy FastAPI Backend
1. **New Resource** → **Service** → **Dockerfile**
2. Configure:
   - Name: `fastapi`
   - Dockerfile: `Dockerfile.fastapi`
   - Port: `8080`
   - **Enable Public Access**
3. Environment Variables:
   ```
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=[your MySQL password]
   DB_NAME=legal_ai
   RASA_SERVER_URL=http://rasa:5005
   PORT=8080
   HOST=0.0.0.0
   ALLOWED_ORIGINS=*
   API_KEY=[generate secure API key]
   PYTHONUNBUFFERED=1
   ```
4. Deploy

### 7. Verify Deployment
```bash
# Health checks
curl http://your-fastapi-url:8080/api/health
curl http://your-rasa-url:5005/health
curl http://your-actions-url:5055/health

# Test chat
# Open: http://your-fastapi-url:8080/chat
```

## 🔑 Important Notes

1. **Service Names**: Use exact service names in environment variables (e.g., `legal-ai-mysql`, `rasa-actions`, `rasa`)

2. **Network**: All services must be in the same project/network to communicate

3. **Passwords**: Generate strong passwords and save them securely

4. **Rasa Model**: If models aren't in repository, add build step: `rasa train` in Dockerfile.rasa

5. **Database Init**: SQL files must be imported manually or via init scripts

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Services can't connect | Check service names match in env vars |
| Rasa model missing | Train model and commit, or add training step |
| Database errors | Verify schema imported, check credentials |
| Health checks fail | Check logs, verify ports, ensure services running |

## 📚 Full Documentation

- **Detailed Guide**: `COOLIFY_DEPLOYMENT.md`
- **Environment Variables**: `ENV_VARIABLES.md`
- **Architecture**: `PROJECT_ANALYSIS.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`

---

**Ready to deploy!** 🎉

