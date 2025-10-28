"""
PDF file operations and rendering
"""

import fitz  # PyMuPDF
import tempfile
from PyQt5.QtGui import QImage, QPixmap
from core.constants import BASE_SCALE
from models import TextAnnotation, ImageAnnotation, DoodleAnnotation


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
                from core.constants import TEXT_ANNOTATION_Y_OFFSET

                # Convert screen coordinates to PDF coordinates
                pdf_x = annotation.x / (BASE_SCALE * zoom_at_creation)
                pdf_y = annotation.y / (BASE_SCALE * zoom_at_creation)

                # X adjustment: In preview, text has 5px left padding inside the rect
                # Convert to PDF space (5px at BASE_SCALE display)
                x_padding_pdf = 5.0 / BASE_SCALE
                pdf_x = pdf_x + x_padding_pdf

                # Y adjustment: annotation.height is calculated at zoom=1.0 with BASE_SCALE font
                # So it's in screen pixels at BASE_SCALE * 1.0
                # Convert height to PDF space
                height_pdf = annotation.height / BASE_SCALE

                # In preview: rect_top = y - height + TEXT_ANNOTATION_Y_OFFSET (in original coords)
                rect_top_original = pdf_y - height_pdf + (TEXT_ANNOTATION_Y_OFFSET / BASE_SCALE)

                # For PDF baseline positioning:
                # Qt's AlignVCenter centers the text visually in the rect
                # PDF's insert_text places text at baseline
                # The baseline should be lower than center - around 65% down from top
                # This accounts for the fact that most glyphs sit above the baseline
                pdf_y = rect_top_original + (height_pdf * 0.65)

                # Build font name with style modifiers
                fontname = annotation.font_family
                # Map common font families to PyMuPDF base fonts
                font_map = {
                    'Times New Roman': 'Times',
                    'Courier New': 'Courier',
                    'Arial': 'Helvetica'
                }
                base_fontname = font_map.get(fontname, fontname)

                # Convert RGB color from 0-255 range to 0-1 range for PyMuPDF
                pdf_color = tuple(c / 255.0 for c in annotation.color)

                # Try to insert text with formatting
                text_inserted = False

                # Attempt 1: Try with bold/italic modifiers
                if annotation.bold or annotation.italic:
                    styled_fontname = base_fontname
                    if annotation.bold and annotation.italic:
                        styled_fontname += '-BoldItalic'
                    elif annotation.bold:
                        styled_fontname += '-Bold'
                    elif annotation.italic:
                        styled_fontname += '-Italic'

                    try:
                        page.insert_text(
                            (pdf_x, pdf_y),
                            annotation.text,
                            fontsize=annotation.font_size,
                            fontname=styled_fontname,
                            color=pdf_color
                        )
                        text_inserted = True
                    except Exception as e:
                        # Font with modifiers not available, will try base font
                        pass

                # Attempt 2: Try base font without modifiers
                if not text_inserted:
                    try:
                        page.insert_text(
                            (pdf_x, pdf_y),
                            annotation.text,
                            fontsize=annotation.font_size,
                            fontname=base_fontname,
                            color=pdf_color
                        )
                        text_inserted = True
                    except Exception as e:
                        # Base font not available, will try default
                        pass

                # Attempt 3: Fallback to Helvetica (always available)
                if not text_inserted:
                    try:
                        page.insert_text(
                            (pdf_x, pdf_y),
                            annotation.text,
                            fontsize=annotation.font_size,
                            fontname='Helvetica',
                            color=pdf_color
                        )
                        text_inserted = True
                    except Exception as e:
                        print(f"Failed to insert text annotation: {e}")

                # Add underline and strikethrough (always drawn, regardless of font)
                if text_inserted:
                    # Calculate text width for underline/strikethrough
                    # Use the actual font metrics from Qt (divided by base scale for PDF coordinates)
                    text_width = annotation.width / BASE_SCALE

                    # Add underline if needed
                    if annotation.underline:
                        underline_y = pdf_y + 1.5
                        try:
                            page.draw_line(
                                (pdf_x, underline_y),
                                (pdf_x + text_width - 5, underline_y),
                                color=pdf_color,
                                width=0.5
                            )
                        except Exception as e:
                            print(f"Failed to add underline: {e}")

                    # Add strikethrough if needed
                    if annotation.strikethrough:
                        strikethrough_y = pdf_y - (annotation.font_size * 0.35)
                        try:
                            page.draw_line(
                                (pdf_x, strikethrough_y),
                                (pdf_x + text_width - 5, strikethrough_y),
                                color=pdf_color,
                                width=0.5
                            )
                        except Exception as e:
                            print(f"Failed to add strikethrough: {e}")

            elif isinstance(annotation, ImageAnnotation):
                # Convert screen coordinates to PDF coordinates
                pdf_x = annotation.x / (BASE_SCALE * zoom_at_creation)
                pdf_y = annotation.y / (BASE_SCALE * zoom_at_creation)
                pdf_width = annotation.width / (BASE_SCALE * zoom_at_creation)
                pdf_height = annotation.height / (BASE_SCALE * zoom_at_creation)

                # Define the rectangle where the image will be placed
                rect = fitz.Rect(pdf_x, pdf_y, pdf_x + pdf_width, pdf_y + pdf_height)

                # Insert the image
                try:
                    page.insert_image(rect, filename=annotation.image_path)
                except Exception as e:
                    print(f"Failed to insert image: {e}")

            elif isinstance(annotation, DoodleAnnotation):
                # Convert screen coordinates to PDF coordinates
                pdf_x = annotation.x / (BASE_SCALE * zoom_at_creation)
                pdf_y = annotation.y / (BASE_SCALE * zoom_at_creation)
                pdf_width = annotation.width / (BASE_SCALE * zoom_at_creation)
                pdf_height = annotation.height / (BASE_SCALE * zoom_at_creation)

                # Define the rectangle where the doodle will be placed
                rect = fitz.Rect(pdf_x, pdf_y, pdf_x + pdf_width, pdf_y + pdf_height)

                # Save the doodle pixmap to a temporary file
                try:
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                        temp_path = tmp_file.name
                        annotation.pixmap.save(temp_path, 'PNG')

                    # Insert the doodle image
                    page.insert_image(rect, filename=temp_path)

                    # Clean up temp file
                    import os
                    os.unlink(temp_path)
                except Exception as e:
                    print(f"Failed to insert doodle: {e}")
