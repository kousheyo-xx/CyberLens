"""
Quick test script for the CyberLens backend.
Usage:
    python test_backend.py <path_to_image>

It will:
  - Load the image
  - Run each processing step individually and save intermediate results
  - Run the full pipeline and save the final result
  - All outputs go into an 'output/' folder beside this script
"""

import sys
import os
import cv2
from processor import (
    to_grayscale,
    apply_threshold,
    swap_color,
    pixelate,
    process_image,
    COLOR_PRESETS,
)


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_backend.py <image_path>")
        sys.exit(1)

    img_path = sys.argv[1]
    if not os.path.isfile(img_path):
        print(f"Error: File not found - {img_path}")
        sys.exit(1)

    # Load
    image = cv2.imread(img_path)
    if image is None:
        print(f"Error: Could not read image - {img_path}")
        sys.exit(1)

    print(f"Loaded image: {img_path}  |  Shape: {image.shape}")

    # Create output directory
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)

    # ── Step 1: Grayscale ────────────────────────────────────────────
    gray = to_grayscale(image)
    cv2.imwrite(os.path.join(out_dir, "1_grayscale.png"), gray)
    print("[OK] Step 1 - Grayscale saved")

    # ── Step 2: Threshold ────────────────────────────────────────────
    binary = apply_threshold(gray, thresh_value=127)
    cv2.imwrite(os.path.join(out_dir, "2_threshold.png"), binary)
    print("[OK] Step 2 - Threshold saved")

    # ── Step 3: Color swap (one per preset) ──────────────────────────
    for name, bgr in COLOR_PRESETS.items():
        colored = swap_color(binary, bgr)
        safe_name = name.lower().replace(" ", "_")
        cv2.imwrite(os.path.join(out_dir, f"3_color_{safe_name}.png"), colored)
        print(f"[OK] Step 3 - Color swap ({name}) saved")

    # ── Step 4: Pixelation at different levels ───────────────────────
    neon_green = swap_color(binary, COLOR_PRESETS["Neon Green"])
    for px in [4, 8, 16]:
        pix = pixelate(neon_green, pixel_size=px)
        cv2.imwrite(os.path.join(out_dir, f"4_pixelated_{px}px.png"), pix)
        print(f"[OK] Step 4 - Pixelated (block size {px}) saved")

    # ── Full pipeline ────────────────────────────────────────────────
    final = process_image(image, color_name="Neon Green", threshold=127, pixel_size=8)
    cv2.imwrite(os.path.join(out_dir, "5_final_pipeline.png"), final)
    print("[OK] Full pipeline result saved")

    print(f"\nAll outputs written to: {out_dir}")


if __name__ == "__main__":
    main()
