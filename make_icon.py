"""Generate icon.ico untuk EduGen app."""
from PIL import Image, ImageDraw, ImageFont
import math

def make_icon():
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background rounded square
    r = 48
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=r,
                            fill=(30, 60, 25, 255))

    # Outer glow ring
    draw.ellipse([18, 18, size-18, size-18], outline=(76, 175, 80, 60), width=3)

    # Lightning bolt ⚡ drawn as polygon
    bolt = [
        (145, 28),
        (95,  118),
        (130, 118),
        (108, 228),
        (168, 128),
        (130, 128),
        (160, 28),
    ]
    draw.polygon(bolt, fill=(102, 187, 106, 255))
    draw.polygon(bolt, outline=(165, 214, 167, 180), width=2)

    # Save multiple sizes as .ico
    sizes = [16, 32, 48, 64, 128, 256]
    icons = []
    for s in sizes:
        icons.append(img.resize((s, s), Image.LANCZOS))

    icons[-1].save(
        "icon.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=icons[:-1],
    )
    print("icon.ico created")

if __name__ == "__main__":
    make_icon()
