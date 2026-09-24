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


def add_grains(base, kind, count, seed):
    rng = random.Random(seed)
    marks = []
    for _ in range(count):
        x, y = rng.uniform(105, 408), rng.uniform(43, 113)
        # Grains stay above the cream-coloured cut face.
        if kind == "dome" and ((x-256)/175)**2 + ((y-105)/82)**2 > .83:
            continue
        color = rng.choice(("#fff1be", "#fbe4a2", "#e9cd80")) if kind == "dome" else rng.choice(("#5c4d3e", "#a98758", "#f5e4af"))
        marks.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rng.uniform(2,4):.1f}" ry="{rng.uniform(1,2):.1f}" fill="{color}" transform="rotate({rng.randint(-70,70)} {x:.1f} {y:.1f})"/>')
    return base.replace("</svg>", ''.join(marks) + "</svg>")


def muffin_top():
    return svg('''
    <path d="M94 78 Q105 42 252 39 Q405 40 419 79 L418 117
      Q408 142 255 144 Q103 141 94 117Z" fill="#d7b275"
      stroke="#986f3f" stroke-width="4"/>
    <ellipse cx="256" cy="81" rx="162" ry="41" fill="#e5c997"
      stroke="#a77c45" stroke-width="4"/>
    <path d="M100 112 Q256 132 413 112" fill="none" stroke="#a27543" stroke-width="3"/>
    <path d="M154 78 Q203 49 270 60 Q320 48 354 77 Q318 99 255 95
      Q192 105 154 78Z" fill="#ffde74" opacity=".92" stroke="#d9ad4b" stroke-width="2"/>
    <path d="M159 113 Q256 130 410 113" fill="none" stroke="#f6dcab" stroke-width="5" opacity=".6"/>
    ''')


def muffin_bottom():
    rng = random.Random(39)
    dots = ''.join(f'<ellipse cx="{rng.uniform(111,403):.1f}" cy="{rng.uniform(72,114):.1f}" rx="{rng.uniform(1,4):.1f}" ry="{rng.uniform(1,2):.1f}" fill="{rng.choice(("#906d4c","#c2a17b","#fff2c9"))}" opacity=".7"/>' for _ in range(50))
    return svg('''
    <path d="M91 79 Q97 54 255 52 Q416 53 421 79 L418 118
      Q405 144 257 145 Q108 143 93 118Z" fill="#bc8b5e"
      stroke="#815d3c" stroke-width="4"/>
    <ellipse cx="256" cy="75" rx="163" ry="36" fill="#dfc19a"
      stroke="#9b7650" stroke-width="4"/>
    <ellipse cx="255" cy="76" rx="136" ry="25" fill="#f2ddb4" opacity=".68"/>
    ''' + dots)


def grain_top():
    return add_grains(bun_top(), "mixed", 94, 123)


def grain_bottom():
    return add_grains(bun_bottom(), "mixed", 55, 43)


def royal_top():
    return add_grains(bun_top(), "dome", 43, 85)


def royal_bottom():
    return bun_bottom()


def big_mac_top():
    return add_grains(bun_top(), "dome", 69, 57)


def big_mac_middle():
    return svg('''
    <path d="M77 75 Q256 46 435 75 L433 111 Q419 137 257 139
      Q92 137 79 111Z" fill="url(#bread)" stroke="#9f612c" stroke-width="4"/>
    <ellipse cx="256" cy="75" rx="179" ry="32" fill="url(#crumb)"
      stroke="#b47d3d" stroke-width="3"/>
    <path d="M108 113 Q256 136 405 113" fill="none" stroke="#f8d997"
      stroke-width="4" opacity=".55"/>
    ''')


def big_mac_bottom():
    return bun_bottom()


