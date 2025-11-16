# Logo Files

## Current File
- `Classk_Logo_FinalVersion_Illustrator.ai` - Adobe Illustrator source file (not web-compatible)

## Required Exports

To use the logo on the website, please export the `.ai` file to web-compatible formats:

1. **SVG** (recommended for vector scalability)
   - Export as: `logo.svg`
   - Format: SVG
   - Preserve vector paths for crisp scaling at any size

2. **PNG** (fallback for older browsers)
   - Export as: `logo.png`
   - Size: 512x512px or higher (for favicon and high-DPI displays)
   - Format: PNG with transparency

## Logo Usage

The logo is used in:
- **Navigation bar** (navbar) - Height: 36px
- **Login/Signup pages** - Size: 32x32px
- **Browser favicon** - 16x16px (will be generated from SVG/PNG)

## Fallback Behavior

If logo files are not found:
- Navbar: Falls back to text "Classk"
- Auth pages: Falls back to "C" letter in styled box

## File Structure After Export

```
static/images/
├── Classk_Logo_FinalVersion_Illustrator.ai (source file)
├── logo.svg (export this)
└── logo.png (export this)
```

