#!/usr/bin/env python3
"""Render original, conceptual project diagrams as looping GIFs and PNG posters.

Run: python3 github-pages/scripts/build-project-motion.py [project-id ...]
Requires Pillow. No downloaded images, model output, or experiment results are used.
Every motion is periodic; frame 48 would equal frame 0. 48 frames × 80 ms = 3.84 s.
"""
from pathlib import Path
import json
import math
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'project-motion'
W, H, SCALE, FRAMES = 600, 260, 2, 48
BG = '#f0f4ee'
WHITE = '#fbfcf8'
INK = '#174e3d'
TEAL = '#318c80'
MINT = '#9bc6af'
PALE = '#d6e5d8'
LINE = '#b4cbbb'
MUTED = '#61796a'
AMBER = '#b99458'
LAV = '#9884ad'


def rgb(c):
    return tuple(int(c[k:k+2], 16) for k in (1, 3, 5)) if isinstance(c, str) else c


def mix(a, b, t):
    t = max(0, min(1, t))
    return tuple(round(x + (y-x)*t) for x, y in zip(rgb(a), rgb(b)))


def pulse(t, offset=0):
    return .5 + .5*math.sin(math.tau*(t-offset))


def smooth(t):
    t = max(0, min(1, t))
    return t*t*(3-2*t)


def font_path(bold=False):
    choices = [
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
    ]
    return next((str(p) for p in map(Path, choices) if p.exists()), None)


FONTS = {(size, bold): ImageFont.truetype(font_path(bold), size*SCALE) if font_path(bold) else ImageFont.load_default(size=size*SCALE)
         for size in [11, 12, 13, 14, 15, 16, 17, 18, 20] for bold in [False, True]}


class Canvas:
    def __init__(self, title, detail):
        self.im = Image.new('RGB', (W*SCALE, H*SCALE), BG)
        self.d = ImageDraw.Draw(self.im)
        self.label(25, 20, title, 12, INK, True)
        # Restrained framing: the little activity mark is part of the diagram.
        self.line([(25, 44), (575, 44)], LINE, .6)
        self.label(25, 236, detail, 11, MUTED)

    def box(self, bounds, fill=WHITE, stroke=LINE, radius=8, width=1):
        b = [round(v*SCALE) for v in bounds]
        self.d.rounded_rectangle(b, radius=radius*SCALE, fill=rgb(fill) if fill else None,
                                 outline=rgb(stroke) if stroke else None, width=max(1, round(width*SCALE)))

    def rect(self, bounds, fill, stroke=None, width=1):
        self.d.rectangle([round(v*SCALE) for v in bounds], fill=rgb(fill),
                         outline=rgb(stroke) if stroke else None, width=max(1, round(width*SCALE)))

    def line(self, points, fill=INK, width=1.5):
        self.d.line([(round(x*SCALE), round(y*SCALE)) for x, y in points], fill=rgb(fill), width=max(1, round(width*SCALE)), joint='curve')

    def poly(self, points, fill, stroke=None, width=1):
        p = [(round(x*SCALE), round(y*SCALE)) for x, y in points]
        self.d.polygon(p, fill=rgb(fill))
        if stroke:
            self.d.line(p+[p[0]], fill=rgb(stroke), width=max(1, round(width*SCALE)), joint='curve')

    def circle(self, x, y, r, fill, stroke=None, width=1):
        self.d.ellipse([round(v*SCALE) for v in (x-r, y-r, x+r, y+r)], fill=rgb(fill) if fill else None,
                       outline=rgb(stroke) if stroke else None, width=max(1, round(width*SCALE)))

    def label(self, x, y, text, size=13, fill=INK, bold=False, center=False):
        self.d.text((round(x*SCALE), round(y*SCALE)), text, font=FONTS[(size, bold)], fill=rgb(fill), anchor='mt' if center else 'lt')

    def arrow(self, points, fill=LINE, width=1.5):
        self.line(points, fill, width)
        (x0, y0), (x, y) = points[-2:]
        a = math.atan2(y-y0, x-x0)
        self.line([(x-6*math.cos(a-.55), y-6*math.sin(a-.55)), (x, y), (x-6*math.cos(a+.55), y-6*math.sin(a+.55))], fill, width)

    def wave(self, x, y, w, amplitude, phase, color=TEAL, frequency=3, kind='sine', width=1.7):
        pts = []
        for i in range(round(w)+1):
            s = i/w
            q = (s*frequency-phase) % 1
            if kind == 'ecg':
                val = (.16*math.exp(-((q-.20)/.055)**2) - .22*math.exp(-((q-.40)/.022)**2)
                       + 1.1*math.exp(-((q-.45)/.014)**2) - .38*math.exp(-((q-.49)/.025)**2)
                       + .26*math.exp(-((q-.70)/.09)**2))
            elif kind == 'neural':
                val = math.sin(math.tau*q)*(.65+.25*math.sin(math.tau*(2*s-phase))) + .15*math.sin(math.tau*(11*s-phase))
            else:
                val = math.sin(math.tau*q)
            pts.append((x+i, y-amplitude*val))
        self.line(pts, color, width)

    def finish(self):
        return self.im.resize((W, H), Image.Resampling.LANCZOS)


