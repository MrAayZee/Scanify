"""
PDF processing utilities for rendering and conversion.
"""
import os
from pathlib import Path
from typing import List, Callable, Optional
import fitz  # PyMuPDF
from PIL import Image
import io

from config import EffectConfig
from effects import apply_scan_effects


class PDFProcessor:
    """Handles PDF rendering and conversion with scan effects."""

    def __init__(self):
        self.pdf_files: List[str] = []

    def add_pdf(self, filepath: str) -> bool:
        """Add a PDF to the processing queue."""
        if os.path.exists(filepath) and filepath.lower().endswith('.pdf'):
            if filepath not in self.pdf_files:
                self.pdf_files.append(filepath)
                return True
        return False

    def remove_pdf(self, filepath: str):
        """Remove a PDF from the queue."""
        if filepath in self.pdf_files:
            self.pdf_files.remove(filepath)

    def clear_queue(self):
        """Clear all PDFs from queue."""
        self.pdf_files.clear()

    def get_queue(self) -> List[str]:
        """Get list of queued PDFs."""
        return self.pdf_files.copy()

    def render_page(self, pdf_path: str, page_num: int, config: EffectConfig) -> Optional[Image.Image]:
        """
        Render a single page from PDF with effects applied.

        Args:
            pdf_path: Path to PDF file
            page_num: Page number (0-indexed)
            config: Effect configuration

        Returns:
            PIL Image or None if error
        """
        try:
            doc = fitz.open(pdf_path)
            if page_num >= len(doc):
                doc.close()
                return None

            page = doc[page_num]

            # Render at specified DPI
            zoom = config.dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            # Convert to PIL Image
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))

            doc.close()

            # Apply scan effects
            processed_image = apply_scan_effects(image, config)

            return processed_image

        except Exception as e:
            print(f"Error rendering page: {e}")
            return None

    def convert_pdf(
        self,
        pdf_path: str,
        output_dir: str,
        config: EffectConfig,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> bool:
        """
        Convert entire PDF with scan effects.

        Args:
            pdf_path: Input PDF path
            output_dir: Output directory
            config: Effect configuration
            progress_callback: Optional callback(current_page, total_pages, message)

        Returns:
            True if successful
        """
        try:
            # Open input PDF
            doc = fitz.open(pdf_path)
            total_pages = len(doc)

            if total_pages == 0:
                doc.close()
                return False

            # Generate output filename
            input_name = Path(pdf_path).stem
            output_path = self._get_unique_output_path(output_dir, input_name)

            # Create output PDF
            output_doc = fitz.open()

            # Process each page
            for page_num in range(total_pages):
                if progress_callback:
                    progress_callback(
                        page_num + 1,
                        total_pages,
                        f"Processing page {page_num + 1}/{total_pages}..."
                    )

                page = doc[page_num]

                # Render page
                zoom = config.dpi / 72.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                # Convert to PIL Image
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))

                # Apply scan effects
                processed_image = apply_scan_effects(image, config)

                # Convert back to bytes
                img_byte_arr = io.BytesIO()
                processed_image.save(
                    img_byte_arr,
                    format='JPEG',
                    quality=config.jpg_quality,
                    optimize=True
                )
                img_byte_arr.seek(0)

                # Create new page and insert image
                img_doc = fitz.open("jpeg", img_byte_arr.read())
                rect = img_doc[0].rect
                pdf_page = output_doc.new_page(width=rect.width, height=rect.height)
                pdf_page.insert_image(rect, stream=img_byte_arr.getvalue())
                img_doc.close()

            # Set metadata
            if config.blank_metadata:
                output_doc.set_metadata({})
            else:
                # Copy original metadata
                output_doc.set_metadata(doc.metadata)

            # Save output
            output_doc.save(output_path, garbage=4, deflate=True)
            output_doc.close()
            doc.close()

            if progress_callback:
                progress_callback(
                    total_pages,
                    total_pages,
                    f"Completed: {os.path.basename(output_path)}"
                )

            return True

        except Exception as e:
            print(f"Error converting PDF: {e}")
            if progress_callback:
                progress_callback(0, 0, f"Error: {str(e)}")
            return False

    def _get_unique_output_path(self, output_dir: str, base_name: str) -> str:
        """Generate unique output filename."""
        output_name = f"{base_name}_scanned.pdf"
        output_path = os.path.join(output_dir, output_name)

        # If file exists, add number
        counter = 2
        while os.path.exists(output_path):
            output_name = f"{base_name}_scanned{counter}.pdf"
            output_path = os.path.join(output_dir, output_name)
            counter += 1

        return output_path

    def get_page_count(self, pdf_path: str) -> int:
        """Get number of pages in PDF."""
        try:
            doc = fitz.open(pdf_path)
            count = len(doc)
            doc.close()
            return count
        except:
            return 0
