"""
Text formatting dialog
"""

from PyQt5.QtWidgets import (QDialog, QLineEdit, QFontComboBox, QSpinBox,
                             QCheckBox, QDialogButtonBox, QFormLayout,
                             QGroupBox, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QFont
from typing import Optional

from core.constants import DEFAULT_FONT, DEFAULT_FONT_SIZE, MIN_FONT_SIZE, MAX_FONT_SIZE
from models import TextFormat


class TextFormatDialog(QDialog):
    """
    Dialog for text input with font formatting options.

    This dialog allows users to enter text and configure its formatting
    properties including font family, size, and text decorations.

    Args:
        parent: Parent widget
        initial_format: Optional TextFormat object with initial values
    """
    def __init__(self, parent=None, initial_format: Optional[TextFormat] = None):
        super().__init__(parent)
        self.setWindowTitle("Text Format")
        self.setMinimumWidth(400)

        # Use provided format or create default
        format_obj = initial_format or TextFormat(text="")

        layout = QVBoxLayout(self)

        # Text input
        form_layout = QFormLayout()
        self.text_edit = QLineEdit(format_obj.text)
        self.text_edit.setPlaceholderText("Enter text here...")
        form_layout.addRow("Text:", self.text_edit)

        # Font selection
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont(format_obj.font_family))
        form_layout.addRow("Font:", self.font_combo)

        # Font size
        self.size_spin = QSpinBox()
        self.size_spin.setMinimum(MIN_FONT_SIZE)
        self.size_spin.setMaximum(MAX_FONT_SIZE)
        self.size_spin.setValue(format_obj.font_size)
        form_layout.addRow("Size:", self.size_spin)

        layout.addLayout(form_layout)

        # Text decorations
        decoration_group = QGroupBox("Text Decorations")
        decoration_layout = QVBoxLayout()

        self.bold_check = QCheckBox("Bold")
        self.bold_check.setChecked(format_obj.bold)
        decoration_layout.addWidget(self.bold_check)

        self.italic_check = QCheckBox("Italic")
        self.italic_check.setChecked(format_obj.italic)
        decoration_layout.addWidget(self.italic_check)

        self.underline_check = QCheckBox("Underline")
        self.underline_check.setChecked(format_obj.underline)
        decoration_layout.addWidget(self.underline_check)

        self.strikethrough_check = QCheckBox("Strikethrough")
        self.strikethrough_check.setChecked(format_obj.strikethrough)
        decoration_layout.addWidget(self.strikethrough_check)

        decoration_group.setLayout(decoration_layout)
        layout.addWidget(decoration_group)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _on_accept(self):
        """Validate input before accepting dialog"""
        text = self.text_edit.text().strip()
        if not text:
            QMessageBox.warning(
                self,
                "Empty Text",
                "Please enter some text before continuing.",
                QMessageBox.Ok
            )
            self.text_edit.setFocus()
            return

        self.accept()

    def get_values(self) -> TextFormat:
        """
        Get the text format from dialog inputs.

        Returns:
            TextFormat object with all formatting properties

        Note:
            The text will be automatically stripped of leading/trailing whitespace.
        """
        return TextFormat(
            text=self.text_edit.text().strip(),
            font_family=self.font_combo.currentFont().family(),
            font_size=self.size_spin.value(),
            bold=self.bold_check.isChecked(),
            italic=self.italic_check.isChecked(),
            underline=self.underline_check.isChecked(),
            strikethrough=self.strikethrough_check.isChecked()
        )
