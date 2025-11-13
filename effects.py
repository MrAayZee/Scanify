"""
Scan effect implementations for realistic scanner simulation.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random

try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


def apply_paper_color(image: Image.Image) -> Image.Image:
    """Add realistic paper color - paper is never pure white, has yellowish tint."""
    img_array = np.array(image, dtype=np.float32)

    # Real paper has cream/ivory/yellowish tint - more visible
    paper_tint = np.array([248, 246, 238], dtype=np.float32)  # Yellowish cream

    # Blend with paper color (noticeable but not overwhelming)
    result = img_array * 0.85 + paper_tint * 0.15
    result = np.clip(result, 0, 255).astype(np.uint8)

    return Image.fromarray(result)


def apply_scan_effects(image: Image.Image, config) -> Image.Image:
    """
    Apply all scan effects to create a realistic scanned document look.

    Args:
        image: PIL Image to process
        config: EffectConfig with effect parameters

    Returns:
        Processed PIL Image
    """
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Get dimensions
    width, height = image.size

    # Scale down for processing if too large
    max_dim = 2200
    scale_factor = 1.0
    if max(width, height) > max_dim:
        scale_factor = max_dim / max(width, height)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        width, height = new_width, new_height

    # Add realistic paper color first (unless B&W)
    if not config.black_and_white:
        image = apply_paper_color(image)

    # Apply color mode conversion if B&W
    if config.black_and_white:
        image = apply_black_and_white(image)

    # Apply warp/distortion
    if config.warp > 0.01:
        image = apply_warp(image, config.warp)

    # Apply lighting gradient
    if config.lighting > 0.01:
        image = apply_lighting(image, config.lighting)

    # Apply wrinkles
    if config.wrinkles > 0.01:
        image = apply_wrinkles(image, config.wrinkles)

    # Apply paper texture
    if config.paper_texture > 0.01:
        image = apply_paper_texture(image, config.paper_texture)

    # Apply shadows
    if config.shadows > 0.01:
        image = apply_shadows(image, config.shadows, config.tilt_randomness)

    # Apply page edge
    if config.page_edge > 0.01:
        image = apply_page_edge(image, config.page_edge, config.tilt_randomness)

    # Apply noise last
    if config.noise > 0.01:
        image = apply_noise(image, config.noise)

    # Scale back up if we scaled down
    if scale_factor != 1.0:
        original_width = int(width / scale_factor)
        original_height = int(height / scale_factor)
        image = image.resize((original_width, original_height), Image.Resampling.LANCZOS)

    return image


def apply_black_and_white(image: Image.Image) -> Image.Image:
    """Convert to true black and white - clean scanning result."""
    # Convert to grayscale first
    gray = image.convert('L')

    if HAS_OPENCV:
        # Use OpenCV for better adaptive thresholding
        gray_array = np.array(gray)

        # Use Otsu's method for automatic optimal threshold
        # This prevents weird artifacts around text
        _, binary = cv2.threshold(
            gray_array, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # Slight denoising to clean up
        binary = cv2.fastNlMeansDenoising(binary, None, 10, 7, 21)

        # Convert back to RGB
        result = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
        return Image.fromarray(result)
    else:
        # Better fallback with auto threshold
        hist = gray.histogram()
        total = sum(hist)

        # Calculate optimal threshold using Otsu-like method
        current_max, threshold = 0, 0
        sum_total, sum_foreground = 0, 0
        weight_background, weight_foreground = 0, 0

        for i in range(256):
            sum_total += i * hist[i]

        for i in range(256):
            weight_background += hist[i]
            if weight_background == 0:
                continue

            weight_foreground = total - weight_background
            if weight_foreground == 0:
                break

            sum_foreground += i * hist[i]

            mean_background = sum_foreground / weight_background
            mean_foreground = (sum_total - sum_foreground) / weight_foreground

            between_variance = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2

            if between_variance > current_max:
                current_max = between_variance
                threshold = i

        # Apply threshold
        binary = gray.point(lambda x: 255 if x > threshold else 0, mode='L')
        return binary.convert('RGB')


def apply_lighting(image: Image.Image, intensity: float) -> Image.Image:
    """Apply realistic uneven lighting - scanners have non-uniform light distribution."""
    if intensity < 0.01:
        return image

    width, height = image.size
    img_array = np.array(image, dtype=np.float32)

    # Create lighting gradient
    lighting = np.ones((height, width), dtype=np.float32)

    # Scanner light typically brighter in center
    center_x = width * random.uniform(0.45, 0.55)
    center_y = height * random.uniform(0.4, 0.6)

    # Create coordinate grids
    y_grid, x_grid = np.mgrid[0:height, 0:width]

    # Calculate distance from light center
    distances = np.sqrt((x_grid - center_x) ** 2 + (y_grid - center_y) ** 2)
    max_dist = np.sqrt(width ** 2 + height ** 2)

    # Normalize distances
    norm_dist = distances / max_dist

    # Apply noticeable lighting gradient - scanners DO have visible light falloff
    brightness_variation = 1.0 + (intensity * 0.25 * (1.0 - norm_dist)) - (intensity * 0.15)
    lighting = brightness_variation

    # Warm color cast from scanner light
    r_channel = img_array[:, :, 0] * lighting * 1.02  # Warm red
    g_channel = img_array[:, :, 1] * lighting * 1.01  # Slight green
    b_channel = img_array[:, :, 2] * lighting * 0.96  # Reduce blue for warmth

    result = np.stack([r_channel, g_channel, b_channel], axis=2)
    result = np.clip(result, 0, 255).astype(np.uint8)

    return Image.fromarray(result)


def apply_warp(image: Image.Image, intensity: float) -> Image.Image:
    """Apply realistic page warp - paper is never perfectly flat on scanner bed."""
    if intensity < 0.01:
        return image

    width, height = image.size
    img_array = np.array(image)

    # Create mesh grid
    y_grid, x_grid = np.mgrid[0:height, 0:width]

    # Real paper warping - RANDOM for each page
    wave_intensity = intensity * random.uniform(15, 35)  # Random warp strength

    # Random wave patterns (different for each page)
    freq_h = random.uniform(0.5, 1.2)  # Random horizontal frequency
    freq_v = random.uniform(0.6, 1.0)  # Random vertical frequency
    phase_h = random.uniform(0, 2 * np.pi)  # Random phase shift
    phase_v = random.uniform(0, 2 * np.pi)

    # Horizontal waves (book spine curve effect) - RANDOM
    dx = wave_intensity * np.sin(2 * np.pi * y_grid / (height * freq_h) + phase_h)

    # Vertical waves (paper not flat) - RANDOM
    dy = wave_intensity * np.sin(2 * np.pi * x_grid / (width * freq_v) + phase_v) * random.uniform(0.4, 0.8)

    # Add slight barrel distortion - RANDOM
    center_x, center_y = width / 2, height / 2
    distortion = intensity * random.uniform(0.0005, 0.0015)
    dx += (x_grid - center_x) * distortion
    dy += (y_grid - center_y) * distortion

    # Create displacement map
    new_x = np.clip(x_grid + dx, 0, width - 1).astype(np.float32)
    new_y = np.clip(y_grid + dy, 0, height - 1).astype(np.float32)

    if HAS_OPENCV:
        result = cv2.remap(img_array, new_x, new_y, cv2.INTER_LINEAR)
        return Image.fromarray(result)
    else:
        # Fallback: just return original
        return image


def apply_wrinkles(image: Image.Image, intensity: float) -> Image.Image:
    """Add realistic paper wrinkles/creases - paper gets folded and wrinkled."""
    if intensity < 0.01:
        return image

    width, height = image.size
    img_array = np.array(image, dtype=np.float32)

    # Create wrinkle overlay
    wrinkle_layer = np.ones((height, width), dtype=np.float32)

    # Many wrinkles for realistic paper
    num_wrinkles = max(8, int(intensity * 30))
    for _ in range(num_wrinkles):
        # Random wrinkle parameters
        if random.random() > 0.5:
            # Horizontal wrinkle
            y = random.randint(int(height * 0.05), int(height * 0.95))
            amplitude = random.uniform(2.0, 6.0) * intensity
            frequency = random.uniform(0.003, 0.015)
            wrinkle_strength = intensity * random.uniform(0.15, 0.3)  # MUCH stronger

            for x in range(width):
                offset = int(amplitude * np.sin(frequency * x + random.uniform(0, 2 * np.pi)))
                y_pos = min(max(y + offset, 0), height - 1)
                # STRONG visible shadow
                wrinkle_layer[y_pos, x] *= (1.0 - wrinkle_strength)
                # Wider smooth transition
                for dy in range(-3, 4):
                    if 0 <= y_pos + dy < height:
                        fade = 1.0 - abs(dy) / 4.0
                        wrinkle_layer[y_pos + dy, x] *= (1.0 - wrinkle_strength * fade * 0.5)
        else:
            # Vertical wrinkle
            x = random.randint(int(width * 0.05), int(width * 0.95))
            amplitude = random.uniform(2.0, 6.0) * intensity
            frequency = random.uniform(0.003, 0.015)
            wrinkle_strength = intensity * random.uniform(0.15, 0.3)

            for y in range(height):
                offset = int(amplitude * np.sin(frequency * y + random.uniform(0, 2 * np.pi)))
                x_pos = min(max(x + offset, 0), width - 1)
                wrinkle_layer[y, x_pos] *= (1.0 - wrinkle_strength)
                for dx in range(-3, 4):
                    if 0 <= x_pos + dx < width:
                        fade = 1.0 - abs(dx) / 4.0
                        wrinkle_layer[y, x_pos + dx] *= (1.0 - wrinkle_strength * fade * 0.5)

    # Small blur to smooth slightly but keep visible
    if HAS_OPENCV:
        blur_size = 3
        wrinkle_layer = cv2.GaussianBlur(wrinkle_layer, (blur_size, blur_size), 0)

    # Apply wrinkle shading
    wrinkle_rgb = np.stack([wrinkle_layer] * 3, axis=2)
    result = img_array * wrinkle_rgb
    result = np.clip(result, 0, 255).astype(np.uint8)

    return Image.fromarray(result)


def apply_shadows(image: Image.Image, intensity: float, tilt: float) -> Image.Image:
    """Add realistic edge vignetting - scanner light doesn't reach edges as well."""
    if intensity < 0.01:
        return image

    width, height = image.size
    img_array = np.array(image, dtype=np.float32)

    # Create shadow vignette from edges
    shadow = np.ones((height, width), dtype=np.float32)

    # Noticeable shadow strength
    shadow_strength = intensity * 0.3

    # Top and bottom edge vignetting
    edge_size = int(height * 0.15)
    for y in range(edge_size):
        fade = (edge_size - y) / edge_size
        shadow[y, :] *= (1.0 - fade * shadow_strength * 0.7)
        shadow[height - 1 - y, :] *= (1.0 - fade * shadow_strength * 0.7)

    # Left and right edge vignetting
    edge_size = int(width * 0.12)
    for x in range(edge_size):
        fade = (edge_size - x) / edge_size
        shadow[:, x] *= (1.0 - fade * shadow_strength * 0.8)
        shadow[:, width - 1 - x] *= (1.0 - fade * shadow_strength * 0.8)

    # Corner vignetting (more pronounced)
    corner_size = min(width, height) // 6
    corner_shadow_strength = shadow_strength * 1.5

    for y in range(corner_size):
        for x in range(corner_size):
            dist = np.sqrt((x / corner_size) ** 2 + (y / corner_size) ** 2)
            if dist < 1.0:
                fade = (1.0 - dist) * corner_shadow_strength
                # Top-left
                shadow[y, x] *= (1.0 - fade)
                # Top-right
                shadow[y, width - 1 - x] *= (1.0 - fade)
                # Bottom-left
                shadow[height - 1 - y, x] *= (1.0 - fade)
                # Bottom-right
                shadow[height - 1 - y, width - 1 - x] *= (1.0 - fade)

    # Moderate blur for soft vignette
    if HAS_OPENCV:
        blur_size = int(15 + intensity * 30)
        if blur_size % 2 == 0:
            blur_size += 1
        shadow = cv2.GaussianBlur(shadow, (blur_size, blur_size), 0)

    # Apply shadow to image
    shadow_rgb = np.stack([shadow] * 3, axis=2)
    result = img_array * shadow_rgb
    result = np.clip(result, 0, 255).astype(np.uint8)

    return Image.fromarray(result)


