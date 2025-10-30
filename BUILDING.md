# Building PDF Editor Executables

This guide explains how to build executable installers for PDF Editor on Mac, Windows, and Linux.

## Overview

PDF Editor uses **PyInstaller** to create standalone executables and **GitHub Actions** to automatically build for all platforms.

## Quick Start: Automated Builds with GitHub Actions

### Prerequisites
- GitHub repository with the code
- Git installed locally

### Creating a Release

1. **Commit and push your code:**
   ```bash
   git add .
   git commit -m "Ready for release"
   git push origin main
   ```

2. **Create and push a version tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **GitHub Actions automatically:**
   - Builds executables for Linux, macOS, and Windows
   - Creates a release at `https://github.com/username/repo/releases`
   - Uploads all three executables to the release

4. **Download installers:**
   - Go to your repository's Releases page
   - Download the appropriate file for your platform:
     - `PDF-Editor-Linux` - Linux executable
     - `PDF-Editor-macOS.app.tar.gz` - macOS app bundle (extract first)
     - `PDF-Editor-Windows.exe` - Windows executable

### Manual Trigger

You can also trigger builds manually without creating a tag:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Build and Release** workflow
4. Click **Run workflow** button
5. Choose branch and click **Run workflow**

This builds executables but doesn't create a release (useful for testing).

## Local Building (Optional)

If you want to build locally instead of using GitHub Actions:

### Prerequisites

```bash
# Activate virtual environment
source .venv/bin/activate  # On Mac/Linux
# or
.venv\Scripts\activate  # On Windows

# Install PyInstaller
pip install pyinstaller
```

### Build Commands

**Using the spec file (recommended):**
```bash
pyinstaller PDF-Editor.spec
```

**Manual command (alternative):**
```bash
pyinstaller --name="PDF-Editor" \
            --windowed \
            --onefile \
            main.py
```

### Output Location

Built executables are in the `dist/` directory:
- **Linux**: `dist/PDF-Editor`
- **macOS**: `dist/PDF-Editor.app`
- **Windows**: `dist/PDF-Editor.exe`

## Understanding the Build Process

### Files Involved

1. **requirements.txt**: Lists Python dependencies
   - PyQt5==5.15.11
   - PyMuPDF==1.26.5

2. **PDF-Editor.spec**: PyInstaller configuration
   - Defines build settings
   - Specifies what to include/exclude
   - Platform-specific options

3. **.github/workflows/build-release.yml**: GitHub Actions workflow
   - Builds on 3 platforms in parallel
   - Creates release with executables
   - Triggers on version tags (v*)

### GitHub Actions Workflow Steps

1. **Checkout**: Gets the code from repository
2. **Setup Python**: Installs Python 3.9
3. **Install Dependencies**: Installs requirements + PyInstaller
4. **Build**: Runs PyInstaller on each platform
5. **Verify**: Checks that build succeeded
6. **Upload Artifacts**: Saves build output
7. **Create Release**: Publishes release with all executables (only on tags)

## Platform-Specific Notes

### macOS

**Built File**: `PDF-Editor.app` (application bundle)

**Distribution**: Tarball (`PDF-Editor-macOS.app.tar.gz`)

**User Installation**:
1. Download and extract the `.tar.gz` file
2. Drag `PDF-Editor.app` to Applications folder
3. First run: Right-click → Open (due to macOS Gatekeeper)

**Signing (Optional)**:
- For distribution outside personal use, you need an Apple Developer account ($99/year)
- Can sign and notarize the app to avoid Gatekeeper warnings

### Windows

**Built File**: `PDF-Editor.exe`

**User Installation**:
1. Download `PDF-Editor-Windows.exe`
2. Double-click to run
3. Windows Defender may show warning (click "More info" → "Run anyway")

**Code Signing (Optional)**:
- For professional distribution, purchase a code signing certificate
- Prevents SmartScreen warnings

### Linux

**Built File**: `PDF-Editor` (executable binary)

**User Installation**:
```bash
# Download the file
chmod +x PDF-Editor-Linux
./PDF-Editor-Linux
```

**Distribution Options**:
- Direct executable (current method)
- AppImage (more portable)
- .deb package (Debian/Ubuntu)
- .rpm package (Fedora/RedHat)

## File Sizes

Expect the following approximate sizes:
- **Linux**: 80-120 MB
- **macOS**: 100-150 MB (app bundle)
- **Windows**: 80-120 MB

Large sizes are normal due to PyQt5 and PyMuPDF bundling.

## Troubleshooting

### Build Fails on GitHub Actions

**Check the Actions log:**
1. Go to Actions tab in your repository
2. Click on the failed workflow run
3. Expand the failed step to see error messages

**Common issues:**
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Syntax errors in code

### "Module not found" error

Add missing modules to `hiddenimports` in `PDF-Editor.spec`:
```python
hiddenimports=[
    'PyQt5.QtPrintSupport',
    'your.missing.module',
],
```

### macOS "App is damaged" message

Users need to:
```bash
xattr -cr PDF-Editor.app
```
Or right-click → Open (first time only)

### Windows SmartScreen warning

This is normal for unsigned executables. Users can:
1. Click "More info"
2. Click "Run anyway"

To avoid this, purchase a code signing certificate.

## Version Numbering

Use semantic versioning for tags:
- `v1.0.0` - Major release
- `v1.1.0` - Minor update (new features)
- `v1.0.1` - Patch (bug fixes)

Examples:
```bash
git tag v1.0.0   # First release
git tag v1.1.0   # Added new feature
git tag v1.0.1   # Bug fix
```

## Advanced: Customizing the Build

### Adding an Icon

1. Create icons:
   - `icon.icns` for macOS
   - `icon.ico` for Windows
   - `icon.png` for Linux

2. Update `PDF-Editor.spec`:
   ```python
   exe = EXE(
       ...
       icon='icon.ico',  # or icon.icns
   )
   ```

3. Update GitHub workflow to include icon in different build steps

### Reducing File Size

Edit `PDF-Editor.spec`:
```python
a = Analysis(
    ...
    excludes=['tkinter', 'matplotlib', 'numpy'],  # Exclude unused modules
)
```

### Creating Installers

**Windows** - Use Inno Setup or NSIS:
- Wrap .exe in installer
- Add shortcuts, uninstaller

**macOS** - Use `create-dmg`:
- Create .dmg disk image
- Drag-and-drop installation

**Linux** - Use `fpm`:
- Create .deb or .rpm packages

## Support

For build issues:
- Check GitHub Actions logs
- Review PyInstaller documentation
- Check the issues page

## License

See main README.md for license information.
