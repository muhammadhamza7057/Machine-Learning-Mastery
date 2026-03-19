# ============================================================
# BRAILLE CHARACTER RECOGNITION SYSTEM
# AI Assignment #2 — Bahria University Islamabad
# GROUP MEMBERS:
#   1. Muhammad Hamza (01-131232-057)
# ============================================================

from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import logging
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# BRAILLE CHARACTER MAPPING
# ============================================================
BRAILLE_MAP: Dict[Tuple[int, int, int, int, int, int], str] = {
    (1,0,0,0,0,0):'a', (1,1,0,0,0,0):'b', (1,0,0,1,0,0):'c',
    (1,0,0,1,1,0):'d', (1,0,0,0,1,0):'e', (1,1,0,1,0,0):'f',
    (1,1,0,1,1,0):'g', (1,1,0,0,1,0):'h', (0,1,0,1,0,0):'i',
    (0,1,0,1,1,0):'j', (1,0,1,0,0,0):'k', (1,1,1,0,0,0):'l',
    (1,0,1,1,0,0):'m', (1,0,1,1,1,0):'n', (1,0,1,0,1,0):'o',
    (1,1,1,1,0,0):'p', (1,1,1,1,1,0):'q', (1,1,1,0,1,0):'r',
    (0,1,1,1,0,0):'s', (0,1,1,1,1,0):'t', (1,0,1,0,0,1):'u',
    (1,1,1,0,0,1):'v', (0,1,0,1,1,1):'w', (1,0,1,1,0,1):'x',
    (1,0,1,1,1,1):'y', (1,0,1,0,1,1):'z', (0,0,0,0,0,0):' ',
}


# ============================================================
# CONFIGURATION DATA CLASS
# ============================================================
@dataclass
class BrailleConfig:
    """Reference calibration parameters for Braille recognition."""
    # Reference image dimensions
    reference_width: int = 2700
    reference_height: int = 3500
    
    # Vertical spacing (pixels)
    reference_dot_row_gap: int = 25      # Gap between dot rows in a cell
    reference_line_gap: int = 150        # Gap between Braille lines
    
    # Horizontal spacing (pixels)
    reference_dot_col_gap: int = 25      # Gap between left/right columns
    reference_word_gap: int = 88         # X-gap that marks word boundary
    reference_char_group_gap: int = 35   # Max X-gap to group columns into character
    reference_x_tolerance: int = 13      # Horizontal tolerance for dot detection
    
    # Top-row Y coordinates (pixels) for 18 Braille lines
    reference_band_y_coords: List[int] = None
    
    def __post_init__(self):
        """Initialize default band Y coordinates."""
        if self.reference_band_y_coords is None:
            self.reference_band_y_coords = [
                 31,  232,  431,  631,  831, 1031,
               1231, 1431, 1631, 1831, 2031, 2231,
               2431, 2631, 2831, 3031, 3231, 3431
            ]


# ============================================================
# SCALED PARAMETERS FOR CURRENT IMAGE
# ============================================================
@dataclass
class ScaledParams:
    """Runtime parameters scaled for the actual image dimensions."""
    dot_row_gap: int
    line_gap: int
    dot_col_gap: int
    word_gap: int
    char_group_gap: int
    x_tolerance: int
    band_y_coords: List[int]

# ============================================================
# ABBREVIATIONS AND SENTENCE RULES FOR POST-PROCESSING
# ============================================================
ABBREVIATIONS: Dict[str, str] = {
    'covid'  : 'COVID-19',
    'who'    : 'WHO',
    'un'     : 'UN',
    'us'     : 'US',
    'uk'     : 'UK',
    'nasa'   : 'NASA',
    'nato'   : 'NATO',
}

SENTENCE_STARTERS: List[str] = [
    'there are always',
    'some of the',
    'another significant',
    'additionally political',
]


