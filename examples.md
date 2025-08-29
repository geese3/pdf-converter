# PDF to Image Converter 사용 예제

## 🚀 기본 사용법

### 1. 단일 PDF 파일 변환

```bash
# 기본 설정으로 PDF를 PNG로 변환
python pdf_converter.py document.pdf

# JPEG 형식으로 변환, 300 DPI
python pdf_converter.py document.pdf -f JPEG -d 300

# 특정 출력 디렉토리 지정
python pdf_converter.py document.pdf -o my_images
```

### 2. 페이지 범위 지정

```bash
# 1-5페이지만 변환
python pdf_converter.py document.pdf --first-page 1 --last-page 5

# 10페이지부터 끝까지 변환
python pdf_converter.py document.pdf --first-page 10
```

### 3. 단일 이미지로 변환

```bash
# 모든 페이지를 하나의 긴 이미지로 연결
python pdf_converter.py document.pdf --single-image

# 고품질 JPEG로 단일 이미지 생성
python pdf_converter.py document.pdf --single-image -f JPEG -d 400
```

## 📁 배치 처리

### 1. 디렉토리 내 모든 PDF 변환

```bash
# 현재 디렉토리의 모든 PDF를 PNG로 변환
python batch_convert.py .

# 특정 디렉토리의 PDF들을 JPEG로 변환
python batch_convert.py /path/to/pdfs -f JPEG

# 하위 디렉토리까지 재귀적으로 검색
python batch_convert.py /path/to/pdfs -r
```

### 2. 고급 배치 옵션

```bash
# 고품질 이미지로 변환 (400 DPI)
python batch_convert.py /path/to/pdfs -d 400

# 특정 페이지 범위만 변환
python batch_convert.py /path/to/pdfs --first-page 1 --last-page 3

# 모든 PDF를 단일 이미지로 변환
python batch_convert.py /path/to/pdfs --single-image

# 상세한 로그 출력
python batch_convert.py /path/to/pdfs -v
```

## 🎨 이미지 형식별 특징

### PNG (권장)
- 투명도 지원
- 무손실 압축
- 텍스트와 그래픽에 적합
- 파일 크기가 큼

```bash
python pdf_converter.py document.pdf -f PNG -d 300
```

### JPEG
- 압축률 높음
- 파일 크기 작음
- 사진과 이미지에 적합
- 투명도 미지원

```bash
python pdf_converter.py document.pdf -f JPEG -d 300
```

### TIFF
- 고품질 이미지
- 다양한 압축 옵션
- 전문가용 형식
- 파일 크기가 큼

```bash
python pdf_converter.py document.pdf -f TIFF -d 400
```

### BMP
- 비트맵 형식
- 압축 없음
- 호환성 좋음
- 파일 크기가 매우 큼

```bash
python pdf_converter.py document.pdf -f BMP -d 200
```

### GIF
- 애니메이션 지원
- 색상 제한 (256색)
- 웹용 이미지
- 단일 페이지만 지원

```bash
python pdf_converter.py document.pdf -f GIF -d 150
```

## ⚙️ DPI 설정 가이드

### 저품질 (웹용)
```bash
python pdf_converter.py document.pdf -d 100
```
- 빠른 처리
- 작은 파일 크기
- 웹 표시용

### 중간 품질 (일반용)
```bash
python pdf_converter.py document.pdf -d 200
```
- 균형잡힌 품질
- 적당한 파일 크기
- 일반적인 용도

### 고품질 (인쇄용)
```bash
python pdf_converter.py document.pdf -d 300
```
- 높은 품질
- 큰 파일 크기
- 인쇄용

### 초고품질 (전문가용)
```bash
python pdf_converter.py document.pdf -d 600
```
- 최고 품질
- 매우 큰 파일 크기
- 전문가용

## 🔧 Python 코드에서 사용

### 기본 변환

```python
from pdf_converter import PDFConverter

# 변환기 초기화
converter = PDFConverter("output_directory")

# PDF를 이미지로 변환
output_files = converter.convert_pdf_to_images(
    "document.pdf",
    output_format="PNG",
    dpi=200
)

print(f"변환 완료: {len(output_files)}개 파일")
```

### 고급 옵션

```python
# 특정 페이지 범위 변환
output_files = converter.convert_pdf_to_images(
    "document.pdf",
    output_format="JPEG",
    dpi=300,
    first_page=1,
    last_page=5
)

# 단일 이미지로 변환
output_file = converter.convert_pdf_to_single_image(
    "document.pdf",
    output_format="PNG",
    dpi=400
)
```

### 배치 처리

```python
from batch_convert import batch_convert

# 디렉토리 내 모든 PDF 변환
success, errors, error_files = batch_convert(
    input_dir="/path/to/pdfs",
    output_dir="converted_images",
    output_format="PNG",
    dpi=200,
    recursive=True
)

print(f"성공: {success}, 실패: {errors}")
```

## 🌐 웹 인터페이스

### Streamlit 앱 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하여 사용하세요.

### 웹 인터페이스 특징
- 드래그 앤 드롭 파일 업로드
- 실시간 미리보기
- 직관적인 설정 조정
- 변환된 이미지 다운로드

## 📊 성능 최적화 팁

### 1. 메모리 사용량 줄이기
```bash
# DPI를 낮게 설정
python pdf_converter.py document.pdf -d 150

# 페이지 범위 제한
python pdf_converter.py document.pdf --first-page 1 --last-page 10
```

### 2. 처리 속도 향상
```bash
# JPEG 형식 사용 (압축 빠름)
python pdf_converter.py document.pdf -f JPEG

# 적절한 DPI 설정
python pdf_converter.py document.pdf -d 200
```

### 3. 배치 처리 최적화
```bash
# 재귀 검색 비활성화 (필요한 경우만)
python batch_convert.py /path/to/pdfs

# 상세 로그 비활성화
python batch_convert.py /path/to/pdfs
```

## 🐛 문제 해결

### 일반적인 오류

1. **poppler 오류**
   ```bash
   # macOS
   brew install poppler
   
   # Ubuntu/Debian
   sudo apt-get install poppler-utils
   ```

2. **메모리 부족**
   ```bash
   # DPI 낮추기
   python pdf_converter.py document.pdf -d 100
   
   # 페이지 범위 제한
   python pdf_converter.py document.pdf --first-page 1 --last-page 5
   ```

3. **권한 오류**
   ```bash
   # 출력 디렉토리 권한 확인
   chmod 755 output_directory
   ```

## 📝 로그 및 디버깅

### 로그 활성화

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 배치 처리 로그

```bash
# 상세한 로그 출력
python batch_convert.py /path/to/pdfs -v

# 로그 파일 확인
cat batch_convert.log
```

이 예제들을 참고하여 PDF 변환 작업을 효율적으로 수행하세요!
