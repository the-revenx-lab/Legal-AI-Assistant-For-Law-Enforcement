# 🚀 Coolify Deployment Guide

This guide will help you deploy the Legal AI Assistant to Coolify step-by-step.

## 📋 Prerequisites

1. **Coolify Account**: Sign up at [coolify.io](https://coolify.io)
2. **Coolify Instance**: Have a Coolify server running (self-hosted or cloud)
3. **Domain** (optional): For custom domain access
4. **Git Repository**: Your project should be in a Git repository (GitHub, GitLab, etc.)

---

## 🎯 Step 1: Prepare Your Repository

### 1.1 Ensure All Files Are Committed

Make sure these files are in your repository:
- ✅ `Dockerfile.rasa`
- ✅ `Dockerfile.actions`
- ✅ `Dockerfile.fastapi`
- ✅ `docker-compose.coolify.yml`
- ✅ `requirements.txt`
- ✅ All Python source files
- ✅ Rasa training data (`data/`, `domain.yml`, etc.)
- ✅ Database schemas (`schema.sql`, `fir_schema.sql`, `chathistory.sql`)

### 1.2 Push to Git

```bash
git add .
git commit -m "Add Coolify deployment configuration"
git push origin main
```

---

## 🏗️ Step 2: Create Project in Coolify

1. **Login to Coolify**
   - Open your Coolify dashboard
   - Navigate to "Projects"

2. **Create New Project**
   - Click "New Project"
   - Name: `Legal AI Assistant`
   - Description: `AI-powered legal assistant for law enforcement`
   - Click "Create"

---

## 🗄️ Step 3: Deploy MySQL Database

### 3.1 Add MySQL Service

1. In your project, click **"New Resource"** → **"Database"**
2. Select **"MySQL"**
3. Configure:
   - **Name**: `legal-ai-mysql`
   - **Database Name**: `legal_ai`
   - **Root Password**: Generate a strong password (save it!)
   - **User**: `legal_ai_user`
   - **Password**: Generate a strong password (save it!)

### 3.2 Initialize Database Schema

After MySQL is running:

1. **Option A: Using Coolify Database Console**
   - Go to your MySQL service
   - Click "Database Console" or "phpMyAdmin"
   - Import `schema.sql`, `fir_schema.sql`, and `chathistory.sql`

2. **Option B: Using Docker Exec**
   ```bash
   # Connect to MySQL container
   docker exec -i legal-ai-mysql mysql -uroot -p<root_password> legal_ai < schema.sql
   docker exec -i legal-ai-mysql mysql -uroot -p<root_password> legal_ai < fir_schema.sql
   docker exec -i legal-ai-mysql mysql -uroot -p<root_password> legal_ai < chathistory.sql
   ```

3. **Option C: Using Init Scripts (Recommended)**
   - Coolify will automatically run SQL files in `/docker-entrypoint-initdb.d/`
   - Ensure your `docker-compose.coolify.yml` has volume mounts for SQL files

---

## 🤖 Step 4: Deploy Rasa Action Server

### 4.1 Create New Service

1. In your project, click **"New Resource"** → **"Docker Compose"** or **"Service"**
2. Select **"Docker Compose"** (if available) or **"Dockerfile"**

### 4.2 Configure Rasa Actions

**If using Docker Compose:**
- Select `docker-compose.coolify.yml`
- Service name: `rasa-actions`

**If using individual service:**
- **Name**: `rasa-actions`
- **Dockerfile**: `Dockerfile.actions`
- **Port**: `5055`
- **Build Context**: Root of your repository

### 4.3 Set Environment Variables

Add these environment variables in Coolify:

```
DB_HOST=legal-ai-mysql
DB_USER=legal_ai_user
DB_PASSWORD=<your_mysql_password>
DB_NAME=legal_ai
PYTHONUNBUFFERED=1
RASA_ACTIONS_PORT=5055
```

### 4.4 Deploy

- Click "Deploy" or "Save & Deploy"
- Wait for build to complete
- Verify health: `http://your-coolify-url:5055/health`

---

## 🧠 Step 5: Deploy Rasa Server

### 5.1 Create New Service

1. **Name**: `rasa`
2. **Dockerfile**: `Dockerfile.rasa`
3. **Port**: `5005`

### 5.2 Set Environment Variables

```
RASA_ACTION_ENDPOINT=http://rasa-actions:5055/webhook
DB_HOST=legal-ai-mysql
DB_USER=legal_ai_user
DB_PASSWORD=<your_mysql_password>
DB_NAME=legal_ai
PYTHONUNBUFFERED=1
RASA_PORT=5005
```

### 5.3 Important: Train Rasa Model First

**Before deploying**, you need a trained Rasa model:

1. **Option A: Train Locally and Commit**
   ```bash
   cd chat
   rasa train
   # Commit the models/ directory
   git add models/
   git commit -m "Add trained Rasa model"
   git push
   ```

2. **Option B: Train in Coolify**
   - Add a one-time build step: `rasa train`
   - Or use a separate "training" service

### 5.4 Deploy

- Deploy the service
- Wait for build
- Verify: `http://your-coolify-url:5005/health`

---

## 🌐 Step 6: Deploy FastAPI Backend

### 6.1 Create New Service

1. **Name**: `fastapi` or `legal-ai-backend`
2. **Dockerfile**: `Dockerfile.fastapi`
3. **Port**: `8080`

### 6.2 Set Environment Variables

```
DB_HOST=legal-ai-mysql
DB_USER=legal_ai_user
DB_PASSWORD=<your_mysql_password>
DB_NAME=legal_ai
RASA_SERVER_URL=http://rasa:5005
PORT=8080
HOST=0.0.0.0
ALLOWED_ORIGINS=*
API_KEY=<generate_secure_api_key>
PYTHONUNBUFFERED=1
```

### 6.3 Configure Public Access

1. **Enable Public URL** (if you want external access)
   - Toggle "Public" in Coolify
   - Coolify will assign a public URL

2. **Custom Domain** (optional)
   - Add your domain in Coolify
   - Configure DNS records as instructed

### 6.4 Deploy

- Deploy the service
- Access via: `http://your-coolify-url:8080` or your custom domain

---

## 🔄 Step 7: Deploy Using Docker Compose (Alternative)

If Coolify supports Docker Compose deployment:

### 7.1 Create Docker Compose Service

1. **Name**: `legal-ai-stack`
2. **Compose File**: `docker-compose.coolify.yml`
3. **Environment File**: Create `.env` in Coolify with all variables

### 7.2 Set All Environment Variables

Copy all variables from `ENV_VARIABLES.md` into Coolify's environment section.

### 7.3 Deploy

- Deploy the entire stack
- All services will start together

---

## ✅ Step 8: Verify Deployment

### 8.1 Health Checks

Test each service:

```bash
# FastAPI
curl http://your-coolify-url:8080/api/health

# Rasa
curl http://your-coolify-url:5005/health

# Actions
curl http://your-coolify-url:5055/health
```

### 8.2 Test Chat Interface

1. Open: `http://your-coolify-url:8080`
2. Login with: `admin` / `admin123`
3. Try chatting: "What is IPC Section 302?"

### 8.3 Test FIR Submission

1. Navigate to: `http://your-coolify-url:8080/fir`
2. Fill out FIR form
3. Submit and verify in database

### 8.4 Check Logs

In Coolify, check logs for each service:
- Look for connection errors
- Verify database connections
- Check for missing dependencies

---

## 🔧 Step 9: Troubleshooting

### Issue: Services Can't Connect to MySQL

**Solution**:
- Verify `DB_HOST` is set to MySQL service name (not `localhost`)
- Check MySQL is running and healthy
- Verify credentials match

### Issue: Rasa Can't Reach Action Server

**Solution**:
- Verify `RASA_ACTION_ENDPOINT` uses service name: `http://rasa-actions:5055/webhook`
- Check both services are in same network
- Verify action server is healthy

### Issue: FastAPI Can't Reach Rasa

**Solution**:
- Verify `RASA_SERVER_URL` uses service name: `http://rasa:5005`
- Check Rasa is running
- Verify port is correct

### Issue: Database Schema Not Initialized

**Solution**:
- Manually run SQL files via database console
- Or use init scripts in docker-compose volumes

### Issue: Rasa Model Not Found

**Solution**:
- Train model locally and commit `models/` directory
- Or add training step to Dockerfile
- Or mount models as volume

---

## 🔐 Step 10: Security Hardening

### 10.1 Change Default Passwords

- ✅ Change `API_KEY` from `changeme`
- ✅ Use strong MySQL passwords
- ✅ Rotate credentials regularly

### 10.2 Restrict CORS

Update `ALLOWED_ORIGINS`:
```
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 10.3 Enable HTTPS

- Configure SSL certificate in Coolify
- Use Let's Encrypt (free)
- Force HTTPS redirect

### 10.4 Database Security

- Use non-root database user
- Restrict database access to application network only
- Enable MySQL SSL if available

---

## 📊 Step 11: Monitoring & Maintenance

### 11.1 Set Up Monitoring

- Use Coolify's built-in monitoring
- Set up alerts for service failures
- Monitor database connections

### 11.2 Regular Backups

- Backup MySQL database regularly
- Export Rasa models
- Backup configuration files

### 11.3 Updates

- Keep dependencies updated
- Retrain Rasa model when adding new intents
- Test updates in staging first

---

## 🎉 Success Checklist

- [ ] MySQL database deployed and initialized
- [ ] Rasa action server running and healthy
- [ ] Rasa server running and healthy
- [ ] FastAPI backend running and healthy
- [ ] All services can communicate
- [ ] Chat interface accessible
- [ ] FIR submission working
- [ ] IPC queries working
- [ ] Health checks passing
- [ ] Logs show no errors
- [ ] Security settings configured
- [ ] Custom domain configured (if applicable)

---

## 📞 Support

If you encounter issues:

1. Check Coolify logs for each service
2. Verify environment variables are set correctly
3. Test database connectivity
4. Review `PROJECT_ANALYSIS.md` for architecture details
5. Check `ENV_VARIABLES.md` for configuration

---

## 📚 Additional Resources

- [Coolify Documentation](https://coolify.io/docs)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Rasa Deployment Guide](https://rasa.com/docs/rasa/deploy)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

**Last Updated**: Generated during deployment setup
**Version**: 1.0

