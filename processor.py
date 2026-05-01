"""
CyberLens — Core Image Processing Backend
==========================================
Converts any photo into a black-and-neon stylized image
with optional pixelation for a retro/cyber art look.

Pipeline:
  1. Grayscale conversion
  2. Binary thresholding (high contrast)
  3. Color swap  (white pixels → chosen neon color)
  4. Pixelation  (shrink + nearest-neighbor blow-up)
"""

import cv2
import numpy as np


# ── Preset neon colours (BGR order for OpenCV) ──────────────────────────
COLOR_PRESETS: dict[str, tuple[int, int, int]] = {
    "Neon Green":  (20, 255, 57),    # RGB [57, 255, 20]  → BGR
    "Cyan":        (255, 255, 0),     # RGB [0, 255, 255]  → BGR
    "Light Pink":  (203, 192, 255),   # RGB [255, 192, 203] → BGR
    "Hot Pink":    (180, 105, 255),   # RGB [255, 105, 180] → BGR
    "Electric Blue": (255, 191, 0),   # RGB [0, 191, 255]  → BGR
    "Vivid Yellow":  (0, 255, 255),   # RGB [255, 255, 0]  → BGR
}


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Step 1 — Convert a BGR image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_threshold(gray: np.ndarray, thresh_value: int = 127) -> np.ndarray:
    """
    Step 2 — Binary threshold.
    Pixels darker than `thresh_value` become 0 (black),
    pixels lighter become 255 (white).
    """
    _, binary = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
    return binary


def swap_color(binary: np.ndarray, color_bgr: tuple[int, int, int]) -> np.ndarray:
    """
    Step 3 — Replace every white pixel with the chosen neon colour.
    Input  : single-channel binary image (0 or 255).
    Output : 3-channel BGR image (black + neon colour).
    """
    # Create a 3-channel black image
    h, w = binary.shape
    colored = np.zeros((h, w, 3), dtype=np.uint8)

    # Boolean mask: where the binary image is white
    white_mask = binary == 255

    # Set those pixels to the target colour
    colored[white_mask] = color_bgr

    return colored


def pixelate(image: np.ndarray, pixel_size: int = 1) -> np.ndarray:
    """
    Step 4 — Pixelation via nearest-neighbor interpolation.
    `pixel_size` controls the blockiness:
      - 1  = no pixelation (original resolution)
      - 2+ = increasingly chunky pixels
    """
    if pixel_size <= 1:
        return image

    h, w = image.shape[:2]

    # Shrink down
    small_w = max(1, w // pixel_size)
    small_h = max(1, h // pixel_size)
    small = cv2.resize(image, (small_w, small_h), interpolation=cv2.INTER_NEAREST)

    # Blow back up — nearest-neighbor keeps the hard pixel edges
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    return pixelated


def process_image(
    image: np.ndarray,
    color_name: str = "Neon Green",
    threshold: int = 127,
    pixel_size: int = 1,
) -> np.ndarray:
    """
    Full pipeline: grayscale → threshold → colour swap → pixelate.
    Returns a BGR image ready to display or save.
    """
    gray = to_grayscale(image)
    binary = apply_threshold(gray, threshold)
    colored = swap_color(binary, COLOR_PRESETS[color_name])
    result = pixelate(colored, pixel_size)
    return result
