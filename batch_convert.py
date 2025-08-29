#!/usr/bin/env python3
"""
PDF 배치 변환 스크립트
여러 PDF 파일을 한 번에 이미지로 변환합니다.
"""

import os
import sys
import argparse
from pathlib import Path
from pdf_converter import PDFConverter
import logging

def setup_logging(verbose=False):
    """로깅 설정"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('batch_convert.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def find_pdf_files(directory, recursive=False):
    """디렉토리에서 PDF 파일들을 찾습니다."""
    pdf_files = []
    dir_path = Path(directory)
    
    if recursive:
        pattern = "**/*.pdf"
    else:
        pattern = "*.pdf"
    
    for pdf_file in dir_path.glob(pattern):
        if pdf_file.is_file():
            pdf_files.append(pdf_file)
    
    return sorted(pdf_files)

def batch_convert(
    input_dir,
    output_dir="converted_images",
    output_format="PNG",
    dpi=200,
    recursive=False,
    first_page=None,
    last_page=None,
    single_image=False,
    verbose=False
):
    """여러 PDF 파일을 배치로 변환합니다."""
    
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    
    logger.info(f"배치 변환 시작: {input_dir}")
    logger.info(f"출력 디렉토리: {output_dir}")
    logger.info(f"출력 형식: {output_format}")
    logger.info(f"DPI: {dpi}")
    logger.info(f"재귀 검색: {recursive}")
    
    # PDF 파일 찾기
    pdf_files = find_pdf_files(input_dir, recursive)
    
    if not pdf_files:
        logger.warning(f"'{input_dir}'에서 PDF 파일을 찾을 수 없습니다.")
        return
    
    logger.info(f"발견된 PDF 파일 수: {len(pdf_files)}")
    
    # 변환기 초기화
    converter = PDFConverter(output_dir)
    
    # 변환 결과 통계
    success_count = 0
    error_count = 0
    error_files = []
    
    # 각 PDF 파일 변환
    for i, pdf_file in enumerate(pdf_files, 1):
        logger.info(f"[{i}/{len(pdf_files)}] 변환 중: {pdf_file.name}")
        
        try:
            if single_image:
                output_file = converter.convert_pdf_to_single_image(
                    str(pdf_file), output_format, dpi
                )
                logger.info(f"✅ {pdf_file.name} 변환 완료: {output_file}")
            else:
                output_files = converter.convert_pdf_to_images(
                    str(pdf_file), output_format, dpi, first_page, last_page
                )
                logger.info(f"✅ {pdf_file.name} 변환 완료: {len(output_files)}개 파일")
            
            success_count += 1
            
        except Exception as e:
            logger.error(f"❌ {pdf_file.name} 변환 실패: {e}")
            error_count += 1
            error_files.append((pdf_file.name, str(e)))
    
    # 결과 요약
    logger.info("=" * 50)
    logger.info("🎯 배치 변환 완료!")
    logger.info(f"✅ 성공: {success_count}개 파일")
    logger.info(f"❌ 실패: {error_count}개 파일")
    
    if error_files:
        logger.info("실패한 파일들:")
        for file_name, error_msg in error_files:
            logger.info(f"  - {file_name}: {error_msg}")
    
    return success_count, error_count, error_files

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="PDF 배치 변환 프로그램")
    
    parser.add_argument("input_dir", help="PDF 파일이 있는 입력 디렉토리")
    parser.add_argument("-o", "--output-dir", default="converted_images",
                       help="출력 디렉토리 (기본값: converted_images)")
    parser.add_argument("-f", "--format", default="PNG",
                       choices=["PNG", "JPEG", "TIFF", "BMP", "GIF"],
                       help="출력 이미지 형식 (기본값: PNG)")
    parser.add_argument("-d", "--dpi", type=int, default=200,
                       help="이미지 해상도 (기본값: 200)")
    parser.add_argument("-r", "--recursive", action="store_true",
                       help="하위 디렉토리까지 재귀적으로 검색")
    parser.add_argument("--first-page", type=int, help="시작 페이지 번호")
    parser.add_argument("--last-page", type=int, help="마지막 페이지 번호")
    parser.add_argument("--single-image", action="store_true",
                       help="모든 페이지를 하나의 이미지로 변환")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="상세한 로그 출력")
    
    args = parser.parse_args()
    
    # 입력 디렉토리 확인
    if not os.path.isdir(args.input_dir):
        print(f"❌ 오류: '{args.input_dir}'는 유효한 디렉토리가 아닙니다.")
        sys.exit(1)
    
    try:
        # 배치 변환 실행
        success, errors, error_files = batch_convert(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            output_format=args.format,
            dpi=args.dpi,
            recursive=args.recursive,
            first_page=args.first_page,
            last_page=args.last_page,
            single_image=args.single_image,
            verbose=args.verbose
        )
        
        if errors > 0:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 예상치 못한 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
