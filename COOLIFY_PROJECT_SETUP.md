# 🚀 Complete Coolify Project Setup - Copy & Paste Guide

## ⚡ Quick Setup (Follow Exactly)

### Step 1: Create Project in Coolify

1. **Login to Coolify** (your dashboard)
2. Click **"Projects"** in left sidebar
3. Click **"New Project"** button
4. Fill in:
   - **Name**: `Legal AI Assistant`
   - **Description**: `AI-powered legal assistant for law enforcement`
5. Click **"Create"**

---

### Step 2: Deploy MySQL Database

1. In your project, click **"New Resource"** → **"Database"**
2. Select **"MySQL"**
3. **Configuration Tab** → Fill exactly:

```
Name: legal-ai-mysql
Image: mysql:8
Description: (leave empty or add description)
Ports Mappings: 3306:3306
Root Password: 1@yLC&%Dvee*JilV@S03MgH%dEjs0%6z
Normal User: legal_ai_user
Normal User Password: !SeG@DZk&4yor3NXusrY1G$#i!b@NTBx
Initial Database: legal_ai
```

4. Click **"Save"**
5. Wait for MySQL to start (check "Logs" tab)
6. Status should show **"Running"** (green)

---

### Step 3: Initialize Database Schema

**Option A: Using Coolify Database Console**
1. Go to MySQL service → Click **"Backups"** tab
2. Look for **"Database Console"** or **"phpMyAdmin"** button
3. Click it to open database interface
4. Select database: `legal_ai`
5. Click **"Import"** tab
6. Import files from your local `chat/` folder:
   - First: `schema.sql` → Click "Go"
   - Second: `fir_schema.sql` → Click "Go"
   - Third: `chathistory.sql` → Click "Go"

**Option B: Using Terminal (if you have SSH access)**
1. Go to MySQL service → **"Terminal"** tab
2. Run these commands:
```bash
mysql -uroot -p'1@yLC&%Dvee*JilV@S03MgH%dEjs0%6z' legal_ai < /path/to/schema.sql
mysql -uroot -p'1@yLC&%Dvee*JilV@S03MgH%dEjs0%6z' legal_ai < /path/to/fir_schema.sql
mysql -uroot -p'1@yLC&%Dvee*JilV@S03MgH%dEjs0%6z' legal_ai < /path/to/chathistory.sql
```

**Verify:** Check tables exist - should see: `ipc_sections`, `crimes`, `fir_reports`, `chat_sessions`, etc.

---

### Step 4: Deploy Rasa Action Server

1. In your project, click **"New Resource"** → **"Service"**
2. Select **"Dockerfile"**
3. **General Tab:**
   - **Name**: `rasa-actions`
   - **Description**: (optional)
4. **Source Tab:**
   - **Repository**: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
   - **Branch**: `main`
   - **Dockerfile Path**: `chat/Dockerfile.actions`
   - **Build Context**: `chat/`
5. **Ports Tab:**
   - **Port**: `5055`
6. **Environment Variables Tab** → Click **"Add"** for each:
   ```
   DB_HOST = legal-ai-mysql
   DB_USER = legal_ai_user
   DB_PASSWORD = !SeG@DZk&4yor3NXusrY1G$#i!b@NTBx
   DB_NAME = legal_ai
   PYTHONUNBUFFERED = 1
   RASA_ACTIONS_PORT = 5055
   ```
7. Click **"Save"** or **"Deploy"**
8. Wait for build (check "Logs" tab)
9. Should see: "Action server is running"

---

### Step 5: Deploy Rasa Server

1. **New Resource** → **Service** → **Dockerfile**
2. **General Tab:**
   - **Name**: `rasa`
3. **Source Tab:**
   - **Repository**: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
   - **Branch**: `main`
   - **Dockerfile Path**: `chat/Dockerfile.rasa`
   - **Build Context**: `chat/`
4. **Ports Tab:**
   - **Port**: `5005`
5. **Environment Variables Tab:**
   ```
   RASA_ACTION_ENDPOINT = http://rasa-actions:5055/webhook
   DB_HOST = legal-ai-mysql
   DB_USER = legal_ai_user
   DB_PASSWORD = !SeG@DZk&4yor3NXusrY1G$#i!b@NTBx
   DB_NAME = legal_ai
   PYTHONUNBUFFERED = 1
   RASA_PORT = 5005
   ```
6. Click **"Save"** or **"Deploy"**
7. Wait for build (5-10 minutes first time)
8. Check logs - should see: "Rasa server is running"

---

### Step 6: Deploy FastAPI Backend

1. **New Resource** → **Service** → **Dockerfile**
2. **General Tab:**
   - **Name**: `fastapi`
   - **Description**: (optional)
3. **Source Tab:**
   - **Repository**: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
   - **Branch**: `main`
   - **Dockerfile Path**: `chat/Dockerfile.fastapi`
   - **Build Context**: `chat/`
4. **Ports Tab:**
   - **Port**: `8080`
   - **Public Port**: (Coolify will assign)
   - **Enable Public Access**: ✅ **CHECK THIS BOX**
5. **Environment Variables Tab:**
   ```
   DB_HOST = legal-ai-mysql
   DB_USER = legal_ai_user
   DB_PASSWORD = !SeG@DZk&4yor3NXusrY1G$#i!b@NTBx
   DB_NAME = legal_ai
   RASA_SERVER_URL = http://rasa:5005
   PORT = 8080
   HOST = 0.0.0.0
   ALLOWED_ORIGINS = *
   API_KEY = Hr4vvONi2fGQd7ObjlV0e_yKj4j0LA3gJP8T2fM8M7lINWNc
   PYTHONUNBUFFERED = 1
   ```
6. Click **"Save"** or **"Deploy"**
7. Wait for build
8. **Note the Public URL** (shown in Coolify)

---

### Step 7: Verify Everything Works

1. **Health Check:**
   - Visit: `http://your-public-url:8080/api/health`
   - Should return: `{"status":"healthy","database":"connected"}`

2. **Test Chat:**
   - Visit: `http://your-public-url:8080/chat`
   - Login: `admin` / `admin123`
   - Send: "What is IPC Section 302?"
   - Should get bot response

3. **Test FIR:**
   - Visit: `http://your-public-url:8080/fir`
   - Fill form and submit
   - Should save successfully

---

## ✅ Deployment Checklist

- [ ] Project created in Coolify
- [ ] MySQL deployed with correct port (3306:3306)
- [ ] Database schema imported (3 SQL files)
- [ ] Rasa Actions deployed and running
- [ ] Rasa Server deployed and running
- [ ] FastAPI deployed with public access
- [ ] Health check passing
- [ ] Chat working
- [ ] FIR submission working

---

## 🆘 If Something Fails

**Check Service Logs:**
- Go to each service → "Logs" tab
- Look for error messages
- Share errors with me for troubleshooting

**Common Issues:**
- Service can't connect → Check service names match exactly
- Database error → Verify credentials and schema imported
- Build fails → Check repository URL and Dockerfile paths
- Port conflict → Each service needs unique port

---

## 🎉 Success!

Once all services are running:
- Your app is live at: `http://your-public-url:8080`
- Chat: `http://your-public-url:8080/chat`
- FIR: `http://your-public-url:8080/fir`

**Everything is automated and ready!** 🚀

