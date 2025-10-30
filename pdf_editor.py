"""
PDF Editor - Main Application
A simple PDF viewer and editor application built with PyQt5 and PyMuPDF.
"""

import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QFileDialog,
                             QAction, QScrollArea, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QDialog, QSlider,
                             QMessageBox)
from PyQt5.QtGui import QFont, QKeySequence, QIcon
from PyQt5.QtCore import Qt

from typing import Optional, List
from PyQt5.QtCore import QPoint

from core.enums import EditMode
from core.constants import (BASE_SCALE, MIN_ZOOM, MAX_ZOOM, DEFAULT_ZOOM,
                             ZOOM_SLIDER_MIN, ZOOM_SLIDER_MAX, ZOOM_SLIDER_DEFAULT,
                             ZOOM_SLIDER_TICK_INTERVAL, ZOOM_SLIDER_WIDTH,
                             WINDOW_MARGIN, DECORATION_HEIGHT, DECORATION_WIDTH,
                             MIN_BUTTON_HEIGHT, BUTTON_HEIGHT_PADDING,
                             DEFAULT_MENUBAR_HEIGHT,
                             TEXT_MODE_CURSOR, IMAGE_MODE_CURSOR, DOODLE_MODE_CURSOR)
from core.config import Config
from ui.dialogs import TextFormatDialog, DoodleDialog
from ui import AllPagesWindow
from ui.styles import TOOLBAR_STYLESHEET
from models import TextAnnotation, ImageAnnotation, DoodleAnnotation, TextFormat, DrawingData
from ui.widgets import PDFViewLabel
from operations import PDFOperations, WindowManager