def tasty_top():
    return svg('''
    <path d="M60 111 C60 42 148 16 256 17 C363 16 450 42 452 111
      Q451 135 426 139 Q255 159 87 139 Q61 136 60 111Z"
      fill="url(#bread)" stroke="#9c5e29" stroke-width="4"/>
    <path d="M78 117 Q256 97 434 117 L433 138 Q256 159 79 138Z"
      fill="url(#crumb)" stroke="#ae7334" stroke-width="3"/>
    <path d="M115 77 Q168 34 249 31" fill="none" stroke="#ffe09a" stroke-width="9" opacity=".42" stroke-linecap="round"/>
    ''')


def tasty_bottom():
    return svg('''
    <path d="M60 71 Q255 35 452 71 L451 121 Q440 148 255 155
      Q73 148 61 121Z" fill="url(#bread)" stroke="#9c5e29" stroke-width="4"/>
    <ellipse cx="256" cy="73" rx="195" ry="38" fill="url(#crumb)"
      stroke="#ad753b" stroke-width="4"/>
    <ellipse cx="256" cy="72" rx="164" ry="24" fill="#fff0be" opacity=".44"/>
    ''')


def long_bun_top(crispy=False):
    col = "#e9a754" if crispy else "#d99a52"
    details = '<path d="M148 46 Q221 26 305 39 M119 92 Q256 76 390 89" fill="none" stroke="#ffe3a5" stroke-width="7" opacity=".45" stroke-linecap="round"/>' if crispy else '<path d="M117 95 Q257 74 394 95" fill="none" stroke="#f9ca87" stroke-width="6" opacity=".47"/>'
    return svg(f'''
    <path d="M52 100 Q58 45 143 37 Q256 22 369 37 Q453 47 460 100
      Q460 129 423 139 Q256 159 89 139 Q52 130 52 100Z"
      fill="{col}" stroke="#a16736" stroke-width="4"/>
    <path d="M70 115 Q256 99 442 115 L437 136 Q256 157 75 136Z"
      fill="url(#crumb)" stroke="#ad733d" stroke-width="3"/>{details}
    ''')


def long_bun_bottom(crispy=False):
    col = "#dc9f59" if crispy else "#ce9052"
    return svg(f'''
    <path d="M56 81 Q256 45 456 81 L453 120 Q437 149 256 154
      Q75 149 58 120Z" fill="{col}" stroke="#9a6438" stroke-width="4"/>
    <ellipse cx="256" cy="80" rx="200" ry="38" fill="url(#crumb)"
      stroke="#ac7542" stroke-width="4"/>
    <ellipse cx="256" cy="79" rx="169" ry="23" fill="#fff1c4" opacity=".42"/>
    ''')


def wrap_tortilla():
    rng = random.Random(56)
    spots = []
    for _ in range(60):
        x,y=rng.uniform(85,427),rng.uniform(54,139)
        if ((x-256)/204)**2+((y-94)/68)**2<.88:
            spots.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rng.uniform(1,5):.1f}" ry="{rng.uniform(1,2.5):.1f}" fill="{rng.choice(("#b78658","#d3a76c","#e9d1a8"))}" opacity=".5"/>')
    return svg('''
    <ellipse cx="256" cy="100" rx="208" ry="68" fill="#c99b66"
      stroke="#966c47" stroke-width="4"/>
    <ellipse cx="256" cy="91" rx="208" ry="68" fill="#ead2a5"
      stroke="#b68b5b" stroke-width="4"/>
    <ellipse cx="256" cy="91" rx="184" ry="53" fill="#f4e0b8" opacity=".56"/>
    '''+''.join(spots))


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


