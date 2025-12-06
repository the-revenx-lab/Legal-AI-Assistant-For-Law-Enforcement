# 🤖 Automated Deployment Guide - Coolify

## 🎯 Complete Step-by-Step Deployment

Follow these exact steps to deploy your project. I've automated everything possible.

---

## ✅ Pre-Deployment Checklist

- [x] Rasa model trained
- [x] All code in GitHub
- [x] Credentials generated
- [x] Dockerfiles optimized
- [x] Configuration files fixed

---

## 📋 Step 1: Fix MySQL Port (CRITICAL!)

**In Coolify MySQL Configuration:**
1. Go to your MySQL service (`legal-ai-mysql`)
2. Click "Configuration" tab
3. Find "Ports Mappings"
4. Change from: `3000:5432` 
5. Change to: `3306:3306`
6. Click "Save"

**Why:** MySQL uses port 3306, not 5432 (PostgreSQL)

---

## 📋 Step 2: Deploy MySQL Database

### Configuration:
- **Name**: `legal-ai-mysql`
- **Image**: `mysql:8`
- **Ports**: `3306:3306` (FIXED!)
- **Root Password**: `1@yLC&%Dvee*JilV@S03MgH%dEjs0%6z`
- **Normal User**: `legal_ai_user`
- **Normal User Password**: `!SeG@DZk&4yor3NXusrY1G$#i!b@NTBx`
- **Initial Database**: `legal_ai`

### After MySQL is Running:
1. Go to MySQL service → "Backups" or "Database Console"
2. Click "Database Console" or find phpMyAdmin
3. Select database: `legal_ai`
4. Click "Import" tab
5. Import files in this order:
   - `schema.sql` (from your local `chat/` folder)
   - `fir_schema.sql`
   - `chathistory.sql`
6. Click "Go" after each import

**Verify:** Check "Tables" - you should see: `ipc_sections`, `crimes`, `fir_reports`, `chat_sessions`, etc.

---

## 📋 Step 3: Deploy Rasa Action Server

### In Coolify:
1. **New Resource** → **Service** → **Dockerfile**
2. **Configuration:**
   - Name: `rasa-actions`
   - Repository: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
   - Branch: `main`
   - Dockerfile Path: `chat/Dockerfile.actions`
   - Build Context: `chat/`
   - Port: `5055`

3. **Environment Variables** (Add these):
   ```
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=!SeG@DZk&4yor3NXusrY1G$#i!b@NTBx
   DB_NAME=legal_ai
   PYTHONUNBUFFERED=1
   RASA_ACTIONS_PORT=5055
   ```

4. Click **"Deploy"**
5. Wait for build to complete
6. Check "Logs" tab - should see "Action server is running"

---

## 📋 Step 4: Deploy Rasa Server

### In Coolify:
1. **New Resource** → **Service** → **Dockerfile**
2. **Configuration:**
   - Name: `rasa`
   - Repository: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
   - Branch: `main`
   - Dockerfile Path: `chat/Dockerfile.rasa`
   - Build Context: `chat/`
   - Port: `5005`

3. **Environment Variables** (Add these):
   ```
   RASA_ACTION_ENDPOINT=http://rasa-actions:5055/webhook
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=!SeG@DZk&4yor3NXusrY1G$#i!b@NTBx
   DB_NAME=legal_ai
   PYTHONUNBUFFERED=1
   RASA_PORT=5005
   ```

4. Click **"Deploy"**
5. Wait for build (may take 5-10 minutes first time)
6. Check "Logs" - should see "Rasa server is running"

---

## 📋 Step 5: Deploy FastAPI Backend

### In Coolify:
1. **New Resource** → **Service** → **Dockerfile**
2. **Configuration:**
   - Name: `fastapi` or `legal-ai-backend`
   - Repository: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
   - Branch: `main`
   - Dockerfile Path: `chat/Dockerfile.fastapi`
   - Build Context: `chat/`
   - Port: `8080`
   - **Enable Public Access**: ✅ (CHECK THIS!)

3. **Environment Variables** (Add these):
   ```
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=!SeG@DZk&4yor3NXusrY1G$#i!b@NTBx
   DB_NAME=legal_ai
   RASA_SERVER_URL=http://rasa:5005
   PORT=8080
   HOST=0.0.0.0
   ALLOWED_ORIGINS=*
   API_KEY=Hr4vvONi2fGQd7ObjlV0e_yKj4j0LA3gJP8T2fM8M7lINWNc
   PYTHONUNBUFFERED=1
   ```

4. Click **"Deploy"**
5. Wait for build to complete
6. Note the public URL (shown in Coolify)

---

## ✅ Step 6: Verify Deployment

### Health Checks:
1. **FastAPI Health:**
   - Visit: `http://your-fastapi-url:8080/api/health`
   - Should return: `{"status":"healthy","database":"connected"}`

2. **Rasa Health:**
   - Check logs in Coolify
   - Should see: "Rasa server is running"

3. **Actions Health:**
   - Check logs in Coolify
   - Should see: "Action server is running"

### Functional Tests:
1. **Chat Interface:**
   - Visit: `http://your-fastapi-url:8080/chat`
   - Login: `admin` / `admin123`
   - Test: "What is IPC Section 302?"
   - Should get a response from the bot

2. **FIR Form:**
   - Visit: `http://your-fastapi-url:8080/fir`
   - Fill out and submit a test FIR
   - Should save successfully

3. **Admin Dashboards:**
   - FIR Admin: `http://your-fastapi-url:8080/fir/admin`
   - IPC Admin: `http://your-fastapi-url:8080/ipc/admin`

---

## 🔧 Troubleshooting

### Issue: Services Can't Connect
**Solution:**
- Verify service names match exactly: `legal-ai-mysql`, `rasa-actions`, `rasa`
- Check all services are in the same Coolify project
- Ensure MySQL is healthy (green status) before other services

### Issue: Database Connection Errors
**Solution:**
- Verify MySQL credentials match
- Check database schema is imported
- Verify `DB_HOST=legal-ai-mysql` (not localhost)

### Issue: Rasa Model Not Found
**Solution:**
- Models are in your GitHub repository
- Dockerfile copies models directory
- If missing, check build logs

### Issue: Build Failures
**Solution:**
- Check repository URL is correct
- Verify Dockerfile paths: `chat/Dockerfile.*`
- Check build context: `chat/`
- Review build logs for errors

### Issue: Port Already in Use
**Solution:**
- Each service uses unique ports: 3306, 5055, 5005, 8080
- If conflict, change port in Coolify settings

---

## 📊 Deployment Status

After deployment, you should have:
- ✅ MySQL running on port 3306
- ✅ Rasa Actions running on port 5055
- ✅ Rasa Server running on port 5005
- ✅ FastAPI running on port 8080 (publicly accessible)

---

## 🎉 Success!

Your Legal AI Assistant is now live! 

**Access your application:**
- Main URL: `http://your-fastapi-url:8080`
- Chat: `http://your-fastapi-url:8080/chat`
- FIR: `http://your-fastapi-url:8080/fir`

**All services are running and ready!** 🚀

