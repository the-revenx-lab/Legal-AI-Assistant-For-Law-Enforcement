# 🔐 Environment Variables Documentation

This document lists all environment variables required for the Legal AI Assistant deployment.

## 📋 Quick Reference

| Variable | Service | Default | Required | Description |
|----------|---------|---------|----------|-------------|
| `MYSQL_ROOT_PASSWORD` | MySQL | - | ✅ | MySQL root password |
| `MYSQL_DATABASE` | MySQL | `legal_ai` | ❌ | Database name |
| `MYSQL_USER` | MySQL | `legal_ai_user` | ❌ | Application database user |
| `MYSQL_PASSWORD` | MySQL | - | ✅ | Application database password |
| `DB_HOST` | All | `localhost` | ❌ | MySQL hostname |
| `DB_USER` | All | `root` | ❌ | Database username |
| `DB_PASSWORD` | All | `pass` | ❌ | Database password |
| `DB_NAME` | All | `legal_ai` | ❌ | Database name |
| `PORT` | FastAPI | `8080` | ❌ | FastAPI port |
| `HOST` | FastAPI | `0.0.0.0` | ❌ | FastAPI host |
| `ALLOWED_ORIGINS` | FastAPI | `*` | ❌ | CORS allowed origins |
| `API_KEY` | FastAPI | `changeme` | ❌ | API key for protected endpoints |
| `RASA_SERVER_URL` | FastAPI | `http://localhost:5005` | ❌ | Rasa server URL |
| `RASA_ACTION_ENDPOINT` | Rasa | `http://localhost:5055/webhook` | ❌ | Action server URL |
| `RASA_PORT` | Rasa | `5005` | ❌ | Rasa server port |
| `RASA_ACTIONS_PORT` | Actions | `5055` | ❌ | Action server port |
| `PYTHONUNBUFFERED` | All | `1` | ❌ | Python output buffering |

---

## 🗄️ MySQL Database Variables

### `MYSQL_ROOT_PASSWORD`
- **Type**: String
- **Required**: ✅ Yes
- **Default**: None
- **Description**: Root password for MySQL database
- **Example**: `MySecureRootPassword123!`
- **Security**: ⚠️ **CRITICAL** - Use a strong password in production

### `MYSQL_DATABASE`
- **Type**: String
- **Required**: ❌ No
- **Default**: `legal_ai`
- **Description**: Name of the database to create
- **Example**: `legal_ai`

### `MYSQL_USER`
- **Type**: String
- **Required**: ❌ No
- **Default**: `legal_ai_user`
- **Description**: Application database user (non-root)
- **Example**: `legal_ai_user`

### `MYSQL_PASSWORD`
- **Type**: String
- **Required**: ✅ Yes
- **Default**: None
- **Description**: Password for the application database user
- **Example**: `MySecureAppPassword123!`
- **Security**: ⚠️ **CRITICAL** - Use a strong password in production

---

## 🔌 Application Database Connection Variables

These variables are used by FastAPI, Rasa, and Action Server to connect to MySQL.

### `DB_HOST`
- **Type**: String
- **Required**: ❌ No
- **Default**: `localhost`
- **Description**: MySQL server hostname
- **Local**: `localhost`
- **Docker**: `mysql` (service name)
- **Production**: Your MySQL server hostname/IP

### `DB_USER`
- **Type**: String
- **Required**: ❌ No
- **Default**: `root` (actions.py) or `root1` (config.py)
- **Description**: Database username
- **Recommendation**: Use `MYSQL_USER` value (non-root user)
- **Example**: `legal_ai_user`

### `DB_PASSWORD`
- **Type**: String
- **Required**: ❌ No
- **Default**: `pass`
- **Description**: Database password
- **Recommendation**: Use `MYSQL_PASSWORD` value
- **Security**: ⚠️ **CRITICAL** - Never use default in production

### `DB_NAME`
- **Type**: String
- **Required**: ❌ No
- **Default**: `legal_ai`
- **Description**: Database name
- **Example**: `legal_ai`

---

## 🚀 FastAPI Backend Variables

### `PORT`
- **Type**: Integer
- **Required**: ❌ No
- **Default**: `8080`
- **Description**: Port on which FastAPI server listens
- **Example**: `8080`

### `HOST`
- **Type**: String
- **Required**: ❌ No
- **Default**: `0.0.0.0`
- **Description**: Host on which FastAPI server binds
- **Local**: `127.0.0.1` or `localhost`
- **Docker/Production**: `0.0.0.0` (all interfaces)