def grid(c, x, y, cols, rows, cell=18, gap=5, t=0, mode='wave'):
    for row in range(rows):
        for col in range(cols):
            v = pulse(t, (col+row*.65)/(cols+rows))
            fill = mix(PALE, TEAL, .12+.74*v)
            if mode == 'static':
                fill = mix(PALE, TEAL, ((col*7+row*3)%11)/14)
            c.box((x+col*(cell+gap), y+row*(cell+gap), x+col*(cell+gap)+cell, y+row*(cell+gap)+cell), fill, None, 3)


def dot_along(c, points, t, color=TEAL, radius=3.5):
    lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
    q = (t % 1)*sum(lengths)
    for (a, b), ln in zip(zip(points, points[1:]), lengths):
        if q <= ln:
            f = q/ln
            c.circle(a[0]+f*(b[0]-a[0]), a[1]+f*(b[1]-a[1]), radius, color)
            return
        q -= ln


def softskill(t):
    c = Canvas('COMPACT SKILL REPRESENTATION', 'Text instructions distilled into a compact learned representation')
    c.box((48, 67, 191, 202), WHITE, LINE, 10)
    for r in range(6):
        for col, width in enumerate([31, 38, 24]):
            x = 64+[0, 39, 85][col]
            shade = mix(PALE, MINT, pulse(t, r/6+col*.17)*.7)
            c.box((x, 84+r*17, x+width, 92+r*17), shade, None, 3)
    c.label(120, 211, 'Text skill', 12, center=True)
    for row in range(3):
        path = [(202, 103+row*27), (254, 103+row*27), (302, 130), (339, 130)]
        c.line(path, PALE, 1)
        u = (t+row/3) % 1
        x = 207+u*122
        y = 103+row*27+(130-(103+row*27))*smooth(u)
        c.box((x-6, y-3, x+6, y+3), mix(BG, TEAL, math.sin(math.pi*u)), None, 2)
    c.box((347, 67, 553, 202), WHITE, LINE, 10)
    grid(c, 366, 83, 8, 4, 17, 6, t)
    c.label(450, 211, '32 learned vectors', 12, center=True)
    return c.finish()


def edgealign(t):
    c = Canvas('LEARNING FROM EXECUTION', 'Tool outcomes guide updates to a compact skill subspace')
    points = [(142, 105), (444, 105), (466, 169), (301, 207), (132, 169), (142, 105)]
    c.line(points, LINE, 1.5)
    for j in range(3):
        dot_along(c, points, t+j/3, TEAL, 4)
    for x, y, title, offset in [(120, 73, 'Agent', 0), (403, 73, 'Tools', .33), (255, 181, 'Feedback', .66)]:
        width = 98 if title == 'Feedback' else 82
        c.box((x, y, x+width, y+48), mix(WHITE, PALE, pulse(t, offset)*.55), LINE, 9)
        c.label(x+width/2, y+16, title, 14, INK, True, True)
    c.box((250, 72, 345, 159), WHITE, LINE, 8)
    grid(c, 264, 83, 4, 3, 12, 6, t)
    c.label(298, 145, 'Skill state', 11, MUTED, center=True)
    c.line([(202, 97), (244, 97)], LINE)
    c.line([(350, 97), (396, 97)], LINE)
    c.line([(300, 164), (300, 174)], LINE)
    return c.finish()


