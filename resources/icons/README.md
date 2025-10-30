# Application Icons

This directory contains application icons for different platforms.

## Required Icon Files

### 1. **icon.png** (Base Icon)
- **Size**: 512x512 or 1024x1024 pixels
- **Format**: PNG with transparency
- **Used for**: Linux, source for conversion

### 2. **icon.ico** (Windows)
- **Sizes**: Multi-size (16x16, 32x32, 48x48, 64x64, 128x128, 256x256)
- **Format**: ICO format
- **Used for**: Windows executable

### 3. **icon.icns** (macOS)
- **Sizes**: Multi-resolution (16x16 to 1024x1024)
- **Format**: ICNS format
- **Used for**: macOS app bundle

## How to Create Icons

### Option 1: Using Online Tools (Easiest)

1. **Create/obtain a 1024x1024 PNG icon**
   - Design tool: Figma, Canva, or Photoshop
   - Free icon sites: Flaticon, Icons8
   - AI generation: DALL-E, Midjourney

2. **Convert to all formats:**
   - Visit: https://cloudconvert.com/
   - Upload your PNG
   - Convert to ICO (Windows)
   - Visit: https://iconverticons.com/online/
   - Convert PNG to ICNS (macOS)

### Option 2: Using Python (Automated)

Install Pillow:
```bash
pip install Pillow
```

Run this script (save as `create_icons.py`):
```python
from PIL import Image

# Load your base icon (1024x1024 PNG)
img = Image.open('icon_base.png')

# Save as PNG (Linux)
img.save('icon.png')

# For Windows ICO (requires Pillow)
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save('icon.ico', sizes=sizes)

print("Icons created successfully!")
print("Note: For macOS .icns, use iconutil on macOS or online converter")
```

### Option 3: Using Command Line Tools

#### macOS - Create ICNS

1. Create iconset directory:
   ```bash
   mkdir icon.iconset
   ```

2. Generate all required sizes:
   ```bash
   sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
   sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
   sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
   sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
   sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
   sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
   sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
   sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
   sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
   sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png
   ```

3. Convert to ICNS:
   ```bash
   iconutil -c icns icon.iconset
   ```

#### Windows - Create ICO

Use ImageMagick:
```bash
convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

## Icon Design Guidelines

### Style Recommendations
- **Simple and clear**: Recognizable at small sizes (16x16)
- **High contrast**: Visible on light and dark backgrounds
- **No text**: Or very minimal, large text only
- **Transparent background**: For proper OS integration

### PDF Editor Icon Ideas
- 📄 PDF document icon
- ✏️ PDF with pencil/pen
- 📝 Document with edit symbol
- 🖊️ Stylized PDF with annotation marks

### Colors
- Professional: Blue (#0078d4), gray
- Friendly: Orange, purple
- Creative: Multicolor gradient

## Quick Start (No Design Skills Needed)

### 1. Use Emoji as Icon (Quick Test)

```python
# install emoji-to-image
pip install pilmoji

# Use a PDF emoji as base
# Save as icon.png, then convert
```

### 2. Use Free Icon Resources

**Flaticon** (https://www.flaticon.com/):
- Search: "pdf editor"
- Download PNG (512px or larger)
- Free with attribution

**Icons8** (https://icons8.com/):
- Search: "pdf document"
- Download as PNG
- Free with link

**Iconfinder** (https://www.iconfinder.com/):
- Search: "pdf edit"
- Filter: Free icons
- Download PNG

### 3. AI-Generated Icons

**Prompt for DALL-E/Midjourney:**
```
"A clean, minimalist app icon for a PDF editor.
Modern design with a document and pencil.
Simple shapes, professional blue color scheme.
Flat design style, transparent background."
```

## After Creating Icons

1. Place all three icon files in this directory:
   - `icon.png` (512x512+)
   - `icon.ico` (multi-size)
   - `icon.icns` (multi-resolution)

2. Icons will be automatically included in builds via:
   - `PDF-Editor.spec` configuration
   - GitHub Actions workflow

## Testing Icons

### Local Test (macOS)
```bash
pyinstaller PDF-Editor.spec
open dist/PDF-Editor.app
# Check app icon in Finder
```

### Local Test (Windows)
```bash
pyinstaller PDF-Editor.spec
# Check icon in File Explorer
```

### Local Test (Linux)
```bash
pyinstaller PDF-Editor.spec
ls -la dist/
# Icon embedded in executable
```

## License

Ensure you have rights to use your icon:
- Created by you: ✅ OK
- Free resource with attribution: ✅ Add attribution in README.md
- AI-generated: ✅ Check terms of service
- Commercial icon: ❌ Requires license

## Current Status

- [ ] icon.png created
- [ ] icon.ico created (Windows)
- [ ] icon.icns created (macOS)
- [ ] Icons tested locally
- [ ] Icons pushed to repository
