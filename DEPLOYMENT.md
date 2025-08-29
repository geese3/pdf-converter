# 🚀 PDF to Image Converter 무료 웹 배포 가이드

이 가이드는 PDF to Image Converter를 **Streamlit Cloud**를 사용하여 무료로 웹에 배포하는 방법을 설명합니다.

## 🌟 Streamlit Cloud란?

**Streamlit Cloud**는 Streamlit 앱을 무료로 호스팅해주는 서비스입니다.
- ✅ **완전 무료** (개인 사용자)
- ✅ **자동 배포** (GitHub 연동)
- ✅ **SSL 인증서** 자동 제공
- ✅ **글로벌 CDN** 지원
- ✅ **자동 업데이트** (GitHub 푸시 시)

## 📋 배포 전 준비사항

### 1. GitHub 계정
- [GitHub](https://github.com)에 가입되어 있어야 합니다.

### 2. Streamlit Cloud 계정
- [Streamlit Cloud](https://share.streamlit.io/)에 가입합니다.

## 🚀 배포 단계

### 1단계: GitHub 저장소 생성

1. **GitHub에서 새 저장소 생성**
   ```
   Repository name: pdf-to-image-converter
   Description: PDF를 이미지로 변환하는 웹 애플리케이션
   Public: ✅ (무료 계정의 경우)
   ```

2. **로컬 프로젝트를 Git 저장소로 초기화**
   ```bash
   cd pdf_to_img
   git init
   git add .
   git commit -m "Initial commit: PDF to Image Converter"
   ```

3. **GitHub 원격 저장소 연결 및 푸시**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/pdf-to-image-converter.git
   git branch -M main
   git push -u origin main
   ```

### 2단계: Streamlit Cloud 배포

1. **Streamlit Cloud 접속**
   - [https://share.streamlit.io/](https://share.streamlit.io/) 접속
   - GitHub 계정으로 로그인

2. **새 앱 배포**
   - "New app" 버튼 클릭
   - GitHub 저장소 선택: `YOUR_USERNAME/pdf-to-image-converter`
   - Main file path: `streamlit_app.py`
   - "Deploy!" 버튼 클릭

3. **배포 완료**
   - 몇 분 후 배포 완료
   - 제공된 URL로 접속 가능 (예: `https://pdf-to-image-converter-xxxxx.streamlit.app`)

## ⚙️ 배포 설정

### Streamlit 설정 파일

프로젝트 루트에 `.streamlit/config.toml` 파일을 생성하여 추가 설정을 할 수 있습니다:

```toml
[server]
maxUploadSize = 200
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

### 환경 변수 설정

Streamlit Cloud에서 환경 변수를 설정할 수 있습니다:

1. 앱 설정 → Secrets
2. 다음 내용 추가:
   ```toml
   [general]
   debug = false
   ```

## 🔧 문제 해결

### 일반적인 배포 오류

#### 1. **poppler-utils 오류**
```
Error: poppler-utils not found
```

**해결방법**: `requirements.txt`에서 `poppler-utils` 제거 (Streamlit Cloud에서 자동 설치됨)

#### 2. **메모리 부족 오류**
```
Error: Memory limit exceeded
```

**해결방법**: 
- DPI 값을 낮게 설정
- 큰 PDF 파일 처리 시 페이지 범위 제한

#### 3. **업로드 크기 제한**
```
Error: File too large
```

**해결방법**: `.streamlit/config.toml`에서 `maxUploadSize` 증가

### 로그 확인

Streamlit Cloud에서 앱 로그를 확인할 수 있습니다:
1. 앱 설정 → Logs
2. 오류 메시지 및 디버깅 정보 확인

## 📱 모바일 최적화

### 반응형 디자인
- Streamlit은 자동으로 모바일 친화적
- 터치 제스처 지원
- 모바일 브라우저 최적화

### 성능 최적화
- 작은 화면에서도 사용하기 편함
- 터치 친화적 UI 요소

## 🔄 자동 업데이트

### GitHub 연동
- GitHub에 코드 푸시 시 자동 배포
- 새로운 기능 추가 시 즉시 반영
- 버그 수정 시 자동 업데이트

### 배포 상태 모니터링
- Streamlit Cloud 대시보드에서 배포 상태 확인
- 성공/실패 알림
- 성능 메트릭 확인

## 💰 비용

### 무료 계정
- **개인 사용자**: 완전 무료
- **팀 계정**: 월 $10부터
- **기업 계정**: 맞춤형 가격

### 제한사항
- **개인 계정**: 앱당 1GB RAM, 1GB 디스크
- **동시 사용자**: 제한 없음
- **월 사용량**: 제한 없음

## 🌍 커스텀 도메인

### 도메인 연결
1. **도메인 소유권 확인**
2. **DNS 설정 변경**
3. **SSL 인증서 자동 발급**

### 예시
```
기본 URL: https://pdf-to-image-converter-xxxxx.streamlit.app
커스텀 도메인: https://pdf-converter.yourdomain.com
```

## 📊 분석 및 모니터링

### 사용 통계
- 일일/월간 방문자 수
- 페이지 뷰
- 사용자 행동 분석

### 성능 모니터링
- 응답 시간
- 오류율
- 리소스 사용량

## 🔒 보안

### 자동 보안 기능
- HTTPS 강제 적용
- XSS 보호
- CSRF 보호
- 파일 업로드 검증

### 개인정보 보호
- 업로드된 파일은 임시 저장
- 자동 정리
- 로그에 민감한 정보 저장 안함

## 🚀 고급 기능

### API 엔드포인트
- RESTful API 제공
- 외부 시스템 연동 가능
- 웹훅 지원

### 데이터베이스 연동
- PostgreSQL, MySQL 지원
- 사용자 데이터 저장
- 변환 히스토리 관리

## 📞 지원

### 공식 지원
- [Streamlit 문서](https://docs.streamlit.io/)
- [Streamlit 커뮤니티](https://discuss.streamlit.io/)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)

### 커뮤니티 지원
- Stack Overflow
- Reddit r/streamlit
- Discord 서버

## 🎯 다음 단계

배포가 완료되면 다음을 고려해보세요:

1. **사용자 피드백 수집**
2. **성능 최적화**
3. **새로운 기능 추가**
4. **사용자 가이드 작성**
5. **마케팅 및 홍보**

---

**🎉 축하합니다!** 이제 PDF to Image Converter가 웹에서 전 세계 사람들이 사용할 수 있게 되었습니다!