def apply_noise(image: Image.Image, intensity: float) -> Image.Image:
    """Add realistic scanner noise - all scanners have some noise."""
    if intensity < 0.01:
        return image

    width, height = image.size
    img_array = np.array(image, dtype=np.float32)

    # Generate visible Gaussian noise
    noise = np.random.normal(0, intensity * 12, img_array.shape)

    # Add noise
    noisy = img_array + noise
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)

    return Image.fromarray(noisy)


def apply_paper_texture(image: Image.Image, intensity: float) -> Image.Image:
    """Add realistic paper grain - paper has visible texture, not smooth."""
    if intensity < 0.01:
        return image

    width, height = image.size
    img_array = np.array(image, dtype=np.float32)

    # Create visible paper grain
    grain_width = width // 2
    grain_height = height // 2

    # Generate STRONG grain texture - paper has visible fibers
    grain = np.random.normal(0, intensity * 15, (grain_height, grain_width)).astype(np.float32)

    # Convert to PIL for smooth upscaling - PIL expects (width, height)!
    grain_pil = Image.new('L', (grain_width, grain_height), 128)
    grain_array = np.array(grain_pil, dtype=np.float32) + grain
    grain_array = np.clip(grain_array, 0, 255).astype(np.uint8)
    grain_img = Image.fromarray(grain_array, mode='L')
    grain_img = grain_img.resize((width, height), Image.Resampling.BILINEAR)
    grain = np.array(grain_img, dtype=np.float32) - 128  # Center around 0

    # Apply texture - VERY visible
    grain_rgb = np.stack([grain] * 3, axis=2)
    result = img_array + grain_rgb * intensity * 1.5  # Much stronger application
    result = np.clip(result, 0, 255).astype(np.uint8)

    return Image.fromarray(result)
