from PIL import Image, ImageDraw, ImageFont
import math, os

SIZE = 1000
img  = Image.new('RGB', (SIZE, SIZE), (10, 10, 15))
draw = ImageDraw.Draw(img)
cx, cy = SIZE//2, SIZE//2

# Radial gradient background
for r in range(490, 0, -3):
    t  = r / 490
    bv = int(10 + (1-t) * 25)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(bv, bv, bv+12))

# Outer gold ring
draw.ellipse([50, 50, 950, 950], outline=(201,168,76), width=9)
# Inner subtle ring
draw.ellipse([92, 92, 908, 908], outline=(55, 48, 22), width=2)

gold  = (201, 168, 76)
light = (235, 205, 128)

# Geometric F
draw.rectangle([300, 260, 395, 740], fill=gold)   # vertical bar
draw.rectangle([300, 260, 655, 352], fill=gold)   # top bar
draw.rectangle([300, 465, 580, 548], fill=gold)   # mid bar

# Accent squares at bar tips
for (x, y) in [(619, 260), (544, 465)]:
    draw.rectangle([x, y, x+36, y+36], fill=light)
    draw.rectangle([x+8, y+8, x+28, y+28], fill=gold)

# Font detection
font_lg = font_sm = None
for p in [
    '/System/Library/Fonts/Helvetica.ttc',
    '/System/Library/Fonts/HelveticaNeue.ttc',
    '/Library/Fonts/Arial.ttf',
    '/System/Library/Fonts/SFNSText.ttf',
    '/System/Library/Fonts/SFNS.ttf',
]:
    if os.path.exists(p):
        try:
            font_lg = ImageFont.truetype(p, 92)
            font_sm = ImageFont.truetype(p, 32)
            break
        except:
            pass

if not font_lg:
    font_lg = ImageFont.load_default(size=92)
    font_sm = ImageFont.load_default(size=32)

# FRANC label
bb = draw.textbbox((0,0), 'FRANC', font=font_lg)
tw = bb[2] - bb[0]
draw.text(((SIZE-tw)//2, 758), 'FRANC', font=font_lg, fill=gold)

# thefranceway
bb2 = draw.textbbox((0,0), 'thefranceway', font=font_sm)
tw2 = bb2[2] - bb2[0]
draw.text(((SIZE-tw2)//2, 870), 'thefranceway', font=font_sm, fill=(88, 86, 108))

# Corner bracket accents (top-left, bottom-right)
lc, lw = (201,168,76), 4
draw.line([(72,148),(72,72),(148,72)],     fill=lc, width=lw)
draw.line([(852,928),(928,928),(928,852)], fill=lc, width=lw)

out = '/Users/multiuniverse/projects/franc-token/assets/franc-token.png'
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print(f'Saved: {out}')
