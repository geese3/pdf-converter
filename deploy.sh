#!/bin/bash

# PDF to Image Converter 배포 스크립트
echo "🚀 PDF to Image Converter 배포 시작..."

# Git 상태 확인
if [ ! -d ".git" ]; then
    echo "📁 Git 저장소 초기화..."
    git init
fi

# 모든 파일 추가
echo "📝 파일 추가 중..."
git add .

# 커밋
echo "💾 커밋 중..."
git commit -m "Update: PDF to Image Converter for Streamlit Cloud deployment"

# 원격 저장소 확인
if ! git remote | grep -q "origin"; then
    echo "⚠️  원격 저장소가 설정되지 않았습니다."
    echo "다음 명령어로 원격 저장소를 추가하세요:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/pdf-to-image-converter.git"
    echo "git branch -M main"
    echo "git push -u origin main"
else
    echo "🚀 GitHub에 푸시 중..."
    git push origin main
    echo "✅ 배포 완료!"
    echo ""
    echo "🌐 다음 단계:"
    echo "1. https://share.streamlit.io/ 접속"
    echo "2. GitHub 계정으로 로그인"
    echo "3. 'New app' 클릭"
    echo "4. 저장소 선택: YOUR_USERNAME/pdf-to-image-converter"
    echo "5. Main file path: streamlit_app.py"
    echo "6. 'Deploy!' 클릭"
    echo ""
    echo "🎉 몇 분 후 웹에서 사용할 수 있습니다!"
fi