def beef_large(size):
    rng = random.Random(301+size)
    left, right = (61,451) if size == 4 else (46,466)
    grains=[]
    for _ in range(175):
        x,y=rng.uniform(left+12,right-12),rng.uniform(57,121)
        if ((x-256)/((right-left)/2))**2+((y-89)/47)**2<.9:
            grains.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rng.uniform(1,3):.1f}" ry="{rng.uniform(1,2):.1f}" fill="{rng.choice(("#9a6547","#bc8964","#33211b"))}" opacity=".6"/>')
    return svg(f'''
      <path d="M{left} 92 Q{left} 47 256 39 Q{right} 47 {right} 92
      L{right-3} 121 Q256 162 {left+3} 121Z" fill="url(#beef)"
      stroke="#35231d" stroke-width="4"/>
      <ellipse cx="256" cy="89" rx="{(right-left)/2}" ry="48"
      fill="#67402e" stroke="#38251f" stroke-width="4"/>
      <path d="M{left+31} 121 Q256 151 {right-28} 121" fill="none"
      stroke="#a66c48" stroke-width="3" opacity=".6"/>
    '''+''.join(grains))


def sausage_patty():
    rng=random.Random(98)
    crumbs=''.join(f'<ellipse cx="{rng.uniform(120,390):.1f}" cy="{rng.uniform(64,121):.1f}" rx="{rng.uniform(2,5):.1f}" ry="2" fill="{rng.choice(("#8a5136","#d19065","#5d3628"))}" opacity=".7"/>' for _ in range(92))
    return svg('''<path d="M90 94 Q90 49 256 43 Q421 49 422 94 L421 119 Q255 158 91 119Z" fill="#935b3e" stroke="#593729" stroke-width="4"/><ellipse cx="256" cy="89" rx="166" ry="46" fill="#a36c49" stroke="#69402c" stroke-width="4"/>'''+crumbs)


def pork_mcrib():
    return svg('''
    <path d="M67 74 Q81 50 136 48 L375 48 Q429 49 445 73 L442 126
      Q427 151 368 149 L138 149 Q74 147 67 123Z" fill="#764034"
      stroke="#472722" stroke-width="4"/>
    <path d="M91 70 Q117 54 155 55 L359 55 Q402 54 421 70
      M93 128 Q257 145 418 128" fill="none" stroke="#b56a46"
      stroke-width="10" opacity=".6" stroke-linecap="round"/>
    <path d="M151 60 Q133 89 153 138 M222 56 Q207 90 224 142
      M295 55 Q279 90 295 141 M365 58 Q349 90 365 137"
      fill="none" stroke="#42241f" stroke-width="9" opacity=".55"/>
    <path d="M81 77 Q260 67 429 80" fill="none" stroke="#d48357"
      stroke-width="4" opacity=".6"/>
    ''')


def fried_patty(kind, half=False):
    rng=random.Random({"tempura":11,"classic":23,"mccrispy":42,"fish":61,"veggie":82}[kind]+int(half))
    colors={"tempura":("#e9bd62","#bd8a3c"),"classic":("#dfa945","#ac762f"),"mccrispy":("#be8c4e","#805935"),"fish":("#d1a45a","#936e38"),"veggie":("#c49d58","#8c703e")}
    main,edge=colors[kind]
    if half:
        outline='M129 84 Q130 54 224 50 L342 57 L342 128 Q225 148 151 132 Q129 121 129 84Z'
    elif kind=="fish":
        outline='M97 56 Q118 40 155 44 L369 44 Q410 42 422 66 L420 121 Q403 146 360 143 L153 143 Q105 142 95 122Z'
    elif kind=="mccrispy":
        outline='M63 92 Q58 64 93 56 Q115 33 150 50 Q187 30 219 44 Q258 32 292 48 Q333 36 364 57 Q415 48 441 81 Q451 113 417 126 Q398 152 361 138 Q328 155 285 143 Q250 155 211 140 Q168 156 133 135 Q83 149 63 116Z'
    else:
        outline='M70 86 Q68 60 107 55 Q128 39 160 49 Q201 34 239 45 Q276 33 310 48 Q345 36 377 54 Q426 52 443 80 Q451 110 418 127 Q385 149 355 138 Q313 151 281 141 Q244 150 213 139 Q167 150 133 135 Q87 141 70 115Z'
    specks=[]
    for _ in range(270):
        x,y=rng.uniform(139 if half else 84,335 if half else 409),rng.uniform(55,128)
        shade=rng.choice(("#fbe0a3","#8f6d38","#7f9950","#674d30")) if kind=="veggie" else rng.choice(("#ffe8a9","#a5793c","#875d2f"))
        specks.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rng.uniform(1,3.5):.1f}" ry="{rng.uniform(1,2.3):.1f}" fill="{shade}" opacity=".55"/>')
    clip='<clipPath id="patty-clip"><path d="'+outline+'"/></clipPath>'
    cut=f'<path d="M342 57 L342 128" stroke="#fbdda3" stroke-width="8" opacity=".68"/>' if half else ''
    return svg(f'<defs>{clip}</defs><path d="{outline}" fill="{main}" stroke="{edge}" stroke-width="5" stroke-linejoin="round"/><g clip-path="url(#patty-clip)">{"".join(specks)}</g>{cut}')


