from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = Path(__file__).resolve().parent
FRAMES = BASE / "demo-frames"
SLIDES = BASE / "demo-slides"
SLIDES.mkdir(exist_ok=True)
W, H = 1280, 720
GREEN = "#183a2b"
PALE = "#edf2e7"
PAPER = "#fbf8ef"
MUTED = "#55715d"
ACCENT = "#d5e5b3"
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"

def font(size, path=FONT):
    return ImageFont.truetype(path, size)

def lines(draw, text, xy, width, size, fill, bold=False, spacing=12):
    f = font(size, BOLD if bold else FONT)
    x, y = xy
    for paragraph in text.split("\n"):
        words = paragraph.split()
        out, line = [], ""
        for word in words:
            candidate = (line + " " + word).strip()
            if draw.textbbox((0, 0), candidate, font=f)[2] > width and line:
                out.append(line)
                line = word
            else:
                line = candidate
        if line:
            out.append(line)
        for line in out:
            draw.text((x, y), line, font=f, fill=fill)
            y += size + spacing
    return y

def base(step, kicker, title, body, screenshot=None, crop=None):
    im = Image.new("RGB", (W, H), PALE)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 11), fill=GREEN)
    d.text((66, 42), "FIVE-MINUTE FIELD NOTES  /  HACKTOBERFEST 2026", font=font(19, BOLD), fill=MUTED)
    d.rounded_rectangle((52, 109, 635, 670), radius=22, fill="#d5ddd0")
    if screenshot:
        shot = Image.open(FRAMES / screenshot).convert("RGB")
        if crop:
            shot = shot.crop(crop)
        shot.thumbnail((555, 533), Image.Resampling.LANCZOS)
        bx = 66 + (555 - shot.width) // 2
        by = 124 + (532 - shot.height) // 2
        im.paste(shot, (bx, by))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((bx-2, by-2, bx+shot.width+2, by+shot.height+2), radius=8, outline="#96ad98", width=2)
    d.rounded_rectangle((695, 134, 1218, 613), radius=24, fill=PAPER)
    d.text((735, 172), kicker.upper(), font=font(20, BOLD), fill=MUTED)
    y = lines(d, title, (735, 226), 438, 48, GREEN, bold=True, spacing=8)
    lines(d, body, (735, y+37), 427, 27, "#385044", spacing=12)
    d.text((735, 566), f"STEP {step}  /  6", font=font(18, BOLD), fill=MUTED)
    d.rounded_rectangle((52, 683, 52+(step/6)*1166, 690), radius=3, fill=GREEN)
    return im

slides = [
    base(1, "The idea", "A short screen moment. A longer outdoor moment.",
         "Choose a nearby place. Let local AI write a tiny observation mission. Then put the screen away.", "01-start.png"),
    base(2, "Pick a place", "Pick a place you can access.",
         "For this demo: balcony or doorstep, sounds, a seated spot, and five minutes.", "02-selected.png"),
    base(3, "Generate", "Gemma writes the card on this Mac.",
         "The app sends fixed choices to local Ollama. No account, location permission, or cloud AI call.", "03-loading.png"),
    base(4, "The result", "Three cues and one question.",
         "The generated card appears with its model name: gemma3:1b. The content changes with each run.",
         "05-card-in-view.png", (13, 230, 738, 725)),
    base(5, "Touch grass", "Take the card. Leave the screen.",
         "Print it or remember the three cues. Use your judgment outside; the app does not know real conditions.",
         "05-card-in-view.png", (13, 230, 738, 725)),
    base(6, "Run it yourself", "Two commands after installing Ollama.",
         "ollama pull gemma3:1b\npython3 app.py\nOpen http://127.0.0.1:8765", "01-start.png"),
]

for i, slide in enumerate(slides, 1):
    slide.save(SLIDES / f"slide-{i:02}.png", optimize=True)
slides[0].save(BASE.parent / "cover.png", optimize=True)