class PDFEditor(QMainWindow, PDFOperations, WindowManager):
    """Main PDF Editor window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor")
        self.setGeometry(*Config.get_default_window_geometry())

        # Initialize state
        self.doc = None
        self.current_page = 0
        self.draft_annotations = []
        self.zoom_level = DEFAULT_ZOOM
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
        self.prev_button = QPushButton("<")
        self.prev_button.setToolTip("Previous Page")
        self.prev_button.clicked.connect(self.prev_page)
        self.prev_button.setEnabled(False)
        self.prev_button.setMaximumWidth(40)
        button_layout.addWidget(self.prev_button)

        # Zoom controls
        button_layout.addWidget(QLabel("Zoom:"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setToolTip("Adjust zoom level (25% - 400%)")
        self.zoom_slider.setMinimum(ZOOM_SLIDER_MIN)
        self.zoom_slider.setMaximum(ZOOM_SLIDER_MAX)
        self.zoom_slider.setValue(ZOOM_SLIDER_DEFAULT)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(ZOOM_SLIDER_TICK_INTERVAL)
        self.zoom_slider.setMaximumWidth(ZOOM_SLIDER_WIDTH)
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        button_layout.addWidget(self.zoom_slider)

        self.zoom_label = QLabel("100%")
        self.zoom_label.setMinimumWidth(50)
        button_layout.addWidget(self.zoom_label)

        # Next button
        self.next_button = QPushButton(">")
        self.next_button.setToolTip("Next Page")
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setEnabled(False)
        self.next_button.setMaximumWidth(40)
        button_layout.addWidget(self.next_button)

        # See All Pages button
        self.all_pages_button = QPushButton("See All Pages")
        self.all_pages_button.setToolTip("View all pages - Reorder and delete pages")
        self.all_pages_button.clicked.connect(self.show_all_pages)
        self.all_pages_button.setEnabled(False)
        button_layout.addWidget(self.all_pages_button)

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

        link_pdf_action = QAction("Link another PDF", self)
        link_pdf_action.triggered.connect(self.merge_pdf)
        file_menu.addAction(link_pdf_action)

    def _setup_toolbar(self):
        """Setup the toolbar"""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Apply styling from constant
        toolbar.setStyleSheet(TOOLBAR_STYLESHEET)

        # Save PDF button
        save_pdf_action = QAction(QIcon.fromTheme("document-save", QIcon()), "💾", self)
        save_pdf_action.setToolTip("Save PDF with annotations (Cmd+S / Ctrl+S)")
        save_pdf_action.triggered.connect(self.save_pdf)
        toolbar.addAction(save_pdf_action)

        # Merge PDF button
        merge_pdf_action = QAction(QIcon.fromTheme("document-merge", QIcon()), "🔗", self)
        merge_pdf_action.setToolTip("Merge another PDF into this document")
        merge_pdf_action.triggered.connect(self.merge_pdf)
        toolbar.addAction(merge_pdf_action)

        toolbar.addSeparator()

        # Add Text button (checkable for mode selection)
        self.add_text_action = QAction(QIcon.fromTheme("format-text", QIcon()), "T", self)
        self.add_text_action.setToolTip("Text Mode - Click to add text annotations")
        self.add_text_action.setCheckable(True)
        self.add_text_action.setChecked(True)  # Default mode
        self.add_text_action.triggered.connect(lambda: self.set_mode(EditMode.TEXT))
        toolbar.addAction(self.add_text_action)

        # Add Image button (checkable for mode selection)
        self.add_image_action = QAction(QIcon.fromTheme("insert-image", QIcon()), "🖼️", self)
        self.add_image_action.setToolTip("Image Mode - Click to add images to PDF")
        self.add_image_action.setCheckable(True)
        self.add_image_action.triggered.connect(lambda: self.set_mode(EditMode.IMAGE))
        toolbar.addAction(self.add_image_action)

        # Add Doodle button (checkable for mode selection)
        self.add_doodle_action = QAction(QIcon.fromTheme("draw-freehand", QIcon()), "✎", self)
        self.add_doodle_action.setToolTip("Doodle Mode - Click to draw on PDF")
        self.add_doodle_action.setCheckable(True)
        self.add_doodle_action.triggered.connect(lambda: self.set_mode(EditMode.DOODLE))
        toolbar.addAction(self.add_doodle_action)

        return toolbar

    def set_mode(self, mode):
        """
        Set the current editing mode (text, image, or doodle).

        Updates button states and cursor to match the selected mode.
        """
        self.current_mode = mode

        # Update button states - only one should be checked
        self.add_text_action.setChecked(mode == EditMode.TEXT)
        self.add_image_action.setChecked(mode == EditMode.IMAGE)
        self.add_doodle_action.setChecked(mode == EditMode.DOODLE)

        # Update label's current mode for cursor changes
        self.label.current_mode = mode

        # Update cursor based on mode
        if mode == EditMode.TEXT:
            self.label.setCursor(TEXT_MODE_CURSOR)
        elif mode == EditMode.IMAGE:
            self.label.setCursor(IMAGE_MODE_CURSOR)
        elif mode == EditMode.DOODLE:
            self.label.setCursor(DOODLE_MODE_CURSOR)

    # PDF Operations
    def open_pdf(self):
        """Open a PDF file"""
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", Config.SUPPORTED_PDF_FORMATS)
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

    def show_page(self, page_num: int) -> None:
        """
        Display a specific page of the PDF.

        Renders the page at the current zoom level and updates the display
        with annotations for this page.

        Args:
            page_num: Zero-indexed page number to display
        """
        page = self.doc[page_num]

        # Render page at current zoom
        zoom_factor = BASE_SCALE * self.zoom_level
        pixmap = self.render_page(page, zoom_factor)

        self.label.setPixmap(pixmap)
        self.label.adjustSize()

        # Update annotations for current page
        self.label.annotations = [a for a in self.draft_annotations if a.page_num == page_num]
        self.label.zoom_level = self.zoom_level
        self.label.update()

    def save_pdf(self):
        """
        Save the PDF file with any modifications.

        This includes:
        - Draft annotations (if any)
        - Merged PDFs
        - Page reordering or deletions
        - Any other document modifications
        """
        if not self.doc:
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", Config.DEFAULT_SAVE_FILENAME, Config.SUPPORTED_PDF_FORMATS)
        if not path:
            return

        # Store current file path to check if saving to same file
        current_file = self.doc.name if hasattr(self.doc, 'name') else None
        is_same_file = current_file and current_file == path

        # Apply annotations to PDF (if any exist)
        if self.draft_annotations:
            self.save_pdf_with_annotations(self.doc, self.draft_annotations)

        # Save document
        if is_same_file:
            # Saving to the same file that's currently open
            # Need to use a temporary file to avoid "save to original must be incremental" error
            import tempfile
            import shutil

            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                temp_path = tmp_file.name

            try:
                # Save to temporary file
                self.doc.save(temp_path)

                # Close the current document
                self.doc.close()

                # Replace original with temporary file
                shutil.move(temp_path, path)

                # Reopen the saved file
                self.doc = self.open_pdf_file(path)
            except Exception as e:
                # If anything fails, try to clean up temp file
                import os
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                QMessageBox.critical(self, "Save Error", f"Failed to save PDF: {str(e)}")
                return
        else:
            # Saving to a different file - direct save works fine
            self.doc.save(path)
            # Close old document and open the new one
            self.doc.close()
            self.doc = self.open_pdf_file(path)

        # Clear draft annotations and reload page
        self.draft_annotations = []
        self.label.annotations = []
        self.show_page(self.current_page)

    def merge_pdf(self) -> None:
        """
        Merge another PDF file into the current document.

        Opens a file dialog for the user to select a PDF file. All pages
        from the selected PDF are appended to the current document.
        Existing annotations are preserved on their original pages.

        The operation shows a success dialog with page count information,
        or a warning dialog if the merge fails.

        Note:
            This operation modifies the document in-place. Use Save to
            persist changes to disk.
        """
        if not self.doc:
            return

        # Open file dialog to select PDF to merge
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF to Merge",
            "",
            Config.SUPPORTED_PDF_FORMATS
        )
        if not path:
            return

        try:
            # Open the PDF to merge
            merge_doc = self.open_pdf_file(path)

            # Store the current page count (where new pages will be inserted)
            original_page_count = len(self.doc)

            # Insert all pages from the merge document
            self.doc.insert_pdf(merge_doc)

            # Close the merge document
            merge_doc.close()

            # Update navigation buttons
            self.update_buttons()

            # Refresh current page display
            self.show_page(self.current_page)

            # Show success message
            QMessageBox.information(
                self,
                "Merge Successful",
                f"Successfully merged PDF.\n\n"
                f"Original pages: {original_page_count}\n"
                f"Added pages: {len(self.doc) - original_page_count}\n"
                f"Total pages: {len(self.doc)}",
                QMessageBox.Ok
            )

        except Exception as e:
            QMessageBox.warning(
                self,
                "Merge Failed",
                f"Failed to merge PDF: {str(e)}",
                QMessageBox.Ok
            )

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
            self.all_pages_button.setEnabled(False)
            return

        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < len(self.doc) - 1)
        self.all_pages_button.setEnabled(True)

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

        menubar_height = self.menuBar().height() if self.menuBar().height() > 0 else DEFAULT_MENUBAR_HEIGHT
        toolbar_height = self.toolbar.height() if self.toolbar.height() > 0 else DECORATION_HEIGHT
        self.prev_button.adjustSize()
        button_height = max(self.prev_button.height(), MIN_BUTTON_HEIGHT) + BUTTON_HEIGHT_PADDING

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
            self._handle_doodle_mode_click(label_pos)

    def _is_clicking_annotation(self, label_pos: QPoint) -> bool:
        """
        Check if click position is on an existing annotation.

        Args:
            label_pos: Position of the click in label coordinates

        Returns:
            True if clicking on an existing annotation, False otherwise
        """
        return any(
            annotation.contains_point(label_pos.x(), label_pos.y(), self.zoom_level)
            for annotation in self.label.annotations
        )

    def _handle_text_mode_click(self, label_pos: QPoint) -> None:
        """
        Handle mouse click in text mode.

        Args:
            label_pos: Position of the click in label coordinates
        """
        # Check if clicking on existing annotation
        if self._is_clicking_annotation(label_pos):
            return

        # Add new text annotation
        dialog = TextFormatDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            text_format = dialog.get_values()
            self.add_draft_text(label_pos.x(), label_pos.y(), text_format)

    def _handle_image_mode_click(self, label_pos: QPoint) -> None:
        """
        Handle mouse click in image mode.

        Args:
            label_pos: Position of the click in label coordinates
        """
        # Check if clicking on existing annotation
        if self._is_clicking_annotation(label_pos):
            return

        # Open file dialog to select image
        image_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            Config.SUPPORTED_IMAGE_FORMATS
        )

        if image_path:
            self.add_draft_image(label_pos.x(), label_pos.y(), image_path)

    def _handle_doodle_mode_click(self, label_pos: QPoint) -> None:
        """
        Handle mouse click in doodle mode.

        Args:
            label_pos: Position of the click in label coordinates
        """
        # Check if clicking on existing annotation
        if self._is_clicking_annotation(label_pos):
            return

        # Open doodle dialog
        dialog = DoodleDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            drawing_data = dialog.get_drawing_data()
            if drawing_data:
                self.add_draft_doodle(label_pos.x(), label_pos.y(), drawing_data)

    def add_draft_text(self, x: float, y: float, text_format: TextFormat) -> None:
        """
        Add text annotation in draft mode.

        Args:
            x: X coordinate in label space
            y: Y coordinate in label space
            text_format: TextFormat object with formatting properties

        Note:
            Uses the TextAnnotation.from_text_format() factory method for
            type-safe creation with all formatting properties including color.
        """
        annotation = TextAnnotation.from_text_format(x, y, self.current_page, text_format)
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

    def add_draft_doodle(self, x: float, y: float, drawing_data: DrawingData) -> None:
        """
        Add doodle annotation in draft mode.

        Args:
            x: X coordinate on the PDF page (in PDF coordinates)
            y: Y coordinate on the PDF page (in PDF coordinates)
            drawing_data: DrawingData object containing all strokes

        Note:
            The doodle will be added to the draft annotations list and displayed
            immediately on the current page.
        """
        annotation = DoodleAnnotation(x, y, self.current_page, drawing_data)
        annotation.created_at_zoom = self.zoom_level

        self.draft_annotations.append(annotation)
        self.label.annotations.append(annotation)
        self.label.update()

    def show_all_pages(self):
        """Open a new window showing all pages of the PDF"""
        if not self.doc:
            return

        # Create and show the all pages window
        all_pages_window = AllPagesWindow(self.doc, self)
        all_pages_window.show()
