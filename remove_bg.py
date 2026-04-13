from PIL import Image
import os, sys

logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

if not os.path.exists(logo_path):
    print("❌ Could not find assets/logo.png")
    sys.exit(1)

img = Image.open(logo_path).convert("RGBA")

# ── New approach: use brightness AS the alpha value directly ──────────────────
# black pixel  (brightness=0)   → alpha=0   (fully transparent)
# white pixel  (brightness=255) → alpha=255 (fully opaque)
# edge pixels                   → semi-transparent (smooth anti-aliasing)
#
# We also force every pixel to pure white so the capybara body
# (which may be dark grey) becomes a bright white outline.
# ─────────────────────────────────────────────────────────────────────────────
brightness = img.convert("L")          # grayscale brightness map

result = Image.new("RGBA", img.size, (255, 255, 255, 255))   # solid white canvas
result.putalpha(brightness)            # brightness → opacity

result.save(logo_path)
print("✅ Done! Background fully removed — pure white outlines, transparent everywhere else.")
print(f"   Saved to: {logo_path}")
