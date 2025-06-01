# Deployment Guide for Legal AI Assistant

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Infrastructure Requirements](#infrastructure-requirements)
4. [Deployment Steps](#deployment-steps)
5. [Security Configuration](#security-configuration)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Backup and Recovery](#backup-and-recovery)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- Ubuntu 20.04 LTS or higher
- Python 3.8+
- MySQL 8.0+
- Node.js 14+ (for development tools)
- Nginx 1.18+
- SSL Certificate
- Git
- A server/cloud platform (Recommended: AWS, Google Cloud, or Azure)

### Resource Requirements
- CPU: Minimum 4 cores
- RAM: Minimum 8GB
- Storage: 50GB SSD
- Network: 100Mbps with public IP

### Access Requirements
- SSH access to server
- GitHub repository access
- Domain name (if applicable)
- SSL certificate
- Database backup location

## Environment Setup

### 1. System Updates
```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade

# Install Python and required system dependencies
sudo apt-get install python3.8 python3.8-venv python3-pip mysql-server nginx

# Install required system libraries
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
```

### 2. Python Environment
```bash
# Clone the repository
git clone https://github.com/the-revenx-lab/Law-Enforcement-AI-Chatbot.git
cd Law-Enforcement-AI-Chatbot

# Create and activate virtual environment
python3.8 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Configure MySQL
sudo mysql_secure_installation

# Create database and user
mysql -u root -p
CREATE DATABASE legal_ai;
CREATE USER 'legal_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON legal_ai.* TO 'legal_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
DB_HOST=localhost
DB_USER=legal_user
DB_PASSWORD=your_secure_password
DB_NAME=legal_ai
RASA_ACTION_ENDPOINT=http://localhost:5055/webhook
ENVIRONMENT=production
```

### 5. Initialize and Train
```bash
# Initialize database
python populate_database.py

# Train Rasa model
rasa train
```

### 6. Setting up Services
Create systemd service files for each component:

#### Rasa Action Server
```ini
# /etc/systemd/system/rasa-actions.service
[Unit]
Description=Rasa Action Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/rasa run actions

[Install]
WantedBy=multi-user.target
```

#### Rasa Server
```ini
# /etc/systemd/system/rasa-server.service
[Unit]
Description=Rasa Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/rasa run --enable-api --cors "*"

[Install]
WantedBy=multi-user.target
```

#### Web Interface
```ini
# /etc/systemd/system/legal-ai-web.service
[Unit]
Description=Legal AI Web Interface
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/python chat.py

[Install]
WantedBy=multi-user.target
```

### 7. Start Services
```bash
sudo systemctl start rasa-actions
sudo systemctl start rasa-server
sudo systemctl start legal-ai-web
sudo systemctl enable rasa-actions
sudo systemctl enable rasa-server
sudo systemctl enable legal-ai-web
```

### 8. Nginx Configuration
```nginx
# /etc/nginx/sites-available/legal-ai
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /webhooks/ {
        proxy_pass http://localhost:5005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 9. SSL Setup (Recommended)
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your_domain.com
```

## Infrastructure Requirements

### Production Server Architecture
```
                                   [Load Balancer]
                                         |
                    +--------------------+--------------------+
                    |                    |                   |
            [Web Server 1]        [Web Server 2]    [Web Server N]
                    |                    |                   |
                    +--------------------+--------------------+
                                         |
                                  [Database Server]
                                         |
                              [Backup/Replica Server]
```

### Server Configuration

1. **Web Servers**
```nginx
# /etc/nginx/sites-available/legal-ai.conf
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

2. **Application Server (Gunicorn)**
```bash
# /etc/supervisor/conf.d/legal-ai.conf
[program:legal-ai]
directory=/opt/legal-ai/Law-Enforcement-AI-Chatbot
command=/opt/legal-ai/Law-Enforcement-AI-Chatbot/venv/bin/gunicorn app:app -w 4 -k gevent -b 127.0.0.1:5000
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/legal-ai/err.log
stdout_logfile=/var/log/legal-ai/out.log
```

## Deployment Steps

### 1. System Setup
```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade

# Install Python and required system dependencies
sudo apt-get install python3.8 python3.8-venv python3-pip mysql-server nginx

# Install required system libraries
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
```

### 2. Project Setup
```bash
# Clone the repository
git clone https://github.com/the-revenx-lab/Law-Enforcement-AI-Chatbot.git
cd Law-Enforcement-AI-Chatbot

# Create and activate virtual environment
python3.8 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Configure MySQL
sudo mysql_secure_installation

# Create database and user
mysql -u root -p
CREATE DATABASE legal_ai;
CREATE USER 'legal_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON legal_ai.* TO 'legal_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
DB_HOST=localhost
DB_USER=legal_user
DB_PASSWORD=your_secure_password
DB_NAME=legal_ai
RASA_ACTION_ENDPOINT=http://localhost:5055/webhook
ENVIRONMENT=production
```

### 5. Initialize and Train
```bash
# Initialize database
python populate_database.py

# Train Rasa model
rasa train
```

### 6. Setting up Services
Create systemd service files for each component:

#### Rasa Action Server
```ini
# /etc/systemd/system/rasa-actions.service
[Unit]
Description=Rasa Action Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/rasa run actions

[Install]
WantedBy=multi-user.target
```

#### Rasa Server
```ini
# /etc/systemd/system/rasa-server.service
[Unit]
Description=Rasa Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/rasa run --enable-api --cors "*"

[Install]
WantedBy=multi-user.target
```

#### Web Interface
```ini
# /etc/systemd/system/legal-ai-web.service
[Unit]
Description=Legal AI Web Interface
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/python chat.py

[Install]
WantedBy=multi-user.target
```

### 7. Start Services
```bash
sudo systemctl start rasa-actions
sudo systemctl start rasa-server
sudo systemctl start legal-ai-web
sudo systemctl enable rasa-actions
sudo systemctl enable rasa-server
sudo systemctl enable legal-ai-web
```

### 8. Nginx Configuration
```nginx
# /etc/nginx/sites-available/legal-ai
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /webhooks/ {
        proxy_pass http://localhost:5005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 9. SSL Setup (Recommended)
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your_domain.com
```

## Security Configuration

### 1. Firewall Setup
```bash
# Configure UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 2. SSL Configuration
```nginx
# Strong SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
ssl_stapling on;
ssl_stapling_verify on;
```

### 3. Security Headers
```nginx
# Security headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Content-Security-Policy "default-src 'self';" always;
```

## Monitoring and Maintenance

### 1. Log Monitoring
```bash
# Application logs
tail -f /var/log/legal-ai/out.log
tail -f /var/log/legal-ai/err.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# System logs
journalctl -u supervisor
journalctl -u nginx
```

### 2. Performance Monitoring
```bash
# Install monitoring tools
sudo apt install -y prometheus node-exporter grafana

# Configure Prometheus
cat << EOF > /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
EOF

# Start monitoring services
sudo systemctl enable prometheus
sudo systemctl start prometheus
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

## Backup and Recovery

### 1. Database Backup
```bash
#!/bin/bash
# /opt/legal-ai/backup.sh

BACKUP_DIR="/backup/legal-ai"
MYSQL_USER="legal_user"
MYSQL_PASS="your_secure_password"
DB_NAME="legal_ai"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
mysqldump -u $MYSQL_USER -p$MYSQL_PASS $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Remove backups older than 30 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +30 -delete
```

### 2. Application Backup
```bash
#!/bin/bash
# /opt/legal-ai/app-backup.sh

BACKUP_DIR="/backup/legal-ai"
APP_DIR="/opt/legal-ai"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup application files
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz $APP_DIR

# Remove backups older than 7 days
find $BACKUP_DIR -name "app_backup_*.tar.gz" -mtime +7 -delete
```

## Troubleshooting

### Common Issues and Solutions

1. **Application Not Starting**
```bash
# Check logs
sudo supervisorctl status legal-ai
tail -f /var/log/legal-ai/err.log

# Check permissions
sudo chown -R www-data:www-data /opt/legal-ai
sudo chmod -R 755 /opt/legal-ai
```

2. **Database Connection Issues**
```bash
# Check MySQL status
sudo systemctl status mysql

# Check connection
mysql -u legal_user -p -e "SELECT 1;"

# Reset MySQL password if needed
sudo mysql -u root
ALTER USER 'legal_user'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

3. **Nginx Issues**
```bash
# Test configuration
sudo nginx -t

# Check status
sudo systemctl status nginx

# Check error logs
tail -f /var/log/nginx/error.log
```

### Health Check Endpoints

```python
@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
```

### Emergency Contacts

Maintain a list of emergency contacts:
- System Administrator: admin@legal-ai.com
- Database Administrator: dba@legal-ai.com
- Security Team: security@legal-ai.com
- Support Team: support@legal-ai.com

## Performance Optimization
1. Configure Nginx worker processes
2. Optimize MySQL settings
3. Use caching where appropriate
4. Monitor and adjust resource allocation

## Scaling Considerations
1. Use load balancer for multiple instances
2. Implement database replication
3. Use container orchestration (optional)
4. Set up monitoring and alerting

Remember to replace placeholders like `your_domain.com` and paths with actual values. 