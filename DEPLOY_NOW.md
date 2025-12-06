# 🚀 Deploy to Coolify - Ready to Go!

## ✅ Status: All Changes Pushed to GitHub

Your repository is updated at:
**https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git**

---

## 🎯 Quick Deployment Steps

### Step 1: Login to Coolify
1. Go to your Coolify dashboard
2. Navigate to **"Projects"**

### Step 2: Create Project
1. Click **"New Project"**
2. Name: `Legal AI Assistant`
3. Description: `AI-powered legal assistant for law enforcement`
4. Click **"Create"**

### Step 3: Deploy MySQL Database

1. In your project, click **"New Resource"** → **"Database"**
2. Select **"MySQL"**
3. Configure:
   - **Name**: `legal-ai-mysql`
   - **Database Name**: `legal_ai`
   - **Root Password**: `[Generate strong password - SAVE THIS!]`
   - **User**: `legal_ai_user`
   - **Password**: `[Generate strong password - SAVE THIS!]`
4. Click **"Deploy"**
5. **Wait for MySQL to be healthy** (green status)

#### Initialize Database Schema:
1. Go to MySQL service → **"Database Console"** or **"phpMyAdmin"**
2. Select database: `legal_ai`
3. Import these files in order:
   - `schema.sql` (from `chat/` directory)
   - `fir_schema.sql` (from `chat/` directory)
   - `chathistory.sql` (from `chat/` directory)

### Step 4: Deploy Rasa Action Server

1. Click **"New Resource"** → **"Service"** → **"Dockerfile"**
2. Configure:
   - **Name**: `rasa-actions`
   - **Repository**: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
   - **Branch**: `main`
   - **Dockerfile Path**: `chat/Dockerfile.actions`
   - **Build Context**: `chat/`
   - **Port**: `5055`
3. **Environment Variables** (Add these):
   ```
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=<your_mysql_app_password_from_step_3>
   DB_NAME=legal_ai
   PYTHONUNBUFFERED=1
   RASA_ACTIONS_PORT=5055
   ```
4. Click **"Deploy"**
5. Wait for build to complete

### Step 5: Deploy Rasa Server

1. Click **"New Resource"** → **"Service"** → **"Dockerfile"**
2. Configure:
   - **Name**: `rasa`
   - **Repository**: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
   - **Branch**: `main`
   - **Dockerfile Path**: `chat/Dockerfile.rasa`
   - **Build Context**: `chat/`
   - **Port**: `5005`
3. **Environment Variables** (Add these):
   ```
   RASA_ACTION_ENDPOINT=http://rasa-actions:5055/webhook
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=<your_mysql_app_password_from_step_3>
   DB_NAME=legal_ai
   PYTHONUNBUFFERED=1
   RASA_PORT=5005
   ```
4. Click **"Deploy"**
5. Wait for build to complete

### Step 6: Deploy FastAPI Backend

1. Click **"New Resource"** → **"Service"** → **"Dockerfile"**
2. Configure:
   - **Name**: `fastapi` or `legal-ai-backend`
   - **Repository**: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`
   - **Branch**: `main`
   - **Dockerfile Path**: `chat/Dockerfile.fastapi`
   - **Build Context**: `chat/`
   - **Port**: `8080`
   - **Enable Public Access**: ✅ (check this box)
3. **Environment Variables** (Add these):
   ```
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=<your_mysql_app_password_from_step_3>
   DB_NAME=legal_ai
   RASA_SERVER_URL=http://rasa:5005
   PORT=8080
   HOST=0.0.0.0
   ALLOWED_ORIGINS=*
   API_KEY=<generate_secure_api_key_here>
   PYTHONUNBUFFERED=1
   ```
4. Click **"Deploy"**
5. Wait for build to complete

### Step 7: Verify Deployment

1. **Check Health Endpoints:**
   - FastAPI: `http://your-fastapi-url:8080/api/health`
   - Should return: `{"status":"healthy","database":"connected"}`

2. **Test Chat Interface:**
   - Visit: `http://your-fastapi-url:8080/chat`
   - Login: `admin` / `admin123`
   - Test message: "What is IPC Section 302?"

3. **Test FIR Form:**
   - Visit: `http://your-fastapi-url:8080/fir`
   - Fill and submit a test FIR

---

## 🔑 Important Notes

1. **Service Names**: Use exact names in environment variables:
   - MySQL: `legal-ai-mysql` (or whatever you named it)
   - Actions: `rasa-actions`
   - Rasa: `rasa`

2. **Passwords**: Save all passwords securely!

3. **Deployment Order**: Must deploy in this order:
   - MySQL → Actions → Rasa → FastAPI

4. **Network**: All services must be in the same Coolify project

---

## 🆘 Troubleshooting

### If services can't connect:
- Verify service names match exactly
- Check all services are in same project
- Ensure MySQL is healthy first

### If build fails:
- Check repository URL is correct
- Verify Dockerfile paths: `chat/Dockerfile.*`
- Check build context: `chat/`

### If database errors:
- Verify schema files imported correctly
- Check MySQL credentials match
- Ensure database is initialized

---

## ✅ Success Checklist

- [ ] MySQL deployed and healthy
- [ ] Database schema initialized (3 SQL files imported)
- [ ] Rasa Action Server deployed
- [ ] Rasa Server deployed
- [ ] FastAPI deployed
- [ ] Health check passing
- [ ] Chat interface working
- [ ] FIR submission working

---

## 📞 Need Help?

If you encounter issues:
1. Check service logs in Coolify
2. Verify environment variables are set correctly
3. Ensure services are in same project
4. Check that MySQL is healthy before other services

**Your repository is ready!** 🎉

**Repository URL**: `https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git`

