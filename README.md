# Amar PDF (PDF Editor)

## Download
Download for Windows, Mac, and Linux from here: [Releases](https://github.com/tareq403/Amar-PDF/releases)

## See Amar PDF in Action
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/R61yBDCa_p0/0.jpg)](https://www.youtube.com/watch?v=R61yBDCa_p0)

A professional PDF viewer and editor application built with PyQt5 and PyMuPDF (fitz). Features a clean, modular architecture with comprehensive annotation tools, page management, and PDF merging capabilities.

## Features

### PDF Viewing
- **High-Quality Rendering**: 2x base scale rendering for crisp display
- **Page Navigation**: Previous/Next buttons with keyboard shortcuts
- **Flexible Zoom**: 25% to 400% with interactive slider
- **Dynamic Window Sizing**: Automatically resizes based on PDF and zoom level
- **Scrollable Viewer**: Handles large documents with smooth scrolling
- **Multi-page Support**: Navigate through multi-page documents seamlessly

### Text Annotations
- **Rich Text Input**: Click anywhere on PDF to add formatted text
- **Font Customization**:
  - Font family selection (Arial, Times, Courier, etc.)
  - Font sizes from 6pt to 72pt
  - Bold, italic, underline, strikethrough styles
  - Color picker for custom text colors
- **Interactive Editing**:
  - Drag annotations to reposition
  - Double-click to edit text and formatting
  - Zoom-aware positioning (annotations stay in place when zooming)
- **Draft Mode**: Preview with dashed blue borders before saving
- **Smart Cursor**: I-beam cursor in text mode for intuitive UX

### Image Annotations
- **Image Import**: Support for PNG, JPG, JPEG, BMP, GIF formats
- **Resize Support**: Drag image edges to resize (maintains aspect ratio)
- **Interactive Placement**: Drag to reposition on the page
- **Smart Cursors**: Resize cursors when hovering over edges

### Doodle/Drawing Annotations
- **Free-Hand Drawing**: Draw directly on PDFs with mouse/stylus
- **Customizable Pen**:
  - Color picker for any color
  - Pen width from 1px to 20px
- **Drawing Canvas**: Dedicated 600x400 canvas for creating doodles
- **Resize Support**: Resize doodles after placing them on PDF
- **Clear Function**: Start over if needed before applying

### Page Management
- **All Pages View**: Overview of all pages in vertical layout
- **Drag & Drop Reordering**: Drag pages to reorder the document
- **Page Deletion**: Delete unwanted pages with confirmation
- **Preview Mode**: Changes are not applied until confirmed
- **Smart Annotation Tracking**: Annotations move with their pages
- **Cancel/Confirm**: Discard or apply page operations
- **PDF Merging**: Merge multiple PDF files into one document

### File Operations
- **Open PDF**: Load PDF files for viewing and editing
- **Save PDF**: Export with all annotations permanently applied
- **Link another PDF**: Merge multiple PDF files seamlessly (available in toolbar and File menu)

### Keyboard Shortcuts
- **Cmd+O / Ctrl+O**: Open PDF
- **Cmd+S / Ctrl+S**: Save PDF with annotations

### Multiple Editing Modes
- **Text Mode**: Add and edit text annotations (default)
- **Image Mode**: Place and resize images
- **Doodle Mode**: Create free-hand drawings
- **Mode Toggle**: Toolbar buttons for quick mode switching

## Project Structure

```
PdfEditor/
├── core/                          # Framework-level code
│   ├── __init__.py
│   ├── annotation_manager.py     # Centralized annotation management
│   ├── config.py                 # Runtime configuration
│   ├── enums.py                  # EditMode, ResizeEdge enums
│   ├── exceptions.py             # Custom exception hierarchy
│   ├── logging_config.py         # Logging infrastructure
│   └── constants/                # Domain-organized constants
│       ├── __init__.py
│       ├── rendering.py          # Rendering and zoom constants
│       ├── ui.py                 # UI dimension constants
│       ├── text.py               # Text and font constants
│       ├── drawing.py            # Drawing and pen constants
│       └── cursors.py            # Mode-specific cursor constants
│
├── models/                        # Data models
│   ├── __init__.py
│   ├── annotation.py             # Base Annotation ABC
│   ├── text_annotation.py        # Text annotation model with color support
│   ├── text_format.py            # Text formatting dataclass
│   ├── image_annotation.py       # Image annotation model
│   ├── doodle_annotation.py      # Doodle annotation model
│   └── drawing_data.py           # Drawing data structures (Stroke, DrawingData)
│
├── ui/                            # User interface components
│   ├── __init__.py
│   ├── dialogs/                  # Dialog windows
│   │   ├── __init__.py
│   │   ├── text_format_dialog.py # Text input with color picker
│   │   └── doodle_dialog.py      # Free-hand drawing dialog
│   ├── widgets/                  # Custom widgets
│   │   ├── __init__.py
│   │   ├── pdf_view_label.py     # Main PDF display with annotations
│   │   └── page_widget.py        # Draggable page widget
│   ├── windows/                  # Window classes
│   │   ├── __init__.py
│   │   └── all_pages_window.py   # Page management window
│   └── styles/                   # Stylesheets
│       └── toolbar.css           # Toolbar styling
│
├── operations/                    # Business logic
│   ├── __init__.py
│   ├── pdf_operations.py         # PDF rendering and saving
│   └── window_manager.py         # Window sizing utilities
│
├── utils/                         # Utility functions
│   ├── __init__.py
│   └── helpers.py                # Coordinate conversion helpers
│
├── main.py                        # Application entry point
├── pdf_editor.py                 # Main PDFEditor window class
└── README.md                      # This file
```

## Architecture

### Design Patterns

1. **Abstract Base Class (ABC)**: `Annotation` base class with abstract `get_rect()` method
2. **Mixin Pattern**: `PDFOperations` and `WindowManager` provide specific functionality
3. **Factory Pattern**: Factory methods for creating annotation instances from various data sources
4. **Singleton Pattern**: `PDFEditorLogger` uses singleton for centralized logging
5. **Dataclass Pattern**: Type-safe data models (`TextFormat`, `DrawingData`, `Stroke`)
6. **Enum Pattern**: Type-safe `EditMode` and `ResizeEdge` enums
7. **Configuration Pattern**: Centralized domain-organized constants and config
8. **Module Pattern**: Package-based organization with clear separation of concerns

### Key Architectural Decisions

#### Rendering and Scaling
- **Base rendering**: 2x scale for high-quality display (`BASE_SCALE = 2.0`)
- **Zoom multiplication**: `render_scale = BASE_SCALE × zoom_level`
  - Example: 200% zoom = 2.0 × 2.0 = 4.0x total scale
- **Font scaling**: `display_font_size = font_size × BASE_SCALE × zoom_level`

#### Coordinate Management
- **Annotation storage**: Coordinates stored in creation-zoom space
- **Position scaling**: `scaled_pos = original_pos × (current_zoom / creation_zoom)`
- **PDF conversion**: `pdf_coords = screen_coords / (BASE_SCALE × creation_zoom)`
- **Benefit**: Annotations maintain correct positions across zoom changes

#### UI Layout Strategy
- **Stretch factors**: Scroll area (1) expands, buttons (0) stay fixed
- **Dynamic sizing**: Window resizes based on:
  - PDF dimensions at current zoom
  - Screen available geometry
  - UI element heights (menubar, toolbar, buttons)
  - Ensures controls always visible

#### Code Organization Principles
- **Single Responsibility**: Each module has one clear purpose
- **Separation of Concerns**: UI, models, operations clearly separated
- **DRY**: No code duplication (centralized constants, enums)
- **Maintainability**: Files kept under 260 lines
- **Testability**: Isolated components ready for unit testing

## Running the Application

### Prerequisites
- Python 3.9+
- PyQt5 (5.15.11)
- PyMuPDF (1.26.5)

### Installation
```bash
cd PdfEditor
source .venv/bin/activate  # Activate virtual environment
```

### Run
```bash
python main.py
```

## Usage Guide

### 1. Opening a PDF
- Click anywhere in the welcome screen, or
- Use **File → Open PDF** (Cmd+O / Ctrl+O)

### 2. Navigating Pages
- Use **Previous/Next** buttons at bottom
- Buttons auto-enable/disable based on page position

### 3. Zooming
- Drag the **zoom slider** (25%-400%)
- Window automatically resizes to fit content
- All annotations scale correctly

### 4. Adding Text Annotations
1. Ensure **Text Mode** is selected (toolbar)
2. Click anywhere on the PDF
3. Enter text and choose formatting:
   - Font family
   - Font size (6-72pt)
   - Bold, Italic, Underline, Strikethrough
   - Text color (click color button to choose)
4. Click **OK**
5. Text appears with blue dashed border (draft mode)

### 5. Adding Image Annotations
1. Click **Image Mode** in toolbar
2. Click on the PDF where you want the image
3. Select an image file (PNG, JPG, JPEG, BMP, GIF)
4. Image appears with blue dashed border
5. **Drag edges** to resize
6. **Drag center** to reposition

### 6. Adding Doodle Annotations
1. Click **Doodle Mode** in toolbar
2. Click on the PDF where you want the doodle
3. In the drawing dialog:
   - Draw with mouse/stylus
   - Click **Choose Color** for different colors
   - Adjust **Pen Width** (1-20px)
   - Click **Clear** to start over
4. Click **OK** to place doodle on PDF
5. **Drag edges** to resize
6. **Drag center** to reposition

### 7. Managing Pages
1. Click **See All Pages** button at bottom of window
2. In the All Pages window:
   - **View**: All pages displayed vertically at 10% zoom
   - **Reorder**: Drag and drop pages to new positions
   - **Delete**: Click red "Delete" button on any page
   - **Select**: Click a page to highlight it
3. Page operations:
   - **Cancel**: Discard all changes and close window
   - **Confirm**: Apply all changes to the document
4. After confirmation:
   - Document reloaded with new page order
   - Annotations automatically move with their pages
   - Annotations on deleted pages are removed

### 8. Merging PDFs
1. Open a PDF document
2. Click **Link PDF** button in toolbar or **File → Link another PDF** menu
3. Select the PDF file to merge
4. The selected PDF's pages are appended to the current document
5. A success dialog shows:
   - Original page count
   - Number of pages added
   - Total pages after merge
6. All existing annotations remain on their original pages

### 9. Editing Annotations
- **Reposition**: Drag annotation to new location
- **Resize** (Images/Doodles): Drag edges or corners
- **Edit Text**: Double-click text annotation

### 10. Saving the PDF
- Use **File → Save** (Cmd+S / Ctrl+S)
- Choose save location
- All annotations are permanently applied to PDF

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Cmd+O / Ctrl+O | Open PDF |
| Cmd+S / Ctrl+S | Save PDF |

## Development

### Adding New Annotation Types

1. Create new model in `models/`:
```python
from models.annotation import Annotation

class MyAnnotation(Annotation):
    def get_rect(self, current_zoom=1.0):
        # Implementation
        pass
```

2. Update `models/__init__.py` to export the new class

3. Add rendering logic in `ui/widgets/pdf_view_label.py`

4. Add save logic in `operations/pdf_operations.py`

### Testing
Run the comprehensive import test:
```bash
python test_imports.py
```

### Code Style
- Follow PEP 8 guidelines
- Keep modules focused and under 300 lines
- Use type hints where appropriate
- Add docstrings to all public methods

## Key Features Summary

- **Multi-mode editing**: Text, Image, and Doodle modes with mode-specific cursors
- **Rich text annotations**: Font customization, styling, and color picker
- **Page management**: Drag-and-drop reordering, deletion, and PDF merging
- **Advanced zoom system**: 25%-400% with zoom-aware annotation positioning
- **Modular architecture**: Clean separation of concerns with domain-organized constants
- **Logging infrastructure**: Comprehensive logging with file and console handlers
- **Custom exceptions**: Hierarchical exception system for robust error handling
- **Factory methods**: Type-safe object creation for all annotation types
- **Non-destructive editing**: Preview mode for page operations before applying

## License

This project is provided as-is for educational purposes.

## Contributing

When contributing, please:
1. Follow the established package structure
2. Add constants to appropriate files in `core/constants/` rather than using magic numbers
3. Keep files focused and under 300 lines
4. Update `__init__.py` files when adding new modules
5. Test imports with `test_imports.py`
6. Update this README if adding new features
7. Use factory methods for object creation when available
8. Follow the established logging patterns for debugging

## Acknowledgments

Built with:
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF manipulation

---

**Project Status**: ✅ Production Ready

**Last Updated**: October 2025

**Architecture**: Modular, OOP-compliant, maintainable