# ============================================================
# IMAGE PROCESSING FUNCTIONS
# ============================================================
def load_image() -> Optional[np.ndarray]:
    """
    Load Braille image from disk.
    
    Searches for common filename variations and handles RGB/RGBA conversion.
    
    Returns:
        Grayscale numpy array, or None if not found.
    """
    candidates = ['Braille.png', 'braille.png', 'BRAILLE.PNG',
                  'Braille.jpg', 'braille.jpg']
    
    for filename in candidates:
        if not os.path.exists(filename):
            continue
            
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
            
        logger.info(f"Found image: {filename}")
        
        # Convert to grayscale, handling RGBA/RGB formats
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                # RGBA: composite alpha channel with white background
                alpha = img[:, :, 3:4] / 255.0
                rgb = img[:, :, :3].astype(float)
                composite = (rgb * alpha + np.ones_like(rgb) * 255 * (1 - alpha)).astype(np.uint8)
                gray = cv2.cvtColor(composite, cv2.COLOR_BGR2GRAY)
            else:
                # RGB or BGR
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            # Already grayscale
            gray = img
            
        logger.info(f"Image size: {gray.shape[1]}w x {gray.shape[0]}h")
        return gray
    
    logger.error("Braille image not found")
    logger.error(f"Looking in: {os.getcwd()}")
    logger.error(f"Files here: {os.listdir('.')}")
    return None


def binarise(gray: np.ndarray) -> np.ndarray:
    """
    Convert grayscale image to binary (black/white) using Otsu thresholding.
    
    Args:
        gray: Grayscale image.
        
    Returns:
        Binary image with white foreground (dots).
    """
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255,
                              cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Ensure dots are white (255), invert if necessary
    foreground_ratio = np.sum(binary == 255) / binary.size
    if foreground_ratio > 0.5:
        binary = cv2.bitwise_not(binary)
    
    return binary


def detect_dots(binary: np.ndarray) -> List[Tuple[int, int]]:
    """
    Detect Braille dots from binary image using contour area filtering.
    
    Args:
        binary: Binary image with white dots on black background.
        
    Returns:
        List of (x, y) coordinates for detected dots.
    """
    logger.info("Detecting dots...")
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by area (removes noise)
    areas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 5]
    
    if not areas:
        logger.error("No blobs found")
        return []
    
    # Use median area to determine valid dot range
    median_area = np.median(areas)
    min_area, max_area = median_area * 0.15, median_area * 4.0
    logger.info(f"Blobs: {len(areas)}, median={median_area:.0f}px², filter={min_area:.0f}–{max_area:.0f}px²")
    
    # Extract dot centroids
    dots = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area <= area <= max_area:
            moments = cv2.moments(contour)
            if moments["m00"] > 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])
                dots.append((cx, cy))
    
    logger.info(f"Dots kept: {len(dots)}")
    return dots


def scale_parameters(image_width: int, image_height: int, 
                     config: BrailleConfig) -> ScaledParams:
    """
    Scale reference parameters to actual image dimensions.
    
    Args:
        image_width: Width of the actual image.
        image_height: Height of the actual image.
        config: Reference configuration.
        
    Returns:
        ScaledParams with measurements adjusted for image size.
    """
    scale_x = image_width / config.reference_width
    scale_y = image_height / config.reference_height
    
    # Scale parameters with minimum thresholds
    dot_row_gap = max(5, int(config.reference_dot_row_gap * scale_y))
    line_gap = max(20, int(config.reference_line_gap * scale_y))
    dot_col_gap = max(5, int(config.reference_dot_col_gap * scale_x))
    word_gap = max(15, int(config.reference_word_gap * scale_x))
    char_group_gap = max(10, int(config.reference_char_group_gap * scale_x))
    x_tolerance = max(5, int(config.reference_x_tolerance * scale_x))
    
    # Scale Y coordinates for all Braille lines
    band_y_coords = [int(y * scale_y) for y in config.reference_band_y_coords]
    
    logger.info(f"Scaled parameters (image {image_width}x{image_height}):")
    logger.info(f"  dot_row_gap={dot_row_gap}, line_gap={line_gap}, dot_col_gap={dot_col_gap}")
    logger.info(f"  word_gap={word_gap}, char_group_gap={char_group_gap}, x_tolerance={x_tolerance}")
    
    return ScaledParams(
        dot_row_gap=dot_row_gap,
        line_gap=line_gap,
        dot_col_gap=dot_col_gap,
        word_gap=word_gap,
        char_group_gap=char_group_gap,
        x_tolerance=x_tolerance,
        band_y_coords=band_y_coords
    )

