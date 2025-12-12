# generate_logo.py
from PIL import Image, ImageDraw, ImageFont
import math
import os
from pathlib import Path

# ======================
# Quick configuration
# ======================
OUT_DIR = Path("LOGOS")  # output folder (created next to where you run the script)
INITIALS = "IGP"
NAME = "IVÁN GÓMEZ PASCUAL"
ROLE = "DATA SCIENTIST | PhD CANDIDATE"

# Palette inspired by a blue/steel UI
NAVY = (10, 32, 56, 255)      # deep navy
CYAN = (30, 144, 255, 255)    # dodger-ish blue
STEEL = (120, 140, 160, 255)  # steel gray
CYAN_SOFT = (30, 144, 255, 120)
STEEL_SOFT = (120, 140, 160, 110)
NAVY_SOFT = (10, 32, 56, 120)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """
    Loads a decent font with cross-platform fallbacks.
    If none are found, falls back to PIL's default bitmap font.
    """
    candidates = [
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        # macOS (common options)
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        # Windows (typical paths)
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
    ]

    for p in candidates:
        if p and os.path.exists(p):
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                pass

    return ImageFont.load_default()


def make_square_logo(size: int = 1024, initials: str = "IGP") -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    cx = cy = size // 2
    r_outer = int(size * 0.40)
    r_mid   = int(size * 0.34)
    r_inner = int(size * 0.27)

    # Concentric rings
    for r, col, w in [
        (r_outer, CYAN_SOFT, int(size * 0.012)),
        (r_mid,   STEEL_SOFT, int(size * 0.010)),
        (r_inner, NAVY_SOFT,  int(size * 0.010)),
    ]:
        bbox = [cx - r, cy - r, cx + r, cy + r]
        d.ellipse(bbox, outline=col, width=w)

    # HUD-like arc segments
    def arc(r: int, start: int, end: int, col, w: int):
        bbox = [cx - r, cy - r, cx + r, cy + r]
        d.arc(bbox, start=start, end=end, fill=col, width=w)

    w1 = int(size * 0.012)
    w2 = int(size * 0.009)
    for a0, a1, col, rr, ww in [
        (300,  30, CYAN,  r_outer, w1),
        (120, 200, STEEL, r_outer, w2),
        (220, 280, CYAN,  r_mid,   w2),
        ( 40,  95, STEEL, r_mid,   w2),
        (155, 205, NAVY,  r_inner, w2),
        (255, 320, CYAN,  r_inner, w2),
    ]:
        arc(rr, a0, a1, col, ww)

    # Radial ticks
    tick_len = int(size * 0.03)
    tick_w   = int(size * 0.006)
    for deg in range(0, 360, 30):
        ang = math.radians(deg)
        x0 = cx + int((r_outer - tick_len) * math.cos(ang))
        y0 = cy + int((r_outer - tick_len) * math.sin(ang))
        x1 = cx + int((r_outer + int(size * 0.008)) * math.cos(ang))
        y1 = cy + int((r_outer + int(size * 0.008)) * math.sin(ang))
        col = CYAN_SOFT if deg % 60 == 0 else STEEL_SOFT
        d.line((x0, y0, x1, y1), fill=col, width=tick_w)

    # Nodes around outer ring
    node_r = int(size * 0.010)
    for deg in [15, 75, 135, 195, 255, 315]:
        ang = math.radians(deg)
        x = cx + int(r_outer * math.cos(ang))
        y = cy + int(r_outer * math.sin(ang))
        d.ellipse((x - node_r, y - node_r, x + node_r, y + node_r), fill=CYAN)

    # Center plate (subtle)
    plate_r = int(size * 0.21)
    d.ellipse(
        (cx - plate_r, cy - plate_r, cx + plate_r, cy + plate_r),
        fill=(255, 255, 255, 20),
        outline=(255, 255, 255, 35),
        width=int(size * 0.004),
    )

    # Initials
    font = load_font(int(size * 0.17), bold=True)
    tb = d.textbbox((0, 0), initials, font=font)
    tw, th = (tb[2] - tb[0]), (tb[3] - tb[1])

    y_shift = int(size * 0.01)
    # textbbox can have non-zero (even negative) left/top offsets depending on font metrics.
    # Compensate those offsets so the rendered glyphs are truly centered.
    d.text(
        (cx - (tw / 2) - tb[0], cy - (th / 2) - tb[1] + y_shift),
        initials,
        font=font,
        fill=NAVY,
    )


    return img


def make_horizontal_logo(
    width: int = 1400,
    height: int = 420,
    name: str = "IVÁN GÓMEZ PASCUAL",
    role: str = "DATA SCIENTIST |PhD CANDIDATE",
) -> Image.Image:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Left: square mark
    mark_size = int(height * 0.90)
    mark = make_square_logo(size=mark_size, initials=INITIALS)
    img.paste(mark, (int(height * 0.05), int((height - mark_size) / 2)), mark)

    # Right: wordmark
    x0 = int(height * 0.05) + mark_size + int(height * 0.07)
    y_center = height // 2

    font_name = load_font(int(height * 0.20), bold=True)
    font_role = load_font(int(height * 0.09), bold=False)

    nb = d.textbbox((0, 0), name, font=font_name)
    nw, nh = nb[2] - nb[0], nb[3] - nb[1]
    d.text((x0, y_center - nh), name, font=font_name, fill=NAVY)

    # Accent underline
    line_y = y_center + int(height * 0.02)
    d.line((x0, line_y, x0 + int(nw * 0.55), line_y), fill=CYAN, width=int(height * 0.02))

    # Role
    d.text((x0, line_y + int(height * 0.04)), role, font=font_role, fill=(10, 32, 56, 200))

    return img


def main():
    # Create output folder next to where you execute the script
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate assets
    square = make_square_logo(1024, INITIALS)
    square_path = OUT_DIR / "logo_square.png"
    square.save(square_path)

    # White background version
    square_white = Image.new("RGBA", square.size, (255, 255, 255, 255))
    square_white.paste(square, (0, 0), square)
    square_white_path = OUT_DIR / "logo_square_white.png"
    square_white.convert("RGB").save(square_white_path)

    # Horizontal
    horiz = make_horizontal_logo(name=NAME, role=ROLE)
    horiz_path = OUT_DIR / "logo_horizontal.png"
    horiz.save(horiz_path)

    # Favicons
    favicon_512 = square.resize((512, 512), resample=Image.LANCZOS)
    favicon_512_path = OUT_DIR / "favicon_512.png"
    favicon_512.save(favicon_512_path)

    favicon_256 = square.resize((256, 256), resample=Image.LANCZOS)
    favicon_256_path = OUT_DIR / "favicon_256.png"
    favicon_256.save(favicon_256_path)

    print("✅ Generated in:", OUT_DIR.resolve())
    print(" -", square_path.name)
    print(" -", square_white_path.name)
    print(" -", horiz_path.name)
    print(" -", favicon_512_path.name)
    print(" -", favicon_256_path.name)


if __name__ == "__main__":
    main()
