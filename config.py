"""
Configuration and settings for Scanify.
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class EffectConfig:
    """Configuration for scan effects."""
    dpi: int = 72
    jpg_quality: int = 50
    lighting: float = 0.6
    tilt_randomness: float = 0.2
    wrinkles: float = 0.15
    shadows: float = 0.05
    warp: float = 0.3
    noise: float = 0.5
    paper_texture: float = 0.4
    page_edge: float = 0.02
    yellowness: float = 0.05  # New slider for yellow tint
    black_and_white: bool = False
    blank_metadata: bool = True

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'dpi': self.dpi,
            'jpg_quality': self.jpg_quality,
            'lighting': self.lighting,
            'tilt_randomness': self.tilt_randomness,
            'wrinkles': self.wrinkles,
            'shadows': self.shadows,
            'warp': self.warp,
            'noise': self.noise,
            'paper_texture': self.paper_texture,
            'page_edge': self.page_edge,
            'yellowness': self.yellowness,
            'black_and_white': self.black_and_white,
            'blank_metadata': self.blank_metadata
        }


# UI Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850
CARD_PADDING = 12
CARD_CORNER_RADIUS = 0
BUTTON_HEIGHT = 32  # Keep height, but buttons will be boxy
SECTION_SPACING = 8
TOP_BAR_HEIGHT = 70

COLOR_BG = "#f6f6f6"  # Slightly more matte
COLOR_CARD = "#fdfdfd"  # Matte white
COLOR_CARD_BORDER = "#d1d1d1"  # Flat, subtle border
COLOR_BUTTON = "#4a90e2"  # Flat blue
COLOR_BUTTON_HOVER = "#357abd"  # Flat hover
COLOR_BUTTON_SECONDARY = "#7a7a7a"  # Flat gray
COLOR_BUTTON_SUCCESS = "#28a745"  # Flat green
COLOR_TEXT = "#222222"  # Flat dark
COLOR_TEXT_SECONDARY = "#7a7a7a"  # Flat secondary
COLOR_ACCENT = "#4a90e2"
COLOR_INPUT_BG = "#f4f4f4"  # Matte input
COLOR_BORDER = "#cccccc"  # Flat border

# Slider Ranges
SLIDER_RANGES = {
    'dpi': (50, 150, 10),  # Lower minimum for more degradation
    'jpg_quality': (20, 100, 10),  # Lower minimum for more compression artifacts
    'lighting': (0, 1, 0.05),
    'tilt_randomness': (0, 1, 0.05),
    'wrinkles': (0, 1, 0.05),
    'shadows': (0, 1, 0.05),
    'warp': (0, 1, 0.05),
    'noise': (0, 1, 0.05),
    'paper_texture': (0, 1, 0.05),
    'page_edge': (0, 1, 0.05),
    'yellowness': (0, 1, 0.05),
}

# Processing Constants
MAX_PREVIEW_DIMENSION = 2200
QUEUE_HEIGHT = 220
PREVIEW_HEIGHT = 280
ACTIVITY_HEIGHT = 220
SLIDER_CARD_HEIGHT = 60
