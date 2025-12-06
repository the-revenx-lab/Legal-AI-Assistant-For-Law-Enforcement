# 🚀 START DEPLOYMENT HERE

## ✅ Everything is Ready!

**Your GitHub Repository**: 
`https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`

**Status**: All deployment files pushed ✅

---

## 📋 What You Need Before Starting

1. **Coolify Account** - Login to your Coolify dashboard
2. **Passwords** - Generate these now:
   - MySQL Root Password (save it!)
   - MySQL App User Password (save it!)
   - FastAPI API Key (generate a secure random string)

---

## 🎯 Quick Deployment (Follow These Steps)

### 1. Open Coolify Dashboard
- Login to your Coolify instance
- Go to **"Projects"**

### 2. Create Project
- Click **"New Project"**
- Name: `Legal AI Assistant`
- Click **"Create"**

### 3. Deploy MySQL (FIRST!)
- **New Resource** → **Database** → **MySQL**
- Name: `legal-ai-mysql`
- Database: `legal_ai`
- Root Password: `[Your generated password]`
- User: `legal_ai_user`
- Password: `[Your generated password]`
- **Deploy** and wait for healthy status
- **Import SQL files**: `schema.sql`, `fir_schema.sql`, `chathistory.sql`

### 4. Deploy Rasa Actions
- **New Resource** → **Service** → **Dockerfile**
- Repository: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
- Branch: `main`
- Dockerfile: `chat/Dockerfile.actions`
- Build Context: `chat/`
- Port: `5055`
- **Environment Variables** (see `COOLIFY_ENV_VARS.txt`)

### 5. Deploy Rasa Server
- **New Resource** → **Service** → **Dockerfile**
- Repository: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
- Branch: `main`
- Dockerfile: `chat/Dockerfile.rasa`
- Build Context: `chat/`
- Port: `5005`
- **Environment Variables** (see `COOLIFY_ENV_VARS.txt`)

### 6. Deploy FastAPI
- **New Resource** → **Service** → **Dockerfile**
- Repository: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
- Branch: `main`
- Dockerfile: `chat/Dockerfile.fastapi`
- Build Context: `chat/`
- Port: `8080`
- **Enable Public Access** ✅
- **Environment Variables** (see `COOLIFY_ENV_VARS.txt`)

---

## 📄 Detailed Instructions

For complete step-by-step instructions, see:
- **`DEPLOY_NOW.md`** - Complete deployment guide
- **`COOLIFY_ENV_VARS.txt`** - Environment variables to copy

---

## 🔑 Key Information

**Repository URL**: 
```
https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git
```

**Service Names** (use exactly as shown):
- MySQL: `legal-ai-mysql`
- Actions: `rasa-actions`
- Rasa: `rasa`
- FastAPI: `fastapi` (or your choice)

**Dockerfile Paths**:
- Actions: `chat/Dockerfile.actions`
- Rasa: `chat/Dockerfile.rasa`
- FastAPI: `chat/Dockerfile.fastapi`

**Build Context**: `chat/` (for all services)

---

## ✅ Deployment Order (IMPORTANT!)

1. MySQL Database ← **START HERE**
2. Rasa Action Server
3. Rasa Server
4. FastAPI Backend ← **END HERE**

**Wait for each service to be healthy before deploying the next!**

---

## 🎉 After Deployment

Test your deployment:
1. Visit: `http://your-fastapi-url:8080/api/health`
2. Should return: `{"status":"healthy"}`
3. Test chat: `http://your-fastapi-url:8080/chat`
4. Login: `admin` / `admin123`

---

## 🆘 Need Help?

- Check service logs in Coolify
- Verify environment variables match `COOLIFY_ENV_VARS.txt`
- Ensure all services are in the same project
- Make sure MySQL is healthy first

**Ready to deploy!** 🚀

