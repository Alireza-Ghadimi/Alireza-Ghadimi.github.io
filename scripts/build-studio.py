"""Render both Research Studio profiles with the portfolio's existing case studies and assets."""
from hashlib import sha256
from pathlib import Path
import runpy

from studio_work import render_work

ROOT = Path(__file__).resolve().parents[1]
portfolio = runpy.run_path(str(ROOT / 'scripts/build-site.py'))
DATA = portfolio['DATA']
FOCUS = [('agents', 'Agentic AI'), ('genai', 'Generative AI'), ('llm', 'LLMs & transformers'),
         ('vision', 'Computer vision'), ('biomedical', 'Biomedical research')]
DOCK = [('home', 'Home', 'home'), ('contact', 'Say hello', 'contact'), ('about', 'About', 'about'),
        ('affiliations', 'Affiliations', 'affiliations'), ('work', 'Projects', 'work'),
        ('work-agents', 'Agents', 'agents'), ('work-genai', 'GenAI', 'genai'),
        ('work-llm', 'LLMs', 'llm'), ('work-vision', 'Vision', 'vision'),
        ('work-biomedical', 'Biomedical', 'biomedical'), ('experience', 'Experience', 'experience'),
        ('research', 'Papers', 'research'), ('background', 'Education', 'background'), ('leaflab', 'LeafLab', 'leaflab')]
# Monochrome wayfinding symbols are paired with visible labels in every tile.
GLYPHS = {
    'home': '<circle cx="10" cy="18" r="5" fill="currentColor"/><circle cx="18" cy="16" r="8" fill="currentColor"/><circle cx="27" cy="15" r="4" fill="currentColor"/>',
    'contact': '<rect x="3" y="7" width="30" height="22" rx="6"/><path d="m5 10 13 10 13-10"/>',
    'about': '<circle cx="18" cy="18" r="15"/><path d="M10 21q8 12 16 0"/><circle cx="12" cy="14" r="1"/><circle cx="24" cy="14" r="1"/>',
    'affiliations': '<circle cx="18" cy="18" r="15"/><ellipse cx="18" cy="18" rx="7" ry="15"/><path d="M3 18h30"/>',
    'work': '<rect x="4" y="4" width="11" height="11" rx="4"/><rect x="21" y="4" width="11" height="11" rx="4"/><rect x="4" y="21" width="11" height="11" rx="4"/><rect x="21" y="21" width="11" height="11" rx="4"/>',
    'agents': '<path d="m7 22 10-13 12 16Z"/><g fill="currentColor"><circle cx="7" cy="22" r="4"/><circle cx="17" cy="9" r="4"/><circle cx="29" cy="25" r="4"/></g>',
    'genai': '<path d="M18 2q2 13 15 16-13 2-15 15Q16 20 3 18 16 16 18 2Z" fill="currentColor"/>',
    'llm': '<g fill="currentColor"><rect x="3" y="17" width="7" height="12" rx="3.5"/><rect x="14" y="5" width="7" height="22" rx="3.5"/><rect x="25" y="12" width="7" height="12" rx="3.5"/></g>',
    'vision': '<path d="M2 18Q17-3 34 18 17 39 2 18Z"/><circle cx="18" cy="18" r="5" fill="currentColor"/>',
    'biomedical': '<path d="M2 18h7l4-10 5 22 5-25 4 13h7" stroke-width="2"/>',
    'experience': '<rect x="3" y="10" width="30" height="21" rx="4"/><path d="M12 10V8q0-4 4-4h4q4 0 4 4v2M3 17q15 8 30 0"/>',
    'research': '<path d="M8 3h15l6 7v23H8zM22 3v8h7M12 16h12M12 21h12M12 26h8"/>',
    'background': '<path d="m2 13 16-9 16 9-16 9zm6 4v8q10 10 20 0v-8m5-3v14"/>',
    'leaflab': '<path d="M4 31Q0 8 31 4q1 28-27 27Zm0 0L24 12M14 21v-6m1 4h7"/>',
}

def icon(name):
    return (f'<svg aria-hidden="true" viewBox="0 0 36 36" fill="none" stroke="currentColor"'
            f' stroke-width="1.35" stroke-linejoin="round" stroke-linecap="round">{GLYPHS[name]}</svg>')


def render(full):
    prefix = '../../' if full else '../'
    local = '../' if full else './'
    assets = prefix + 'assets/'
    resume = 'Alireza-Ghadimi-Resume' + ('-Full' if full else '') + '.pdf'
    pdf = assets + resume
    sig = portfolio['signature'](prefix)
    chapters = ''.join(f'<a href="#work-{key}"><canvas data-mark="{key}" width="240" height="158" aria-hidden="true"></canvas><span>{label}</span></a>' for key, label in FOCUS)
    tiles = ''.join(f'<a href="#{key}"' + (' aria-current="location"' if key == 'home' else '') + f'>{icon(glyph)}<span>{label}</span></a>' for key, label, glyph in DOCK)
    case_dialogs = ''.join(portfolio['project_dialog'](item) for item in DATA['projects'])
    # Shared assets can be cached independently of the generated profile HTML.
    def versioned(name):
        digest = sha256((ROOT / 'studio' / name).read_bytes()).hexdigest()[:10]
        return f'{local}{name}?v={digest}'

    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#ffffff"><meta name="robots" content="noindex,follow"><title>Alireza Ghadimi — Research Studio</title>
