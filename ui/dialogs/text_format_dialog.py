"""
Text formatting dialog
"""

from PyQt5.QtWidgets import (QDialog, QLineEdit, QFontComboBox, QSpinBox,
                             QCheckBox, QDialogButtonBox, QFormLayout,
                             QGroupBox, QVBoxLayout, QMessageBox, QPushButton,
                             QHBoxLayout, QColorDialog)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
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

        # Store current color
        self.current_color = QColor(*format_obj.color)

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

        # Color selection
        color_layout = QHBoxLayout()
        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self._choose_color)
        self.color_button.setMinimumHeight(30)
        self._update_color_button()
        color_layout.addWidget(self.color_button)
        color_layout.addStretch()
        form_layout.addRow("Color:", color_layout)

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

    def _choose_color(self):
        """Open color picker dialog"""
        color = QColorDialog.getColor(self.current_color, self, "Choose Text Color")
        if color.isValid():
            self.current_color = color
            self._update_color_button()

    def _update_color_button(self):
        """Update the color button's appearance to show current color"""
        # Set background color and adjust text color for contrast
        r, g, b = self.current_color.red(), self.current_color.green(), self.current_color.blue()
        # Calculate brightness to determine text color
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        text_color = "black" if brightness > 128 else "white"

        self.color_button.setStyleSheet(
            f"background-color: rgb({r}, {g}, {b}); "
            f"color: {text_color}; "
            f"border: 1px solid #999; "
            f"padding: 5px;"
        )

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
            strikethrough=self.strikethrough_check.isChecked(),
            color=(self.current_color.red(), self.current_color.green(), self.current_color.blue())
        )
