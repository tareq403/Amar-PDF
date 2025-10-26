import fitz  # PyMuPDF
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QFileDialog,
                             QAction, QScrollArea, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QDialog,
                             QLineEdit, QFontComboBox, QSpinBox, QCheckBox,
                             QDialogButtonBox, QFormLayout, QGroupBox)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QRect, QPoint
import sys


class TextFormatDialog(QDialog):
    """Dialog for text input with font formatting options"""
    def __init__(self, parent=None, initial_text="", initial_font="Arial", initial_size=12,
                 initial_bold=False, initial_italic=False, initial_underline=False, initial_strikethrough=False):
        super().__init__(parent)
        self.setWindowTitle("Text Format")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # Text input
        form_layout = QFormLayout()
        self.text_edit = QLineEdit(initial_text)
        form_layout.addRow("Text:", self.text_edit)

        # Font selection
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont(initial_font))
        form_layout.addRow("Font:", self.font_combo)

        # Font size
        self.size_spin = QSpinBox()
        self.size_spin.setMinimum(6)
        self.size_spin.setMaximum(72)
        self.size_spin.setValue(initial_size)
        form_layout.addRow("Size:", self.size_spin)

        layout.addLayout(form_layout)

        # Text decorations
        decoration_group = QGroupBox("Text Decorations")
        decoration_layout = QVBoxLayout()

        self.bold_check = QCheckBox("Bold")
        self.bold_check.setChecked(initial_bold)
        decoration_layout.addWidget(self.bold_check)

        self.italic_check = QCheckBox("Italic")
        self.italic_check.setChecked(initial_italic)
        decoration_layout.addWidget(self.italic_check)

        self.underline_check = QCheckBox("Underline")
        self.underline_check.setChecked(initial_underline)
        decoration_layout.addWidget(self.underline_check)

        self.strikethrough_check = QCheckBox("Strikethrough")
        self.strikethrough_check.setChecked(initial_strikethrough)
        decoration_layout.addWidget(self.strikethrough_check)

        decoration_group.setLayout(decoration_layout)
        layout.addWidget(decoration_group)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_values(self):
        """Return the text and formatting options"""
        return {
            'text': self.text_edit.text(),
            'font_family': self.font_combo.currentFont().family(),
            'font_size': self.size_spin.value(),
            'bold': self.bold_check.isChecked(),
            'italic': self.italic_check.isChecked(),
            'underline': self.underline_check.isChecked(),
            'strikethrough': self.strikethrough_check.isChecked()
        }


class TextAnnotation:
    """Represents a text annotation in draft mode"""
    def __init__(self, x, y, text, page_num, font_family="Arial", font_size=12,
                 bold=False, italic=False, underline=False, strikethrough=False):
        self.x = x
        self.y = y
        self.text = text
        self.page_num = page_num
        self.font_family = font_family
        self.font_size = font_size  # This is the actual PDF font size
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough
        self.update_bounds()

    def update_bounds(self):
        """Calculate bounding box for the text"""
        font = self.get_qfont()
        metrics = QFontMetrics(font)
        self.width = metrics.horizontalAdvance(self.text) + 10
        self.height = metrics.height() + 6

    def get_qfont(self):
        """Get QFont object with all formatting applied for 2x scaled display"""
        # Font size needs to be 2x for the 2x scaled PDF display
        display_font_size = self.font_size * 2
        font = QFont(self.font_family, display_font_size)
        font.setBold(self.bold)
        font.setItalic(self.italic)
        font.setUnderline(self.underline)
        font.setStrikeOut(self.strikethrough)
        return font

    def get_rect(self):
        """Get the bounding rectangle"""
        return QRect(int(self.x), int(self.y - self.height + 4), int(self.width), int(self.height))

    def contains_point(self, x, y):
        """Check if point is inside the annotation"""
        return self.get_rect().contains(x, y)


