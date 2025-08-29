#!/usr/bin/env python3
"""
PDF 변환기 테스트 스크립트
"""

import os
import tempfile
from pathlib import Path
from pdf_converter import PDFConverter

def test_pdf_converter():
    """PDF 변환기 기능을 테스트합니다."""
    
    print("🧪 PDF 변환기 테스트 시작")
    print("=" * 50)
    
    # 테스트용 임시 디렉토리 생성
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 임시 디렉토리 생성: {temp_dir}")
        
        # 변환기 초기화
        converter = PDFConverter(temp_dir)
        
        # 지원되는 형식 확인
        supported_formats = converter.get_supported_formats()
        print(f"✅ 지원되는 이미지 형식: {', '.join(supported_formats)}")
        
        # 테스트용 간단한 PDF 생성 (실제로는 존재하지 않는 파일)
        test_pdf_path = os.path.join(temp_dir, "test.pdf")
        
        # PDF 파일이 존재하지 않으므로 오류 처리 테스트
        try:
            converter.convert_pdf_to_images(test_pdf_path)
        except FileNotFoundError as e:
            print(f"✅ 파일 없음 오류 처리 테스트 통과: {e}")
        
        # 출력 디렉토리 정리 테스트
        try:
            converter.cleanup_output_dir()
            print("✅ 출력 디렉토리 정리 테스트 통과")
        except Exception as e:
            print(f"⚠️ 출력 디렉토리 정리 테스트 실패: {e}")
        
        print("\n" + "=" * 50)
        print("🎯 테스트 완료!")
        print("\n📝 실제 PDF 파일로 테스트하려면:")
        print("1. PDF 파일을 준비하세요")
        print("2. python pdf_converter.py your_file.pdf 명령을 실행하세요")
        print("3. 또는 streamlit run app.py로 웹 인터페이스를 사용하세요")

def test_with_sample_pdf():
    """샘플 PDF가 있는 경우 실제 변환을 테스트합니다."""
    
    # 현재 디렉토리에서 PDF 파일 찾기
    current_dir = Path(".")
    pdf_files = list(current_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("📄 테스트할 PDF 파일이 없습니다.")
        print("PDF 파일을 현재 디렉토리에 넣고 다시 실행하세요.")
        return
    
    print(f"📄 발견된 PDF 파일: {pdf_files[0].name}")
    
    # 첫 번째 PDF 파일로 테스트
    test_pdf = pdf_files[0]
    
    try:
        # 변환기 초기화
        converter = PDFConverter("test_output")
        
        print(f"🔄 {test_pdf.name} 변환 테스트 시작...")
        
        # PNG 형식으로 변환 (첫 페이지만)
        output_files = converter.convert_pdf_to_images(
            str(test_pdf),
            output_format="PNG",
            dpi=150,
            first_page=1,
            last_page=1
        )
        
        print(f"✅ 변환 완료! {len(output_files)}개 파일 생성")
        for file in output_files:
            print(f"  - {file}")
        
        # 출력 디렉토리 정리
        converter.cleanup_output_dir()
        print("🧹 테스트 출력 파일 정리 완료")
        
    except Exception as e:
        print(f"❌ 변환 테스트 실패: {e}")
        print("📋 requirements.txt의 패키지들이 설치되어 있는지 확인하세요.")

if __name__ == "__main__":
    print("🚀 PDF to Image Converter 테스트")
    print()
    
    # 기본 기능 테스트
    test_pdf_converter()
    
    print()
    
    # 실제 PDF 파일이 있는 경우 변환 테스트
    test_with_sample_pdf()