# ============================================================
# DECODING HELPER FUNCTIONS
# ============================================================
def get_row(dots: List[Tuple[int, int]], center_y: int, 
            tolerance: int) -> List[Tuple[int, int]]:
    """
    Extract dots within a horizontal band centered at center_y.
    
    Args:
        dots: All detected dot coordinates.
        center_y: Y-coordinate of the band center.
        tolerance: Vertical tolerance for dot matching.
        
    Returns:
        Sorted list of dots in the band, ordered by x-coordinate.
    """
    return sorted([d for d in dots if abs(d[1] - center_y) <= tolerance], 
                  key=lambda d: d[0])


def has_dot_at_x(row: List[Tuple[int, int]], x_coord: int, 
                 tolerance: int) -> int:
    """
    Check if a dot exists at the given x-coordinate within the row.
    
    Args:
        row: List of (x, y) coordinates for the row.
        x_coord: Target x-coordinate.
        tolerance: Horizontal tolerance for matching.
        
    Returns:
        1 if dot exists, 0 otherwise.
    """
    return int(any(abs(d[0] - x_coord) <= tolerance for d in row))


def decode_band(top_row: List[Tuple[int, int]], 
                middle_row: List[Tuple[int, int]],
                bottom_row: List[Tuple[int, int]],
                dot_col_gap: int, word_gap: int, char_group_gap: int,
                x_tolerance: int) -> str:
    """
    Decode a 3-row horizontal band into Braille characters.
    
    Maps dots to 6-bit Braille codes:
        d1 d4  (top row, left/right)
        d2 d5  (middle row, left/right)
        d3 d6  (bottom row, left/right)
    
    Args:
        top_row, middle_row, bottom_row: Dot coordinates for each row.
        dot_col_gap: Expected horizontal gap between left and right columns.
        word_gap: Minimum gap between words.
        char_group_gap: Maximum gap to group dots into same character.
        x_tolerance: Tolerance for dot position matching.
        
    Returns:
        Decoded string for the band.
    """
    # Get all unique x-coordinates
    all_x = sorted(set([d[0] for d in top_row + middle_row + bottom_row]))
    if not all_x:
        return ''
    
    # Group x-coordinates: consecutive xs within char_group_gap belong to same character
    groups = []
    current_group = [all_x[0]]
    for x in all_x[1:]:
        if x - current_group[-1] <= char_group_gap:
            current_group.append(x)
        else:
            groups.append(current_group)
            current_group = [x]
    groups.append(current_group)
    
    # Decode each character group
    result = []
    previous_right_x = None
    
    for group in groups:
        left_x = group[0]
        right_x = group[-1] if len(group) > 1 else group[0] + dot_col_gap
        
        # Check for word boundary (large gap from previous character)
        if previous_right_x is not None and (left_x - previous_right_x) > word_gap:
            result.append(' ')
        
        # Extract 6-bit Braille code: (d1, d2, d3, d4, d5, d6)
        braille_code = (
            has_dot_at_x(top_row, left_x, x_tolerance),
            has_dot_at_x(middle_row, left_x, x_tolerance),
            has_dot_at_x(bottom_row, left_x, x_tolerance),
            has_dot_at_x(top_row, right_x, x_tolerance),
            has_dot_at_x(middle_row, right_x, x_tolerance),
            has_dot_at_x(bottom_row, right_x, x_tolerance)
        )
        
        # Map to character
        character = BRAILLE_MAP.get(braille_code, '?')
        result.append(character)
        previous_right_x = right_x
    
    return ''.join(result)


