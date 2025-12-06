# 🎯 Step-by-Step Coolify Deployment

## Prerequisites Check

Before we start, confirm:
- ✅ Rasa model is trained (you've done this!)
- ✅ Code is in Git repository
- ✅ You have Coolify account access

---

## Step 1: Prepare Git Repository

If not already done:
```bash
cd chat
git add .
git commit -m "Ready for Coolify deployment - trained Rasa model included"
git push origin main
```

---

## Step 2: Create Coolify Project

1. Login to your Coolify dashboard
2. Click **"Projects"** → **"New Project"**
3. Name: `Legal AI Assistant`
4. Description: `AI-powered legal assistant for law enforcement`
5. Click **"Create"**

---

## Step 3: Deploy MySQL Database

### Option A: Using Coolify Database Service (Recommended)

1. In your project, click **"New Resource"** → **"Database"**
2. Select **"MySQL"**
3. Configure:
   - **Name**: `legal-ai-mysql`
   - **Database Name**: `legal_ai`
   - **Root Password**: `[Generate and save this!]`
   - **User**: `legal_ai_user`
   - **Password**: `[Generate and save this!]`
4. Click **"Deploy"**
5. Wait for MySQL to be healthy (green status)

### Initialize Database Schema

After MySQL is running:

**Method 1: Using Coolify Database Console**
1. Go to your MySQL service
2. Click **"Database Console"** or **"phpMyAdmin"**
3. Select database: `legal_ai`
4. Import files in this order:
   - `schema.sql`
   - `fir_schema.sql`
   - `chathistory.sql`

**Method 2: Using SQL Command (if you have SSH access)**
```bash
# Get the MySQL container name from Coolify
docker exec -i <mysql-container-name> mysql -uroot -p<root_password> legal_ai < schema.sql
docker exec -i <mysql-container-name> mysql -uroot -p<root_password> legal_ai < fir_schema.sql
docker exec -i <mysql-container-name> mysql -uroot -p<root_password> legal_ai < chathistory.sql
```

---

## Step 4: Deploy Rasa Action Server

1. In your project, click **"New Resource"** → **"Service"**
2. Select **"Dockerfile"**
3. Configure:
   - **Name**: `rasa-actions`
   - **Repository**: Your Git repository URL
   - **Branch**: `main` (or your branch)
   - **Dockerfile Path**: `chat/Dockerfile.actions`
   - **Build Context**: `chat/`
   - **Port**: `5055`

4. **Environment Variables** (Add these):
   ```
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=<your_mysql_app_password>
   DB_NAME=legal_ai
   PYTHONUNBUFFERED=1
   RASA_ACTIONS_PORT=5055
   ```

5. Click **"Deploy"**
6. Wait for build to complete
7. Verify health: Check logs for "Action server is running"

---

## Step 5: Deploy Rasa Server

1. In your project, click **"New Resource"** → **"Service"**
2. Select **"Dockerfile"**
3. Configure:
   - **Name**: `rasa`
   - **Repository**: Your Git repository URL
   - **Branch**: `main` (or your branch)
   - **Dockerfile Path**: `chat/Dockerfile.rasa`
   - **Build Context**: `chat/`
   - **Port**: `5005`

4. **Environment Variables** (Add these):
   ```
   RASA_ACTION_ENDPOINT=http://rasa-actions:5055/webhook
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=<your_mysql_app_password>
   DB_NAME=legal_ai
   PYTHONUNBUFFERED=1
   RASA_PORT=5005
   ```

5. Click **"Deploy"**
6. Wait for build to complete
7. Verify health: Check logs for "Rasa server is running"

**Note**: If you see model errors, the Dockerfile will need to train the model during build (add `rasa train` as build step).

---

## Step 6: Deploy FastAPI Backend

1. In your project, click **"New Resource"** → **"Service"**
2. Select **"Dockerfile"**
3. Configure:
   - **Name**: `fastapi` or `legal-ai-backend`
   - **Repository**: Your Git repository URL
   - **Branch**: `main` (or your branch)
   - **Dockerfile Path**: `chat/Dockerfile.fastapi`
   - **Build Context**: `chat/`
   - **Port**: `8080`
   - **Enable Public Access**: ✅ (if you want external access)

4. **Environment Variables** (Add these):
   ```
   DB_HOST=legal-ai-mysql
   DB_USER=legal_ai_user
   DB_PASSWORD=<your_mysql_app_password>
   DB_NAME=legal_ai
   RASA_SERVER_URL=http://rasa:5005
   PORT=8080
   HOST=0.0.0.0
   ALLOWED_ORIGINS=*
   API_KEY=<generate_secure_api_key>
   PYTHONUNBUFFERED=1
   ```

5. Click **"Deploy"**
6. Wait for build to complete
7. Verify health: Check logs or visit `/api/health`

---

## Step 7: Verify Deployment

### Health Checks
```bash
# FastAPI
curl http://your-fastapi-url:8080/api/health

# Rasa
curl http://your-rasa-url:5005/health

# Actions (if health endpoint exists)
curl http://your-actions-url:5055/health
```

### Functional Tests
1. **Chat Interface**
   - Visit: `http://your-fastapi-url:8080/chat`
   - Login: `admin` / `admin123`
   - Send a test message: "What is IPC Section 302?"

2. **FIR Form**
   - Visit: `http://your-fastapi-url:8080/fir`
   - Fill out and submit a test FIR

3. **Admin Dashboards**
   - FIR Admin: `http://your-fastapi-url:8080/fir/admin`
   - IPC Admin: `http://your-fastapi-url:8080/ipc/admin`

---

## 🔧 Troubleshooting

### Services Can't Connect
- **Check**: Service names match exactly in environment variables
- **Check**: All services are in the same Coolify project
- **Check**: MySQL is healthy before other services start

### Rasa Model Not Found
- **Solution**: Models should be in `models/` directory (you've trained them)
- **Alternative**: Add build step `rasa train` in Dockerfile.rasa

### Database Connection Errors
- **Check**: MySQL credentials are correct
- **Check**: Database schema is initialized
- **Check**: MySQL service name matches `DB_HOST`

### Build Failures
- **Check**: All files are in Git repository
- **Check**: Dockerfile paths are correct
- **Check**: Build context is set correctly

---

## 📝 Important Notes

1. **Service Names**: Use exact service names in environment variables
   - MySQL: `legal-ai-mysql` (or whatever you named it)
   - Actions: `rasa-actions`
   - Rasa: `rasa`

2. **Network**: All services must be in the same Coolify project to communicate

3. **Passwords**: Save all passwords securely - you'll need them!

4. **Order Matters**: Deploy in this order:
   - MySQL → Actions → Rasa → FastAPI

---

## ✅ Success Checklist

- [ ] MySQL deployed and healthy
- [ ] Database schema initialized
- [ ] Rasa Action Server deployed and running
- [ ] Rasa Server deployed and running
- [ ] FastAPI deployed and running
- [ ] Health checks passing
- [ ] Chat interface working
- [ ] FIR submission working
- [ ] IPC queries working

---

**Ready to deploy!** Follow these steps and let me know if you encounter any issues!

