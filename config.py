"""
Configuration and settings for Scanify.
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class EffectConfig:
    """Configuration for scan effects."""
    dpi: int = 100
    jpg_quality: int = 50
    lighting: float = 0.3
    tilt_randomness: float = 0.55
    wrinkles: float = 0.6
    shadows: float = 0.45
    warp: float = 0.25
    noise: float = 0.75
    paper_texture: float = 0.70
    page_edge: float = 0.1
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
            'black_and_white': self.black_and_white,
            'blank_metadata': self.blank_metadata
        }


# UI Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850
CARD_PADDING = 12
CARD_CORNER_RADIUS = 8
BUTTON_HEIGHT = 32
SECTION_SPACING = 8
TOP_BAR_HEIGHT = 70

# Color Scheme - Clean Light Theme
COLOR_BG = "#f5f5f5"
COLOR_CARD = "#ffffff"
COLOR_CARD_BORDER = "#e0e0e0"
COLOR_BUTTON = "#4a90e2"
COLOR_BUTTON_HOVER = "#357abd"
COLOR_BUTTON_SECONDARY = "#6c757d"
COLOR_BUTTON_SUCCESS = "#28a745"
COLOR_TEXT = "#2c3e50"
COLOR_TEXT_SECONDARY = "#6c757d"
COLOR_ACCENT = "#4a90e2"
COLOR_INPUT_BG = "#f8f9fa"
COLOR_BORDER = "#dee2e6"

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
}

# Processing Constants
MAX_PREVIEW_DIMENSION = 2200
QUEUE_HEIGHT = 220
PREVIEW_HEIGHT = 280
ACTIVITY_HEIGHT = 220
SLIDER_CARD_HEIGHT = 60