def armd(t):
    c = Canvas('PARALLEL MASKED GENERATION', 'Multiple token positions are refined together')
    words = [['A', 'model', 'can', 'refine', 'several', 'tokens'], ['in', 'parallel', 'using', 'shared', 'context', '.']]
    c.box((39, 66, 561, 207), WHITE, LINE, 11)
    for r, row in enumerate(words):
        for col, word in enumerate(row):
            x, y = 57+col*82, 87+r*55
            # Different groups resolve simultaneously, then return smoothly to masks.
            reveal = smooth((pulse(t, (col%3)*.065+r*.025)-.22)/.55)
            c.box((x, y, x+73, y+39), mix(PALE, '#d8e8df', reveal), mix(LINE, TEAL, reveal*.55), 7)
            if reveal < .7:
                c.box((x+23, y+16, x+50, y+23), mix(MINT, PALE, reveal), None, 3)
            if reveal > .25:
                c.label(x+36.5, y+12, word, 12, mix(PALE, INK, (reveal-.25)/.75), center=True)
    for j in range(3):
        c.box((230+j*48, 215, 264+j*48, 219), mix(PALE, LAV, pulse(t, j*.16)), None, 2)
    return c.finish()


def skill_memory(t):
    c = Canvas('CONTEXT-AWARE SKILL MEMORY', 'Capture recurrent state · gate an update · reuse through tool calls')
    xs = [49, 247, 445]
    for j, x in enumerate(xs):
        c.box((x, 72, x+108, 181), WHITE, LINE, 10)
        grid(c, x+19, 87, 4, 3, 13, 6, t-j*.13)
        c.label(x+54, 157, ['Capture', 'Gated update', 'Reuse'][j], 12, center=True)
    for x in [161, 359]:
        c.arrow([(x, 126), (x+81, 126)])
        dot_along(c, [(x, 126), (x+81, 126)], t, TEAL)
    # The update gate changes its aperture without implying a performance result.
    aperture = 4+9*pulse(t)
    c.line([(214, 108), (214, 126-aperture)], LAV, 3)
    c.line([(214, 126+aperture), (214, 144)], LAV, 3)
    loop = [(499, 185), (499, 207), (103, 207), (103, 185)]
    c.arrow(loop, LINE, 1.2)
    dot_along(c, loop, t+.4, AMBER, 3)
    return c.finish()


def document_rag(t):
    c = Canvas('DOCUMENT RETRIEVAL', 'Relevant document passages become grounded model context')
    for k in [2, 1, 0]:
        x, y = 40+k*12, 76-k*7
        c.box((x, y, x+109, y+125), WHITE, LINE, 7)
    for row in range(6):
        v = pulse(t, row*.16)
        c.box((54, 91+row*16, 133-row%3*10, 97+row*16), mix(PALE, TEAL, v*.72), None, 2)
    c.label(96, 211, 'Documents', 12, center=True)
    c.arrow([(174, 134), (237, 134)])
    dot_along(c, [(177, 134), (234, 134)], t, TEAL)
    c.box((245, 84, 337, 181), WHITE, LINE, 10)
    grid(c, 260, 100, 4, 3, 11, 7, t)
    c.label(291, 164, 'Retrieve', 12, center=True)
    c.arrow([(345, 134), (408, 134)])
    dot_along(c, [(348, 134), (405, 134)], t+.35, AMBER)
    c.box((417, 69, 560, 202), WHITE, LINE, 9)
    c.label(433, 84, 'Context', 14, INK, True)
    for row in range(4):
        fill = mix(PALE, MINT, pulse(t, row*.15)*.75)
        c.box((433, 115+row*18, 544-row%2*17, 124+row*18), fill, None, 3)
    return c.finish()


