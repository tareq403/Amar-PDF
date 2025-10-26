"""
PDF Editor - Main Application
A simple PDF viewer and editor application built with PyQt5 and PyMuPDF.
"""

import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QFileDialog,
                             QAction, QScrollArea, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QDialog)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt

from dialogs import TextFormatDialog
from models import TextAnnotation
from widgets import PDFViewLabel


class PDFEditor(QMainWindow):
    """Main PDF Editor window"""
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
        """Open a PDF file"""
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
        """Display a specific page of the PDF"""
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
        """Navigate to the previous page"""
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)
            self.update_buttons()

    def next_page(self):
        """Navigate to the next page"""
        if self.doc and self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.show_page(self.current_page)
            self.update_buttons()

    def update_buttons(self):
        """Update navigation button states"""
        if not self.doc:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < len(self.doc) - 1)

    def mousePressEvent(self, event):
        """Handle mouse press events for adding text annotations"""
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