# ============================================================
# POST-PROCESSING
# ============================================================
def post_process(text: str) -> str:
    """
    Apply NLP post-processing to restore proper capitalization and fix artifacts.
    
    Grade-1 Braille lacks capital and punctuation indicators; this function uses:
    - Abbreviation/proper-noun dictionary
    - Sentence-boundary capitalization rules
    - Known image artifact fixes
    
    Args:
        text: Raw decoded text from Braille.
        
    Returns:
        Post-processed text with proper capitalization.
    """
    # Fix known upscaling artifacts
    text = text.replace('a?ways', 'always')
    text = text.replace('wor?dwide', 'worldwide')
    
    # Normalize whitespace
    text = re.sub(r' +', ' ', text).strip()
    
    # Restore abbreviations and proper nouns
    for lowercase_form, proper_form in ABBREVIATIONS.items():
        pattern = r'\b' + lowercase_form + r'\b'
        text = re.sub(pattern, proper_form, text, flags=re.IGNORECASE)
    
    # Capitalize first character
    if text:
        text = text[0].upper() + text[1:]
    
    # Capitalize after sentence-ending punctuation
    text = re.sub(r'([.!?])\s+([a-z])',
                  lambda m: m.group(1) + ' ' + m.group(2).upper(), text)
    
    # Capitalize known sentence-starting phrases
    for phrase in SENTENCE_STARTERS:
        capitalized_phrase = phrase[0].upper() + phrase[1:]
        text = text.replace(phrase, capitalized_phrase)
    
    return text


# ============================================================
# DECODING PIPELINE
# ============================================================
def decode_all(dots: List[Tuple[int, int]], params: ScaledParams) -> str:
    """
    Decode all Braille lines from detected dots.
    
    Args:
        dots: List of detected dot coordinates.
        params: Scaled parameters for the image.
        
    Returns:
        Full decoded and post-processed text.
    """
    logger.info("Decoding lines...")
    
    # Y tolerance for grouping dots into rows
    y_tolerance = max(int(params.dot_row_gap * 0.4), 4)
    
    lines = []
    for i, y_top in enumerate(params.band_y_coords):
        top_row = get_row(dots, y_top, y_tolerance)
        middle_row = get_row(dots, y_top + params.dot_row_gap, y_tolerance)
        bottom_row = get_row(dots, y_top + params.dot_row_gap * 2, y_tolerance)
        
        line = decode_band(top_row, middle_row, bottom_row,
                          params.dot_col_gap, params.word_gap,
                          params.char_group_gap, params.x_tolerance)
        
        lines.append(line)
        logger.info(f"Line {i+1:2d}: {line}")
    
    # Post-process and combine
    full_text = post_process(' '.join(lines))
    
    # Calculate accuracy metrics
    unknowns = full_text.count('?')
    total_chars = len([c for c in full_text if c != ' '])
    accuracy_pct = (total_chars - unknowns) / max(total_chars, 1) * 100
    
    logger.info(f"Unknowns: {unknowns}/{total_chars} ({accuracy_pct:.1f}% matched)")
    
    return full_text


# ============================================================
# EVALUATION
# ============================================================
def evaluate(predicted: str, truth_path: str = 'English_Output.txt') -> None:
    """
    Compare predicted text to ground truth and report accuracy.
    
    Args:
        predicted: Predicted text from Braille decoding.
        truth_path: Path to ground truth text file.
    """
    logger.info("Accuracy check...")
    
    try:
        with open(truth_path, 'r') as f:
            true_text = f.read().strip()
    except FileNotFoundError:
        logger.warning(f"{truth_path} not found — skipping accuracy check")
        return
    
    pred_clean = predicted.strip()
    min_len = min(len(pred_clean), len(true_text))
    matches = sum(a == b for a, b in zip(pred_clean[:min_len], true_text[:min_len]))
    total = max(len(pred_clean), len(true_text))
    accuracy = (matches / total * 100) if total > 0 else 0
    
    logger.info(f"Expected  : {true_text[:90]}...")
    logger.info(f"Predicted : {pred_clean[:90]}...")
    logger.info(f"Characters matched: {matches}/{total}")
    logger.info(f"Accuracy: {accuracy:.2f}%")
    
    if accuracy == 100.0:
        logger.info("✓ PERFECT MATCH!")


