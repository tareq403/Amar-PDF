"""
Text formatting dialog
"""

from PyQt5.QtWidgets import (QDialog, QLineEdit, QFontComboBox, QSpinBox,
                             QCheckBox, QDialogButtonBox, QFormLayout,
                             QGroupBox, QVBoxLayout)
from PyQt5.QtGui import QFont

from core.constants import DEFAULT_FONT, DEFAULT_FONT_SIZE, MIN_FONT_SIZE, MAX_FONT_SIZE


class TextFormatDialog(QDialog):
    """Dialog for text input with font formatting options"""
    def __init__(self, parent=None, initial_text="", initial_font=DEFAULT_FONT, initial_size=DEFAULT_FONT_SIZE,
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
        self.size_spin.setMinimum(MIN_FONT_SIZE)
        self.size_spin.setMaximum(MAX_FONT_SIZE)
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
