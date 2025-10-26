#!/usr/bin/env python3
"""
PDF Editor - Main Entry Point
A simple PDF viewer and editor application built with PyQt5 and PyMuPDF.

Usage:
    python main.py
"""

import sys
from PyQt5.QtWidgets import QApplication
from pdf_editor import PDFEditor


def main():
    """Main entry point for the PDF Editor application"""
    app = QApplication(sys.argv)
    window = PDFEditor()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
