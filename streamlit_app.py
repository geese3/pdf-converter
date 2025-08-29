import streamlit as st
import os
from pathlib import Path
import tempfile
from pdf_converter import PDFConverter

# 페이지 설정
st.set_page_config(
    page_title="PDF to Image Converter",
    page_icon="🔄",
    layout="wide"
)

# 제목과 설명
st.title("🔄 PDF to Image Converter")
st.markdown("PDF 파일을 PNG, JPEG, TIFF 등의 이미지 형식으로 변환하는 프로그램입니다.")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 출력 형식 선택
    output_format = st.selectbox(
        "출력 이미지 형식",
        ["PNG", "JPEG", "TIFF", "BMP", "GIF"],
        index=0
    )
    
    # DPI 설정
    dpi = st.slider("이미지 해상도 (DPI)", 100, 600, 200, 50)
    
    # 출력 디렉토리 설정
    output_dir = st.text_input("출력 디렉토리", "converted_images")
    
    # 변환 옵션
    st.subheader("변환 옵션")
    convert_to_single = st.checkbox("모든 페이지를 하나의 이미지로 변환")
    
    if not convert_to_single:
        st.info("페이지별로 개별 이미지 생성")
    else:
        st.info("모든 페이지를 세로로 연결하여 하나의 긴 이미지 생성")
    
    # 페이지 범위 설정
    if not convert_to_single:
        st.subheader("페이지 범위")
        use_page_range = st.checkbox("특정 페이지 범위만 변환")
        
        if use_page_range:
            col1, col2 = st.columns(2)
            with col1:
                first_page = st.number_input("시작 페이지", min_value=1, value=1)
            with col2:
                last_page = st.number_input("마지막 페이지", min_value=1, value=1)

# 메인 컨텐츠
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📁 PDF 파일 업로드")
    
    uploaded_file = st.file_uploader(
        "PDF 파일을 선택하거나 드래그 앤 드롭하세요",
        type=['pdf'],
        help="PDF 파일만 업로드 가능합니다."
    )

with col2:
    st.subheader("📊 파일 정보")
    if uploaded_file is not None:
        file_details = {
            "파일명": uploaded_file.name,
            "파일 크기": f"{uploaded_file.size / 1024:.1f} KB",
            "파일 타입": uploaded_file.type
        }
        
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")
        
        # PDF 페이지 수 확인 (간단한 방법)
        try:
            import PyPDF2
            uploaded_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            page_count = len(pdf_reader.pages)
            st.write(f"**총 페이지 수:** {page_count}")
            
            # 페이지 범위 설정이 활성화된 경우 기본값 설정
            if 'use_page_range' in locals() and use_page_range:
                if 'last_page' in locals():
                    st.session_state.last_page = page_count
                    last_page = page_count
        except Exception as e:
            st.error(f"PDF 정보를 읽을 수 없습니다: {e}")

# 변환 실행
if uploaded_file is not None:
    st.subheader("🚀 변환 실행")
    
    if st.button("변환 시작", type="primary"):
        try:
            with st.spinner("PDF를 이미지로 변환 중..."):
                # 임시 파일로 PDF 저장
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_pdf_path = tmp_file.name
                
                try:
                    # PDF 변환기 초기화
                    converter = PDFConverter(output_dir)
                    
                    # 변환 실행
                    if convert_to_single:
                        output_file = converter.convert_pdf_to_single_image(
                            tmp_pdf_path, output_format, dpi
                        )
                        st.success(f"✅ 변환 완료!")
                        st.info(f"출력 파일: {output_file}")
                        
                        # 변환된 이미지 표시
                        st.image(output_file, caption="변환된 이미지", use_container_width=True)
                        
                    else:
                        # 페이지 범위 설정
                        first_page_arg = None
                        last_page_arg = None
                        
                        if 'use_page_range' in locals() and use_page_range:
                            first_page_arg = first_page
                            last_page_arg = last_page
                        
                        output_files = converter.convert_pdf_to_images(
                            tmp_pdf_path, output_format, dpi,
                            first_page_arg, last_page_arg
                        )
                        
                        st.success(f"✅ 변환 완료! {len(output_files)}개 파일이 생성되었습니다.")
                        
                        # 변환된 이미지들 표시
                        st.subheader("🖼️ 변환된 이미지들")
                        
                        # 이미지를 그리드 형태로 표시
                        cols = st.columns(min(3, len(output_files)))
                        for i, file_path in enumerate(output_files):
                            col_idx = i % 3
                            with cols[col_idx]:
                                st.image(file_path, caption=Path(file_path).name, use_container_width=True)
                        
                        # 다운로드 링크 제공
                        st.subheader("📥 다운로드")
                        for file_path in output_files:
                            file_name = Path(file_path).name
                            with open(file_path, 'rb') as f:
                                st.download_button(
                                    label=f"📄 {file_name} 다운로드",
                                    data=f.read(),
                                    file_name=file_name,
                                    mime="image/png" if output_format.lower() == "png" else "image/jpeg"
                                )
                
                finally:
                    # 임시 파일 정리
                    os.unlink(tmp_pdf_path)
                    
        except Exception as e:
            st.error(f"❌ 변환 중 오류가 발생했습니다: {str(e)}")
            st.exception(e)

# 사용법 안내
with st.expander("📖 사용법"):
    st.markdown("""
    ### 기본 사용법
    1. **PDF 파일 업로드**: 변환할 PDF 파일을 선택하거나 드래그 앤 드롭하세요
    2. **설정 조정**: 사이드바에서 출력 형식, 해상도 등을 설정하세요
    3. **변환 실행**: '변환 시작' 버튼을 클릭하세요
    
    ### 고급 옵션
    - **페이지별 변환**: 각 페이지를 개별 이미지로 변환
    - **단일 이미지 변환**: 모든 페이지를 하나의 긴 이미지로 연결
    - **페이지 범위**: 특정 페이지만 변환
    - **해상도 조정**: DPI 값을 조정하여 이미지 품질 설정
    
    ### 지원 형식
    - **입력**: PDF
    - **출력**: PNG, JPEG, TIFF, BMP, GIF
    
    ### 팁
    - 고품질 이미지가 필요한 경우 DPI를 높게 설정하세요
    - 파일 크기를 줄이고 싶다면 JPEG 형식을 사용하세요
    - 투명도가 필요한 경우 PNG 형식을 사용하세요
    """)

# 문제 해결
with st.expander("🔧 문제 해결"):
    st.markdown("""
    ### 자주 발생하는 문제들
    
    **1. 라이브러리 설치 오류**
    ```bash
    pip install -r requirements.txt
    ```
    
    **2. macOS에서 pdf2image 오류**
    ```bash
    brew install poppler
    ```
    
    **3. Windows에서 pdf2image 오류**
    - poppler-windows를 다운로드하여 PATH에 추가
    
    **4. 메모리 부족 오류**
    - DPI 값을 낮추거나
    - 페이지 범위를 제한하여 변환
    
    **5. 파일 권한 오류**
    - 출력 디렉토리에 쓰기 권한이 있는지 확인
    """)

# 푸터
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Python")