### `ALLOWED_ORIGINS`
- **Type**: String (comma-separated)
- **Required**: ❌ No
- **Default**: `*` (all origins)
- **Description**: CORS allowed origins
- **Example**: `http://localhost:8080,https://yourdomain.com`
- **Security**: ⚠️ Restrict in production

### `API_KEY`
- **Type**: String
- **Required**: ❌ No
- **Default**: `changeme`
- **Description**: API key for protected endpoints (FIR/IPC admin operations)
- **Security**: ⚠️ **CRITICAL** - Change in production
- **Example**: `your-secure-api-key-here`

### `RASA_SERVER_URL`
- **Type**: String (URL)
- **Required**: ❌ No
- **Default**: `http://localhost:5005`
- **Description**: Rasa server URL
- **Local**: `http://localhost:5005`
- **Docker**: `http://rasa:5005`
- **Production**: `https://your-rasa-server.com`

---

## 🤖 Rasa Server Variables

### `RASA_ACTION_ENDPOINT`
- **Type**: String (URL)
- **Required**: ❌ No
- **Default**: `http://localhost:5055/webhook`
- **Description**: Rasa action server webhook URL
- **Local**: `http://localhost:5055/webhook`
- **Docker**: `http://rasa-actions:5055/webhook`
- **Production**: `https://your-action-server.com/webhook`

### `RASA_PORT`
- **Type**: Integer
- **Required**: ❌ No
- **Default**: `5005`
- **Description**: Port on which Rasa server listens
- **Example**: `5005`

---

## ⚙️ Rasa Action Server Variables

### `RASA_ACTIONS_PORT`
- **Type**: Integer
- **Required**: ❌ No
- **Default**: `5055`
- **Description**: Port on which Rasa action server listens
- **Example**: `5055`

---

## 🐍 Python Configuration

### `PYTHONUNBUFFERED`
- **Type**: String
- **Required**: ❌ No
- **Default**: `1`
- **Description**: Disable Python output buffering (useful for Docker logs)
- **Values**: `1` (enabled) or `0` (disabled)
- **Recommendation**: Keep as `1` for Docker deployments

---

## 📝 Environment-Specific Configurations

### Local Development
```bash
DB_HOST=localhost
DB_USER=root1
DB_PASSWORD=pass
DB_NAME=legal_ai
RASA_SERVER_URL=http://localhost:5005
RASA_ACTION_ENDPOINT=http://localhost:5055/webhook
ALLOWED_ORIGINS=http://localhost:8080
```

### Docker Compose
```bash
DB_HOST=mysql
DB_USER=legal_ai_user
DB_PASSWORD=legal_ai_pass_change_me
DB_NAME=legal_ai
RASA_SERVER_URL=http://rasa:5005
RASA_ACTION_ENDPOINT=http://rasa-actions:5055/webhook
ALLOWED_ORIGINS=*
```

### Production (Coolify)
```bash
DB_HOST=mysql
DB_USER=legal_ai_user
DB_PASSWORD=<strong-secure-password>
DB_NAME=legal_ai
RASA_SERVER_URL=http://rasa:5005
RASA_ACTION_ENDPOINT=http://rasa-actions:5055/webhook
ALLOWED_ORIGINS=https://yourdomain.com
API_KEY=<strong-secure-api-key>
MYSQL_ROOT_PASSWORD=<strong-secure-root-password>
MYSQL_PASSWORD=<strong-secure-app-password>
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong passwords** for all database credentials
3. **Restrict `ALLOWED_ORIGINS`** in production
4. **Change `API_KEY`** from default value
5. **Use non-root database user** for applications
6. **Enable SSL/TLS** for database connections in production
7. **Rotate credentials** regularly
8. **Use secrets management** (Coolify has built-in support)

---

## 🧪 Testing Environment Variables

To verify your environment variables are loaded correctly:

### FastAPI
```bash
curl http://localhost:8080/api/health
```

### Rasa
```bash
curl http://localhost:5005/health
```

### Action Server
```bash
curl http://localhost:5055/health
```

---

## 📚 Additional Resources

- [Coolify Environment Variables Documentation](https://coolify.io/docs/environment-variables)
- [Docker Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [FastAPI Configuration](https://fastapi.tiangolo.com/advanced/settings/)

---

**Last Updated**: Generated during deployment setup
**Version**: 1.0