<meta name="description" content="Explore Alireza Ghadimi’s work on agent learning, generative AI, and efficient language models.">
<link rel="icon" href="{assets}favicon.svg"><link rel="stylesheet" href="{versioned('studio.css')}"><link rel="stylesheet" href="{versioned('work.css')}">
<script defer src="{prefix}app.js"></script><script defer src="{versioned('studio.js')}"></script><script defer src="{versioned('marks.js')}"></script><script defer src="{versioned('work.js')}"></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<nav class="dock" aria-label="Portfolio sections">{tiles}</nav>
<main id="main">
<section id="home" class="home">
<div class="mast"><a href="#about" aria-label="About Alireza Ghadimi">{sig}</a><div><span>Toronto / Waterloo</span><button type="button" class="motion-switch" hidden aria-pressed="false">Pause motion</button></div></div>
<div class="home-core"><h1>Alireza Ghadimi</h1><p class="role">ML Research Scientist · PhD Student</p><div class="focus-row">{chapters}</div>
<p class="home-thesis">Efficient models. Adaptive agents.</p><a class="home-school" href="#background">University of Waterloo</a></div></section>
<section class="story chapter" id="about"><div class="section-wrap"><h2>About me</h2>
<div class="portrait"><svg viewBox="440 270 1480 1470" preserveAspectRatio="xMidYMin slice" role="img" aria-label="Alireza Ghadimi in a blue suit"><image href="{assets}alireza-portrait-original.jpg" width="2080" height="3120"/></svg></div>
<p class="biography">{portfolio['profile_bio'](full)}</p><div class="action-row"><a class="pill" href="#work">Explore my work</a><a class="pill outline" href="{pdf}" download>Download résumé</a></div>
<div class="focus-copy"><h3>Making agents learn.<br>Making models efficient.</h3><div><p>How can an agent turn execution feedback into a reusable skill? How can a generative model make better use of its computation? These questions guide my research.</p><p>I work across <strong>learned agent skills, compact memory, and efficient generation</strong>, connecting model research with the training, inference, and evaluation systems needed to test it.</p></div></div>
<div class="highlights"><div><strong>Agent learning</strong><p>Skills and memory that improve through execution feedback</p></div><div><strong>32 vectors</strong><p>Compact learned skills evaluated in my SoftSkill reproduction</p></div><div><strong>Efficient GenAI</strong><p>Masked diffusion, parallel generation, and GPU-aware model research</p></div></div></div></section>
<section class="affiliations chapter" id="affiliations"><div class="section-wrap"><h2>Where I’ve worked<br>and studied</h2><div class="logo-matrix">{portfolio['affiliation_logos'](prefix)}</div></div></section>
{render_work(DATA,prefix)}
<section class="career chapter" id="experience"><div class="section-wrap"><header class="chapter-head">{icon('experience')}<h2>Experience</h2><p>From the research question to the running system.</p></header>{portfolio['experience'](full,prefix)}</div></section>
<section class="papers chapter" id="research"><div class="section-wrap"><header class="chapter-head">{icon('research')}<h2>Research papers</h2><p>Publications and manuscripts in progress.</p></header>{portfolio['publications']()}</div></section>
<section class="schools chapter" id="background"><div class="section-wrap"><header class="chapter-head">{icon('background')}<h2>Education</h2><p>From electrical and biomedical engineering to computer science and efficient AI.</p></header><div class="schools-grid">{portfolio['education'](prefix)}</div>
<div class="award"><span aria-hidden="true">✳</span><div><h3>Hackathon winner</h3><p>AI in Finance Summer School · August 2026</p><p>Selected participant in AIFSS, presented by RBC Borealis in Vancouver. Winner of the final participant hackathon challenge.</p></div></div></div></section>
<section class="contact chapter" id="contact"><div class="section-wrap"><header class="chapter-head">{icon('contact')}<h2>Let’s talk.</h2><p>Working on agents, generative models, or efficient LLMs? I’d love to hear what you’re building or researching.</p></header><div class="email-row"><a href="mailto:arghadimi.bme@gmail.com">arghadimi.bme@gmail.com</a><button class="copy-email" type="button">Copy email</button><span id="copy-status" class="sr-only" role="status"></span></div>
<div class="action-row"><a href="https://github.com/Alireza-Ghadimi">GitHub</a><a href="https://www.linkedin.com/in/Alireza-Ghadimi">LinkedIn</a><a href="{pdf}" download>Download résumé</a></div></div></section></main>
<footer><div class="colophon"><a href="#home" aria-label="Back to home">{sig}</a><span>© <span id="year">2026</span> Alireza Ghadimi</span><a href="credits.html">Image credits</a></div>
<section class="leaf" id="leaflab"><img src="{assets}leaflab-logo-green-puzzle.png" width="1706" height="922" loading="lazy" alt="LeafLab’s interlocking green leaf"><h2>LeafLab</h2><p>Exploring a research lab for efficient language models.</p></section></footer>
{case_dialogs}</body></html>'''


if __name__ == '__main__':
    for full in (False, True):
        folder = ROOT / 'studio' / ('full-profile' if full else '')
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'index.html').write_text(render(full))
        (folder / 'credits.html').write_text(portfolio['credits'](full, motion=True))
