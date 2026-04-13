import base64, os, re, sys

# Find any image in assets/
assets_dir = os.path.join(os.path.dirname(__file__), "assets")
if not os.path.exists(assets_dir):
    print("❌ No assets folder found. Make sure it exists next to app.py")
    sys.exit(1)

image_file = None
for f in os.listdir(assets_dir):
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
        image_file = os.path.join(assets_dir, f)
        break

if not image_file:
    print("❌ No image found in assets/ folder.")
    sys.exit(1)

ext = os.path.splitext(image_file)[1].lower().replace(".", "")
if ext == "jpg":
    ext = "jpeg"

print(f"✅ Found image: {image_file}")

with open(image_file, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

data_uri = f"data:image/{ext};base64,{b64}"

# Read app.py
app_path = os.path.join(os.path.dirname(__file__), "app.py")
with open(app_path, "r") as f:
    content = f.read()

# Replace all /assets/logo.png references with embedded base64
new_content = content.replace('"/assets/logo.png"', f'"{data_uri}"')

count = content.count('"/assets/logo.png"')
if count == 0:
    print("❌ No logo references found in app.py — make sure you're using the latest version.")
    sys.exit(1)

with open(app_path, "w") as f:
    f.write(new_content)

print(f"✅ Done! Embedded logo into app.py ({count} places). Restart the app now.")
