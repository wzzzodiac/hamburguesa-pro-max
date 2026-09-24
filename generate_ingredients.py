"""Render original, transparent ingredient art for the practice game.

Run: python generate_ingredients.py
Requires Inkscape on PATH. The SVG definitions remain editable here; PNGs are
the assets used by the browser.
"""

from pathlib import Path
import subprocess
import random
import math

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "ingredients"
OUT.mkdir(parents=True, exist_ok=True)

DEFS = '''
<defs>
  <linearGradient id="bread" x1="0" y1="0" x2="0.12" y2="1">
    <stop stop-color="#f9ca71"/><stop offset=".47" stop-color="#e7a843"/>
    <stop offset="1" stop-color="#bb742e"/>
  </linearGradient>
  <linearGradient id="crumb" x1="0" y1="0" x2="0" y2="1">
    <stop stop-color="#fff0bf"/><stop offset="1" stop-color="#ebc88d"/>
  </linearGradient>
  <linearGradient id="beef" x1="0" y1="0" x2="0" y2="1">
    <stop stop-color="#704435"/><stop offset=".63" stop-color="#573324"/>
    <stop offset="1" stop-color="#39251f"/>
  </linearGradient>
  <linearGradient id="cheese" x1="0" y1="0" x2="1" y2="1">
    <stop stop-color="#ffe174"/><stop offset=".62" stop-color="#f5c842"/>
    <stop offset="1" stop-color="#df9d29"/>
  </linearGradient>
  <linearGradient id="pickle" x1="0" y1="0" x2="0" y2="1">
    <stop stop-color="#a8ca4c"/><stop offset=".58" stop-color="#779e32"/>
    <stop offset="1" stop-color="#567b29"/>
  </linearGradient>
  <linearGradient id="ketchup" x1="0" y1="0" x2="0" y2="1">
    <stop stop-color="#f25737"/><stop offset=".7" stop-color="#d82c26"/>
    <stop offset="1" stop-color="#a71b20"/>
  </linearGradient>
</defs>
'''


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="192" viewBox="0 0 512 192">{DEFS}{body}</svg>'


def bun_top():
    return svg('''
    <path d="M69 109 C73 44 152 19 255 19 C358 19 437 44 443 109
      Q443 126 423 133 Q256 153 89 133 Q69 126 69 109Z"
      fill="url(#bread)" stroke="#9f612c" stroke-width="4"/>
    <path d="M88 112 Q256 88 424 112 L424 128 Q256 151 88 128Z"
      fill="url(#crumb)" stroke="#a96e35" stroke-width="3"/>
    <path d="M111 88 Q159 39 248 34" fill="none" stroke="#ffe4a1"
      stroke-width="8" stroke-linecap="round" opacity=".43"/>
    <path d="M99 129 Q255 151 413 129" fill="none" stroke="#b27439"
      stroke-width="3" opacity=".45"/>
    ''')


def bun_bottom():
    return svg('''
    <path d="M72 76 Q256 43 440 76 L439 122 Q429 147 255 151
      Q84 147 73 122Z" fill="url(#bread)" stroke="#9f612c" stroke-width="4"/>
    <ellipse cx="256" cy="77" rx="183" ry="36" fill="url(#crumb)"
      stroke="#b47d3d" stroke-width="4"/>
    <ellipse cx="256" cy="74" rx="158" ry="23" fill="#fae6b5" opacity=".52"/>
    <path d="M91 126 Q256 150 422 126" fill="none" stroke="#aa7038"
      stroke-width="3" opacity=".5"/>
    ''')


def patty_beef_10_1():
    rng = random.Random(101)
    specks = []
    for _ in range(185):
        x, y = rng.uniform(82, 429), rng.uniform(64, 129)
        edge = ((x-256)/181)**2 + ((y-93)/49)**2
        if edge < .91:
            tone = rng.choice(("#a9785a", "#d4a36e", "#36231e", "#8c593d"))
            specks.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rng.uniform(1,3):.1f}" ry="{rng.uniform(1,2):.1f}" fill="{tone}" opacity=".55"/>')
    onions = []
    for _ in range(39):
        x, y = rng.uniform(107, 402), rng.uniform(68, 106)
        onions.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{rng.uniform(5,9):.1f}" height="{rng.uniform(3,6):.1f}" rx="1" transform="rotate({rng.randint(-35,35)} {x:.1f} {y:.1f})" fill="#e8d9c0" stroke="#b9ad97" stroke-width=".8"/>')
    return svg('''
      <path d="M74 93 C73 65 154 43 256 43 C358 43 437 65 438 93
      L437 119 C422 143 359 149 256 150 C154 150 90 143 75 119Z"
      fill="url(#beef)" stroke="#30201c" stroke-width="4"/>
      <ellipse cx="256" cy="85" rx="181" ry="46" fill="#67402f"
      stroke="#35221c" stroke-width="4"/>
      <path d="M104 117 Q167 139 232 131 M291 134 Q371 135 409 117"
      fill="none" stroke="#a16a48" stroke-width="3" opacity=".63"/>
    ''' + ''.join(specks) + ''.join(onions))


