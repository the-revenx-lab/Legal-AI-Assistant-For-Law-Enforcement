# Development Guide

## Table of Contents
1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Code Standards](#code-standards)
4. [Development Workflow](#development-workflow)
5. [Testing](#testing)
6. [Database Management](#database-management)
7. [Deployment](#deployment)

## Development Setup

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Node.js 14+ (for development tools)
- Git

### Local Environment Setup

1. **Clone Repository**
```bash
git clone https://github.com/the-revenx-lab/Law-Enforcement-AI-Chatbot.git
cd Law-Enforcement-AI-Chatbot
```

2. **Create Virtual Environment**
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix/MacOS
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
Create `.env` file:
```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=legal_ai_db

# Rasa Configuration
RASA_ACTION_ENDPOINT=http://localhost:5055/webhook
RASA_MODEL_PATH=./models

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES=3600
```

5. **Database Setup**
```bash
# Create database
mysql -u root -p < schema.sql

# Populate initial data
python populate_database.py
```

6. **Train Rasa Model**
```bash
rasa train
```

## Project Structure

```
Legal-AI-Assistant/
├── actions/                 # Rasa custom actions
│   ├── __init__.py
│   └── actions.py
├── data/                   # Training data for Rasa
│   ├── nlu.yml
│   ├── rules.yml
│   └── stories.yml
├── static/                 # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/              # HTML templates
├── tests/                 # Test files
├── utils/                 # Utility functions
├── config.yml             # Rasa configuration
├── domain.yml            # Rasa domain
└── requirements.txt
```

## Code Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use type hints for function arguments and return values
- Maximum line length: 88 characters (Black formatter)
- Use docstrings for classes and functions

Example:
```python
from typing import List, Optional

def process_fir_data(
    fir_id: str,
    sections: List[str],
    description: Optional[str] = None
) -> dict:
    """
    Process FIR data and return formatted information.

    Args:
        fir_id (str): Unique identifier for the FIR
        sections (List[str]): List of IPC sections
        description (Optional[str]): Case description

    Returns:
        dict: Processed FIR data
    """
    # Implementation
```

### JavaScript Code Style
- Use ES6+ features
- Follow Airbnb JavaScript Style Guide
- Use JSDoc for documentation

### Git Workflow
1. Create feature branch from main
```bash
git checkout -b feature/feature-name
```

2. Make changes and commit
```bash
git add .
git commit -m "type: description"
```

3. Push changes and create PR
```bash
git push origin feature/feature-name
```

### Commit Message Format
```
type: Subject line

Body (optional)

Footer (optional)
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

## Development Workflow

### 1. Feature Development
1. Create issue in GitHub
2. Create feature branch
3. Implement changes
4. Write tests
5. Update documentation
6. Create pull request

### 2. Code Review Process
1. Self-review changes
2. Request review from team members
3. Address feedback
4. Update PR as needed
5. Merge after approval

### 3. Testing Requirements
- Unit tests for new features
- Integration tests for API endpoints
- Update existing tests if needed
- Minimum 80% code coverage

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_fir.py

# Run with coverage
pytest --cov=app tests/
```

### Test Structure
```python
# test_fir.py
import pytest
from app.models import FIR

def test_create_fir():
    fir = FIR(
        complainant="John Doe",
        sections=["IPC 302"]
    )
    assert fir.sections == ["IPC 302"]
    assert fir.status == "pending"

@pytest.mark.asyncio
async def test_async_operation():
    result = await some_async_function()
    assert result is not None
```

## Database Management

### Database Migrations
Using Alembic for migrations:
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Backup and Restore
```bash
# Backup
mysqldump -u root -p legal_ai_db > backup.sql

# Restore
mysql -u root -p legal_ai_db < backup.sql
```

## Deployment

### Production Setup
1. Update environment variables
2. Configure NGINX/Apache
3. Set up SSL certificates
4. Configure database
5. Set up monitoring

### Deployment Checklist
- [ ] Update dependencies
- [ ] Run tests
- [ ] Check security settings
- [ ] Backup database
- [ ] Update documentation
- [ ] Deploy to staging
- [ ] Verify functionality
- [ ] Deploy to production

### Monitoring
- Use Sentry for error tracking
- Set up logging
- Monitor system resources
- Set up alerts

## Troubleshooting

### Common Issues

1. **Database Connection**
```python
# Check connection
from app.db import db
try:
    db.connect()
except Exception as e:
    print(f"Connection failed: {e}")
```

2. **Rasa Server**
```bash
# Check Rasa logs
tail -f rasa.log

# Restart Rasa server
pm2 restart rasa
```

3. **API Issues**
- Check logs in `/var/log/app/`
- Verify environment variables
- Check database connectivity
- Validate JWT tokens

## Security Guidelines

1. **Code Security**
- Use parameterized queries
- Validate all inputs
- Sanitize user data
- Use secure dependencies

2. **API Security**
- Implement rate limiting
- Use HTTPS
- Validate JWT tokens
- Implement CORS properly

3. **Database Security**
- Use prepared statements
- Encrypt sensitive data
- Regular backups
- Access control

## Performance Optimization

1. **Database**
- Index frequently queried fields
- Optimize complex queries
- Use connection pooling
- Cache frequent queries

2. **API**
- Implement caching
- Paginate results
- Optimize response size
- Use async operations

3. **Frontend**
- Minimize asset sizes
- Use lazy loading
- Implement caching
- Optimize images

## Support

For development support:
- GitHub Issues: Report bugs and feature requests
- Documentation: https://docs.legalai-assistant.org
- Email: dev-support@legalai-assistant.org 