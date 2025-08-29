# PDF to Image Converter

PDF 파일을 다양한 이미지 형식(PNG, JPEG, TIFF, BMP, GIF)으로 변환하는 Python 프로그램입니다.

## 🌟 **NEW: 설치 없이 사용하는 웹 버전!**

**poppler나 Python 설치 없이** 바로 사용할 수 있는 웹 버전이 추가되었습니다!

- 🌐 **웹에서 바로 사용**: https://pdf-converter-owners.streamlit.app/
- 📱 **모바일 친화적**: 터치 인터페이스 지원
- 🚀 **설치 불필요**: 브라우저만 있으면 OK
- ⚡ **PyMuPDF 기반**: poppler 의존성 제거

## 🚀 주요 기능

- **다양한 이미지 형식 지원**: PNG, JPEG, TIFF, BMP, GIF
- **페이지별 변환**: 각 페이지를 개별 이미지로 변환
- **단일 이미지 변환**: 모든 페이지를 하나의 긴 이미지로 연결
- **페이지 범위 선택**: 특정 페이지만 변환 가능
- **해상도 조정**: DPI 값을 조정하여 이미지 품질 설정
- **웹 인터페이스**: Streamlit을 사용한 사용자 친화적인 GUI
- **명령줄 인터페이스**: CLI를 통한 배치 처리 지원

## 📋 요구사항

- Python 3.7+
- macOS, Windows, Linux 지원

## 🔧 설치 방법

### 1. 저장소 클론 또는 다운로드
```bash
git clone <repository-url>
cd pdf_to_img
```

### 2. 가상환경 생성 및 활성화 (권장)
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows
```

### 3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 시스템 의존성 설치

#### macOS
```bash
brew install poppler
```

#### Ubuntu/Debian
```bash
sudo apt-get install poppler-utils
```

#### Windows
1. [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases) 다운로드
2. 압축 해제 후 `bin` 폴더를 시스템 PATH에 추가

## 🎯 사용 방법

### 🌐 웹 인터페이스 (Streamlit) - **추천!**

#### **방법 1: 설치 없이 웹에서 바로 사용 (NEW!)**
**가장 간단한 방법입니다!**

🌐 **바로 사용하기**: https://pdf-converter-owners.streamlit.app/

- ✅ **설치 불필요**
- ✅ **poppler 불필요**
- ✅ **모바일 지원**
- ✅ **언제 어디서나 접근 가능**

#### **방법 2: 로컬에서 실행**
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하여 사용하세요.

### 명령줄 인터페이스

#### 기본 사용법
```bash
python pdf_converter.py document.pdf
```

#### 고급 옵션
```bash
# JPEG 형식으로 변환, 300 DPI
python pdf_converter.py document.pdf -f JPEG -d 300

# 특정 페이지 범위만 변환
python pdf_converter.py document.pdf --first-page 1 --last-page 5

# 모든 페이지를 하나의 이미지로 변환
python pdf_converter.py document.pdf --single-image

# 출력 디렉토리 지정
python pdf_converter.py document.pdf -o my_images
```

#### 도움말 보기
```bash
python pdf_converter.py --help
```

### Python 코드에서 사용

```python
from pdf_converter import PDFConverter

# 변환기 초기화
converter = PDFConverter("output_directory")

# PDF를 이미지로 변환
output_files = converter.convert_pdf_to_images(
    "document.pdf",
    output_format="PNG",
    dpi=200,
    first_page=1,
    last_page=5
)

# 모든 페이지를 하나의 이미지로 변환
output_file = converter.convert_pdf_to_single_image(
    "document.pdf",
    output_format="JPEG",
    dpi=300
)
```

## 📁 출력 파일

- **페이지별 변환**: `filename_page_001.png`, `filename_page_002.png`, ...
- **단일 이미지 변환**: `filename_combined.png`
- 기본 출력 디렉토리: `converted_images/`

## ⚙️ 설정 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `-f, --format` | 출력 이미지 형식 | PNG |
| `-d, --dpi` | 이미지 해상도 | 200 |
| `-o, --output-dir` | 출력 디렉토리 | converted_images |
| `--first-page` | 시작 페이지 번호 | 1 |
| `--last-page` | 마지막 페이지 번호 | 마지막 페이지 |
| `--single-image` | 모든 페이지를 하나의 이미지로 변환 | False |

## 🔍 지원 형식

### 입력
- **PDF**: 모든 표준 PDF 파일

### 출력
- **PNG**: 투명도 지원, 무손실 압축
- **JPEG**: 압축률 높음, 파일 크기 작음
- **TIFF**: 고품질, 다양한 압축 옵션
- **BMP**: 비트맵 형식, 압축 없음
- **GIF**: 애니메이션 지원 (단일 페이지만)

## 🐛 문제 해결

### 일반적인 오류

1. **pdf2image 오류**
   - poppler가 설치되어 있는지 확인
   - 시스템 PATH에 poppler가 추가되어 있는지 확인

2. **메모리 부족**
   - DPI 값을 낮춰보세요
   - 페이지 범위를 제한해보세요

3. **권한 오류**
   - 출력 디렉토리에 쓰기 권한이 있는지 확인

4. **라이브러리 설치 오류**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### 디버깅

로깅을 활성화하여 문제를 진단할 수 있습니다:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해주세요.