def round_egg():
    return svg('''
    <path d="M84 100 Q72 63 125 59 Q165 40 203 61 Q248 31 291 57
      Q344 41 376 68 Q432 58 431 104 Q433 141 370 140 Q317 157 266 139
      Q207 158 162 138 Q99 150 84 100Z" fill="#fff9e8"
      stroke="#d3ccb2" stroke-width="4"/>
    <ellipse cx="256" cy="97" rx="65" ry="42" fill="#f4b52e"
      stroke="#da9221" stroke-width="4"/>
    <ellipse cx="239" cy="77" rx="23" ry="10" fill="#fff4b1" opacity=".6"/>
    ''')


def scrambled_egg():
    rng=random.Random(31)
    lumps=[]
    for _ in range(35):
        x,y=rng.uniform(110,407),rng.uniform(81,121)
        lumps.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rng.uniform(11,25):.1f}" ry="{rng.uniform(5,11):.1f}" fill="{rng.choice(("#f8c444","#ffdc6d","#e7aa31"))}" stroke="#d69b31" stroke-width="1"/>')
    return svg('<path d="M82 122 Q103 97 140 104 Q160 72 195 92 Q224 57 258 82 Q286 65 315 89 Q350 70 376 104 Q418 99 433 123 Q433 149 255 147 Q83 148 82 122Z" fill="#e5a430" stroke="#bc7f25" stroke-width="4"/>'+''.join(lumps))


def bacon_strip():
    return svg('''
    <path d="M61 96 C110 45 165 112 218 73 C274 38 338 105 451 55
      L451 93 C342 142 291 72 232 116 C159 158 119 83 62 135Z"
      fill="#ad4e40" stroke="#79392f" stroke-width="4"/>
    <path d="M65 106 C117 57 164 121 222 85 C287 48 336 114 447 70"
      fill="none" stroke="#f4d4b0" stroke-width="16" opacity=".91"/>
    <path d="M71 124 C129 79 170 144 233 101 C290 62 348 134 446 86"
      fill="none" stroke="#dc947d" stroke-width="5" opacity=".8"/>
    ''')


def cheese():
    return svg('''
    <path d="M70 102 L247 38 L448 100 L271 164Z" fill="url(#cheese)"
      stroke="#bd872c" stroke-width="4" stroke-linejoin="round"/>
    <path d="M70 102 L271 164 L448 100 L448 112 L271 178 L70 114Z"
      fill="#d99b2a" stroke="#ad7420" stroke-width="3" stroke-linejoin="round"/>
    <path d="M91 103 L249 48 L409 99" fill="none" stroke="#ffe991"
      stroke-width="5" opacity=".48" stroke-linecap="round"/>
    ''')


