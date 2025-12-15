# 🎨 Tezniti IA 3D Generator Pro

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![Kivy](https://img.shields.io/badge/Kivy-2.3%2B-orange)
![License](https://img.shields.io/badge/license-MIT-purple)

**مولّد النماذج ثلاثية الأبعاد المدعوم بالذكاء الاصطناعي**

*An AI-Powered 3D Model Generator with Natural Language Understanding*

</div>

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Features](#-features)
3. [Installation](#-installation)
4. [Quick Start](#-quick-start)
5. [Supported Model Types](#-supported-model-types)
6. [AI Bridge & NLP](#-ai-bridge--nlp)
7. [Architecture](#-architecture)
8. [User Interface Guide](#-user-interface-guide)
9. [API Reference](#-api-reference)
10. [Troubleshooting](#-troubleshooting)
11. [Contributing](#-contributing)

---

## 🌟 Overview

**Tezniti IA 3D Generator Pro** is an intelligent CAD-like application that generates parametric 3D models from natural language descriptions. It combines the power of:

- **Bayan Language Model**: For understanding Arabic, English, and French text descriptions
- **Trimesh**: For robust 3D mesh generation and manipulation
- **PyVista**: For high-quality off-screen rendering
- **Kivy**: For a modern, cross-platform user interface

The application is designed for engineers, designers, and makers who want to quickly prototype mechanical parts or furniture components without manual CAD modeling.

---

## ✨ Features

### 🧠 AI-Powered Understanding
- **Multilingual NLP**: Understands descriptions in Arabic (العربية), English, and French
- **Semantic Analysis**: Uses Bayan's Istinbat Engine for deep linguistic understanding
- **Parameter Extraction**: Automatically extracts dimensions from text (e.g., "diameter 50mm")

### 🔧 Mechanical Parts Library
- Gears (Spur, Helical, Bevel, Worm)
- Fasteners (Bolts, Nuts, Washers)
- Structural (Beams, Brackets, Flanges)
- Motion (Shafts, Bearings, Ball Screws, Lead Screws)
- Connectors (Hinges, Pipes, Housings)
- Springs and Pulleys

### 🪑 Furniture Components
- **Full Chair Assembly**: Complete chair with legs, seat, and backrest
- **Curved Panels**: Ergonomic S-curved backrests for CNC cutting
- **Table Tops**: Flat surfaces with optional corner rounding
- **Shelves and Plates**: Simple flat components

### 📐 Professional Output
- **STL Export**: Industry-standard format for 3D printing and CNC
- **PDF Reports**: Technical documentation with dimensions
- **Live Preview**: Real-time 3D visualization within the app
- **External Viewer Support**: Open in MeshLab, Blender, or F3D

### 🖌️ 2D Sketching
- Built-in sketch canvas for freehand drawing
- Image import for tracing
- Vision AI integration for sketch-to-3D (Baseera)

---

## 🛠️ Installation

### Prerequisites

```bash
# System dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libgl1-mesa-dev libgles2-mesa-dev xclip
```

### Python Environment

```bash
# Create virtual environment (recommended)
python3 -m venv tezniti_env
source tezniti_env/bin/activate

# Install dependencies
pip install kivy[base] numpy trimesh pyvista pillow reportlab plyer \
    langdetect deep_translator sentence-transformers
```

### Clone & Run

```bash
cd /path/to/bayan_python_ide22/tezniti_3d
python3 tezniti_3d.py
```

---

## 🚀 Quick Start

### Example 1: Generate a Spur Gear

```text
Generate a spur gear with 24 teeth, module 2.5mm, and face width 15mm.
Include a center bore of diameter 12mm.
```

### Example 2: Generate a Full Chair

```text
Object Name: Modern Wooden Chair
Description:
Generate a complete 3D model of a modern minimalist chair.
Assembly Features:
1. Four cylindrical legs (diameter 40mm).
2. Solid seat base (thickness 30mm).
3. Integrated S-curved backrest for ergonomic support.
Dimensions:
Seat Height: 450 mm
Seat Width: 450 mm
Seat Depth: 450 mm
Backrest Height: 500 mm
```

### Example 3: Generate a Chair Backrest Panel Only

```text
Object Name: Chair Backrest Panel
Description:
Generate a single curved backrest panel for a modern chair.
Geometric Features:
- Organic S-shaped curve from top to bottom.
- Wide at bottom, narrow at top.
- Thickness: 18mm (MDF).
```

---

## 📦 Supported Model Types

| Type | Keywords (EN) | Keywords (AR) | Description |
|------|---------------|---------------|-------------|
| `helical_gear` | helical gear, helix | ترس حلزوني | Helical gear with helix angle |
| `spur_gear` | spur gear, straight gear | ترس مستقيم | Standard spur gear |
| `bevel_gear` | bevel gear, conical | ترس مخروطي | Bevel/conical gear |
| `worm_gear` | worm gear, endless screw | ترس دودي | Worm gear mechanism |
| `nut` | nut, hex nut | صامولة | Hexagonal nut |
| `washer` | washer, rondelle | حلقة | Flat washer |
| `shaft` | shaft, axle | محور, عمود | Cylindrical shaft with optional keyway |
| `pipe` | pipe, tube | أنبوب | Hollow pipe |
| `flange` | flange, bride | فلنجة | Flange with bolt holes |
| `bearing` | bearing, roulement | محمل | Ball bearing (simplified) |
| `bolt` | bolt, screw | مسمار, برغي | Hex bolt |
| `hinge` | hinge, charnière | مفصلة | Door hinge |
| `bracket` | bracket, equerre | كتيفة | L-bracket |
| `beam` | beam, poutre, i-beam | عارضة | I-beam profile |
| `ball_screw` | ball screw | برغي كروي | Ball screw for linear motion |
| `lead_screw` | lead screw, vis mère | برغي قيادي | Lead screw |
| `housing` | housing, enclosure | غلاف | Hollow box enclosure |
| `spring` | spring, coil | نابض, زنبرك | Compression spring |
| `pulley` | pulley, poulie | بكرة | V-groove pulley |
| `rack_and_pinion` | rack, crémaillère | جريدة | Rack gear |
| `chair` | chair, modern chair | كرسي | **Full chair assembly** |
| `curved_panel` | backrest, curved panel | ظهر, لوحة منحنية | S-curved backrest panel |
| `plate` | plate, sheet | صفيحة | Flat plate |
| `table_top` | table top, surface | سطح طاولة | Table surface |
| `shelf` | shelf, étagère | رف | Simple shelf |

---

## 🧠 AI Bridge & NLP

The `ai_bridge.py` module provides the intelligence layer between natural language and 3D generation.

### Core Class: `TeznitiIntelligenceBridge`

```python
from ai_bridge import TeznitiIntelligenceBridge

bridge = TeznitiIntelligenceBridge()

# Understand a text request
result = bridge.understand_request("Generate a bolt with diameter 10mm and length 50mm")

print(result.equation_type)  # 'bolt'
print(result.parameters)     # {'diameter': 10, 'length': 50, ...}
print(result.confidence)     # 0.92
print(result.reasoning)      # 'Identified bolt/screw...'
```

### Output: `ShapeEquation` Dataclass

| Field | Type | Description |
|-------|------|-------------|
| `equation_type` | `str` | Model type (e.g., 'bolt', 'chair') |
| `parameters` | `dict` | Extracted dimensions and properties |
| `confidence` | `float` | 0.0 to 1.0 confidence score |
| `reasoning` | `str` | Human-readable explanation |

### Integration with Bayan Engine

The bridge attempts to connect to the real Bayan Istinbat Engine for:
- **Semantic concept extraction** (e.g., "strength" → material properties)
- **Arabic morphological analysis** via Arramooz dictionary
- **Multilingual embeddings** via `sentence-transformers`

If Bayan is unavailable, it falls back to keyword-based matching.

---

## 🏗️ Architecture

```
tezniti_3d/
├── tezniti_3d.py          # Main Kivy application (UI + Generation)
├── ai_bridge.py           # NLP and AI integration
├── renderer.py            # Isolated PyVista renderer (subprocess)
├── Amiri-Regular.ttf      # Arabic font
├── mechanical_keywords_5000.xlsx  # Keyword database
└── verify_tezniti_logic.py        # Test script
```

### Key Design Decisions

1. **Process Isolation for Rendering**
   - PyVista runs in a separate subprocess (`renderer.py`) to prevent OpenGL conflicts with Kivy.
   - The main app exports STL → calls renderer → loads PNG.

2. **Parametric Mesh Generation**
   - Uses `trimesh` for all geometry.
   - Boolean operations via `manifold3d` (if available) or fallback.

3. **AI Priority Logic**
   - Full assemblies ("chair") take precedence over parts ("backrest").
   - Explicit "part" keywords override assembly detection.

---

## 🖥️ User Interface Guide

### Main Interface Layout

```
┌─────────────────────────────────────────────────────────┐
│  🎨 TEZNITI IA 3D GENERATOR PRO                        │
├─────────────────────────────────────────────────────────┤
│  📝 Description de la Pièce    │  🎨 3D Viewport       │
│  ┌─────────────────────────┐   │  ┌─────────────────┐  │
│  │ [Text Input Area]       │   │  │ [3D Preview]    │  │
│  │ Enter description in    │   │  │                 │  │
│  │ Arabic, English, or FR  │   │  │                 │  │
│  └─────────────────────────┘   │  └─────────────────┘  │
│  ┌───────────┐ ┌───────────┐   │                       │
│  │ Generate  │ │ Sketch 2D │   │                       │
│  └───────────┘ └───────────┘   │                       │
│  ┌───────────┐ ┌───────────┐   │                       │
│  │Export STL │ │PDF Report │   │                       │
│  └───────────┘ └───────────┘   │                       │
│  ┌───────────┐ ┌───────────┐   │                       │
│  │External 3D│ │Copy Dims  │   │                       │
│  └───────────┘ └───────────┘   │                       │
├─────────────────────────────────────────────────────────┤
│  Status: ✅ Ready | جاهز                               │
└─────────────────────────────────────────────────────────┘
```

### Button Functions

| Button | Function |
|--------|----------|
| 🔧 توليد (Generate 3D) | Parse text and generate 3D model |
| ✏️ رسم (Sketch 2D) | Switch to 2D sketch mode |
| 📥 Import Image | Load image for tracing |
| 🗑️ مسح (Clear) | Clear sketch canvas |
| 💾 Export STL | Save model as STL file |
| 📄 PDF Report | Generate technical PDF |
| 🔍 عارض 3D خارجي | Open in external viewer |
| 📏 نسخ الأبعاد | Copy dimensions to clipboard |

---

## 📚 API Reference

### `TeznitiApp` (Main Application Class)

#### Key Methods

| Method | Description |
|--------|-------------|
| `generate_3d(instance)` | Main entry point for 3D generation |
| `parse_text(text) → dict` | Converts text to parameters via AI Bridge |
| `generate_model(params) → Trimesh` | Creates 3D mesh from parameters |
| `visualize_model()` | Renders preview via subprocess |
| `export_stl(instance)` | Saves current model to STL |
| `generate_pdf(instance)` | Creates technical PDF report |
| `open_3d_external_viewer()` | Opens model in system viewer |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `current_model` | `trimesh.Trimesh` | Active 3D mesh |
| `calculated_dimensions` | `dict` | Computed dimensions for display |
| `extracted_params` | `dict` | Parameters from last parse |
| `text_input` | `TextInput` | User input widget |
| `viewer_3d` | `Label` | 3D preview container |

### `generate_model(params)` Parameters

Common parameters across all model types:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | str | 'box' | Model type identifier |
| `diameter` | float | varies | Primary diameter (mm) |
| `length` / `height` | float | varies | Primary dimension (mm) |
| `width` | float | varies | Secondary dimension (mm) |
| `thickness` | float | varies | Material thickness (mm) |

---

## ❓ Troubleshooting

### Problem: Application Freezes on Linux

**Cause**: OpenGL context conflict between Kivy and PyVista.

**Solution**: This has been fixed by isolating PyVista in `renderer.py`. If issues persist:
```bash
export KIVY_GL_BACKEND=sdl2
python3 tezniti_3d.py
```

### Problem: Arabic Text Not Displaying

**Cause**: Missing Arabic font.

**Solution**: Ensure `Amiri-Regular.ttf` is in the same directory as `tezniti_3d.py`.

### Problem: "ModuleNotFoundError: No module named 'trimesh'"

**Solution**:
```bash
pip install trimesh[easy]
```

### Problem: PDF Export Fails

**Solution**:
```bash
pip install reportlab
```

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. **More Model Types**: Add support for springs with actual helix geometry, threads on bolts, etc.
2. **Dimension Extraction**: Improve regex patterns for extracting measurements from text.
3. **Sketch-to-3D**: Enhance Baseera Vision integration for automatic sketch interpretation.
4. **Material Properties**: Add density, weight calculations, and material selection.

---

## 📄 License

This project is part of the **Bayan Programming Language** ecosystem and is licensed under the MIT License.

---

<div align="center">

**Built with ❤️ by the Bayan Team**

*Powered by Bayan Istinbat Engine & Baseera Vision*

</div>
