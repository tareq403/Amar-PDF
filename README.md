# PDF Editor

A simple PDF viewer and editor application built with PyQt5 and PyMuPDF (fitz).

## Features

- **PDF Viewing**:
  - Open and view PDF files with high-quality rendering (2x base scale)
  - Navigate between pages with Previous/Next buttons
  - Zoom from 25% to 400% with interactive slider
  - Dynamic window resizing based on PDF dimensions and zoom level
  - Scrollable PDF viewer for large documents

- **Text Annotations**:
  - Click anywhere on the PDF to add text
  - Choose font family, size, and styling (bold, italic, underline, strikethrough)
  - Preview annotations with dashed blue borders before saving (draft mode)
  - Drag annotations to reposition them
  - Double-click to edit annotation text and formatting
  - Annotations scale correctly with zoom changes
  - Save edited PDFs with all annotations applied at original size

## Project Structure

```
PdfEditor/
├── pdf_editor.py        # Main application (279 lines)
├── pdf_operations.py    # PDF rendering and saving (89 lines)
├── window_manager.py    # Window sizing utilities (61 lines)
├── dialogs.py           # Dialog windows (79 lines)
├── models.py            # Data models (57 lines)
├── widgets.py           # Custom widgets (112 lines)
└── README.md            # This file
```

## Module Overview

### pdf_editor.py
Main application file containing the `PDFEditor` class (QMainWindow).

**Responsibilities:**
- Window initialization and UI setup
- Application state management (zoom, current page, annotations)
- Event handling (mouse events, navigation)
- Orchestrates PDF operations and window management

**Uses mixins:** `PDFOperations`, `WindowManager`

### pdf_operations.py
PDF file operations using PyMuPDF.

**Classes:**
- `PDFOperations` (mixin): PDF rendering, opening, and annotation saving

**Key methods:**
- `open_pdf_file()`: Open and return PDF document
- `render_page()`: Render page at zoom level to QPixmap
- `save_pdf_with_annotations()`: Apply all annotations to PDF

### window_manager.py
Window sizing and positioning utilities.

**Classes:**
- `WindowManager` (mixin): Window dimension calculations and positioning

**Key methods:**
- `calculate_window_size()`: Compute optimal window size for PDF and screen
- `center_window()`: Center window on screen

### dialogs.py
Custom dialog windows for user interaction.

**Classes:**
- `TextFormatDialog`: Dialog for text input with font selection, size, and decorations

### models.py
Data model classes for representing application state.

**Classes:**
- `TextAnnotation`: Represents a text annotation with position, formatting, and zoom awareness

### widgets.py
Custom Qt widgets with specialized behavior.

**Classes:**
- `PDFViewLabel`: Custom QLabel that renders PDF pages and draft annotations with interactive features (drag, edit, zoom)

## Running the Application

```bash
cd PdfEditor
source .venv/bin/activate  # Activate virtual environment
python pdf_editor.py
```

## Dependencies

- Python 3.9+
- PyQt5 (5.15.11) - GUI framework
- PyMuPDF (1.26.5) - PDF manipulation and rendering

## Usage

1. **Open a PDF**:
   - Click anywhere in the window, or
   - Use File → Open PDF menu

2. **Zoom In/Out**:
   - Use the zoom slider at the bottom (25%-400%)
   - Window automatically resizes to fit zoomed content

3. **Navigate Pages**:
   - Use Previous/Next buttons at the bottom

4. **Add Text Annotation**:
   - Click on the PDF where you want to add text
   - Enter text and choose formatting options
   - Text appears with a blue dashed border (draft mode)

5. **Edit Annotation**:
   - Double-click on any draft annotation to edit

6. **Move Annotation**:
   - Click and drag the dashed border to reposition
   - Annotations maintain correct position when zoom changes

7. **Save PDF**:
   - Use File → Save menu
   - All draft annotations are applied to the PDF
   - Choose save location

## Architecture Notes

### Rendering and Scaling
- **Base rendering**: PDF pages rendered at 2x scale for high-quality display
- **Zoom system**: Zoom level (0.25-4.0) multiplied by base 2x scale
  - Example: 200% zoom = 2.0 × 2.0 = 4.0x total rendering scale
- **Font rendering**: Font sizes scaled to match (font_size × 2 × zoom_level)

### Coordinate Management
- **Annotation coordinates**: Stored in the zoom level they were created at
- **Position scaling**: `scaled_position = original_position × (current_zoom / creation_zoom)`
- **Saving to PDF**: Coordinates divided by (2.0 × creation_zoom) to get original PDF coordinates
- This ensures annotations stay at correct document positions across zoom changes

### UI Layout
- **Stretch factors**: Scroll area (1) expands, button layout (0) stays fixed
- **Window sizing**: Dynamically calculates optimal size based on:
  - PDF dimensions at current zoom
  - Screen available space (excludes taskbar)
  - UI element heights (menubar, buttons)
  - Always ensures navigation controls remain visible

### Code Organization
- **Mixin pattern**: PDFEditor uses PDFOperations and WindowManager mixins
- **Separation of concerns**: Each module has single, clear responsibility
- **File sizes**: All modules under 280 lines for maintainability
