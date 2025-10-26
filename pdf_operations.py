"""
PDF file operations and rendering
"""

import fitz  # PyMuPDF
from PyQt5.QtGui import QImage, QPixmap
from models import TextAnnotation, ImageAnnotation


class PDFOperations:
    """Mixin class for PDF operations"""

    def open_pdf_file(self, path):
        """Open a PDF file and return the document"""
        return fitz.open(path)

    def render_page(self, page, zoom_factor):
        """Render a PDF page at given zoom factor and return QPixmap"""
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        return QPixmap.fromImage(image)

    def save_pdf_with_annotations(self, doc, annotations):
        """
        Apply all annotations to the PDF document

        Args:
            doc: PyMuPDF document
            annotations: List of TextAnnotation and ImageAnnotation objects
        """
        for annotation in annotations:
            page = doc[annotation.page_num]
            zoom_at_creation = getattr(annotation, 'created_at_zoom', 1.0)

            if isinstance(annotation, TextAnnotation):
                # Convert screen coordinates to PDF coordinates
                # Divide by the zoom level at creation time and the base 2x high DPI matrix
                pdf_x = annotation.x / (2.0 * zoom_at_creation)
                pdf_y = annotation.y / (2.0 * zoom_at_creation)

                # Build font name with style modifiers
                fontname = annotation.font_family
                # Map common font families to PyMuPDF base fonts
                font_map = {
                    'Times New Roman': 'Times',
                    'Courier New': 'Courier',
                    'Arial': 'Helvetica'
                }
                fontname = font_map.get(fontname, fontname)

                # Add bold/italic modifiers
                if annotation.bold and annotation.italic:
                    fontname += '-BoldItalic'
                elif annotation.bold:
                    fontname += '-Bold'
                elif annotation.italic:
                    fontname += '-Italic'

                # Insert text with formatting
                try:
                    page.insert_text(
                        (pdf_x, pdf_y),
                        annotation.text,
                        fontsize=annotation.font_size,
                        fontname=fontname,
                        color=(0, 0, 0)
                    )

                    # Calculate text width for underline/strikethrough
                    # Use the actual font metrics from Qt (divided by 2 for PDF coordinates)
                    text_width = annotation.width / 2

                    # Add underline if needed
                    if annotation.underline:
                        underline_y = pdf_y + 1.5
                        page.draw_line((pdf_x, underline_y), (pdf_x + text_width - 5, underline_y),
                                      color=(0, 0, 0), width=0.5)

                    # Add strikethrough if needed
                    if annotation.strikethrough:
                        strikethrough_y = pdf_y - (annotation.font_size * 0.35)
                        page.draw_line((pdf_x, strikethrough_y), (pdf_x + text_width - 5, strikethrough_y),
                                      color=(0, 0, 0), width=0.5)
                except:
                    # Fallback to basic font if custom font fails
                    page.insert_text(
                        (pdf_x, pdf_y),
                        annotation.text,
                        fontsize=annotation.font_size,
                        color=(0, 0, 0)
                    )

            elif isinstance(annotation, ImageAnnotation):
                # Convert screen coordinates to PDF coordinates
                pdf_x = annotation.x / (2.0 * zoom_at_creation)
                pdf_y = annotation.y / (2.0 * zoom_at_creation)
                pdf_width = annotation.width / (2.0 * zoom_at_creation)
                pdf_height = annotation.height / (2.0 * zoom_at_creation)

                # Define the rectangle where the image will be placed
                rect = fitz.Rect(pdf_x, pdf_y, pdf_x + pdf_width, pdf_y + pdf_height)

                # Insert the image
                try:
                    page.insert_image(rect, filename=annotation.image_path)
                except Exception as e:
                    print(f"Failed to insert image: {e}")
