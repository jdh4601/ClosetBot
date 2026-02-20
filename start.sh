#!/bin/bash

# Fashion Influencer Matcher - Quick Start Script

echo "🚀 Fashion Influencer Matcher 시작 중..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다. .env.example을 복사합니다."
    cp .env.example .env
    echo "📝 .env 파일을 편집하여 Instagram API 키를 설정하세요."
fi

# Start Docker Compose
echo "🐳 Docker Compose 시작..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ 서비스 시작 대기 중..."
sleep 10

# Check services
echo "🔍 서비스 상태 확인..."
docker-compose ps

echo ""
echo "✅ 모든 서비스가 시작되었습니다!"
echo ""
echo "🌐 접속 주소:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 종료하려면: docker-compose down"
