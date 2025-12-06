#!/bin/bash
# Automated Deployment Script for Legal AI Assistant
# This script automates the deployment process

set -e  # Exit on error

echo "🚀 Starting Legal AI Assistant Deployment Automation"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: requirements.txt not found. Please run this script from the chat/ directory${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Project structure verified${NC}"

# Check if Rasa model exists
if [ ! -d "models" ] || [ -z "$(ls -A models/*.tar.gz 2>/dev/null)" ]; then
    echo -e "${YELLOW}⚠ Warning: No Rasa models found. Training model...${NC}"
    rasa train
    echo -e "${GREEN}✓ Rasa model trained${NC}"
else
    echo -e "${GREEN}✓ Rasa models found${NC}"
fi

# Verify SQL files exist
for sql_file in schema.sql fir_schema.sql chathistory.sql; do
    if [ ! -f "$sql_file" ]; then
        echo -e "${RED}Error: $sql_file not found${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✓ All SQL files verified${NC}"

# Verify Dockerfiles exist
for dockerfile in Dockerfile.rasa Dockerfile.actions Dockerfile.fastapi; do
    if [ ! -f "$dockerfile" ]; then
        echo -e "${RED}Error: $dockerfile not found${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✓ All Dockerfiles verified${NC}"

echo ""
echo -e "${GREEN}✅ Pre-deployment checks passed!${NC}"
echo ""
echo "📋 Next Steps:"
echo "1. Push all changes to GitHub:"
echo "   git add ."
echo "   git commit -m 'Ready for deployment'"
echo "   git push origin main"
echo ""
echo "2. In Coolify, deploy services in this order:"
echo "   - MySQL Database (legal-ai-mysql)"
echo "   - Rasa Action Server (rasa-actions)"
echo "   - Rasa Server (rasa)"
echo "   - FastAPI Backend (fastapi)"
echo ""
echo "3. Use credentials from DEPLOYMENT_CREDENTIALS.txt"
echo ""
echo "🎉 Deployment automation complete!"

