"""
PDF Editor - Main Application
A simple PDF viewer and editor application built with PyQt5 and PyMuPDF.
"""

import sys
from enum import Enum
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QFileDialog,
                             QAction, QScrollArea, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QDialog, QSlider)
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt

from dialogs import TextFormatDialog
from models import TextAnnotation, ImageAnnotation
from widgets import PDFViewLabel
from pdf_operations import PDFOperations
from window_manager import WindowManager


class EditMode(Enum):
    """Editing modes for the PDF editor"""
    TEXT = "text"
    IMAGE = "image"
    DOODLE = "doodle"


class PDFEditor(QMainWindow, PDFOperations, WindowManager):
    """Main PDF Editor window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor")
        self.setGeometry(100, 100, 800, 600)

        # Initialize state
        self.doc = None
        self.current_page = 0
        self.draft_annotations = []
        self.zoom_level = 1.0
        self.current_mode = EditMode.TEXT  # Default mode

        # Setup UI
        self._setup_ui()
        self._setup_menubar()
        self.toolbar = self._setup_toolbar()

    def _setup_ui(self):
        """Setup the user interface"""
        # Create central widget with layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
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
        self.label.current_mode = self.current_mode  # Initialize with current mode

        # Start with welcome label in scroll area
        self.scroll_area.setWidget(self.welcome_label)

        # Create navigation controls
        self._setup_navigation_controls(main_layout)

        self.setCentralWidget(central_widget)

    def _setup_navigation_controls(self, main_layout):
        """Setup navigation buttons and zoom slider"""
        button_layout = QHBoxLayout()

        # Previous button
        self.prev_button = QPushButton("Previous Page")
        self.prev_button.clicked.connect(self.prev_page)
        self.prev_button.setEnabled(False)
        button_layout.addWidget(self.prev_button)

        # Zoom controls
        button_layout.addWidget(QLabel("Zoom:"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(25)
        self.zoom_slider.setMaximum(400)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(25)
        self.zoom_slider.setMaximumWidth(200)
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        button_layout.addWidget(self.zoom_slider)

        self.zoom_label = QLabel("100%")
        self.zoom_label.setMinimumWidth(50)
        button_layout.addWidget(self.zoom_label)

        # Next button
        self.next_button = QPushButton("Next Page")
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setEnabled(False)
        button_layout.addWidget(self.next_button)

        main_layout.addLayout(button_layout, 0)  # stretch factor 0 - fixed size

    def _setup_menubar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_action = QAction("Open PDF", self)
        open_action.setShortcut(QKeySequence.Open)  # CMD+O on Mac, Ctrl+O on other OS
        open_action.triggered.connect(self.open_pdf)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)  # CMD+S on Mac, Ctrl+S on other OS
        save_action.triggered.connect(self.save_pdf)
        file_menu.addAction(save_action)

    def _setup_toolbar(self):
        """Setup the toolbar"""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setMovable(False)

        # Save PDF button
        save_pdf_action = QAction("Save PDF", self)
        save_pdf_action.triggered.connect(self.save_pdf)
        toolbar.addAction(save_pdf_action)

        toolbar.addSeparator()

        # Add Text button (checkable for mode selection)
        self.add_text_action = QAction("Add Text", self)
        self.add_text_action.setCheckable(True)
        self.add_text_action.setChecked(True)  # Default mode
        self.add_text_action.triggered.connect(lambda: self.set_mode(EditMode.TEXT))
        toolbar.addAction(self.add_text_action)

        # Add Image button (checkable for mode selection)
        self.add_image_action = QAction("Add Image", self)
        self.add_image_action.setCheckable(True)
        self.add_image_action.triggered.connect(lambda: self.set_mode(EditMode.IMAGE))
        toolbar.addAction(self.add_image_action)

        # Add Doodle button (checkable for mode selection)
        self.add_doodle_action = QAction("Add Doodle", self)
        self.add_doodle_action.setCheckable(True)
        self.add_doodle_action.triggered.connect(lambda: self.set_mode(EditMode.DOODLE))
        toolbar.addAction(self.add_doodle_action)

        return toolbar

    def set_mode(self, mode):
        """Set the current editing mode (text, image, or doodle)"""
        self.current_mode = mode

        # Update button states - only one should be checked
        self.add_text_action.setChecked(mode == EditMode.TEXT)
        self.add_image_action.setChecked(mode == EditMode.IMAGE)
        self.add_doodle_action.setChecked(mode == EditMode.DOODLE)

        # Update label's current mode for cursor changes
        self.label.current_mode = mode

    # PDF Operations
    def open_pdf(self):
        """Open a PDF file"""
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if not path:
            return

        self.doc = self.open_pdf_file(path)
        self.current_page = 0
        self.draft_annotations = []

        # Switch from welcome message to PDF label
        old_widget = self.scroll_area.takeWidget()
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(False)

        self.show_page(self.current_page)
        self.update_buttons()
        self.resize_window_to_pdf()

    def show_page(self, page_num):
        """Display a specific page of the PDF"""
        page = self.doc[page_num]

        # Render page at current zoom
        zoom_factor = 2.0 * self.zoom_level
        pixmap = self.render_page(page, zoom_factor)

        self.label.setPixmap(pixmap)
        self.label.adjustSize()

        # Update annotations for current page
        self.label.annotations = [a for a in self.draft_annotations if a.page_num == page_num]
        self.label.zoom_level = self.zoom_level
        self.label.update()

    def save_pdf(self):
        """Save all draft annotations to the PDF file"""
        if not self.doc or not self.draft_annotations:
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "edited.pdf", "PDF Files (*.pdf)")
        if not path:
            return

        # Apply annotations to PDF
        self.save_pdf_with_annotations(self.doc, self.draft_annotations)

        # Save document
        self.doc.save(path)

        # Clear and reload
        self.draft_annotations = []
        self.label.annotations = []
        self.doc = self.open_pdf_file(path)
        self.show_page(self.current_page)

    # Navigation
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

    # Zoom Operations
    def on_zoom_changed(self, value):
        """Handle zoom slider value change"""
        self.zoom_level = value / 100.0
        self.zoom_label.setText(f"{value}%")

        if self.doc:
            self.show_page(self.current_page)
            self.resize_window_to_pdf()

    def resize_window_to_pdf(self):
        """Resize window to fit PDF dimensions within screen bounds"""
        if not self.doc:
            return

        pdf_width = self.label.pixmap().width()
        pdf_height = self.label.pixmap().height()

        menubar_height = self.menuBar().height() if self.menuBar().height() > 0 else 25
        toolbar_height = self.toolbar.height() if self.toolbar.height() > 0 else 40
        self.prev_button.adjustSize()
        button_height = max(self.prev_button.height(), 40) + 10

        # Calculate optimal size using WindowManager mixin
        width, height = self.calculate_window_size(
            pdf_width, pdf_height, menubar_height + toolbar_height, button_height
        )

        self.resize(width, height)
        self.center_window(self)

    # Annotation Operations
    def mousePressEvent(self, event):
        """Handle mouse press events based on current mode"""
        if not self.doc:
            self.open_pdf()
            return

        label_pos = self.label.mapFromGlobal(event.globalPos())

        if not self.label.rect().contains(label_pos):
            return

        # Handle different modes
        if self.current_mode == EditMode.TEXT:
            self._handle_text_mode_click(label_pos)
        elif self.current_mode == EditMode.IMAGE:
            self._handle_image_mode_click(label_pos)
        elif self.current_mode == EditMode.DOODLE:
            # Doodle mode - not implemented yet
            pass

    def _handle_text_mode_click(self, label_pos):
        """Handle mouse click in text mode"""
        # Check if clicking on existing annotation
        for annotation in self.label.annotations:
            if annotation.contains_point(label_pos.x(), label_pos.y(), self.zoom_level):
                return

        # Add new text annotation
        dialog = TextFormatDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            values = dialog.get_values()
            if values['text']:
                self.add_draft_text(label_pos.x(), label_pos.y(), values)

    def _handle_image_mode_click(self, label_pos):
        """Handle mouse click in image mode"""
        # Check if clicking on existing annotation
        for annotation in self.label.annotations:
            if annotation.contains_point(label_pos.x(), label_pos.y(), self.zoom_level):
                return

        # Open file dialog to select image
        image_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if image_path:
            self.add_draft_image(label_pos.x(), label_pos.y(), image_path)

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
        annotation.created_at_zoom = self.zoom_level

        self.draft_annotations.append(annotation)
        self.label.annotations.append(annotation)
        self.label.update()

    def add_draft_image(self, x, y, image_path):
        """Add image annotation in draft mode"""
        annotation = ImageAnnotation(x, y, image_path, self.current_page)
        annotation.created_at_zoom = self.zoom_level

        self.draft_annotations.append(annotation)
        self.label.annotations.append(annotation)
        self.label.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFEditor()
    window.show()
    sys.exit(app.exec_())
