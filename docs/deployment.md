# Deployment Guide

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
sudo apt update
sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3-pip python3-venv nginx mysql-server supervisor
```

### 2. Python Environment
```bash
# Create project directory
mkdir -p /opt/legal-ai
cd /opt/legal-ai

# Clone repository
git clone https://github.com/the-revenx-lab/Law-Enforcement-AI-Chatbot.git
cd Law-Enforcement-AI-Chatbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
mysql -u root -p <<EOF
CREATE DATABASE legal_ai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'legal_ai_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON legal_ai_db.* TO 'legal_ai_user'@'localhost';
FLUSH PRIVILEGES;
EOF

# Import schema
mysql -u legal_ai_user -p legal_ai_db < schema.sql
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

### 1. Initial Deployment

```bash
# Create deployment directory
sudo mkdir -p /opt/legal-ai
sudo chown -R www-data:www-data /opt/legal-ai

# Clone repository
cd /opt/legal-ai
git clone https://github.com/the-revenx-lab/Law-Enforcement-AI-Chatbot.git

# Setup environment
cd Law-Enforcement-AI-Chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
nano .env  # Edit with production values

# Initialize database
python manage.py db upgrade

# Start services
sudo systemctl start nginx
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start legal-ai
```

### 2. Updates and Maintenance

```bash
# Pull updates
cd /opt/legal-ai/Law-Enforcement-AI-Chatbot
git pull origin master

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Apply database migrations
python manage.py db upgrade

# Restart services
sudo supervisorctl restart legal-ai
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
MYSQL_USER="legal_ai_user"
MYSQL_PASS="your_secure_password"
DB_NAME="legal_ai_db"
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
mysql -u legal_ai_user -p -e "SELECT 1;"

# Reset MySQL password if needed
sudo mysql -u root
ALTER USER 'legal_ai_user'@'localhost' IDENTIFIED BY 'new_password';
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
- System Administrator: reachirfankhani@gmail.com
- Database Administrator: reachirfankhani@gmail.com
- Security Team: reachirfankhani@gmail.com
- Support Team: reachirfankhani@gmail.com 