def cheese_half():
    return svg('''
    <path d="M117 106 L279 46 L395 113 L252 160Z" fill="url(#cheese)"
      stroke="#bd872c" stroke-width="4" stroke-linejoin="round"/>
    <path d="M117 106 L252 160 L395 113 L395 126 L252 173 L117 119Z"
      fill="#d99b2a" stroke="#ad7420" stroke-width="3"/>
    <path d="M133 106 L278 56" stroke="#ffe991" stroke-width="5"
      opacity=".5" stroke-linecap="round"/>
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


def tomato():
    rng=random.Random(12)
    seeds=[]
    for _ in range(14):
        x,y=rng.uniform(186,326),rng.uniform(72,108)
        seeds.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="4" ry="2" fill="#ffe5a0" opacity=".8" transform="rotate({rng.randrange(-70,70)} {x:.1f} {y:.1f})"/>')
    return svg('''
    <ellipse cx="256" cy="113" rx="109" ry="44" fill="#a9232a"/>
    <ellipse cx="256" cy="88" rx="111" ry="49" fill="#ec5151"
      stroke="#b72c33" stroke-width="5"/>
    <ellipse cx="256" cy="88" rx="88" ry="34" fill="#f07569"
      stroke="#d03e43" stroke-width="3"/>
    <ellipse cx="256" cy="88" rx="47" ry="20" fill="#eb4146"/>
    '''+''.join(seeds))


def onion_fresh():
    parts=[]
    for i,(x,y,rot) in enumerate(((123,86,-15),(200,72,7),(274,91,-8),(340,70,14))):
        parts.append(f'<g transform="rotate({rot} {x} {y})"><path d="M{x-52} {y+32} Q{x-26} {y-41} {x+45} {y-23} Q{x+8} {y-14} {x-15} {y+35}Z" fill="#fff8dd" stroke="#c1b9a3" stroke-width="4"/><path d="M{x-39} {y+18} Q{x-11} {y-27} {x+29} {y-22}" fill="none" stroke="#d8d1bc" stroke-width="3"/></g>')
    return svg(''.join(parts))


def crispy_onions():
    rng=random.Random(117)
    bits=[]
    for _ in range(105):
        x,y=rng.gauss(255,81),rng.gauss(107,22)
        if 84<x<429 and 60<y<151:
            c=rng.choice(("#ae7137","#d29b4a","#efc167","#734a29"))
            bits.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{rng.uniform(5,15):.1f}" height="{rng.uniform(2,5):.1f}" rx="1.5" fill="{c}" transform="rotate({rng.randint(-65,65)} {x:.1f} {y:.1f})"/>')
    return svg(''.join(bits))


def jalapeno():
    rng=random.Random(25)
    seeds=[]
    for _ in range(17):
        x,y=rng.uniform(196,317),rng.uniform(70,108)
        seeds.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="3" ry="2" fill="#f4e9bd"/>')
    return svg('''
    <ellipse cx="256" cy="105" rx="92" ry="42" fill="#315d25"/>
    <ellipse cx="256" cy="86" rx="92" ry="43" fill="#4e993f"
      stroke="#2b662c" stroke-width="5"/>
    <ellipse cx="256" cy="86" rx="66" ry="27" fill="#b8d892"
      stroke="#49913f" stroke-width="4"/>
    <ellipse cx="256" cy="86" rx="38" ry="17" fill="#edf1bd"/>
    '''+''.join(seeds))


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


def sauce(color, dark, light, style):
    rng=random.Random(sum(ord(c) for c in style))
    flecks=[]
    if style in ("tartar", "big_mac", "big_tasty", "honig_senf", "sweet_chili", "hot_chili_cheese", "breakfast"):
        for _ in range(26):
            x,y=rng.uniform(153,358),rng.uniform(92,128)
            shade={"tartar":"#6f9a5a","big_mac":"#d99063","big_tasty":"#884d30","honig_senf":"#9a6925","sweet_chili":"#c53b25","hot_chili_cheese":"#d96f2e","breakfast":"#a9784e"}[style]
            flecks.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rng.uniform(1,2.5):.1f}" fill="{shade}" opacity=".7"/>')
    return svg(f'''
      <path d="M124 118 Q130 96 156 97 Q167 66 190 83 Q209 56 229 78
      Q255 44 275 80 Q299 59 315 85 Q338 74 353 102 Q382 101 390 119
      Q385 141 324 144 L185 144 Q126 141 124 118Z" fill="{color}"
      stroke="{dark}" stroke-width="4"/>
      <path d="M157 106 Q180 79 200 104 M230 85 Q251 59 270 89
      M301 95 Q330 79 348 108" fill="none" stroke="{light}"
      stroke-width="5" opacity=".7" stroke-linecap="round"/>
      {''.join(flecks)}
      ''')


ART = {
    "bun_hamburger_oberteil": bun_top,
    "bun_hamburger_unterteil": bun_bottom,
    "patty_beef_10_1": patty_beef_10_1,
    "cheese_standard": cheese,
    "salzgurke": pickle,
    "eisbergsalat": lettuce,
    "sauce_ketchup": ketchup,
    "bun_mcmuffin_oberteil": muffin_top,
    "bun_mcmuffin_unterteil": muffin_bottom,
    "bun_koernerbroetchen_oberteil": grain_top,
    "bun_koernerbroetchen_unterteil": grain_bottom,
    "bun_hamburger_royal_oberteil": royal_top,
    "bun_hamburger_royal_unterteil": royal_bottom,
    "bun_big_mac_oberteil": big_mac_top,
    "bun_big_mac_mittelteil": big_mac_middle,
    "bun_big_mac_unterteil": big_mac_bottom,
    "bun_big_tasty_oberteil": tasty_top,
    "bun_big_tasty_unterteil": tasty_bottom,
    "bun_mcrib_oberteil": lambda: long_bun_top(False),
    "bun_mcrib_unterteil": lambda: long_bun_bottom(False),
    "bun_mccrispy_oberteil": lambda: long_bun_top(True),
    "bun_mccrispy_unterteil": lambda: long_bun_bottom(True),
    "wrap_tortilla": wrap_tortilla,
    "patty_beef_4_1": lambda: beef_large(4),
    "patty_beef_3_1": lambda: beef_large(3),
    "patty_sausage": sausage_patty,
    "patty_pork_mcrib": pork_mcrib,
    "patty_chicken_tempura": lambda: fried_patty("tempura"),
    "patty_chicken_classic": lambda: fried_patty("classic"),
    "patty_chicken_classic_half": lambda: fried_patty("classic",True),
    "patty_mccrispy": lambda: fried_patty("mccrispy"),
    "patty_filet_o_fish": lambda: fried_patty("fish"),
    "patty_veggie": lambda: fried_patty("veggie"),
    "patty_veggie_half": lambda: fried_patty("veggie",True),
    "round_egg": round_egg,
    "ruehrei": scrambled_egg,
    "bacon_streifen": bacon_strip,
    "cheese_standard_half": cheese_half,
    "tomate": tomato,
    "zwiebeln_frisch_weiss": onion_fresh,
    "crispy_onions": crispy_onions,
    "jalapenos": jalapeno,
    "sauce_sandwich": lambda: sauce("#f9f4e9","#d1c6b5","#ffffff","sandwich"),
    "sauce_breakfast": lambda: sauce("#c39263","#986941","#e7c49b","breakfast"),
    "sauce_senf": lambda: sauce("#f1c52f","#ba8c20","#ffe47b","senf"),
    "sauce_big_mac": lambda: sauce("#e2ad83","#b97759","#f9d7af","big_mac"),
    "sauce_big_tasty": lambda: sauce("#be8054","#895332","#dfab75","big_tasty"),
    "sauce_honig_senf": lambda: sauce("#d6af55","#9d7739","#f6d885","honig_senf"),
    "sauce_tartar": lambda: sauce("#f6f2e2","#b8baa5","#ffffff","tartar"),
    "sauce_sweet_chili": lambda: sauce("#e46d39","#b74324","#ffa567","sweet_chili"),
    "sauce_hot_chili_cheese": lambda: sauce("#efad27","#bc7222","#ffdc5f","hot_chili_cheese"),
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
