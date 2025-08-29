import streamlit as st
import os
from pathlib import Path
import tempfile
import io
from pdf_converter_web import PDFConverterWeb

st.set_page_config(
    page_title="PDF to Image Converter (Web)",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 PDF 이미지 변환기")
st.markdown("**설치 없이 바로 사용할 수 있는 PDF 변환기입니다!**")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 변환 설정")
    
    # 출력 형식 선택
    output_format = st.selectbox(
        "출력 형식",
        ["PNG", "JPEG", "JPG"],
        help="변환할 이미지 형식을 선택하세요"
    )
    
    # DPI 설정
    dpi = st.slider(
        "DPI (해상도)",
        min_value=72,
        max_value=600,
        value=200,
        step=24,
        help="높은 DPI = 더 선명한 이미지, 하지만 파일 크기가 커집니다"
    )
    
    # 변환 모드 선택
    conversion_mode = st.radio(
        "변환 모드",
        ["개별 페이지", "단일 이미지로 결합"],
        help="개별 페이지: 각 페이지를 별도 파일로 저장\n단일 이미지: 모든 페이지를 하나의 이미지로 결합"
    )
    
    # 페이지 범위 설정
    st.subheader("📄 페이지 범위")
    use_page_range = st.checkbox("특정 페이지 범위만 변환")
    
    if use_page_range:
        first_page = st.number_input("시작 페이지", min_value=1, value=1)
        last_page = st.number_input("끝 페이지", min_value=1, value=1)
    else:
        first_page = None
        last_page = None

# 메인 영역
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📁 PDF 파일 업로드")
    
    uploaded_file = st.file_uploader(
        "PDF 파일을 선택하세요",
        type=['pdf'],
        help="최대 200MB까지 업로드 가능합니다"
    )

# 세로 구분선 추가
st.markdown("---")

with col2:
    if uploaded_file is not None:
        st.subheader("📋 파일 정보")
        
        # 파일 정보 표시
        file_details = {
            "파일명": uploaded_file.name,
            "파일 크기": f"{uploaded_file.size / 1024 / 1024:.2f} MB",
            "파일 타입": uploaded_file.type
        }
        
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")
        
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # PDF 정보 가져오기
        converter = PDFConverterWeb()
        pdf_info = converter.get_pdf_info(tmp_file_path)
        
        st.write(f"**총 페이지 수:** {pdf_info['page_count']}페이지")
        if pdf_info['title']:
            st.write(f"**제목:** {pdf_info['title']}")
        if pdf_info['author']:
            st.write(f"**작성자:** {pdf_info['author']}")
        
        # 페이지 범위 업데이트
        if use_page_range and first_page and last_page:
            if last_page > pdf_info['page_count']:
                st.warning(f"⚠️ 끝 페이지가 총 페이지 수({pdf_info['page_count']})를 초과합니다. 자동으로 조정됩니다.")
                last_page = pdf_info['page_count']
        else:
            first_page = 1
            last_page = pdf_info['page_count']
    else:
        st.info("📁 PDF 파일을 업로드해주세요.")

# 변환 실행 섹션
if uploaded_file is not None:
    st.subheader("🚀 변환 실행")
    
    if st.button("🔄 변환 시작", type="primary", use_container_width=True):
        with st.spinner("PDF를 이미지로 변환하는 중..."):
            try:
                # 변환 실행
                if conversion_mode == "개별 페이지":
                    output_files = converter.convert_pdf_to_images(
                        tmp_file_path,
                        output_format=output_format,
                        dpi=dpi,
                        first_page=first_page,
                        last_page=last_page
                    )
                    
                    st.success(f"✅ 변환 완료! {len(output_files)}개의 이미지 파일이 생성되었습니다.")
                    
                    # 결과 표시
                    st.subheader("📸 변환된 이미지")
                    
                    # 이미지들을 가로로 나열 (안정적인 레이아웃)
                    num_images = len(output_files)
                    
                    # 이미지 개수에 따라 동적으로 컬럼 생성
                    if num_images <= 4:
                        # 4개 이하면 한 행에 모두 표시
                        cols = st.columns(num_images)
                        
                        for i, file_path in enumerate(output_files):
                            with open(file_path, "rb") as img_file:
                                img_data = img_file.read()
                            
                            with cols[i]:
                                # 이미지 표시
                                st.image(img_data, caption=f"페이지 {i+1}", width=200)
                                
                                # 다운로드 버튼 (이미지와 같은 너비)
                                filename = Path(file_path).name
                                st.download_button(
                                    label=f"📥 다운로드",
                                    data=img_data,
                                    file_name=filename,
                                    mime=f"image/{output_format.lower()}",
                                    use_container_width=True
                                )
                    else:
                        # 4개 초과시 여러 행으로 나누기
                        rows = (num_images + 3) // 4  # 올림 나눗셈
                        
                        for row in range(rows):
                            start_idx = row * 4
                            end_idx = min(start_idx + 4, num_images)
                            row_images = end_idx - start_idx
                            
                            # 현재 행의 컬럼 생성
                            cols = st.columns(4)
                            
                            for i in range(4):
                                if i < row_images:
                                    # 실제 이미지 인덱스
                                    img_idx = start_idx + i
                                    file_path = output_files[img_idx]
                                    
                                    with open(file_path, "rb") as img_file:
                                        img_data = img_file.read()
                                    
                                    with cols[i]:
                                        # 이미지 표시
                                        st.image(img_data, caption=f"페이지 {img_idx+1}", width=200)
                                        
                                        # 다운로드 버튼 (이미지와 같은 너비)
                                        filename = Path(file_path).name
                                        st.download_button(
                                            label=f"📥 다운로드",
                                            data=img_data,
                                            file_name=filename,
                                            mime=f"image/{output_format.lower()}",
                                            use_container_width=True
                                        )
                                else:
                                    # 빈 컬럼
                                    with cols[i]:
                                        st.empty()
                            
                            # 행 간 구분선 (마지막 행 제외)
                            if row < rows - 1:
                                st.markdown("---")
                
                else:  # 단일 이미지로 결합
                    output_file = converter.convert_pdf_to_single_image(
                        tmp_file_path,
                        output_format=output_format,
                        dpi=dpi,
                        first_page=first_page,
                        last_page=last_page
                    )
                    
                    if output_file:
                        st.success("✅ 변환 완료! 단일 이미지 파일이 생성되었습니다.")
                        
                        # 결과 표시
                        st.subheader("📸 변환된 이미지")
                        
                        with open(output_file, "rb") as img_file:
                            img_data = img_file.read()
                        
                        # 이미지와 다운로드 버튼을 나란히 배치
                        col_img, col_btn = st.columns([3, 1])
                        
                        with col_img:
                            # 이미지 크기 제한 (최대 너비 600px)
                            st.image(img_data, caption="결합된 이미지", width=600)
                        
                        with col_btn:
                            # 다운로드 버튼
                            filename = Path(output_file).name
                            st.download_button(
                                label=f"📥 다운로드",
                                data=img_data,
                                file_name=filename,
                                mime=f"image/{output_format.lower()}",
                                use_container_width=True
                            )
            
            except Exception as e:
                st.error(f"❌ 변환 중 오류가 발생했습니다: {str(e)}")
            
            finally:
                # 임시 파일 정리
                try:
                    os.unlink(tmp_file_path)
                    converter.cleanup_output_dir()
                except:
                    pass
else:
    st.info("📁 PDF 파일을 업로드해주세요.")

# 하단 정보
st.markdown("---")
st.markdown("""
### 💡 사용 팁
- **PNG**: 투명도 지원, 무손실 압축 (파일 크기 큼)
- **JPEG/JPG**: 손실 압축, 작은 파일 크기 (투명도 없음)
- **DPI**: 200-300이 일반적으로 적당합니다
- **단일 이미지**: 모든 페이지를 세로로 연결한 하나의 이미지
""")

# 푸터
st.markdown("---")
st.markdown("Made with using Streamlit and PyMuPDF")
