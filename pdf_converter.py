import os
import sys
from pathlib import Path
from typing import List, Optional
import logging

# PDF 변환을 위한 라이브러리들
try:
    from pdf2image import convert_from_path
    from PIL import Image
    import PyPDF2
except ImportError as e:
    print(f"필요한 라이브러리가 설치되지 않았습니다: {e}")
    print("pip install -r requirements.txt를 실행해주세요.")
    sys.exit(1)

class PDFConverter:
    """PDF를 이미지로 변환하는 클래스"""
    
    def __init__(self, output_dir: str = "converted_images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def convert_pdf_to_images(
        self, 
        pdf_path: str, 
        output_format: str = "PNG",
        dpi: int = 200,
        first_page: Optional[int] = None,
        last_page: Optional[int] = None
    ) -> List[str]:
        """
        PDF를 이미지로 변환합니다.
        
        Args:
            pdf_path: PDF 파일 경로
            output_format: 출력 이미지 형식 (PNG, JPEG, TIFF 등)
            dpi: 이미지 해상도
            first_page: 시작 페이지 (1부터 시작)
            last_page: 마지막 페이지
        
        Returns:
            생성된 이미지 파일 경로 리스트
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
            
            self.logger.info(f"PDF 변환 시작: {pdf_path.name}")
            
            # PDF 페이지 수 확인
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                self.logger.info(f"총 페이지 수: {total_pages}")
            
            # 페이지 범위 설정
            if first_page is None:
                first_page = 1
            if last_page is None:
                last_page = total_pages
            
            # 페이지 번호 조정 (0부터 시작하는 인덱스로 변환)
            start_idx = max(0, first_page - 1)
            end_idx = min(total_pages, last_page)
            
            # PDF를 이미지로 변환
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                first_page=start_idx + 1,
                last_page=end_idx
            )
            
            # 이미지 저장
            saved_files = []
            for i, image in enumerate(images):
                page_num = start_idx + i + 1
                filename = f"{pdf_path.stem}_page_{page_num:03d}.{output_format.lower()}"
                output_path = self.output_dir / filename
                
                # 이미지 형식에 따른 저장
                if output_format.upper() == "JPEG":
                    # JPEG는 RGB 모드로 변환 필요
                    if image.mode in ('RGBA', 'LA', 'P'):
                        image = image.convert('RGB')
                    image.save(output_path, 'JPEG', quality=95)
                else:
                    image.save(output_path, output_format.upper())
                
                saved_files.append(str(output_path))
                self.logger.info(f"페이지 {page_num} 저장 완료: {filename}")
            
            self.logger.info(f"변환 완료! {len(saved_files)}개 파일이 {self.output_dir}에 저장되었습니다.")
            return saved_files
            
        except Exception as e:
            self.logger.error(f"PDF 변환 중 오류 발생: {e}")
            raise
    
    def convert_pdf_to_single_image(
        self, 
        pdf_path: str, 
        output_format: str = "PNG",
        dpi: int = 200
    ) -> str:
        """
        PDF의 모든 페이지를 하나의 긴 이미지로 변환합니다.
        
        Args:
            pdf_path: PDF 파일 경로
            output_format: 출력 이미지 형식
            dpi: 이미지 해상도
        
        Returns:
            생성된 이미지 파일 경로
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
            
            self.logger.info(f"PDF를 단일 이미지로 변환 시작: {pdf_path.name}")
            
            # PDF를 이미지로 변환
            images = convert_from_path(pdf_path, dpi=dpi)
            
            if not images:
                raise ValueError("PDF에서 이미지를 추출할 수 없습니다.")
            
            # 이미지들을 세로로 연결
            total_width = max(img.width for img in images)
            total_height = sum(img.height for img in images)
            
            # 새 이미지 생성
            combined_image = Image.new('RGB', (total_width, total_height), 'white')
            
            y_offset = 0
            for i, image in enumerate(images):
                # 이미지가 total_width보다 작은 경우 중앙 정렬
                x_offset = (total_width - image.width) // 2
                combined_image.paste(image, (x_offset, y_offset))
                y_offset += image.height
                
                self.logger.info(f"페이지 {i+1} 처리 완료")
            
            # 파일 저장
            filename = f"{pdf_path.stem}_combined.{output_format.lower()}"
            output_path = self.output_dir / filename
            
            if output_format.upper() == "JPEG":
                combined_image.save(output_path, 'JPEG', quality=95)
            else:
                combined_image.save(output_path, output_format.upper())
            
            self.logger.info(f"단일 이미지 변환 완료: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"단일 이미지 변환 중 오류 발생: {e}")
            raise
    
    def get_supported_formats(self) -> List[str]:
        """지원되는 이미지 형식을 반환합니다."""
        return ["PNG", "JPEG", "TIFF", "BMP", "GIF"]
    
    def cleanup_output_dir(self):
        """출력 디렉토리의 모든 파일을 삭제합니다."""
        try:
            for file in self.output_dir.glob("*"):
                if file.is_file():
                    file.unlink()
            self.logger.info("출력 디렉토리 정리 완료")
        except Exception as e:
            self.logger.error(f"디렉토리 정리 중 오류 발생: {e}")


def main():
    """메인 함수 - 명령줄에서 실행할 때 사용"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PDF를 이미지로 변환하는 프로그램")
    parser.add_argument("pdf_path", help="변환할 PDF 파일 경로")
    parser.add_argument("-f", "--format", default="PNG", 
                       choices=["PNG", "JPEG", "TIFF", "BMP", "GIF"],
                       help="출력 이미지 형식 (기본값: PNG)")
    parser.add_argument("-d", "--dpi", type=int, default=200,
                       help="이미지 해상도 (기본값: 200)")
    parser.add_argument("-o", "--output-dir", default="converted_images",
                       help="출력 디렉토리 (기본값: converted_images)")
    parser.add_argument("--first-page", type=int, help="시작 페이지 번호")
    parser.add_argument("--last-page", type=int, help="마지막 페이지 번호")
    parser.add_argument("--single-image", action="store_true",
                       help="모든 페이지를 하나의 이미지로 변환")
    
    args = parser.parse_args()
    
    try:
        converter = PDFConverter(args.output_dir)
        
        if args.single_image:
            output_file = converter.convert_pdf_to_single_image(
                args.pdf_path, args.format, args.dpi
            )
            print(f"변환 완료: {output_file}")
        else:
            output_files = converter.convert_pdf_to_images(
                args.pdf_path, args.format, args.dpi,
                args.first_page, args.last_page
            )
            print(f"변환 완료: {len(output_files)}개 파일")
            for file in output_files:
                print(f"  - {file}")
                
    except Exception as e:
        print(f"오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
