"""
Preview window with zoom, pan, and navigation controls.
"""
import customtkinter as ctk
from PIL import Image, ImageTk
from config import COLOR_BG, COLOR_CARD, COLOR_BUTTON, COLOR_BUTTON_HOVER


class PreviewWindow(ctk.CTkToplevel):
    """Dedicated preview window with zoom and pan controls."""

    def __init__(self, parent, image: Image.Image, title: str = "Preview"):
        super().__init__(parent)

        self.title(title)
        self.geometry("900x700")
        self.configure(fg_color=COLOR_BG)

        # Make it light themed
        self.attributes('-topmost', False)

        # Image data
        self.original_image = image
        self.zoom_level = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        self.pan_x = 0
        self.pan_y = 0
        self.drag_start_x = 0
        self.drag_start_y = 0

        self._build_ui()
        self._display_image()

        # Bind events
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)

    def _build_ui(self):
        """Build preview window UI."""
        # Top toolbar
        toolbar = ctk.CTkFrame(self, fg_color=COLOR_CARD, height=50)
        toolbar.pack(fill="x", padx=10, pady=(10, 5))
        toolbar.pack_propagate(False)

        # Zoom controls
        zoom_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        zoom_frame.pack(side="left", padx=10)

        ctk.CTkLabel(
            zoom_frame,
            text="🔍 Zoom:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            zoom_frame,
            text="−",
            width=40,
            height=32,
            command=lambda: self._zoom(-0.2),
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=2)

        self.zoom_label = ctk.CTkLabel(
            zoom_frame,
            text="100%",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=70
        )
        self.zoom_label.pack(side="left", padx=8)

        ctk.CTkButton(
            zoom_frame,
            text="+",
            width=40,
            height=32,
            command=lambda: self._zoom(0.2),
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            zoom_frame,
            text="Fit",
            width=60,
            height=32,
            command=self._fit_to_window,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(10, 0))

        ctk.CTkButton(
            zoom_frame,
            text="100%",
            width=60,
            height=32,
            command=self._reset_zoom,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=5)

        # Info label
        ctk.CTkLabel(
            toolbar,
            text="💡 Use mouse wheel to zoom • Click and drag to pan",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(side="right", padx=10)

        # Canvas with scrollbars
        canvas_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Create canvas
        self.canvas = ctk.CTkCanvas(
            canvas_frame,
            bg="#e8e8e8",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

    def _display_image(self):
        """Display the image at current zoom level."""
        # Calculate new size
        new_width = int(self.original_image.width * self.zoom_level)
        new_height = int(self.original_image.height * self.zoom_level)

        # Resize image
        if self.zoom_level != 1.0:
            resample = Image.Resampling.LANCZOS if self.zoom_level < 1.0 else Image.Resampling.BICUBIC
            display_img = self.original_image.resize((new_width, new_height), resample)
        else:
            display_img = self.original_image

        # Convert to PhotoImage
        self.photo = ImageTk.PhotoImage(display_img)

        # Clear canvas and display
        self.canvas.delete("all")

        # Center image with pan offset
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        x = (canvas_width - new_width) // 2 + self.pan_x
        y = (canvas_height - new_height) // 2 + self.pan_y

        self.canvas.create_image(x, y, anchor="nw", image=self.photo)

        # Update zoom label
        self.zoom_label.configure(text=f"{int(self.zoom_level * 100)}%")

    def _zoom(self, delta: float):
        """Zoom in or out."""
        new_zoom = self.zoom_level + delta
        new_zoom = max(self.min_zoom, min(self.max_zoom, new_zoom))

        if new_zoom != self.zoom_level:
            self.zoom_level = new_zoom
            self._display_image()

    def _on_mousewheel(self, event):
        """Handle mouse wheel zoom."""
        delta = 0.1 if event.delta > 0 else -0.1
        self._zoom(delta)

    def _on_drag_start(self, event):
        """Start dragging."""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.canvas.config(cursor="fleur")

    def _on_drag_motion(self, event):
        """Handle drag motion."""
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        self.pan_x += dx
        self.pan_y += dy

        self.drag_start_x = event.x
        self.drag_start_y = event.y

        self._display_image()

    def _reset_zoom(self):
        """Reset to 100% zoom."""
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self._display_image()

    def _fit_to_window(self):
        """Fit image to window."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 100 or canvas_height < 100:
            return

        # Calculate zoom to fit
        width_ratio = (canvas_width - 40) / self.original_image.width
        height_ratio = (canvas_height - 40) / self.original_image.height

        self.zoom_level = min(width_ratio, height_ratio)
        self.zoom_level = max(self.min_zoom, min(self.max_zoom, self.zoom_level))

        self.pan_x = 0
        self.pan_y = 0
        self._display_image()