class PDFViewLabel(QLabel):
    """Custom label that can paint draft text annotations"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.annotations = []
        self.dragging_annotation = None
        self.drag_offset = QPoint(0, 0)

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.annotations:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw each draft annotation
        for annotation in self.annotations:
            # Draw dashed border
            pen = QPen(Qt.blue, 2, Qt.DashLine)
            painter.setPen(pen)
            rect = annotation.get_rect()
            painter.drawRect(rect)

            # Draw text with formatting
            font = annotation.get_qfont()
            painter.setFont(font)
            pen = QPen(Qt.black)
            painter.setPen(pen)
            painter.drawText(rect.adjusted(5, 0, -5, 0), Qt.AlignLeft | Qt.AlignVCenter, annotation.text)

        painter.end()

    def mousePressEvent(self, event):
        # Check if clicking on existing annotation
        for annotation in self.annotations:
            if annotation.contains_point(event.x(), event.y()):
                self.dragging_annotation = annotation
                self.drag_offset = QPoint(event.x() - int(annotation.x), event.y() - int(annotation.y))
                event.accept()
                return

        # Pass to parent if not clicking on annotation
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging_annotation:
            self.dragging_annotation.x = event.x() - self.drag_offset.x()
            self.dragging_annotation.y = event.y() - self.drag_offset.y()
            self.update()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.dragging_annotation:
            self.dragging_annotation = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        # Check if double-clicking on existing annotation to edit
        for annotation in self.annotations:
            if annotation.contains_point(event.x(), event.y()):
                dialog = TextFormatDialog(
                    self,
                    initial_text=annotation.text,
                    initial_font=annotation.font_family,
                    initial_size=annotation.font_size,
                    initial_bold=annotation.bold,
                    initial_italic=annotation.italic,
                    initial_underline=annotation.underline,
                    initial_strikethrough=annotation.strikethrough
                )
                if dialog.exec_() == QDialog.Accepted:
                    values = dialog.get_values()
                    if values['text']:
                        annotation.text = values['text']
                        annotation.font_family = values['font_family']
                        annotation.font_size = values['font_size']
                        annotation.bold = values['bold']
                        annotation.italic = values['italic']
                        annotation.underline = values['underline']
                        annotation.strikethrough = values['strikethrough']
                        annotation.update_bounds()
                        self.update()
                event.accept()
                return

        super().mouseDoubleClickEvent(event)


class PDFEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget with layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        # Create welcome message label
        self.welcome_label = QLabel("Open a PDF file to edit")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(18)
        self.welcome_label.setFont(font)
        self.welcome_label.setStyleSheet("color: gray; cursor: pointer;")
        self.welcome_label.mousePressEvent = lambda event: self.open_pdf()

        # Create PDF view label
        self.label = PDFViewLabel()
        self.label.setAlignment(Qt.AlignCenter)

        # Start with welcome label in scroll area
        self.scroll_area.setWidget(self.welcome_label)

        # Create navigation buttons
        button_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous Page")
        self.next_button = QPushButton("Next Page")
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        main_layout.addLayout(button_layout)

        self.setCentralWidget(central_widget)

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        open_action = QAction("Open PDF", self)
        open_action.triggered.connect(self.open_pdf)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_pdf)
        file_menu.addAction(save_action)

        self.doc = None
        self.current_page = 0
        self.draft_annotations = []  # All draft annotations across all pages

    def open_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if not path:
            return
        self.doc = fitz.open(path)
        self.current_page = 0
        self.draft_annotations = []  # Clear draft annotations when opening new file

        # Switch from welcome message to PDF label
        # Important: Save old widget reference to prevent Qt from deleting it
        old_widget = self.scroll_area.takeWidget()
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(False)

        self.show_page(self.current_page)
        self.update_buttons()

    def show_page(self, page_num):
        page = self.doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # High DPI render
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        self.label.adjustSize()

        # Update label's annotations to only show current page's annotations
        self.label.annotations = [a for a in self.draft_annotations if a.page_num == page_num]
        self.label.update()

    def prev_page(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)
            self.update_buttons()

    def next_page(self):
        if self.doc and self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.show_page(self.current_page)
            self.update_buttons()

    def update_buttons(self):
        if not self.doc:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < len(self.doc) - 1)


    def mousePressEvent(self, event):
        if not self.doc:
            # If no PDF is loaded, trigger file open
            self.open_pdf()
            return

        # Get position relative to the label widget
        label_pos = self.label.mapFromGlobal(event.globalPos())

        # Check if clicking inside the label bounds
        if not self.label.rect().contains(label_pos):
            return

        # Check if clicking on an existing annotation (handled by label's mouse events)
        for annotation in self.label.annotations:
            if annotation.contains_point(label_pos.x(), label_pos.y()):
                return  # Let the label handle it

        # Add new annotation with formatting dialog
        dialog = TextFormatDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            values = dialog.get_values()
            if values['text']:
                self.add_draft_text(label_pos.x(), label_pos.y(), values)

    def add_draft_text(self, x, y, format_values):
        """Add text annotation in draft mode"""
        annotation = TextAnnotation(
            x, y,
            format_values['text'],
            self.current_page,
            font_family=format_values['font_family'],
            font_size=format_values['font_size'],
            bold=format_values['bold'],
            italic=format_values['italic'],
            underline=format_values['underline'],
            strikethrough=format_values['strikethrough']
        )
        self.draft_annotations.append(annotation)
        self.label.annotations.append(annotation)
        self.label.update()

    def save_pdf(self):
        """Save all draft annotations to the PDF file"""
        if not self.doc:
            return

        if not self.draft_annotations:
            return

        # Ask for save location
        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "edited.pdf", "PDF Files (*.pdf)")
        if not path:
            return

        # Add all draft annotations to the PDF
        for annotation in self.draft_annotations:
            page = self.doc[annotation.page_num]
            # Convert screen coordinates to PDF coordinates (divide by 2 for the 2x matrix)
            pdf_x = annotation.x / 2
            pdf_y = annotation.y / 2

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
                    page.draw_line((pdf_x, underline_y), (pdf_x + text_width - 5, underline_y), color=(0, 0, 0), width=0.5)

                # Add strikethrough if needed
                if annotation.strikethrough:
                    strikethrough_y = pdf_y - (annotation.font_size * 0.35)
                    page.draw_line((pdf_x, strikethrough_y), (pdf_x + text_width - 5, strikethrough_y), color=(0, 0, 0), width=0.5)
            except:
                # Fallback to basic font if custom font fails
                page.insert_text(
                    (pdf_x, pdf_y),
                    annotation.text,
                    fontsize=annotation.font_size,
                    color=(0, 0, 0)
                )

        # Save the document
        self.doc.save(path)

        # Clear draft annotations after saving
        self.draft_annotations = []
        self.label.annotations = []

        # Reload the saved document
        self.doc = fitz.open(path)
        self.show_page(self.current_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFEditor()
    window.show()
    sys.exit(app.exec_())
