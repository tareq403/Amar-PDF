"""
PDF Editor - Main Application
A simple PDF viewer and editor application built with PyQt5 and PyMuPDF.
"""

import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QFileDialog,
                             QAction, QScrollArea, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QDialog, QSlider)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QRect

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
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        # Add stretch factor to allow scroll area to expand but not push buttons out
        main_layout.addWidget(self.scroll_area, 1)  # stretch factor 1

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

        # Create navigation buttons and zoom slider
        button_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous Page")
        self.next_button = QPushButton("Next Page")
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        button_layout.addWidget(self.prev_button)

        # Zoom slider
        button_layout.addWidget(QLabel("Zoom:"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(25)  # 25% zoom
        self.zoom_slider.setMaximum(400)  # 400% zoom
        self.zoom_slider.setValue(100)  # 100% default
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(25)
        self.zoom_slider.setMaximumWidth(200)
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        button_layout.addWidget(self.zoom_slider)

        self.zoom_label = QLabel("100%")
        self.zoom_label.setMinimumWidth(50)
        button_layout.addWidget(self.zoom_label)

        button_layout.addWidget(self.next_button)
        # Add button layout with stretch factor 0 to keep it fixed at bottom
        main_layout.addLayout(button_layout, 0)  # stretch factor 0 - fixed size

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
        self.zoom_level = 1.0  # 100% zoom (default is 2x for high DPI, zoom adjusts from there)

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
        self.resize_window_to_pdf()

    def show_page(self, page_num):
        """Display a specific page of the PDF"""
        page = self.doc[page_num]
        # Apply zoom: base 2x for high DPI, then multiply by zoom_level
        zoom_factor = 2.0 * self.zoom_level
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        self.label.adjustSize()

        # Update label's annotations to only show current page's annotations
        self.label.annotations = [a for a in self.draft_annotations if a.page_num == page_num]
        # Pass zoom level to label for rendering annotations
        self.label.zoom_level = self.zoom_level
        self.label.update()

    def on_zoom_changed(self, value):
        """Handle zoom slider value change"""
        self.zoom_level = value / 100.0  # Convert percentage to decimal
        self.zoom_label.setText(f"{value}%")

        if self.doc:
            self.show_page(self.current_page)
            self.resize_window_to_pdf()

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

    def resize_window_to_pdf(self):
        """Resize window to fit PDF dimensions within screen bounds"""
        if not self.doc:
            return

        # Get PDF dimensions (already scaled by 2x * zoom_level for display)
        pdf_width = self.label.pixmap().width()
        pdf_height = self.label.pixmap().height()

        # Get screen dimensions
        screen = QApplication.primaryScreen().availableGeometry()  # Use availableGeometry to exclude taskbar
        screen_width = screen.width()
        screen_height = screen.height()

        # Calculate non-PDF UI element heights
        menubar_height = self.menuBar().height() if self.menuBar().height() > 0 else 25

        # Force update button geometry to get accurate height
        self.prev_button.adjustSize()
        button_height = max(self.prev_button.height(), 40) + 10  # buttons + margins, minimum 40px

        decoration_height = 40  # window title bar (more conservative estimate)
        decoration_width = 20   # window borders

        # Maximum window height MUST fit buttons on screen
        # Reserve space for menubar, buttons, and decorations
        max_window_height = screen_height - 50  # 50px margin from screen edge

        # Height available for PDF scroll area
        max_pdf_display_height = max_window_height - menubar_height - button_height - decoration_height

        # Calculate desired window dimensions
        # Width: fit PDF width or screen width, whichever is smaller
        desired_width = min(pdf_width + decoration_width, screen_width - 50)

        # Height: CRITICAL - ensure buttons are always visible
        # If PDF is smaller than available space, size to PDF
        # If PDF is larger, size to max_window_height (PDF will scroll)
        if pdf_height <= max_pdf_display_height:
            # PDF fits in available space - size window to PDF
            desired_height = pdf_height + menubar_height + button_height + decoration_height
        else:
            # PDF is too large - size window to maximum that keeps buttons visible
            desired_height = max_window_height

        # Final safety check - never exceed screen bounds
        desired_height = min(desired_height, max_window_height)
        desired_width = min(desired_width, screen_width - 50)

        # Resize window
        self.resize(int(desired_width), int(desired_height))

        # Center window on screen
        window_rect = self.frameGeometry()
        center_point = screen.center()
        window_rect.moveCenter(center_point)
        self.move(window_rect.topLeft())

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
            if annotation.contains_point(label_pos.x(), label_pos.y(), self.zoom_level):
                return  # Let the label handle it

        # Add new annotation with formatting dialog
        dialog = TextFormatDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            values = dialog.get_values()
            if values['text']:
                self.add_draft_text(label_pos.x(), label_pos.y(), values)

    def add_draft_text(self, x, y, format_values):
        """Add text annotation in draft mode"""
        # Convert clicked position to normalized coordinates (accounting for current zoom)
        # The position needs to scale with zoom when displayed
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
        # Store the zoom level at which this annotation was created
        annotation.created_at_zoom = self.zoom_level
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
            # Convert screen coordinates to PDF coordinates
            # Divide by the zoom level at creation time and the base 2x high DPI matrix
            zoom_at_creation = getattr(annotation, 'created_at_zoom', 1.0)
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
