"""
CustomTkinter UI components for Scanify.
"""
import customtkinter as ctk
from typing import Callable, Optional
from config import (
    CARD_PADDING, CARD_CORNER_RADIUS, COLOR_CARD, COLOR_CARD_BORDER,
    COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_INPUT_BG, BUTTON_HEIGHT
)


class Card(ctk.CTkFrame):
    """A styled card container with clean borders."""

    def __init__(self, parent, title: str = "", **kwargs):
        super().__init__(
            parent,
            corner_radius=CARD_CORNER_RADIUS,
            fg_color=COLOR_CARD,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            **kwargs
        )

        if title:
            self.title_label = ctk.CTkLabel(
                self,
                text=title,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=COLOR_TEXT
            )
            self.title_label.pack(pady=(CARD_PADDING, CARD_PADDING-3), padx=CARD_PADDING, anchor="w")


class SliderCard(Card):
    """Ultra-compact slider card design."""

    def __init__(
        self,
        parent,
        label: str,
        min_val: float,
        max_val: float,
        step: float,
        default_val: float,
        command: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.command = command
        self.step = step

        # Single row: Label, Slider, Value
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="x", padx=CARD_PADDING, pady=CARD_PADDING)

        # Label (left)
        self.label = ctk.CTkLabel(
            content,
            text=label,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_TEXT,
            width=80,
            anchor="w"
        )
        self.label.pack(side="left", padx=(0, 8))

        # Slider (center, expandable)
        self.slider = ctk.CTkSlider(
            content,
            from_=min_val,
            to=max_val,
            number_of_steps=int((max_val - min_val) / step),
            command=self._on_slider_change,
            height=16
        )
        self.slider.set(default_val)
        self.slider.pack(side="left", fill="x", expand=True, padx=(0, 8))

        # Value (right)
        self.value_label = ctk.CTkLabel(
            content,
            text=self._format_value(default_val),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_TEXT_SECONDARY,
            width=50,
            anchor="e"
        )
        self.value_label.pack(side="right")

    def _format_value(self, value: float) -> str:
        """Format value for display."""
        if self.step >= 1:
            return f"{int(value)}"
        else:
            return f"{value:.2f}"

    def _on_slider_change(self, value: float):
        """Handle slider change."""
        # Round to step
        rounded = round(value / self.step) * self.step
        self.value_label.configure(text=self._format_value(rounded))
        if self.command:
            self.command(rounded)

    def get(self) -> float:
        """Get current slider value."""
        value = self.slider.get()
        return round(value / self.step) * self.step

    def set(self, value: float):
        """Set slider value."""
        self.slider.set(value)
        self.value_label.configure(text=self._format_value(value))


class FileQueueList(ctk.CTkTextbox):
    """A textbox for displaying file queue."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            font=ctk.CTkFont(size=11),
            wrap="none",
            fg_color=COLOR_INPUT_BG,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            text_color=COLOR_TEXT,
            **kwargs
        )
        self.configure(state="disabled")

    def update_files(self, files: list):
        """Update displayed file list."""
        self.configure(state="normal")
        self.delete("1.0", "end")

        if files:
            for i, file in enumerate(files, 1):
                self.insert("end", f"{i}. {file}\n")
        else:
            self.insert("end", "No files in queue")

        self.configure(state="disabled")


class ActivityLog(ctk.CTkTextbox):
    """A textbox for activity logging."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            font=ctk.CTkFont(size=10, family="Consolas"),
            wrap="word",
            fg_color=COLOR_INPUT_BG,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            text_color=COLOR_TEXT,
            **kwargs
        )
        self.configure(state="disabled")

    def log(self, message: str):
        """Add message to log."""
        self.configure(state="normal")
        self.insert("end", f"{message}\n")
        self.see("end")
        self.configure(state="disabled")

    def clear(self):
        """Clear log."""
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")
