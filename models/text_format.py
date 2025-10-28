"""
Text formatting data model
"""

from dataclasses import dataclass
from core.constants import DEFAULT_FONT, DEFAULT_FONT_SIZE


@dataclass
class TextFormat:
    """
    Data class representing text formatting options.

    This class encapsulates all formatting properties for text annotations,
    providing a type-safe alternative to dictionary-based data passing.

    Attributes:
        text: The text content to display
        font_family: Font family name (e.g., "Arial", "Times New Roman")
        font_size: Font size in points
        bold: Whether text should be bold
        italic: Whether text should be italic
        underline: Whether text should be underlined
        strikethrough: Whether text should have strikethrough
    """
    text: str
    font_family: str = DEFAULT_FONT
    font_size: int = DEFAULT_FONT_SIZE
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False

    def __post_init__(self):
        """Validate text format data after initialization"""
        # Strip whitespace from text
        self.text = self.text.strip() if self.text else ""

        # Validate font size
        from core.constants import MIN_FONT_SIZE, MAX_FONT_SIZE
        if not (MIN_FONT_SIZE <= self.font_size <= MAX_FONT_SIZE):
            raise ValueError(
                f"Font size must be between {MIN_FONT_SIZE} and {MAX_FONT_SIZE}, "
                f"got {self.font_size}"
            )

    def is_valid(self) -> bool:
        """Check if the format has valid text content"""
        return bool(self.text and self.text.strip())
