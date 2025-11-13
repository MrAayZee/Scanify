"""
PDF2Scan - Desktop PDF to Scanned Document Converter
Main application with CustomTkinter UI - Modern Compact Layout
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from pathlib import Path
from PIL import Image, ImageTk
import tkinterdnd2 as tkdnd
import sys
import webbrowser
import urllib.request
import json
from datetime import datetime

from config import (
    EffectConfig, WINDOW_WIDTH, WINDOW_HEIGHT, CARD_PADDING, SECTION_SPACING,
    SLIDER_RANGES, QUEUE_HEIGHT, PREVIEW_HEIGHT, ACTIVITY_HEIGHT, BUTTON_HEIGHT,
    COLOR_BG, COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_BUTTON_SECONDARY,
    COLOR_BUTTON_SUCCESS, COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_CARD, TOP_BAR_HEIGHT
)
from ui_components import Card, SliderCard, FileQueueList, ActivityLog
from pdf_processor import PDFProcessor
from preview_window import PreviewWindow

# Version info
VERSION = "1.0.0"
GITHUB_REPO = "MrAayZee/Scanify"
UPDATE_CHECK_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


class PDF2ScanApp(ctk.CTk, tkdnd.TkinterDnD.DnDWrapper):
    """Main application class."""

    def __init__(self):
        super().__init__()

        # Initialize DnD
        self.TkdndVersion = tkdnd.TkinterDnD._require(self)

        # Window setup
        self.title("PDF2Scan - Convert PDFs to Scanned Documents")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(fg_color=COLOR_BG)

        # Fix Windows dark title bar - force light theme
        if sys.platform == "win32":
            try:
                import ctypes
                # DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
                value = ctypes.c_int(0)  # 0 = light, 1 = dark
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 20, ctypes.byref(value), ctypes.sizeof(value)
                )
            except:
                pass

        # Set appearance - LIGHT THEME
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Initialize processor
        self.processor = PDFProcessor()
        self.config = EffectConfig()

        # UI state
        self.auto_output = ctk.BooleanVar(value=True)
        self.output_dir = ctk.StringVar(value="")
        self.preview_image = None
        self.is_processing = False

        # Build UI
        self._build_ui()

        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Check for updates in background
        threading.Thread(target=self._check_for_updates, daemon=True).start()

    def _build_ui(self):
        """Build modern compact layout."""
        # Main container (no scrolling for cleaner look)
        main_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === TOP BAR: File Controls + Output + Actions ===
        self._build_top_bar(main_frame)

        # === MIDDLE SECTION: Split into left and right ===
        middle_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        middle_frame.pack(fill="both", expand=True, pady=(SECTION_SPACING, 0))

        # Left panel - Queue, Buttons, Activity
        left_panel = ctk.CTkFrame(middle_frame, fg_color="transparent")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, SECTION_SPACING))

        # Right panel - Effect sliders (2 columns)
        right_panel = ctk.CTkFrame(middle_frame, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew")

        # Configure grid
        middle_frame.grid_columnconfigure(0, weight=2, minsize=400)
        middle_frame.grid_columnconfigure(1, weight=3, minsize=650)
        middle_frame.grid_rowconfigure(0, weight=1)

        # Build sections
        self._build_left_panel(left_panel)
        self._build_right_sliders(right_panel)

    def _build_top_bar(self, parent):
        """Build compact top bar with all file/output/action controls."""
        top_bar = Card(parent)
        top_bar.pack(fill="x", pady=(0, SECTION_SPACING))

        content = ctk.CTkFrame(top_bar, fg_color="transparent")
        content.pack(fill="x", padx=CARD_PADDING, pady=CARD_PADDING)

        # === ROW 1: File Controls ===
        row1 = ctk.CTkFrame(content, fg_color="transparent")
        row1.pack(fill="x", pady=(0, SECTION_SPACING))

        ctk.CTkLabel(
            row1,
            text="📁 Files:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=(0, 10))

        self.browse_btn = ctk.CTkButton(
            row1, text="Browse", command=self._browse_files,
            width=90, height=BUTTON_HEIGHT, fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER, font=ctk.CTkFont(size=12)
        )
        self.browse_btn.pack(side="left", padx=(0, 5))

        self.remove_btn = ctk.CTkButton(
            row1, text="Remove", command=self._remove_selected,
            width=80, height=BUTTON_HEIGHT, fg_color=COLOR_BUTTON_SECONDARY,
            hover_color="#5a6268", font=ctk.CTkFont(size=12)
        )
        self.remove_btn.pack(side="left", padx=(0, 5))

        self.clear_btn = ctk.CTkButton(
            row1, text="Clear", command=self._clear_files,
            width=70, height=BUTTON_HEIGHT, fg_color=COLOR_BUTTON_SECONDARY,
            hover_color="#5a6268", font=ctk.CTkFont(size=12)
        )
        self.clear_btn.pack(side="left", padx=(0, 20))

        # Drag and drop hint
        ctk.CTkLabel(
            row1,
            text="💡 Drag & drop PDFs anywhere",
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXT_SECONDARY
        ).pack(side="left")

        # Help and About buttons (right side)
        self.about_btn = ctk.CTkButton(
            row1, text="ℹ️ About", command=self._show_about,
            width=90, height=BUTTON_HEIGHT, fg_color=COLOR_BUTTON_SECONDARY,
            hover_color="#5a6268", font=ctk.CTkFont(size=12)
        )
        self.about_btn.pack(side="right", padx=(5, 0))

        self.update_btn = ctk.CTkButton(
            row1, text="🔄 Check Updates", command=self._check_updates_manual,
            width=130, height=BUTTON_HEIGHT, fg_color=COLOR_BUTTON_SECONDARY,
            hover_color="#5a6268", font=ctk.CTkFont(size=12)
        )
        self.update_btn.pack(side="right")

        # Enable drag and drop on top bar
        top_bar.drop_target_register(tkdnd.DND_FILES)
        top_bar.dnd_bind('<<Drop>>', self._on_drop)

        # === ROW 2: Output + Actions ===
        row2 = ctk.CTkFrame(content, fg_color="transparent")
        row2.pack(fill="x")

        # Output section
        ctk.CTkLabel(
            row2,
            text="📂 Output:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=(0, 10))

        self.auto_checkbox = ctk.CTkCheckBox(
            row2, text="Auto", variable=self.auto_output,
            command=self._toggle_auto_output,
            font=ctk.CTkFont(size=11), width=60
        )
        self.auto_checkbox.pack(side="left", padx=(0, 5))

        self.output_entry = ctk.CTkEntry(
            row2, textvariable=self.output_dir,
            placeholder_text="Output directory...",
            height=BUTTON_HEIGHT, font=ctk.CTkFont(size=11), width=250
        )
        self.output_entry.pack(side="left", padx=(0, 5))

        self.browse_output_btn = ctk.CTkButton(
            row2, text="Browse", command=self._browse_output,
            width=80, height=BUTTON_HEIGHT, fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER, font=ctk.CTkFont(size=12)
        )
        self.browse_output_btn.pack(side="left", padx=(0, 20))

        # Actions section
        ctk.CTkLabel(
            row2,
            text="⚙️ Mode:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=(0, 10))

        self.bw_switch = ctk.CTkSwitch(
            row2, text="B&W", command=self._toggle_bw,
            font=ctk.CTkFont(size=11), width=70
        )
        self.bw_switch.pack(side="left", padx=(0, 10))

        self.metadata_checkbox = ctk.CTkCheckBox(
            row2, text="Blank metadata", command=self._toggle_metadata,
            font=ctk.CTkFont(size=11), width=120
        )
        self.metadata_checkbox.select()  # Checked by default
        self.metadata_checkbox.pack(side="left")

    def _build_left_panel(self, parent):
        """Build compact left panel with queue, buttons, activity."""
        # === QUEUE ===
        queue_card = Card(parent, "📋 Queue")
        queue_card.pack(fill="both", expand=False, pady=(0, SECTION_SPACING))

        self.queue_list = FileQueueList(queue_card, height=QUEUE_HEIGHT)
        self.queue_list.pack(fill="both", padx=CARD_PADDING, pady=(0, CARD_PADDING))

        # Enable drag and drop on queue
        queue_card.drop_target_register(tkdnd.DND_FILES)
        queue_card.dnd_bind('<<Drop>>', self._on_drop)

        # === ACTION BUTTONS ===
        buttons_card = Card(parent, "🎬 Actions")
        buttons_card.pack(fill="x", pady=(0, SECTION_SPACING))

        btn_content = ctk.CTkFrame(buttons_card, fg_color="transparent")
        btn_content.pack(fill="x", padx=CARD_PADDING, pady=(0, CARD_PADDING))

        self.preview_btn = ctk.CTkButton(
            btn_content,
            text="🔍 Preview First Page",
            command=self._preview_first_page,
            height=BUTTON_HEIGHT + 4,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.preview_btn.pack(fill="x", pady=(0, 8))

        self.convert_btn = ctk.CTkButton(
            btn_content,
            text="✨ Convert All PDFs",
            command=self._convert_pdfs,
            height=BUTTON_HEIGHT + 8,
            fg_color=COLOR_BUTTON_SUCCESS,
            hover_color="#218838",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.convert_btn.pack(fill="x")

        # === PROGRESS BAR ===
        progress_card = Card(parent, "📊 Progress")
        progress_card.pack(fill="x", pady=(0, SECTION_SPACING))

        self.progress = ctk.CTkProgressBar(
            progress_card,
            height=20,
            corner_radius=10,
            progress_color=COLOR_BUTTON_SUCCESS
        )
        self.progress.pack(fill="x", padx=CARD_PADDING, pady=(0, CARD_PADDING))
        self.progress.set(0)

        # === ACTIVITY LOG ===
        activity_card = Card(parent, "📝 Activity Log")
        activity_card.pack(fill="both", expand=True)

        self.activity_log = ActivityLog(activity_card, height=ACTIVITY_HEIGHT)
        self.activity_log.pack(fill="both", expand=True, padx=CARD_PADDING, pady=(0, CARD_PADDING))

    def _build_right_sliders(self, parent):
        """Build compact two-column slider panel with preview underneath."""
        # Container for sliders
        sliders_container = ctk.CTkFrame(parent, fg_color="transparent")
        sliders_container.pack(fill="x", pady=(0, SECTION_SPACING))

        # Two equal columns
        col1_frame = ctk.CTkFrame(sliders_container, fg_color="transparent")
        col1_frame.grid(row=0, column=0, sticky="nsew", padx=(0, SECTION_SPACING//2))

        col2_frame = ctk.CTkFrame(sliders_container, fg_color="transparent")
        col2_frame.grid(row=0, column=1, sticky="nsew", padx=(SECTION_SPACING//2, 0))

        sliders_container.grid_columnconfigure(0, weight=1)
        sliders_container.grid_columnconfigure(1, weight=1)

        # Compact slider definitions
        sliders_col1 = [
            ("DPI", "dpi"),
            ("Lighting", "lighting"),
            ("Wrinkles", "wrinkles"),
            ("Warp", "warp"),
            ("Texture", "paper_texture"),
        ]

        sliders_col2 = [
            ("Quality", "jpg_quality"),
            ("Tilt", "tilt_randomness"),
            ("Shadows", "shadows"),
            ("Noise", "noise"),
            ("Edge", "page_edge"),
        ]

        self.sliders = {}

        # Build column 1
        for i, (label, key) in enumerate(sliders_col1):
            min_val, max_val, step = SLIDER_RANGES[key]
            default_val = getattr(self.config, key)

            slider = SliderCard(
                col1_frame,
                label=label,
                min_val=min_val,
                max_val=max_val,
                step=step,
                default_val=default_val,
                command=lambda v, k=key: self._update_config(k, v)
            )
            slider.grid(row=i, column=0, sticky="ew", pady=(0, SECTION_SPACING))
            self.sliders[key] = slider

        # Build column 2
        for i, (label, key) in enumerate(sliders_col2):
            min_val, max_val, step = SLIDER_RANGES[key]
            default_val = getattr(self.config, key)

            slider = SliderCard(
                col2_frame,
                label=label,
                min_val=min_val,
                max_val=max_val,
                step=step,
                default_val=default_val,
                command=lambda v, k=key: self._update_config(k, v)
            )
            slider.grid(row=i, column=0, sticky="ew", pady=(0, SECTION_SPACING))
            self.sliders[key] = slider

        # === PREVIEW SECTION BELOW SLIDERS ===
        preview_card = Card(parent, "🖼️ Preview (click to open zoom window)")
        preview_card.pack(fill="both", expand=True)

        # Make preview card clickable to open zoom window (not generate)
        preview_card.bind("<Button-1>", lambda e: self._open_zoom_window())

        # Preview display area
        self.preview_frame = ctk.CTkFrame(
            preview_card,
            fg_color=COLOR_BG,
            corner_radius=6,
            border_width=2,
            border_color="#d0d0d0",
            cursor="hand2"
        )
        self.preview_frame.pack(fill="both", expand=True, padx=CARD_PADDING, pady=(0, CARD_PADDING))
        self.preview_frame.bind("<Button-1>", lambda e: self._open_zoom_window())

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="No preview\n\n👆 Click 'Preview First Page' button above",
            text_color=COLOR_TEXT_SECONDARY,
            font=ctk.CTkFont(size=13),
            cursor="hand2"
        )
        self.preview_label.pack(expand=True)
        self.preview_label.bind("<Button-1>", lambda e: self._open_zoom_window())

        # Track if preview window is open
        self.preview_window = None

        self.preview_image = None

    def _update_config(self, key: str, value):
        """Update configuration value."""
        setattr(self.config, key, value)

    def _toggle_bw(self):
        """Toggle black and white mode."""
        self.config.black_and_white = self.bw_switch.get() == 1

    def _toggle_metadata(self):
        """Toggle blank metadata."""
        self.config.blank_metadata = self.metadata_checkbox.get() == 1
        print("this was ran")

    def _toggle_auto_output(self):
        """Toggle auto output directory."""
        if self.auto_output.get():
            self.output_entry.configure(state="disabled")
            self.browse_output_btn.configure(state="disabled")
            self._update_auto_output()
        else:
            self.output_entry.configure(state="normal")
            self.browse_output_btn.configure(state="normal")

    def _update_auto_output(self):
        """Update output dir based on first PDF."""
        if self.auto_output.get() and self.processor.pdf_files:
            first_pdf = self.processor.pdf_files[0]
            self.output_dir.set(str(Path(first_pdf).parent))

    def _browse_files(self):
        """Browse for PDF files."""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        for file in files:
            self.processor.add_pdf(file)

        self._update_queue()
        self._update_auto_output()

    def _remove_selected(self):
        """Remove selected file from queue."""
        if not self.processor.pdf_files:
            return

        # For now, remove the first file (could be enhanced with selection)
        if self.processor.pdf_files:
            self.processor.remove_pdf(self.processor.pdf_files[0])
            self._update_queue()

    def _clear_files(self):
        """Clear all files from queue."""
        self.processor.clear_queue()
        self._update_queue()
        self.preview_label.configure(image=None, text="No preview")

    def _update_queue(self):
        """Update queue display."""
        self.queue_list.update_files(self.processor.pdf_files)

    def _on_drop(self, event):
        """Handle drag and drop."""
        files = self.tk.splitlist(event.data)

        for file in files:
            # Clean up file path
            file = file.strip('{}')
            if file.lower().endswith('.pdf'):
                self.processor.add_pdf(file)

        self._update_queue()
        self._update_auto_output()

    def _browse_output(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_dir.set(directory)

    def _show_output(self):
        """Open output directory in file explorer."""
        output = self.output_dir.get()
        if output and os.path.exists(output):
            os.startfile(output)
        else:
            messagebox.showwarning("Warning", "Output directory not set or doesn't exist")

    def _preview_first_page(self):
        """Preview first page in dedicated window with zoom/pan."""
        if not self.processor.pdf_files:
            messagebox.showwarning("Warning", "No PDF files in queue")
            return

        # Show progress in button
        self.preview_btn.configure(text="⏳ Generating preview...", state="disabled")
        self.activity_log.log("🔄 Generating preview...")
        self.update()  # Force UI update

        def preview_thread():
            try:
                pdf_path = self.processor.pdf_files[0]
                pdf_name = os.path.basename(pdf_path)

                # Render with effects
                image = self.processor.render_page(pdf_path, 0, self.config)

                if image:
                    # Open preview window in main thread
                    self.after(0, lambda: self._show_preview_window(image, pdf_name))
                    self.after(0, lambda: self.activity_log.log("✓ Preview opened successfully"))
                else:
                    self.after(0, lambda: self.activity_log.log("✗ Failed to generate preview"))
                    self.after(0, lambda: messagebox.showerror("Error", "Could not render preview"))

            except Exception as e:
                error_msg = str(e)
                self.after(0, lambda: self.activity_log.log(f"✗ Error: {error_msg}"))
                self.after(0, lambda: messagebox.showerror("Error", f"Preview failed: {error_msg}"))

            finally:
                self.after(0, lambda: self.preview_btn.configure(
                    text="🔍 Preview First Page", state="normal"
                ))

        thread = threading.Thread(target=preview_thread, daemon=True)
        thread.start()

    def _show_preview_window(self, image: Image.Image, pdf_name: str):
        """Update inline thumbnail only - don't auto-open zoom window."""
        # Store the preview image for later
        self.cached_preview_image = image
        self.cached_preview_name = pdf_name

        # Update inline preview thumbnail
        self._update_inline_preview(image)

        # Make preview clickable to open zoom window
        self.preview_frame.bind("<Button-1>", lambda e: self._open_zoom_window())
        self.preview_label.bind("<Button-1>", lambda e: self._open_zoom_window())

    def _open_zoom_window(self):
        """Open the zoom window when user clicks preview - only one window at a time."""
        if not hasattr(self, 'cached_preview_image') or not self.cached_preview_image:
            self.activity_log.log("⚠ Generate preview first")
            return

        # Close existing preview window if open
        if self.preview_window and self.preview_window.winfo_exists():
            self.preview_window.lift()  # Just bring to front if already open
            self.preview_window.focus()
            return

        # Open new preview window
        self.preview_window = PreviewWindow(self, self.cached_preview_image, f"Preview - {self.cached_preview_name}")
        self.preview_window.lift()  # Bring to front
        self.preview_window.focus()  # Make active
        self.preview_window.attributes('-topmost', True)  # Force to top
        self.preview_window.after(100, lambda: self.preview_window.attributes('-topmost', False))  # Then allow normal behavior

    def _update_inline_preview(self, image: Image.Image):
        """Update the inline preview thumbnail."""
        try:
            # Get preview frame dimensions
            frame_width = self.preview_frame.winfo_width()
            frame_height = self.preview_frame.winfo_height()

            # Use reasonable defaults if frame not yet sized
            if frame_width < 100:
                frame_width = 600
            if frame_height < 100:
                frame_height = 300

            # Calculate scaling to fit
            width_ratio = (frame_width - 40) / image.width
            height_ratio = (frame_height - 40) / image.height
            scale = min(width_ratio, height_ratio, 1.0)

            new_width = int(image.width * scale)
            new_height = int(image.height * scale)

            # Resize for display
            display_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to CTkImage to avoid warning and support HighDPI
            ctk_image = ctk.CTkImage(
                light_image=display_image,
                dark_image=display_image,
                size=(new_width, new_height)
            )

            # Update label
            self.preview_image = ctk_image  # Keep reference
            self.preview_label.configure(
                image=ctk_image,
                text="",
                fg_color="transparent"
            )
        except Exception as e:
            self.activity_log.log(f"✗ Preview thumbnail update failed: {e}")

    def _convert_pdfs(self):
        """Convert all PDFs in queue."""
        if not self.processor.pdf_files:
            messagebox.showwarning("Warning", "No PDF files in queue")
            return

        # Check output directory
        output = self.output_dir.get()
        if not output:
            messagebox.showwarning("Warning", "Please select an output directory")
            return

        if not os.path.exists(output):
            try:
                os.makedirs(output)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory: {e}")
                return

        # Disable UI
        self.is_processing = True
        self._set_ui_state(False)
        self.activity_log.clear()
        self.activity_log.log("Starting conversion...")

        def conversion_thread():
            total_files = len(self.processor.pdf_files)

            for idx, pdf_path in enumerate(self.processor.pdf_files):
                file_name = os.path.basename(pdf_path)
                self.after(0, lambda f=file_name: self.activity_log.log(f"\n[{idx + 1}/{total_files}] Processing: {f}"))

                def progress_callback(current, total, message):
                    if total > 0:
                        progress_val = (idx / total_files) + (current / total / total_files)
                        self.after(0, lambda p=progress_val: self.progress.set(p))
                    self.after(0, lambda m=message: self.activity_log.log(m))

                success = self.processor.convert_pdf(
                    pdf_path,
                    output,
                    self.config,
                    progress_callback
                )

                if not success:
                    self.after(0, lambda f=file_name: self.activity_log.log(f"Failed: {f}"))

            # Complete
            self.after(0, lambda: self.progress.set(1.0))
            self.after(0, lambda: self.activity_log.log("\n✓ All conversions completed!"))
            self.after(0, lambda: self._set_ui_state(True))
            self.after(0, lambda: setattr(self, 'is_processing', False))

        thread = threading.Thread(target=conversion_thread, daemon=True)
        thread.start()

    def _set_ui_state(self, enabled: bool):
        """Enable or disable UI elements."""
        state = "normal" if enabled else "disabled"

        self.browse_btn.configure(state=state)
        self.remove_btn.configure(state=state)
        self.clear_btn.configure(state=state)
        self.preview_btn.configure(state=state)
        self.convert_btn.configure(state=state)
        self.browse_output_btn.configure(state=state)

        if not enabled:
            self.progress.set(0)

    def _on_closing(self):
        """Handle window close."""
        if self.is_processing:
            if messagebox.askyesno("Confirm", "Conversion in progress. Are you sure you want to exit?"):
                self.destroy()
        else:
            self.destroy()

    def _check_for_updates(self):
        """Check for updates in background on startup."""
        try:
            req = urllib.request.Request(UPDATE_CHECK_URL)
            req.add_header('User-Agent', 'PDF2Scan')

            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data['tag_name'].lstrip('v')

                if self._compare_versions(latest_version, VERSION) > 0:
                    # New version available
                    self.after(0, lambda: self._show_update_notification(latest_version, data['html_url']))
        except Exception as e:
            # Silently fail - don't bother user on startup
            pass

    def _check_updates_manual(self):
        """Manually check for updates when user clicks button."""
        self.activity_log.log("Checking for updates...")

        try:
            req = urllib.request.Request(UPDATE_CHECK_URL)
            req.add_header('User-Agent', 'PDF2Scan')

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                latest_version = data['tag_name'].lstrip('v')

                if self._compare_versions(latest_version, VERSION) > 0:
                    self.activity_log.log(f"✓ New version available: {latest_version}")
                    if messagebox.askyesno(
                        "Update Available",
                        f"A new version is available!\n\nCurrent: {VERSION}\nLatest: {latest_version}\n\nWould you like to download it?",
                        icon='info'
                    ):
                        webbrowser.open(data['html_url'])
                else:
                    self.activity_log.log(f"✓ You're running the latest version ({VERSION})")
                    messagebox.showinfo("Up to Date", f"You're running the latest version ({VERSION})")
        except Exception as e:
            self.activity_log.log(f"✗ Failed to check for updates: {str(e)}")
            messagebox.showerror("Update Check Failed", f"Could not check for updates.\n\n{str(e)}")

    def _show_update_notification(self, new_version, download_url):
        """Show notification about available update."""
        if messagebox.askyesno(
            "Update Available",
            f"A new version of PDF2Scan is available!\n\nCurrent: {VERSION}\nLatest: {new_version}\n\nWould you like to download it?",
            icon='info'
        ):
            webbrowser.open(download_url)

    def _compare_versions(self, v1, v2):
        """Compare version strings. Returns 1 if v1 > v2, -1 if v1 < v2, 0 if equal."""
        try:
            parts1 = [int(x) for x in v1.split('.')]
            parts2 = [int(x) for x in v2.split('.')]

            for i in range(max(len(parts1), len(parts2))):
                p1 = parts1[i] if i < len(parts1) else 0
                p2 = parts2[i] if i < len(parts2) else 0
                if p1 > p2:
                    return 1
                elif p1 < p2:
                    return -1
            return 0
        except:
            return 0

    def _show_about(self):
        """Show About dialog."""
        about_window = ctk.CTkToplevel(self)
        about_window.title("About PDF2Scan")
        about_window.geometry("500x500")
        about_window.configure(fg_color=COLOR_BG)
        about_window.resizable(False, False)

        # Center window
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (about_window.winfo_screenheight() // 2) - (500 // 2)
        about_window.geometry(f"500x500+{x}+{y}")

        # Make modal
        about_window.transient(self)
        about_window.grab_set()

        # Content frame
        content = ctk.CTkFrame(about_window, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)

        # Icon/Title
        ctk.CTkLabel(
            content,
            text="📄 PDF2Scan",
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(pady=(0, 10))

        # Version
        ctk.CTkLabel(
            content,
            text=f"Version {VERSION}",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_TEXT_SECONDARY
        ).pack(pady=(0, 20))

        # Description
        ctk.CTkLabel(
            content,
            text="Convert PDF documents to realistic scanned images",
            font=ctk.CTkFont(size=13),
            wraplength=440
        ).pack(pady=(0, 10))

        # Features
        features_frame = ctk.CTkFrame(content, fg_color=COLOR_CARD, corner_radius=10)
        features_frame.pack(fill="x", pady=20)

        features = [
            "✨ Realistic scan effects (wrinkles, texture, shadows)",
            "🎨 Adjustable quality and DPI settings",
            "📐 Page warping and edge effects",
            "🖼️ Real-time preview with zoom/pan",
            "📦 Batch processing support",
            "🔒 Metadata removal for privacy"
        ]

        for feature in features:
            ctk.CTkLabel(
                features_frame,
                text=feature,
                font=ctk.CTkFont(size=11),
                anchor="w"
            ).pack(fill="x", padx=20, pady=5)

        # Links frame
        links_frame = ctk.CTkFrame(content, fg_color="transparent")
        links_frame.pack(pady=20)

        # GitHub button
        github_btn = ctk.CTkButton(
            links_frame,
            text="🌐 GitHub Repository",
            command=lambda: webbrowser.open(f"https://github.com/{GITHUB_REPO}"),
            width=200,
            height=35,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER
        )
        github_btn.pack(pady=5)

        # Report Issue button
        issue_btn = ctk.CTkButton(
            links_frame,
            text="🐛 Report Issue",
            command=lambda: webbrowser.open(f"https://github.com/{GITHUB_REPO}/issues"),
            width=200,
            height=35,
            fg_color=COLOR_BUTTON_SECONDARY,
            hover_color="#5a6268"
        )
        issue_btn.pack(pady=5)

        # Copyright
        ctk.CTkLabel(
            content,
            text=f"© {datetime.now().year} PDF2Scan\nReleased under MIT License",
            font=ctk.CTkFont(size=10),
            text_color=COLOR_TEXT_SECONDARY
        ).pack(pady=(20, 0))

        # Close button
        close_btn = ctk.CTkButton(
            about_window,
            text="Close",
            command=about_window.destroy,
            width=100,
            height=35,
            fg_color=COLOR_BUTTON_SUCCESS,
            hover_color="#218838"
        )
        close_btn.pack(pady=(0, 20))


def main():
    """Main entry point."""
    app = PDF2ScanApp()
    app.mainloop()


if __name__ == "__main__":
    main()