def apply_page_edge(image: Image.Image, intensity: float, tilt: float) -> Image.Image:
    """Add realistic scanner bed background with gradient - like real flatbed scanner with non-uniform border."""
    if intensity < 0.01:
        return image

    width, height = image.size

    # NON-UNIFORM border based on tilt (paper not perfectly centered)
    border_base = int(min(width, height) * 0.08 * intensity)
    if border_base < 5:
        return image

    # Tilt makes borders uneven
    border_variation = int(border_base * tilt * random.uniform(0.3, 0.8))
    border_top = border_base + random.randint(-border_variation, border_variation)
    border_bottom = border_base + random.randint(-border_variation, border_variation)
    border_left = border_base + random.randint(-border_variation, border_variation)
    border_right = border_base + random.randint(-border_variation, border_variation)

    # Ensure positive borders
    border_top = max(5, border_top)
    border_bottom = max(5, border_bottom)
    border_left = max(5, border_left)
    border_right = max(5, border_right)

    new_width = width + border_left + border_right
    new_height = height + border_top + border_bottom

    # Create REALISTIC scanner bed - multi-tone gradient like real scanner glass
    bg_array = np.zeros((new_height, new_width, 3), dtype=np.float32)

    # Create coordinate grids
    y_grid, x_grid = np.mgrid[0:new_height, 0:new_width]

    # REALISTIC scanner bed - medium-light gray with SUBTLE gradient
    # Real scanner beds are NOT dark - they're light/medium gray!
    base_gray = random.randint(140, 170)  # LIGHTER base - like real scanners

    # Start with uniform light gray
    bg_array[:, :, 0] = base_gray + random.randint(-8, 8)  # Slight color variation
    bg_array[:, :, 1] = base_gray + random.randint(-8, 8)
    bg_array[:, :, 2] = base_gray + random.randint(-8, 8)

    # Add SUBTLE gradient - scanner light varies slightly
    # Distance from page center for realistic light falloff ONLY in border area
    page_center_x = border_left + width / 2
    page_center_y = border_top + height / 2

    # Create mask for border-only gradient
    for y in range(new_height):
        for x in range(new_width):
            # Only apply gradient in the BORDER areas, not the whole image
            in_border = (x < border_left or x >= border_left + width or
                        y < border_top or y >= border_top + height)

            if in_border:
                # Calculate distance from nearest page edge
                dist_x = min(abs(x - border_left), abs(x - (border_left + width)))
                dist_y = min(abs(y - border_top), abs(y - (border_top + height)))
                edge_dist = min(dist_x, dist_y)

                # VERY SUBTLE darkening as you go further from page (0-15 gray levels max)
                darkening = int(edge_dist * 0.15)
                bg_array[y, x] = np.clip(bg_array[y, x] - darkening, 100, 255)

    # Add fine noise/texture (dust, scanner bed imperfections)
    noise = np.random.normal(0, 4, (new_height, new_width, 3))  # Subtle noise
    bg_array += noise

    # Add a few subtle vertical streaks (scanner glass very minor scratches)
    num_streaks = random.randint(3, 8)
    for _ in range(num_streaks):
        streak_x = random.randint(0, new_width - 1)
        streak_variation = random.uniform(2, 6)  # Very subtle
        streak_width = 1
        bg_array[:, max(0, streak_x - streak_width):min(new_width, streak_x + streak_width)] -= streak_variation

    # Add very few small dust spots
    num_spots = random.randint(10, 25)
    for _ in range(num_spots):
        spot_x = random.randint(0, new_width - 1)
        spot_y = random.randint(0, new_height - 1)
        spot_size = random.randint(1, 2)
        spot_change = random.uniform(-8, -3)  # Subtle spots
        y1, y2 = max(0, spot_y - spot_size), min(new_height, spot_y + spot_size)
        x1, x2 = max(0, spot_x - spot_size), min(new_width, spot_x + spot_size)
        bg_array[y1:y2, x1:x2] = np.clip(bg_array[y1:y2, x1:x2] + spot_change, 100, 255)

    # Clip to valid range - keep it LIGHT
    bg_array = np.clip(bg_array, 100, 255).astype(np.uint8)

    # Create PIL image from background
    result = Image.fromarray(bg_array, mode='RGB')

    # Paste the document page (non-uniform position due to tilt)
    result.paste(image, (border_left, border_top))

    # Add subtle drop shadow around page (page is slightly above scanner bed)
    shadow_overlay = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow_overlay)

    # Soft shadow parameters
    shadow_offset = 3
    avg_border = (border_top + border_bottom + border_left + border_right) // 4
    shadow_blur = int(avg_border * 0.4)

    # Draw shadow rectangle (slightly offset) - using actual page position
    shadow_rect = [
        border_left + shadow_offset,
        border_top + shadow_offset,
        border_left + width + shadow_offset,
        border_top + height + shadow_offset
    ]

    # Create gradient shadow (darker near page, lighter away)
    for i in range(10):
        alpha = int(30 * (10 - i) / 10)
        offset = i
        draw.rectangle(
            [shadow_rect[0] - offset, shadow_rect[1] - offset,
             shadow_rect[2] + offset, shadow_rect[3] + offset],
            outline=(0, 0, 0, alpha)
        )

    # Blur the shadow for realism
    shadow_overlay = shadow_overlay.filter(ImageFilter.GaussianBlur(radius=shadow_blur))

    # Composite shadow
    result = Image.alpha_composite(result.convert('RGBA'), shadow_overlay).convert('RGB')

    return result
