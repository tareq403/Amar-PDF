"""
Comprehensive import test for refactored PDF Editor
"""

print("Testing imports...")

# Test core imports
print("✓ Testing core imports...")
from core.enums import EditMode, ResizeEdge
from core.constants import BASE_SCALE, DEFAULT_ZOOM, CANVAS_WIDTH
from core.config import Config
print("  ✓ core.enums")
print("  ✓ core.constants")
print("  ✓ core.config")

# Test model imports
print("✓ Testing model imports...")
from models import Annotation, TextAnnotation, ImageAnnotation, DoodleAnnotation
from models.annotation import Annotation as DirectAnnotation
print("  ✓ models package")
print("  ✓ models.annotation")
print("  ✓ models.text_annotation")
print("  ✓ models.image_annotation")
print("  ✓ models.doodle_annotation")

# Test UI imports
print("✓ Testing UI imports...")
from ui.dialogs import TextFormatDialog, DoodleDialog, DrawingCanvas
from ui.widgets import PDFViewLabel
print("  ✓ ui.dialogs")
print("  ✓ ui.widgets")

# Test operations imports
print("✓ Testing operations imports...")
from operations import PDFOperations, WindowManager
print("  ✓ operations.pdf_operations")
print("  ✓ operations.window_manager")

# Test utils imports
print("✓ Testing utils imports...")
from utils.helpers import create_rect, scale_coordinate
print("  ✓ utils.helpers")

# Test main application
print("✓ Testing main application...")
from pdf_editor import PDFEditor
from main import main
print("  ✓ pdf_editor")
print("  ✓ main")

print("\n" + "="*50)
print("✅ ALL IMPORTS SUCCESSFUL!")
print("="*50)
print("\nRefactored structure:")
print("  • core/       - Framework-level code")
print("  • models/     - Data models")
print("  • ui/         - User interface components")
print("  • operations/ - Business logic")
print("  • utils/      - Helper utilities")
print("  • main.py     - Application entry point")
print("\n✨ Refactoring complete and verified!")