def linear_attention(t):
    c = Canvas('STRUCTURED ATTENTION', 'Causal structure and recurrent state shape the computation')
    c.label(146, 62, 'Causal interactions', 12, center=True)
    for r in range(7):
        for col in range(7):
            v = pulse(t, r/7)
            fill = mix(PALE, TEAL, .2+.65*v) if col <= r else mix(BG, WHITE, .55)
            c.box((76+col*21, 85+r*17, 92+col*21, 97+r*17), fill, None, 2)
    c.arrow([(238, 142), (329, 142)], LINE)
    dot_along(c, [(240, 142), (326, 142)], t, TEAL, 4)
    c.label(285, 157, 'update', 11, MUTED, center=True)
    c.box((346, 80, 477, 191), WHITE, LINE, 10)
    grid(c, 365, 96, 5, 4, 14, 6, t)
    c.label(412, 202, 'Recurrent state', 12, center=True)
    recur = [(480, 109), (521, 109), (521, 164), (480, 164)]
    c.arrow(recur, LINE)
    dot_along(c, recur, t+.5, LAV, 3.5)
    return c.finish()


def multimodal(t):
    c = Canvas('RGB + HYPERSPECTRAL FUSION', 'Aligned visual and spectral features inform a shared representation')
    c.box((39, 63, 190, 133), WHITE, LINE, 8)
    c.label(55, 77, 'RGB', 12, INK, True)
    colors = [MINT, '#c7b796', '#a4b8c8', '#d1cfb2', TEAL]
    for r in range(3):
        for col in range(5):
            c.box((107+col*13, 78+r*13, 117+col*13, 88+r*13), colors[(r*3+col)%5], None, 2)
    c.box((39, 149, 190, 218), WHITE, LINE, 8)
    c.label(55, 162, 'Spectral', 12, INK, True)
    for k in range(3):
        c.wave(55, 191+k*6, 116, 5, t+k*.12, [TEAL, LAV, AMBER][k], 1.5, width=1.4)
    c.arrow([(199, 99), (266, 99), (300, 140), (357, 140)])
    c.arrow([(199, 184), (266, 184), (300, 140)])
    dot_along(c, [(201, 99), (266, 99), (300, 140), (355, 140)], t, TEAL)
    dot_along(c, [(201, 184), (266, 184), (300, 140), (355, 140)], t+.12, LAV)
    c.circle(300, 140, 18, WHITE, LINE)
    c.line([(292, 140), (308, 140)], TEAL)
    c.line([(300, 132), (300, 148)], TEAL)
    c.box((367, 72, 560, 205), WHITE, LINE, 10)
    for r in range(6):
        for col in range(8):
            v = (.5+.5*math.sin(col*.7+r*1.2))*.65+.2*pulse(t, col*.13)
            fill = mix(PALE, [TEAL, LAV, AMBER][(r+col//3)%3], v)
            c.box((386+col*20, 89+r*16, 402+col*20, 101+r*16), fill, None, 2)
    c.label(463, 211, 'Fused representation', 12, center=True)
    return c.finish()


def road_vision(t):
    c = Canvas('ROAD SEGMENTATION + FEEDBACK', 'Conceptual scene masks and reviewed edge cases support retraining')
    c.box((35, 63, 385, 221), WHITE, LINE, 9)
    c.poly([(44, 73), (142, 73), (187, 112), (162, 149), (44, 151)], '#d8e5cc')
    c.poly([(44, 157), (150, 157), (174, 211), (44, 211)], '#c7d9ca')
    c.poly([(247, 73), (375, 73), (375, 146), (276, 146), (231, 110)], '#dfdfcb')
    c.poly([(275, 151), (375, 151), (375, 211), (218, 211)], '#d0ded5')
    # Keep the thick road strokes inside the inset scene bounds.
    scene_base = c.im.copy()
    road = [(186, 65), (217, 100), (203, 134), (229, 168), (197, 220)]
    c.line(road, '#bbc7bf', 54)
    c.line(road, '#edf0e7', 37)
    for j in range(10):
        # A dashed center line suggests a road without using a project photograph.
        u = j/10
        dot_along(c, road, u, '#bac5b6', 1.6)
    scene_bounds = tuple(v*SCALE for v in (44, 73, 376, 212))
    scene_base.paste(c.im.crop(scene_bounds), scene_bounds[:2])
    c.im = scene_base
    c.d = ImageDraw.Draw(c.im)
    c.poly([(187, 128), (213, 122), (229, 145), (211, 156), (192, 147)], mix('#d7c395', AMBER, .15+.25*pulse(t)), AMBER)
    scanx = 52+315*pulse(t-.25)
    c.line([(scanx, 72), (scanx, 211)], mix(MINT, TEAL, .45), 2)
    c.circle(scanx, 72, 3, TEAL)
    c.arrow([(390, 143), (432, 143)])
    c.box((438, 90, 562, 197), WHITE, LINE, 10)
    c.label(500, 105, 'Human review', 12, INK, True, True)
    c.box((473, 132, 527, 169), mix(PALE, MINT, pulse(t)*.5), None, 5)
    c.line([(484, 150), (494, 159), (515, 139)], TEAL, 2.5)
    c.line([(498, 202), (498, 217), (398, 217)], LINE, 1.2)
    dot_along(c, [(498, 202), (498, 217), (398, 217)], t, AMBER, 3)
    return c.finish()


def neural_dynamics(t):
    c = Canvas('INFERRING SYNAPTIC DYNAMICS', 'Stimulation and recorded responses inform a dynamical model')
    c.label(37, 65, 'Stimulation', 12, MUTED)
    c.line([(38, 111), (330, 111)], PALE, 1)
    for j in range(10):
        x = 47+j*29
        amp = 16+11*pulse(t, j*.1)
        c.line([(x, 111), (x, 111-amp), (x+4, 111-amp), (x+4, 111)], TEAL, 1.6)
    c.label(37, 142, 'Recorded response', 12, MUTED)
    c.line([(38, 188), (330, 188)], PALE, 1)
    c.wave(38, 188, 292, 20, t, TEAL, 4, 'neural', 1.8)
    c.arrow([(344, 148), (392, 148)])
    dot_along(c, [(345, 148), (390, 148)], t, AMBER, 3.5)
    c.box((401, 72, 565, 217), WHITE, LINE, 10)
    nodes = [(438, 115), (521, 115), (479, 166)]
    for a, b in [(0, 1), (1, 2), (2, 0)]:
        c.line([nodes[a], nodes[b]], LINE, 1.2)
    for j, (x, y) in enumerate(nodes):
        c.circle(x, y, 12+2*pulse(t, j/3), mix(PALE, TEAL, .2+.5*pulse(t, j/3)), LINE)
    c.label(484, 193, 'Latent dynamics', 12, center=True)
    return c.finish()


def eeg(t):
    c = Canvas('CONTRASTIVE EEG REPRESENTATIONS', 'Multiple channels contribute to an identity-focused embedding')
    c.label(114, 64, 'EEG channels', 12, center=True)
    c.box((35, 85, 214, 211), WHITE, LINE, 9)
    for k in range(5):
        c.line([(48, 103+k*22), (201, 103+k*22)], PALE, .6)
        c.wave(48, 103+k*22, 153, 6, t+k*.18, mix(TEAL, LAV, k/7), 3+k*.5, 'neural', 1.25)
    for k in range(5):
        c.line([(220, 103+k*22), (265, 147)], LINE, .8)
    c.box((269, 117, 348, 177), WHITE, LINE, 9)
    for j in range(4):
        c.box((281+j*14, 131, 289+j*14, 160), mix(PALE, TEAL, pulse(t, j*.15)), None, 3)
    c.label(308, 188, 'Encoder', 12, center=True)
    c.arrow([(355, 147), (403, 147)])
    dot_along(c, [(356, 147), (400, 147)], t, TEAL, 3)
    c.circle(484, 147, 64, WHITE, LINE)
    for j in range(13):
        a = j*2.399
        rad = 9+8*(j%4)
        x = 475+rad*math.cos(a)+2*math.sin(math.tau*t+a)
        y = 146+rad*.7*math.sin(a)+2*math.cos(math.tau*t+a)
        c.circle(x, y, 3.6, TEAL if j%3 else MINT)
    for j in range(4):
        c.circle(518+(j%2)*9, 118+(j//2)*10, 2.6, LAV)
    c.label(484, 216, 'Embedding', 12, center=True)
    return c.finish()


def physiological_sensing(t):
    c = Canvas('PHYSIOLOGICAL SIGNAL SEPARATION', 'Adaptive filtering disentangles mixed sources and noise')
    c.label(125, 70, 'Mixed signal', 12, center=True)
    c.box((33, 97, 219, 189), WHITE, LINE, 9)
    pts = []
    for i in range(162):
        s = i/162
        q = (s*2-t) % 1
        main = .85*math.exp(-((q-.45)/.023)**2)-.2*math.exp(-((q-.49)/.025)**2)
        noise = .12*math.sin(math.tau*(s*24-2*t))+.14*math.sin(math.tau*(s*7-t))
        pts.append((45+i, 149-34*(main+noise)))
    c.line([(45, 149), (207, 149)], PALE, 1)
    c.line(pts, MUTED, 1.5)
    c.arrow([(224, 144), (264, 144)])
    c.box((271, 103, 329, 183), mix(WHITE, PALE, .5), LINE, 8)
    for j in range(3):
        y = 121+j*21
        c.line([(281, y), (319, y)], LINE, 1)
        c.circle(288+24*pulse(t, j/3), y, 3.8, TEAL)
    c.label(300, 193, 'Filter', 12, center=True)
    c.arrow([(336, 144), (376, 144)])
    c.label(475, 70, 'Separated signals', 12, center=True)
    c.box((383, 97, 567, 189), WHITE, LINE, 9)
    c.line([(394, 129), (556, 129)], PALE, .8)
    c.line([(394, 166), (556, 166)], PALE, .8)
    c.wave(394, 129, 162, 21, t, TEAL, 2, 'ecg', 1.7)
    c.wave(394, 166, 162, 13, t, LAV, 3, 'ecg', 1.5)
    return c.finish()


def image_cell(row, col, variant=0):
    # Abstract, procedural landscape-like patchwork, not an experimental output.
    if row < 3:
        base = '#b9d1cd'
    elif row < 5+math.sin(col*.7+variant):
        base = '#a4bcac'
    elif row < 7+math.cos(col*.5+variant):
        base = '#578c73'
    else:
        base = '#c5b98e'
    return mix(base, WHITE, .08*((row*7+col*3)%4))


def colorization(t):
    c = Canvas('CONDITIONAL IMAGE COLORIZATION', 'Illustrative patches: input structure conditions generated color')
    for side, x in enumerate([45, 365]):
        c.box((x, 69, x+190, 211), WHITE, LINE, 9)
        for r in range(8):
            for col in range(10):
                color = image_cell(r+1, col)
                gray = tuple([round(sum(color)/3)]*3)
                amount = 0 if side == 0 else .28+.72*smooth((pulse(t, col*.025)-.1)/.8)
                c.rect((x+12+col*16.8, 82+r*14, x+27+col*16.8, 94+r*14), mix(gray, color, amount))
    c.label(140, 216, 'Grayscale structure', 12, center=True)
    c.label(460, 216, 'Plausible color', 12, center=True)
    c.arrow([(246, 140), (354, 140)])
    c.box((265, 111, 335, 168), WHITE, LINE, 8)
    c.label(300, 123, 'cGAN', 14, INK, True, True)
    for j, color in enumerate([MINT, AMBER, LAV]):
        c.circle(283+j*17, 150, 4, mix(PALE, color, .4+.6*pulse(t, j/3)))
    return c.finish()


def geological_generation(t):
    c = Canvas('HYPERSPECTRAL DATA AUGMENTATION', 'Conditional generation explores variation in spectral image data')
    for layer in range(3, -1, -1):
        x, y = 43+layer*10, 98-layer*10
        c.box((x, y, x+131, y+106), mix(WHITE, MINT, layer*.12), LINE, 6)
        if layer == 0:
            for r in range(5):
                for col in range(7):
                    v = .35+.4*math.sin(r*.8+col*.7)**2
                    c.box((x+9+col*16, y+10+r*16, x+21+col*16, y+22+r*16), mix(PALE, [TEAL, AMBER, LAV][(r+col)%3], v), None, 2)
    c.label(116, 213, 'Spectral cube', 12, center=True)
    c.arrow([(212, 143), (268, 143)])
    c.circle(300, 143, 25, WHITE, LINE)
    c.line([(288, 143), (312, 143)], TEAL, 1.5)
    c.line([(300, 131), (300, 155)], TEAL, 1.5)
    for row, y in enumerate([70, 123, 176]):
        c.line([(329, 143), (368, y+20), (401, y+20)], LINE, 1)
        dot_along(c, [(329, 143), (368, y+20), (401, y+20)], t+row/3, [TEAL, LAV, AMBER][row], 3)
        c.box((410, y, 557, y+40), WHITE, LINE, 6)
        for col in range(9):
            for r in range(2):
                color = mix(PALE, [TEAL, LAV, AMBER][row], .2+.6*pulse(t, col*.08+r*.11+row*.19))
                c.box((420+col*14, y+9+r*13, 430+col*14, y+18+r*13), color, None, 2)
    c.label(484, 221, 'Conditional variants', 11, center=True)
    return c.finish()


def face_representations(t):
    c = Canvas('GEOMETRY + APPEARANCE', 'Landmark locations provide an additional spatial representation')
    yaw = .15*math.sin(math.tau*t)
    cx, cy = 151, 139
    outline = [(cx+57*math.sin(math.tau*i/32)*(1+yaw*.4), cy-73*math.cos(math.tau*i/32)) for i in range(33)]
    c.poly(outline, WHITE, LINE, 1.2)
    landmarks = [(-30,-20), (-18,-23), (-5,-19), (14,-21), (29,-23), (40,-18), (5,-10), (3,6), (1,19), (-17,40), (2,35), (21,40), (2,47), (-35,4), (39,5), (-25,57), (24,57)]
    pts = [(cx+x*(1-abs(yaw))+yaw*(70-abs(x)), cy+y) for x, y in landmarks]
    connections = [(0,1),(1,2),(3,4),(4,5),(6,7),(7,8),(9,10),(10,11),(11,12),(12,9),(0,13),(5,14),(13,9),(14,11),(9,15),(11,16),(15,16),(2,6),(3,6),(8,10),(13,8),(14,8)]
    for a, b in connections:
        c.line([pts[a], pts[b]], LINE, 1)
    for j, (x, y) in enumerate(pts):
        c.circle(x, y, 2.5, TEAL if j%3 else LAV)
    c.label(cx, 218, 'Landmark geometry', 12, center=True)
    c.arrow([(231, 140), (335, 140)])
    dot_along(c, [(234, 140), (332, 140)], t, LAV)
    c.box((353, 66, 552, 211), WHITE, LINE, 9)
    centers = [(3.2+yaw*2, 3.3), (8+yaw*2, 3.3), (5.8+yaw*2, 5.1), (5.5+yaw*2, 7)]
    for r in range(9):
        for col in range(12):
            vals = [math.exp(-((col-x)**2+(r-y)**2)/2) for x,y in centers]
            v = max(vals)
            color = mix(PALE, TEAL if vals.index(v)<2 else LAV, v*.92)
            c.box((367+col*14, 77+r*14, 377+col*14, 87+r*14), color, None, 2)
    c.label(452, 218, 'Spatial heatmaps', 12, center=True)
    return c.finish()


def mlops(t):
    c = Canvas('REPRODUCIBLE MODEL SERVING', 'A packaged model moves through automated checks to an API')
    xs = [33, 176, 319, 462]
    for j, x in enumerate(xs):
        c.box((x, 85, x+105, 194), WHITE, LINE, 10)
        c.label(x+52.5, 170, ['Model', 'Package', 'Checks', 'API'][j], 12, INK, True, True)
        if j < 3:
            path = [(x+111, 132), (x+137, 132)]
            c.arrow(path, LINE)
            dot_along(c, path, t+j*.23, TEAL, 3.5)
    # Small network.
    for y in [112, 139]:
        for yy in [105, 125, 145]:
            c.line([(60, y), (85, yy)], LINE, .8)
            c.line([(85, yy), (112, 125)], LINE, .8)
    for x, y in [(60,112),(60,139),(85,105),(85,125),(85,145),(112,125)]:
        c.circle(x, y, 4, mix(MINT, TEAL, pulse(t, x/100)))
    # Container layers.
    for row in range(3):
        c.box((198, 103+row*17, 259, 115+row*17), mix(PALE, MINT, pulse(t,row*.16)*.7), None, 3)
        c.circle(250, 109+row*17, 1.5, TEAL)
    # Check run indicators.
    for row in range(3):
        y = 109+row*18
        c.circle(341, y, 5, mix(PALE, MINT, pulse(t,row*.15)))
        c.line([(338, y), (340, y+2), (344, y-3)], TEAL, 1.2)
        c.line([(353, y), (401-row%2*10, y)], LINE, 2)
    c.label(514, 107, '{ }', 20, TEAL, True, True)
    c.box((486, 140, 542, 148), mix(PALE, TEAL, .3+.3*pulse(t)), None, 4)
    path = [(514, 201), (514, 218), (86, 218), (86, 201)]
    c.line(path, LINE, 1)
    dot_along(c, path, t, AMBER, 3)
    return c.finish()


RENDERERS = {
    'softskill': softskill, 'edgealign': edgealign, 'armd': armd,
    'skill-memory': skill_memory, 'document-rag': document_rag,
    'linear-attention': linear_attention, 'multimodal': multimodal,
    'road-vision': road_vision, 'neural-dynamics': neural_dynamics, 'eeg': eeg,
    'physiological-sensing': physiological_sensing, 'colorization': colorization,
    'geological-generation': geological_generation, 'face-representations': face_representations,
    'mlops': mlops,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    projects = json.loads((ROOT/'content'/'portfolio.json').read_text())['projects']
    requested = sys.argv[1:]
    valid = {p['id'] for p in projects}
    unknown = set(requested)-valid
    if unknown:
        raise SystemExit(f'Unknown projects: {sorted(unknown)}')
    manifest = {}
    for project in projects:
        key = project['id']
        if requested and key not in requested:
            continue
        render = RENDERERS[key]
        frames = [render(i/FRAMES) for i in range(FRAMES)]
        # A shared palette prevents color flicker; all alpha blends are explicit.
        palette_source = Image.new('RGB', (W*4, H))
        for j, idx in enumerate([0, 12, 24, 36]):
            palette_source.paste(frames[idx], (W*j, 0))
        palette = palette_source.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
        gif = OUT/f'{key}.gif'
        indexed[0].save(gif, save_all=True, append_images=indexed[1:], optimize=True,
                        duration=80, loop=0, disposal=1)
        # The poster is a complete informative diagram for reduced-motion use.
        frames[6].save(OUT/f'{key}.png', optimize=True)
        with Image.open(gif) as check:
            assert check.n_frames == FRAMES, (key, check.n_frames)
            assert check.size == (W, H)
            assert check.info.get('loop') == 0
        assert render(0).tobytes() == render(1).tobytes(), f'Nonperiodic renderer: {key}'
        item = {'gif': f'{key}.gif', 'poster': f'{key}.png', 'width': W, 'height': H,
                'frames': FRAMES, 'durationMs': FRAMES*80, 'bytes': gif.stat().st_size,
                'description': project['short'] + ' — conceptual method animation'}
        manifest[key] = item
        print(f'{key:24} {gif.stat().st_size/1024:7.1f} KiB   48 frames', flush=True)
    if not requested:
        (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
        print(f'Total GIFs: {sum(v["bytes"] for v in manifest.values())/1024/1024:.2f} MiB')


if __name__ == '__main__':
    main()
