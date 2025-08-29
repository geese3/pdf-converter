import os
import sys
from pathlib import Path
from typing import List, Optional
import logging
import io

try:
    import PyPDF2
    from PIL import Image, ImageDraw, ImageFont
    import fitz  # PyMuPDF
except ImportError as e:
    print(f"필요한 라이브러리가 설치되지 않았습니다: {e}")
    print("pip install PyPDF2 Pillow PyMuPDF를 실행해주세요.")
    sys.exit(1)

class PDFConverterWeb:
    def __init__(self, output_dir: str = "converted_images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
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
        PDF를 이미지로 변환 (poppler 없이 PyMuPDF 사용)
        """
        try:
            # PDF 파일 열기
            pdf_document = fitz.open(pdf_path)
            
            # 페이지 범위 설정
            if first_page is None:
                first_page = 1
            if last_page is None:
                last_page = len(pdf_document)
            
            # 페이지 번호 조정 (0-based indexing)
            first_page = max(1, first_page) - 1
            last_page = min(len(pdf_document), last_page)
            
            output_files = []
            
            for page_num in range(first_page, last_page):
                # 페이지 가져오기
                page = pdf_document[page_num]
                
                # DPI에 따른 스케일 팩터 계산
                scale_factor = dpi / 72.0
                mat = fitz.Matrix(scale_factor, scale_factor)
                
                # 페이지를 이미지로 렌더링
                pix = page.get_pixmap(matrix=mat)
                
                # PIL Image로 변환
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # 파일명 생성
                base_name = Path(pdf_path).stem
                output_filename = f"{base_name}_page_{page_num + 1:03d}.{output_format.lower()}"
                output_path = self.output_dir / output_filename
                
                # 이미지 저장
                if output_format.upper() == "PNG":
                    img.save(output_path, "PNG")
                elif output_format.upper() == "JPEG":
                    # JPEG는 RGB 모드 필요
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    img.save(output_path, "JPEG", quality=95)
                elif output_format.upper() == "JPG":
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    img.save(output_path, "JPEG", quality=95)
                else:
                    img.save(output_path, output_format.upper())
                
                output_files.append(str(output_path))
                self.logger.info(f"페이지 {page_num + 1} 변환 완료: {output_filename}")
            
            pdf_document.close()
            return output_files
            
        except Exception as e:
            self.logger.error(f"PDF 변환 중 오류 발생: {e}")
            raise

    def convert_pdf_to_single_image(
        self,
        pdf_path: str,
        output_format: str = "PNG",
        dpi: int = 200,
        first_page: Optional[int] = None,
        last_page: Optional[int] = None
    ) -> str:
        """
        PDF의 여러 페이지를 하나의 이미지로 결합
        """
        try:
            # PDF 파일 열기
            pdf_document = fitz.open(pdf_path)
            
            # 페이지 범위 설정
            if first_page is None:
                first_page = 1
            if last_page is None:
                last_page = len(pdf_document)
            
            # 페이지 번호 조정
            first_page = max(1, first_page) - 1
            last_page = min(len(pdf_document), last_page)
            
            # 모든 페이지를 이미지로 변환
            page_images = []
            max_width = 0
            total_height = 0
            
            for page_num in range(first_page, last_page):
                page = pdf_document[page_num]
                scale_factor = dpi / 72.0
                mat = fitz.Matrix(scale_factor, scale_factor)
                pix = page.get_pixmap(matrix=mat)
                
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                page_images.append(img)
                max_width = max(max_width, img.width)
                total_height += img.height
            
            # 결합된 이미지 생성
            if page_images:
                combined_image = Image.new('RGB', (max_width, total_height), 'white')
                y_offset = 0
                
                for img in page_images:
                    # 이미지를 중앙에 배치
                    x_offset = (max_width - img.width) // 2
                    combined_image.paste(img, (x_offset, y_offset))
                    y_offset += img.height
                
                # 파일명 생성
                base_name = Path(pdf_path).stem
                output_filename = f"{base_name}_combined.{output_format.lower()}"
                output_path = self.output_dir / output_filename
                
                # 이미지 저장
                if output_format.upper() == "PNG":
                    combined_image.save(output_path, "PNG")
                elif output_format.upper() in ["JPEG", "JPG"]:
                    combined_image.save(output_path, "JPEG", quality=95)
                else:
                    combined_image.save(output_path, output_format.upper())
                
                pdf_document.close()
                return str(output_path)
            
            pdf_document.close()
            return ""
            
        except Exception as e:
            self.logger.error(f"PDF 단일 이미지 변환 중 오류 발생: {e}")
            raise

    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        PDF 파일 정보 가져오기
        """
        try:
            pdf_document = fitz.open(pdf_path)
            info = {
                'page_count': len(pdf_document),
                'title': pdf_document.metadata.get('title', ''),
                'author': pdf_document.metadata.get('author', ''),
                'subject': pdf_document.metadata.get('subject', ''),
                'creator': pdf_document.metadata.get('creator', '')
            }
            pdf_document.close()
            return info
        except Exception as e:
            self.logger.error(f"PDF 정보 가져오기 중 오류 발생: {e}")
            return {'page_count': 0, 'title': '', 'author': '', 'subject': '', 'creator': ''}

    def cleanup_output_dir(self):
        """
        출력 디렉토리 정리
        """
        try:
            for file in self.output_dir.glob("*"):
                if file.is_file():
                    file.unlink()
            self.logger.info("출력 디렉토리 정리 완료")
        except Exception as e:
            self.logger.error(f"디렉토리 정리 중 오류 발생: {e}")
