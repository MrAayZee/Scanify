# PDF2Scan 📄 ✨

A professional desktop application to convert PDFs into realistic scanned documents with customizable effects. Built with Python and CustomTkinter with a clean, modern **light theme** interface.

![PDF2Scan](https://img.shields.io/badge/Python-3.8+-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

> **⚠️ IMPORTANT**: Before uploading to GitHub, update the `GITHUB_REPO` variable in `pdf2scan.py` (line ~26) with your GitHub username:
>
> ```python
> GITHUB_REPO = "yourusername/PDF2Scan"  # Change this!
> ```

## ✨ Features

### Core Functionality

- 🎯 **Drag & Drop Support** - Simply drag PDF files into the application
- 🖼️ **Live Preview** - Preview first page with all effects applied
- 📦 **Batch Processing** - Convert multiple PDFs at once
- 📊 **Real-time Progress** - Track conversion progress with detailed activity log
- 🎨 **Black & White Mode** - True monochrome with adaptive thresholding
- 🔄 **Auto-Update Check** - Automatic update notifications on startup
- ℹ️ **About Dialog** - View app info, version, and access GitHub repository

### Realistic Scan Effects

- 💡 **Lighting Gradient** - Subtle lighting variations like real scanners
- 📐 **Tilt Randomness** - Slight page rotation for authentic look
- 📄 **Wrinkles** - Paper texture distortion
- 🌑 **Shadows** - Realistic shadow effects
- 🔄 **Warp** - Document warping simulation
- ⚡ **Noise** - Scanner noise simulation
- 🎨 **Paper Texture** - Realistic paper grain
- 🖼️ **Page Edge** - Optional page border/rim effect
- 📐 **Adjustable DPI** - 70-300 DPI output
- 📊 **JPG Quality** - 40-100% quality control

### Smart Features

- 🤖 **Auto Output Directory** - Automatically uses source PDF folder
- 📝 **Blank Metadata** - Remove PDF metadata for privacy
- 🔍 **Preview Optimization** - Fast preview with intelligent downscaling
- 💾 **Smart Naming** - Automatic file naming with conflict resolution
- 🎯 **Performance Optimized** - Efficient processing for multi-page PDFs

## 🖥️ Interface - Clean Light Theme

### Modern Design

- **Left Panel**: Main controls (Files, Queue, Preview, Activity Log, Output, Actions)
- **Right Panel**: Two columns of effect sliders with real-time value display
- **Organized Layout**: Cards with clear sections, subtle borders, and visual hierarchy
- **Professional Look**: Flat, clean design with light background and accent colors

### Layout Structure

```
┌─────────────────────────────────┬──────────────────────────┐
│ 📁 Files                        │ 📐 DPI    │ 📊 Quality   │
│ ├─ Browse/Remove/Clear All      │ 💡 Light  │ 📐 Tilt      │
│ └─ Drag & drop hint             │ 📄 Wrinkle│ 🌑 Shadows   │
│                                 │ 🔄 Warp   │ ⚡ Noise     │
│ 📋 Queue (150px)                │ 🎨 Texture│ 🖼️ Edge      │
│                                 │           │              │
│ ┌──────────────┬──────────────┐ │  Each slider shows:    │
│ │🖼️ Preview     │📝 Activity   │ │  - Label with icon     │
│ │  (350px)     │  Log (350px) │ │  - Current value       │
│ │              │              │ │  - Slider control      │
│ └──────────────┴──────────────┘ │                          │
│                                 │                          │
│ 📂 Output Directory             │                          │
│ ├─ Auto (use first PDF folder) │                          │
│ └─ Path / Browse / Open Folder  │                          │
│                                 │                          │
│ ⚙️ Modes & Actions               │                          │
│ ├─ BW Mode  │ 🔍 Preview First  │                          │
│ ├─ Metadata │ ✨ Convert PDFs   │                          │
│ └─ ════════ Progress Bar ══════ │                          │
└─────────────────────────────────┴──────────────────────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download

```bash
git clone https://github.com/yourusername/PDF2Scan.git
cd PDF2Scan
```

> **Note**: Replace `yourusername` with the actual GitHub username

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Update GitHub Repository (Important!)

Before running, edit `pdf2scan.py` and update the GitHub repository info:

```python
# Line ~26 in pdf2scan.py
GITHUB_REPO = "yourusername/PDF2Scan"  # Replace with your actual GitHub username
```

This enables the auto-update checker to work correctly.

## 🚀 Usage

### Running the Application

```bash
python pdf2scan.py
```

### Quick Start Guide

1. **Add PDF Files**

   - Click "Browse Files" or drag & drop PDFs
   - Files appear in the Queue section

2. **Adjust Effects**

   - Use the 10 sliders on the right to customize scan effects
   - Values update in real-time next to each slider
   - Each slider has an icon and clear label

3. **Preview Results**

   - Click "🔍 Preview First Page" to see the effect
   - Preview appears in the left panel
   - Preview is optimized for speed

4. **Configure Output**

   - Enable "Auto" to use source PDF's folder
   - Or click "Browse" to select custom output directory
   - Click "Open Folder" to view output location

5. **Convert**

   - Toggle "Black & White Mode" if needed
   - Enable "Blank metadata" for privacy
   - Click "✨ Convert PDFs" to start processing
   - Monitor progress bar and activity log

6. **Updates & Info**
   - Click "🔄 Check Updates" to manually check for new versions
   - Click "ℹ️ About" to view app info and version
   - App automatically checks for updates on startup

### Effect Slider Reference

| Slider                 | Range  | Step | Description                                        |
| ---------------------- | ------ | ---- | -------------------------------------------------- |
| **📐 DPI**             | 70-300 | 10   | Output resolution (higher = larger files, sharper) |
| **📊 JPG Quality**     | 40-100 | 10   | JPEG compression (higher = better quality)         |
| **💡 Lighting**        | 0-1    | 0.05 | Subtle lighting gradient intensity                 |
| **📐 Tilt Randomness** | 0-1    | 0.05 | Random page rotation amount                        |
| **📄 Wrinkles**        | 0-1    | 0.05 | Paper distortion/crease strength                   |
| **🌑 Shadows**         | 0-1    | 0.05 | Corner shadow effect intensity                     |
| **🔄 Warp**            | 0-1    | 0.05 | Document curve/warp amount                         |
| **⚡ Noise**           | 0-1    | 0.05 | Scanner noise/grain level                          |
| **🎨 Paper Texture**   | 0-1    | 0.05 | Paper surface texture visibility                   |
| **🖼️ Page Edge**       | 0-1    | 0.05 | Border/rim darkening strength                      |

### Recommended Settings by Use Case

**📄 Standard Documents**

- DPI: 150 | Quality: 85
- Lighting: 0.3 | Tilt: 0.2 | Wrinkles: 0.25
- Shadows: 0.4 | Warp: 0.2 | Noise: 0.15
- Texture: 0.25 | Edge: 0.3

**🧾 Receipts/Bills**

- DPI: 100-120 | Quality: 75
- B&W Mode: ON
- Higher Noise: 0.4-0.5
- All other effects: 0.3-0.5

**📋 Forms/Applications**

- DPI: 200 | Quality: 90
- Low effects: 0.1-0.2
- Keep text readable

**📸 Photo Documents**

- DPI: 200+ | Quality: 95
- Minimal effects: 0.1-0.2
- Preserve image quality

## 🛠️ Technical Details

### Project Structure

```
PDF2Scan/
├── pdf2scan.py        # Main application (entry point) ⭐
├── config.py          # Configuration, colors, constants
├── ui_components.py   # Custom widgets (Card, Slider, Log)
├── effects.py         # Scan effect implementations
├── pdf_processor.py   # PDF I/O and processing logic
├── requirements.txt   # Python dependencies
└── README.md         # This documentation
```

### Dependencies

```
customtkinter==5.2.2      # Modern UI framework
pillow>=10.0.0            # Image processing
pymupdf>=1.23.0           # PDF rendering and creation
numpy>=1.24.0             # Numerical operations
opencv-python>=4.8.0      # Advanced B&W thresholding
tkinterdnd2>=0.3.0        # Drag and drop support
```

### Effect Processing Pipeline

1. **Page Rendering** - PyMuPDF renders PDF page to image
2. **Scaling** - Downscale to ~2200px max dimension for performance
3. **Color Mode** - Apply B&W adaptive threshold if enabled
4. **Warp Effect** - Wave distortion for page curvature
5. **Lighting** - Radial gradient overlay from random point
6. **Wrinkles** - Random line patterns with Gaussian blur
7. **Paper Texture** - Grain simulation overlay
8. **Shadows** - Corner shadows with soft gradients
9. **Page Edge** - Border darkening effect
10. **Noise** - Gaussian noise for scanner artifacts
11. **Upscaling** - Scale back to target DPI dimensions
12. **PDF Insertion** - Create new PDF with processed images

### Performance Optimization

- **Multi-threading**: UI remains responsive during conversion
- **Smart Scaling**: Process at reduced size, upscale after effects
- **Preview Caching**: Single-page preview for quick feedback
- **Efficient Blending**: NumPy array operations for speed
- **Batch Processing**: All pages in one operation per PDF

### File Naming Convention

- Output: `original_scanned.pdf`
- Conflict handling: `original_scanned2.pdf`, `original_scanned3.pdf`, etc.
- Preserves original filename structure
- Saves to output directory (manual or auto)

## 🎨 Customization

### Change Light Theme Colors

Edit `config.py`:

```python
# Background and cards
COLOR_BG = "#f5f5f5"              # Main background (light gray)
COLOR_CARD = "#ffffff"             # Card background (white)
COLOR_CARD_BORDER = "#e0e0e0"     # Card borders (light)

# Buttons
COLOR_BUTTON = "#4a90e2"           # Primary button (blue)
COLOR_BUTTON_HOVER = "#357abd"     # Hover state (darker blue)
COLOR_BUTTON_SECONDARY = "#6c757d" # Secondary buttons (gray)
COLOR_BUTTON_SUCCESS = "#28a745"   # Convert button (green)

# Text
COLOR_TEXT = "#2c3e50"             # Main text (dark)
COLOR_TEXT_SECONDARY = "#6c757d"   # Secondary text (gray)

# Inputs
COLOR_INPUT_BG = "#f8f9fa"         # Input backgrounds
COLOR_BORDER = "#dee2e6"           # Input borders
```

### Adjust Default Effect Values

Edit `config.py` in the `EffectConfig` dataclass:

```python
@dataclass
class EffectConfig:
    dpi: int = 150              # Change default DPI
    jpg_quality: int = 85       # Change default quality
    lighting: float = 0.3       # Adjust lighting
    tilt_randomness: float = 0.2
    wrinkles: float = 0.3
    shadows: float = 0.4
    warp: float = 0.2
    noise: float = 0.15
    paper_texture: float = 0.25
    page_edge: float = 0.3
    # ... modify any defaults
```

### Change Slider Ranges

Edit `SLIDER_RANGES` dictionary in `config.py`:

```python
SLIDER_RANGES = {
    'dpi': (50, 400, 10),       # (min, max, step)
    'jpg_quality': (30, 100, 5),
    'lighting': (0, 1, 0.1),    # Larger steps
    # ... modify ranges as needed
}
```

### Modify Layout Dimensions

Edit constants in `config.py`:

```python
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 950
CARD_PADDING = 15
SECTION_SPACING = 12
QUEUE_HEIGHT = 150
PREVIEW_HEIGHT = 350
ACTIVITY_HEIGHT = 350
```

## � Updates & Releases

### How Updates Work

- The app automatically checks GitHub for new releases on startup
- You'll get a notification if a new version is available
- Manual check available via "🔄 Check Updates" button
- No data is collected - just a simple version comparison

### Creating Releases (For Maintainers)

1. Update `VERSION` in `pdf2scan.py`
2. Commit and push changes
3. Create a new release on GitHub:
   ```bash
   git tag -a v1.0.1 -m "Release v1.0.1"
   git push origin v1.0.1
   ```
4. Create release on GitHub with tag `v1.0.1`
5. Users will be notified automatically

## �🐛 Troubleshooting

### Update Check Fails

- ✓ Check internet connection
- ✓ Verify `GITHUB_REPO` is set correctly in `pdf2scan.py`
- ✓ Ensure GitHub repository is public
- ✓ Check if repository has any releases

### Application Won't Start

**Check Python version:**

```bash
python --version  # Should be 3.8 or higher
```

**Reinstall dependencies:**

```bash
pip install -r requirements.txt --force-reinstall
```

### Import Errors

**Missing CustomTkinter:**

```bash
pip install customtkinter --upgrade
```

**Missing tkinterdnd2:**

```bash
pip install tkinterdnd2
```

**All dependencies:**

```bash
pip install customtkinter pillow pymupdf numpy opencv-python tkinterdnd2
```

### Preview Not Displaying

- ✓ Ensure PDF file is valid and not corrupted
- ✓ Check if file path contains special characters
- ✓ Try a different, simple PDF file
- ✓ Verify PIL/Pillow is correctly installed

### Conversion Fails

- ✓ Verify output directory exists and is writable
- ✓ Check available disk space
- ✓ Ensure PDFs aren't password-protected
- ✓ Check Activity Log for specific error messages

### Black & White Mode Issues

**OpenCV not available** - B&W will use fallback:

```bash
pip install opencv-python
```

**Fallback mode** works but adaptive thresholding requires OpenCV for best results.

### Performance Issues

- Lower DPI for faster processing (100-150)
- Reduce effect intensity values
- Process fewer PDFs at once
- Close other applications

### Drag & Drop Not Working

- Ensure tkinterdnd2 is installed
- Try restarting the application
- Use "Browse Files" button as alternative

## � Building for Distribution

### Windows Installer

See `build_complete.py` for creating a Windows installer with Inno Setup:

```bash
# Install dependencies
pip install pyinstaller

# Build standalone executable + installer
python build_complete.py
```

This creates:

- Standalone `.exe` in `dist/`
- Professional installer in `installer_output/`
- Portable ZIP package

For detailed instructions, see the comments in `build_complete.py` and `installer.iss`.

## �📝 License

MIT License - Free for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

### Potential Enhancements

- [x] **Auto-Update**: Check GitHub for new versions ✅
- [x] **About Dialog**: App information and links ✅
- [ ] **Effect Presets**: One-click presets (Receipt, Form, Photo)
- [ ] **Batch Templates**: Save/load slider configurations
- [ ] **Advanced B&W**: More thresholding algorithms
- [ ] **Paper Colors**: Custom paper background colors
- [ ] **Watermarks**: Add text/image watermarks
- [ ] **OCR Integration**: Extract text from PDFs
- [ ] **Encryption**: Password-protect output PDFs
- [ ] **Multi-threading**: Parallel page processing
- [ ] **Preview All**: Gallery view of all pages
- [ ] **Undo/Redo**: Effect history management

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📧 Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check existing issues or start a discussion
- **Feature Requests**: Open an issue with [Feature] tag

## 🙏 Acknowledgments

- **CustomTkinter** - Modern, customizable UI framework
- **PyMuPDF** - Fast and powerful PDF processing
- **Pillow** - The Python Imaging Library
- **OpenCV** - Advanced image processing capabilities
- **NumPy** - Numerical computing foundation

## 📸 Screenshots

### Main Interface

Clean light theme with organized card layout, clear sections, and intuitive controls.

### Slider Panel

Two columns of effect sliders with real-time value display and icon labels.

### Processing

Live activity log shows conversion progress with detailed messages and progress bar.

---

## 📦 Publishing to GitHub

### First Time Setup

1. Create a new repository on GitHub named `PDF2Scan`
2. **Important**: Update `GITHUB_REPO` in `pdf2scan.py`:
   ```python
   GITHUB_REPO = "yourusername/PDF2Scan"
   ```
3. Initialize and push:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - PDF2Scan v1.0.0"
   git branch -M main
   git remote add origin https://github.com/yourusername/PDF2Scan.git
   git push -u origin main
   ```

### Creating Your First Release

1. On GitHub, go to your repository
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Title: `PDF2Scan v1.0.0`
5. Description: Add release notes
6. Publish release

Now the auto-update feature will work!

---

**Made with ❤️ using Python and CustomTkinter**

**Version 1.0.0** - Clean Light Theme Edition with Auto-Updates
