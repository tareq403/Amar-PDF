"""
Widget for displaying a single draggable PDF page
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QMimeData, QPoint
from PyQt5.QtGui import QDrag


class PageWidget(QWidget):
    """Widget representing a single page that can be dragged and selected"""

    def __init__(self, page_num, pixmap, parent_window):
        """
        Initialize page widget

        Args:
            page_num: Page number (0-indexed)
            pixmap: QPixmap of the rendered page
            parent_window: Reference to AllPagesWindow
        """
        super().__init__()
        self.page_num = page_num
        self.parent_window = parent_window
        self.is_selected = False
        self.drag_start_position = None

        # Setup layout
        self._setup_ui(pixmap)

    def _setup_ui(self, pixmap):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Page number label and delete button
        header_layout = QHBoxLayout()
        self.page_label = QLabel(f"Page {self.page_num + 1}")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet("font-weight: bold; color: #333;")
        header_layout.addStretch()
        header_layout.addWidget(self.page_label)
        header_layout.addStretch()

        # Delete button
        delete_button = QPushButton("Delete")
        delete_button.setMaximumWidth(80)
        delete_button.clicked.connect(self.on_delete_clicked)
        delete_button.setStyleSheet("background-color: #dc3545; color: white; padding: 3px;")
        header_layout.addWidget(delete_button)

        layout.addLayout(header_layout)

        # Page image
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Make widget interactive
        self.setAcceptDrops(True)
        self.update_style()

    def update_style(self):
        """Update widget styling based on selection state"""
        if self.is_selected:
            self.setStyleSheet("""
                PageWidget {
                    border: 3px solid #007bff;
                    background-color: #e7f3ff;
                }
            """)
            self.image_label.setStyleSheet("border: 1px solid #ccc; background-color: white;")
        else:
            self.setStyleSheet("""
                PageWidget {
                    border: 1px solid #ccc;
                    background-color: white;
                }
            """)
            self.image_label.setStyleSheet("border: 1px solid #ccc; background-color: white;")

    def mousePressEvent(self, event):
        """Handle mouse press for selection and drag start"""
        if event.button() == Qt.LeftButton:
            # Select this page
            self.parent_window.select_page(self.page_num)
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse move for drag operation"""
        if not (event.buttons() & Qt.LeftButton):
            return
        if self.drag_start_position is None:
            return

        # Check if drag distance is sufficient
        if (event.pos() - self.drag_start_position).manhattanLength() < 10:
            return

        # Start drag operation
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(str(self.page_num))
        drag.setMimeData(mime_data)

        # Set drag pixmap (smaller version of page)
        scaled_pixmap = self.image_label.pixmap().scaled(
            150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        drag.setPixmap(scaled_pixmap)
        drag.setHotSpot(QPoint(scaled_pixmap.width() // 2, scaled_pixmap.height() // 2))

        # Execute drag
        drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event - reorder pages"""
        if event.mimeData().hasText():
            source_page = int(event.mimeData().text())
            target_page = self.page_num

            if source_page != target_page:
                self.parent_window.reorder_pages(source_page, target_page)

            event.acceptProposedAction()

    def on_delete_clicked(self):
        """Handle delete button click"""
        self.parent_window.delete_page(self.page_num)
