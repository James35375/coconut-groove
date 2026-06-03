# Coconut Groove — Engraving Pipeline

Converts customer designs (AI-generated or uploaded) into laser-ready files
for engraving on coconuts.

## Phase 1A — Vector pipeline (this folder)

For clean line art and logos. Output is an SVG that EZCAD2 imports as paths.

### Setup (one time)

1. Install [potrace](https://potrace.sourceforge.net/) and ensure `potrace` is on your PATH.
2. From your venv: `pip install Pillow` (already in the project's `requirements.txt`).

### Usage

```powershell
# Activate the project venv first
.\venv\Scripts\Activate.ps1

# Basic: black-on-white logo
python pipeline\vector_pipeline.py logo.png logo.svg

# Adjust threshold for noisy or low-contrast images
python pipeline\vector_pipeline.py noisy.png out.svg --threshold 100

# White-on-black source
python pipeline\vector_pipeline.py white_text.png out.svg --invert
```

### What good input looks like

- **Strong contrast.** Pure black on pure white traces best.
- **Clean edges.** Anti-aliasing is fine; gradients are not.
- **Reasonable size.** Anywhere from 500–3000px wide. Too small and detail is lost; too big slows tracing.
- **Logos, icons, line art, single-color illustrations.** Not photos.

### What doesn't work here

Photos and grayscale images. Those need the **raster pipeline** (Phase 1A, part 2),
which dithers to a 1-bit BMP instead of vectorizing.

### How it fits with EZCAD2

1. Run the pipeline → get an SVG
2. Open EZCAD2 → `File → Import` → select the SVG
3. The design appears in the marking field as paths
4. Set pen parameters (speed, power, hatch fill for solid regions)
5. Frame with red light, focus on coconut, mark

### Test it out

A test image isn't included — grab any logo PNG or icon and run the script against it.
Open the resulting SVG in a browser to confirm it traced something sensible.
