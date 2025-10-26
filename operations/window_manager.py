"""
Window sizing and positioning utilities
"""

from PyQt5.QtWidgets import QApplication
from core.constants import WINDOW_MARGIN, DECORATION_HEIGHT, DECORATION_WIDTH


class WindowManager:
    """Mixin class for window management operations"""

    def calculate_window_size(self, pdf_width, pdf_height, menubar_height, button_height):
        """
        Calculate optimal window size based on PDF and screen dimensions

        Args:
            pdf_width: Width of rendered PDF in pixels
            pdf_height: Height of rendered PDF in pixels
            menubar_height: Height of menu bar
            button_height: Height of button area

        Returns:
            tuple: (width, height) for window
        """
        # Get screen dimensions
        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Maximum window height MUST fit buttons on screen
        max_window_height = screen_height - WINDOW_MARGIN

        # Height available for PDF scroll area
        max_pdf_display_height = max_window_height - menubar_height - button_height - DECORATION_HEIGHT

        # Calculate desired window dimensions
        desired_width = min(pdf_width + DECORATION_WIDTH, screen_width - WINDOW_MARGIN)

        # Height: ensure buttons are always visible
        if pdf_height <= max_pdf_display_height:
            # PDF fits in available space - size window to PDF
            desired_height = pdf_height + menubar_height + button_height + DECORATION_HEIGHT
        else:
            # PDF is too large - size window to maximum that keeps buttons visible
            desired_height = max_window_height

        # Final safety check
        desired_height = min(desired_height, max_window_height)
        desired_width = min(desired_width, screen_width - WINDOW_MARGIN)

        return int(desired_width), int(desired_height)

    def center_window(self, window):
        """Center window on screen"""
        screen = QApplication.primaryScreen().availableGeometry()
        window_rect = window.frameGeometry()
        center_point = screen.center()
        window_rect.moveCenter(center_point)
        window.move(window_rect.topLeft())
