"""Coconut Groove — Vector Engraving Pipeline.

Converts a raster image (PNG/JPG) into an SVG suitable for laser engraving
on a coconut.

Pipeline:
    1. Open input image (any common format).
    2. Convert to grayscale.
    3. Threshold to pure black & white (configurable threshold).
    4. Save as temporary PBM (potrace's required input format).
    5. Run potrace to produce an SVG.
    6. Clean up intermediates.

Usage:
    python vector_pipeline.py INPUT OUTPUT [--threshold N] [--invert]

Examples:
    python vector_pipeline.py logo.png logo.svg
    python vector_pipeline.py photo.jpg out.svg --threshold 140
    python vector_pipeline.py white_on_black.png out.svg --invert

Notes:
    - The output SVG is what gets imported into EZCAD as paths.
    - "Threshold" controls what becomes black vs white before tracing.
      Lower threshold = more becomes white (less detail). Higher = more black.
      Default 128 (middle gray) works for clean line art.
    - "--invert" handles white-on-black source images.
    - For best engraving results, feed this script clean line art with
      strong contrast. Photos won't vectorize well — use the raster pipeline
      (next phase) for those.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps


def check_potrace_available() -> None:
    """Fail fast with a clear message if potrace isn't on PATH."""
    if shutil.which("potrace") is None:
        sys.exit(
            "ERROR: potrace not found on PATH.\n"
            "Install from https://potrace.sourceforge.net/ and add to PATH."
        )


def rasterize_to_pbm(
    input_path: Path,
    pbm_path: Path,
    threshold: int,
    invert: bool,
) -> None:
    """Convert an input image to a 1-bit PBM file potrace can read."""
    img = Image.open(input_path)

    # If RGBA, flatten alpha against white background so transparent areas
    # don't become black after grayscale conversion.
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        img = bg

    gray = img.convert("L")

    if invert:
        gray = ImageOps.invert(gray)

    # Threshold to pure B&W. Pixels >= threshold become white (255),
    # below become black (0). Potrace traces the black regions.
    bw = gray.point(lambda p: 255 if p >= threshold else 0, mode="1")
    bw.save(pbm_path, format="PPM")  # mode "1" saves as PBM


def trace_to_svg(pbm_path: Path, svg_path: Path) -> None:
    """Run potrace on the PBM, producing an SVG."""
    result = subprocess.run(
        [
            "potrace",
            "--svg",
            "--output", str(svg_path),
            str(pbm_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"potrace failed:\n{result.stderr}")


def run_pipeline(
    input_path: Path,
    output_path: Path,
    threshold: int,
    invert: bool,
) -> None:
    check_potrace_available()

    if not input_path.exists():
        sys.exit(f"ERROR: input file not found: {input_path}")

    # Use a temp directory for the intermediate PBM so we don't litter.
    with tempfile.TemporaryDirectory() as tmpdir:
        pbm_path = Path(tmpdir) / "intermediate.pbm"
        rasterize_to_pbm(input_path, pbm_path, threshold, invert)
        trace_to_svg(pbm_path, output_path)

    print(f"OK -> {output_path}")
    print(f"     threshold={threshold}, invert={invert}")
    print("Open the SVG in a browser or vector editor to inspect.")
    print("Then import into EZCAD2 (File -> Import) to engrave.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a raster image to a vector SVG for laser engraving."
    )
    parser.add_argument("input", type=Path, help="Input image (PNG, JPG, etc.)")
    parser.add_argument("output", type=Path, help="Output SVG path")
    parser.add_argument(
        "--threshold",
        type=int,
        default=128,
        help="B&W threshold 0-255 (default 128). Higher = more black.",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Invert before tracing (use for white-on-black sources).",
    )
    args = parser.parse_args()
    run_pipeline(args.input, args.output, args.threshold, args.invert)


if __name__ == "__main__":
    main()
