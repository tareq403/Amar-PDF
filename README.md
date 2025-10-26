# PDF Editor

A simple PDF viewer and editor application built with PyQt5 and PyMuPDF (fitz).

## Features

- Open and view PDF files with high-quality rendering
- Navigate between pages with Previous/Next buttons
- Add text annotations with draft mode:
  - Click anywhere on the PDF to add text
  - Choose font family, size, and styling (bold, italic, underline, strikethrough)
  - Preview annotations with dashed blue borders before saving
  - Drag annotations to reposition them
  - Double-click to edit annotation text and formatting
- Save edited PDFs with all annotations applied
- Scrollable PDF viewer for large documents

## Project Structure

```
PdfEditor/
├── pdf_editor.py      # Main application and PDFEditor class
├── dialogs.py         # Dialog windows (TextFormatDialog)
├── models.py          # Data models (TextAnnotation)
├── widgets.py         # Custom widgets (PDFViewLabel)
└── README.md          # This file
```

## Module Overview

### pdf_editor.py
Main application file containing the `PDFEditor` class (QMainWindow).

**Responsibilities:**
- Window initialization and layout
- PDF file loading and page navigation
- Menu actions (Open, Save)
- Coordinate mapping for annotations
- PDF saving with font formatting

### dialogs.py
Custom dialog windows for user interaction.

**Classes:**
- `TextFormatDialog`: Dialog for text input with font selection, size, and decorations

### models.py
Data model classes for representing application state.

**Classes:**
- `TextAnnotation`: Represents a text annotation in draft mode with position, text, page number, and formatting properties

### widgets.py
Custom Qt widgets with specialized behavior.

**Classes:**
- `PDFViewLabel`: Custom QLabel that renders PDF pages and draft annotations with interactive features (drag, edit)

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

2. **Navigate Pages**:
   - Use Previous/Next buttons at the bottom

3. **Add Text Annotation**:
   - Click on the PDF where you want to add text
   - Enter text and choose formatting options
   - Text appears with a blue dashed border (draft mode)

4. **Edit Annotation**:
   - Double-click on any draft annotation to edit

5. **Move Annotation**:
   - Click and drag the dashed border to reposition

6. **Save PDF**:
   - Use File → Save menu
   - All draft annotations are applied to the PDF
   - Choose save location

## Architecture Notes

- PDF pages are rendered at 2x scale for high-quality display
- Font sizes are doubled in preview to match the scaled rendering
- Coordinates are converted from screen space (2x) to PDF space (1x) when saving
- Draft annotations are stored separately and only applied on save
- The scroll area automatically manages viewport scrolling for large PDFs