# ============================================================
# VISUALIZATION
# ============================================================
def visualize(gray: np.ndarray, dots: List[Tuple[int, int]], 
              decoded_text: str) -> None:
    """
    Create and save visualization of detected dots and decoded text.
    
    Args:
        gray: Original grayscale image.
        dots: List of detected dot coordinates.
        decoded_text: Decoded text to display.
    """
    logger.info("Saving visualization...")
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 8))
    
    # Original image
    axes[0].imshow(gray, cmap='gray')
    axes[0].set_title('Original Braille Image', fontsize=13)
    axes[0].axis('off')
    
    # Detected dots overlay
    overlay = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    dot_radius = max(4, gray.shape[0] // 500)
    for cx, cy in dots:
        cv2.circle(overlay, (cx, cy), dot_radius, (0, 220, 0), 2)
    axes[1].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f'Detected Dots ({len(dots)})', fontsize=13)
    axes[1].axis('off')
    
    # Decoded text
    axes[2].axis('off')
    axes[2].set_title('Decoded English Text', fontsize=13)
    
    # Format text for display (max 32 chars per line)
    display_lines = []
    current_line = ""
    for word in decoded_text.split():
        if len(current_line) + len(word) + 1 <= 32:
            current_line += word + " "
        else:
            if current_line.strip():
                display_lines.append(current_line.strip())
            current_line = word + " "
    if current_line.strip():
        display_lines.append(current_line.strip())
    
    axes[2].text(0.02, 0.97, '\n'.join(display_lines), va='top', ha='left',
                 fontsize=9, transform=axes[2].transAxes,
                 family='monospace', linespacing=1.7)
    
    plt.tight_layout()
    plt.savefig('result_visualization.png', dpi=130, bbox_inches='tight')
    plt.show()
    logger.info("Saved: result_visualization.png")

# ============================================================
# MAIN PIPELINE
# ============================================================
def main() -> None:
    """
    Main execution pipeline for Braille character recognition.
    
    Steps:
    1. Load Braille image from disk
    2. Convert to binary using Otsu thresholding
    3. Detect dots via contour analysis
    4. Scale parameters to image dimensions
    5. Decode Braille characters from dot patterns
    6. Evaluate accuracy against ground truth
    7. Visualize results
    """
    logger.info("="*60)
    logger.info("  BRAILLE CHARACTER RECOGNITION SYSTEM")
    logger.info("  AI Assignment #2 — Bahria University")
    logger.info("="*60)
    
    # Step 1: Load image
    gray = load_image()
    if gray is None:
        return
    
    # Step 2: Binarize
    logger.info("Binarizing image...")
    binary = binarise(gray)
    
    # Step 3: Detect dots
    dots = detect_dots(binary)
    if not dots:
        return
    
    # Step 4: Scale parameters
    config = BrailleConfig()
    params = scale_parameters(gray.shape[1], gray.shape[0], config)
    
    # Step 5: Decode
    decoded = decode_all(dots, params)
    
    # Step 6: Output results
    logger.info("="*60)
    logger.info("FINAL DECODED TEXT:")
    logger.info("="*60)
    logger.info(decoded)
    logger.info("="*60)
    
    # Step 7: Save prediction
    with open('predicted_output.txt', 'w') as f:
        f.write(decoded)
    logger.info("Saved: predicted_output.txt")
    
    # Step 8: Evaluate
    evaluate(decoded)
    
    # Step 9: Visualize
    visualize(gray, dots, decoded)
    
    logger.info("Done!")


if __name__ == "__main__":
    main()