def cheese():
    return svg('''
    <path d="M70 102 L247 38 L448 100 L271 164Z" fill="url(#cheese)"
      stroke="#bd872c" stroke-width="4" stroke-linejoin="round"/>
    <path d="M70 102 L271 164 L448 100 L448 112 L271 178 L70 114Z"
      fill="#d99b2a" stroke="#ad7420" stroke-width="3" stroke-linejoin="round"/>
    <path d="M91 103 L249 48 L409 99" fill="none" stroke="#ffe991"
      stroke-width="5" opacity=".48" stroke-linecap="round"/>
    ''')


def pickle():
    rng = random.Random(40)
    seeds = []
    for _ in range(13):
        x, y = rng.uniform(194, 316), rng.uniform(65, 106)
        if ((x-256)/78)**2 + ((y-87)/34)**2 < .8:
            seeds.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="5" ry="2" fill="#e3dda3" opacity=".87" transform="rotate({rng.randrange(-50,50)} {x:.1f} {y:.1f})"/>')
    return svg('''
    <ellipse cx="256" cy="110" rx="88" ry="43" fill="#527529"/>
    <path d="M169 89 C174 60 212 41 259 44 C310 45 343 63 344 89
      Q341 122 257 130 Q176 121 169 89Z" fill="url(#pickle)"
      stroke="#496c2b" stroke-width="5"/>
    <ellipse cx="256" cy="87" rx="70" ry="27" fill="#bad16f"
      stroke="#719744" stroke-width="3"/>
    <ellipse cx="256" cy="87" rx="47" ry="17" fill="#d7d893" opacity=".67"/>
    ''' + ''.join(seeds))


def lettuce():
    rng = random.Random(4)
    leaves = []
    for j, (dx, dy, rot) in enumerate(((-103,10,-17),(-50,-2,-9),(4,8,7),(58,-1,15),(102,10,23))):
        x, y = 256+dx, 87+dy
        points = []
        for k in range(32):
            a = 2 * math.pi * k / 32
            # Uneven toothed edges read as torn lettuce in a small sprite.
            radius = (49 if k % 2 == 0 else 35) * rng.uniform(.78, 1.14)
            points.append(f'{x + radius * math.cos(a):.1f},{y + radius * .72 * math.sin(a):.1f}')
        paths = [
          f'<polygon points="{" ".join(points)}" fill="{("#71ab41","#83b94c","#6fa43d")[j%3]}" stroke="#396b34" stroke-width="3" stroke-linejoin="round" transform="rotate({rot} {x} {y})"/>',
          f'<path d="M{x-28} {y+10} Q{x} {y+5} {x+29} {y-17} M{x} {y+5} L{x-8} {y-17} M{x+14} {y-3} L{x+24} {y+20}" fill="none" stroke="#c6dc81" stroke-width="2.5" opacity=".8" transform="rotate({rot} {x} {y})"/>'
        ]
        leaves.extend(paths)
    return svg(''.join(leaves))


def ketchup():
    return svg('''
    <path d="M127 111 Q133 94 153 98 Q157 77 177 81 Q193 57 210 78
      Q225 46 244 73 Q264 44 284 72 Q306 56 319 83 Q344 73 353 99
      Q379 101 386 116 Q386 139 321 142 L190 142 Q126 139 127 111Z"
      fill="url(#ketchup)" stroke="#a32420" stroke-width="4"/>
    <path d="M158 106 Q169 91 182 104 M218 80 Q229 70 241 84
      M267 81 Q280 67 294 84 M325 103 Q340 91 353 109"
      fill="none" stroke="#ff8060" stroke-width="5" opacity=".68"
      stroke-linecap="round"/>
    <path d="M153 124 Q260 151 358 124" fill="none" stroke="#a81f1b"
      stroke-width="3" opacity=".45"/>
    ''')


ART = {
    "bun_hamburger_oberteil": bun_top,
    "bun_hamburger_unterteil": bun_bottom,
    "patty_beef_10_1": patty_beef_10_1,
    "cheese_standard": cheese,
    "salzgurke": pickle,
    "eisbergsalat": lettuce,
    "sauce_ketchup": ketchup,
}


if __name__ == "__main__":
    for name, draw in ART.items():
        svg_path = OUT / f"{name}.svg"
        png_path = OUT / f"{name}.png"
        svg_path.write_text(draw(), encoding="utf-8")
        subprocess.run(["inkscape", str(svg_path), "--export-type=png",
                        f"--export-filename={png_path}"], check=True,
                       stdout=subprocess.DEVNULL)
        print(png_path)
