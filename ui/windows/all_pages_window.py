"""
Window for displaying all pages of a PDF document
"""

import fitz
import tempfile
import os
from PyQt5.QtWidgets import (QMainWindow, QScrollArea, QWidget, QVBoxLayout,
                             QPushButton, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from operations import PDFOperations
from ui.widgets import PageWidget


class AllPagesWindow(QMainWindow, PDFOperations):
    """Window that displays all pages of a PDF in vertical layout"""

    def __init__(self, doc, parent=None):
        """
        Initialize the all pages window

        Args:
            doc: PyMuPDF document object
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.original_doc = doc
        self.parent_editor = parent
        self.selected_page = None
        self.page_widgets = []
        self.setWindowTitle("All Pages - Reorder & Delete")

        # Create a working copy of the document for preview
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        self.temp_file.close()
        doc.save(self.temp_file.name)
        self.doc = fitz.open(self.temp_file.name)

        # Track page mapping from preview to original
        # page_mapping[current_index] = original_page_number
        self.page_mapping = list(range(len(self.doc)))

        # Set window size (800x600 default)
        self.setGeometry(100, 100, 800, 600)

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        """Setup the user interface"""
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Create container widget for all pages
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setSpacing(20)  # Space between pages
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Render all pages
        self.render_all_pages()

        # Add stretch to push pages to top
        self.layout.addStretch()

        # Set container as scroll area widget
        self.scroll_area.setWidget(self.container)

        # Add scroll area to main layout
        main_layout.addWidget(self.scroll_area, 1)  # stretch factor 1

        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)
        button_layout.setSpacing(10)

        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumHeight(40)
        cancel_button.clicked.connect(self.on_cancel)
        cancel_button.setStyleSheet("background-color: #6c757d; color: white; font-size: 14px;")
        button_layout.addWidget(cancel_button)

        # Confirm button
        confirm_button = QPushButton("Confirm")
        confirm_button.setMinimumHeight(40)
        confirm_button.clicked.connect(self.on_confirm)
        confirm_button.setStyleSheet("background-color: #28a745; color: white; font-size: 14px;")
        button_layout.addWidget(confirm_button)

        # Add button layout to main layout
        main_layout.addLayout(button_layout, 0)  # stretch factor 0 - fixed size

        # Set main widget as central widget
        self.setCentralWidget(main_widget)

    def render_all_pages(self):
        """Render all pages of the document"""
        # Clear existing widgets
        self.page_widgets.clear()

        # Render all pages at 10% zoom (0.1 * 2.0 BASE_SCALE = 0.2 total)
        zoom_factor = 0.2  # 10% of original size at BASE_SCALE

        for page_num in range(len(self.doc)):
            # Render page
            page = self.doc[page_num]
            pixmap = self.render_page(page, zoom_factor)

            # Create page widget
            page_widget = PageWidget(page_num, pixmap, self)
            self.page_widgets.append(page_widget)
            self.layout.insertWidget(page_num, page_widget)

    def refresh_display(self):
        """Refresh the display after reordering or deletion"""
        # Remove all widgets from layout
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Re-render all pages
        self.render_all_pages()

        # Add stretch at the end
        self.layout.addStretch()

    def select_page(self, page_num):
        """Select a page"""
        # Deselect previous
        if self.selected_page is not None and self.selected_page < len(self.page_widgets):
            self.page_widgets[self.selected_page].is_selected = False
            self.page_widgets[self.selected_page].update_style()

        # Select new
        self.selected_page = page_num
        if page_num < len(self.page_widgets):
            self.page_widgets[page_num].is_selected = True
            self.page_widgets[page_num].update_style()

    def reorder_pages(self, source_page, target_page):
        """
        Reorder pages in the preview document

        Args:
            source_page: Page being moved (0-indexed)
            target_page: Target position (0-indexed)
        """
        if source_page == target_page:
            return

        # Move the page in the preview document
        self.doc.move_page(source_page, target_page)

        # Update page mapping
        original_page = self.page_mapping.pop(source_page)
        self.page_mapping.insert(target_page, original_page)

        # Refresh display
        self.refresh_display()

    def delete_page(self, page_num):
        """
        Delete a page from the preview document

        Args:
            page_num: Page to delete (0-indexed)
        """
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            'Delete Page',
            f'Are you sure you want to delete Page {page_num + 1}?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        # Cannot delete if only one page remains
        if len(self.doc) <= 1:
            QMessageBox.warning(
                self,
                'Cannot Delete',
                'Cannot delete the last page of the document.',
                QMessageBox.Ok
            )
            return

        # Delete the page from preview
        self.doc.delete_page(page_num)

        # Update page mapping - remove the deleted page
        self.page_mapping.pop(page_num)

        # Refresh display
        self.selected_page = None
        self.refresh_display()

    def on_cancel(self):
        """Cancel changes and close window"""
        # Clean up temp file
        self.doc.close()
        os.unlink(self.temp_file.name)

        # Close window without applying changes
        self.close()

    def on_confirm(self):
        """Apply changes to the real document"""
        # Create new document with reordered/remaining pages
        new_doc = fitz.open()

        # Copy pages in the new order
        for page_idx in self.page_mapping:
            new_doc.insert_pdf(self.original_doc, from_page=page_idx, to_page=page_idx)

        # Update annotations based on page mapping
        if self.parent_editor and hasattr(self.parent_editor, 'draft_annotations'):
            new_annotations = []
            deleted_pages = set(range(len(self.original_doc))) - set(self.page_mapping)

            for annotation in self.parent_editor.draft_annotations:
                original_page = annotation.page_num

                # Skip annotations on deleted pages
                if original_page in deleted_pages:
                    continue

                # Find new page number
                if original_page in self.page_mapping:
                    new_page_num = self.page_mapping.index(original_page)
                    annotation.page_num = new_page_num
                    new_annotations.append(annotation)

            self.parent_editor.draft_annotations = new_annotations

        # Replace original document
        if self.parent_editor and hasattr(self.parent_editor, 'doc'):
            self.parent_editor.doc.close()
            self.parent_editor.doc = new_doc
            self.parent_editor.current_page = 0
            self.parent_editor.show_page(0)
            self.parent_editor.update_buttons()

        # Clean up temp file
        self.doc.close()
        os.unlink(self.temp_file.name)

        # Close window
        self.close()

    def closeEvent(self, event):
        """Handle window close event"""
        # Clean up temp file if it still exists
        try:
            self.doc.close()
            if hasattr(self, 'temp_file'):
                os.unlink(self.temp_file.name)
        except:
            pass
        event.accept()
