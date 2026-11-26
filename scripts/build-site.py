#!/usr/bin/env python3
"""Build the public animated homepage, its credits, and legacy links."""
from pathlib import Path
from html import escape as e
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/portfolio.json').read_text())
BASE = 'https://alireza-ghadimi.github.io/'

def asset(name):
    return 'assets/' + name

def link(label, url, cls='text-link'):
    return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)}</a>'

def signature():
    return f'<span class="signature-mark"><img src="{asset("ag-signature.png")}" width="1254" height="1254" alt=""></span>'

def project_card(p):
    poster = asset('project-motion/' + p['id'] + '.png')
    gif = asset('project-motion/' + p['id'] + '.gif')
    visual = f'<img class="project-motion" src="{poster}" data-poster="{poster}" data-gif="{gif}" width="600" height="260" alt="" loading="lazy" decoding="async">'
    return f'''<article class="work-card" data-category="{' '.join(p['categories'])}" data-featured="{str(p['featured']).lower()}" {'hidden' if not p['featured'] else ''}>
      <div class="work-art">{visual}<span class="project-status">{e(p['status'])}</span></div>
      <div class="work-card-body"><p class="overline work-context">{e(p['context'])}</p><h3>{e(p['title'])}</h3><p class="work-summary">{p['summary']}</p>
      <ul class="tags" aria-label="Methods">{''.join(f'<li>{e(t)}</li>' for t in p['tags'])}</ul>
      <div class="work-links"><button type="button" class="case-link" data-case="{p['id']}" aria-haspopup="dialog" aria-label="Read case study: {e(p['short'])}">Read case study<span aria-hidden="true">＋</span></button>{link('Paper' if p['id']=='neural-dynamics' else 'Repository',p['links'][0]['url']) if p['links'] else ''}</div></div></article>'''

def project_dialog(p):
    benchmark=''
    if p.get('benchmark'):
        benchmark='''<div class="benchmark"><p class="overline">SEARCHQA · QWEN3-8B · TEST-HARD</p><table><caption>Accuracy in the public reproduction</caption><thead><tr><th scope="col">Method</th><th scope="col">Skill footprint</th><th scope="col">Accuracy</th></tr></thead><tbody><tr><th scope="row">No skill</th><td>0</td><td>67.9%</td></tr><tr><th scope="row">Text skill</th><td>1,995 tokens</td><td>71.7%</td></tr><tr class="best-result"><th scope="row">Trained soft skill</th><td>32 vectors</td><td>74.2 ± 0.3%</td></tr></tbody></table><p>SoftSkill result across three seeds. Skill footprint is the added instruction representation, not the entire model context.</p></div>'''
    return f'''<dialog class="case-dialog" id="case-{p['id']}" aria-labelledby="title-{p['id']}"><button class="dialog-close" type="button" aria-label="Close case study">×</button><div class="dialog-inner"><p class="overline">{e(p['context'])} · {e(p['status'])}</p><h2 id="title-{p['id']}">{e(p['short'])}</h2><p class="dialog-lead">{p['summary']}</p><section><h3>The question</h3><p>{e(p['problem'])}</p></section><section><h3>My contribution</h3><ul class="contribution-list">{''.join(f'<li>{e(t)}</li>' for t in p['contributions'])}</ul></section>{benchmark}<section><h3>Evidence & current status</h3><p>{e(p['evidence'])}</p><p class="case-note">{e(p['note'])}</p></section><div class="dialog-links">{''.join(link(l['label'],l['url'],'button button-green') for l in p['links'])}</div></div></dialog>'''

def experience():
    first = {'date':'Sep 2026–present','name':'Agentic AI research & engineering','role':'Industry project experience','meta':'Learned skills · Execution feedback · Evaluation','logo':None,'body':'Researching how agents improve through <strong>learned skills and execution feedback</strong>, under constraints on compute and context.','bullets':['Designed the <strong>EdgeAlign research prototype</strong> around forward-only skill optimization.','Built prompt-embedding and sandboxed evaluation support, and investigated feedback from tool execution.']}
    rows=[first,
      {'date':'Jan–Jul 2026','name':'Strayos','role':'AI Engineer · Computer Vision','meta':'Toronto, ON','logo':'company-strayos-logo.svg','body':'Owned <strong>road-scene segmentation and anomaly detection</strong> from data curation through training, evaluation, and deployment.','bullets':['Built a <strong>human-in-the-loop active-learning pipeline</strong> to turn corrected annotations into model improvements.','Analyzed failures, prioritized difficult cases, and improved the retraining workflow.']},
      {'date':'May 2022–Dec 2024','name':'EnerSoft','role':'Lead Data Scientist · Computer Vision','meta':'Toronto, ON','logo':'company-enersoft-logo.png','body':'Built and deployed <strong>RGB–hyperspectral perception systems</strong> that reduced manual-review costs by <strong>$200K annually</strong>.','bullets':['Led production troubleshooting for <strong>6+ months</strong>, coordinating model-failure analysis and fixes.','Built scalable training, inference, and distributed evaluation workflows; improved legacy-code reliability.']},
      {'date':'Feb–May 2022','name':'Fusion Analytics','role':'Data Engineer','meta':'Toronto, ON','logo':'company-fusion-logo.png','body':'Built the data infrastructure behind analytical workflows: <strong>Azure and SQL ETL pipelines</strong>, large-scale auditing, and Python dashboards.','bullets':['Used <strong>PySpark and SQL</strong> to audit and balance datasets for downstream analysis.']}]
    out=[]
    for r in rows:
        mark=f'<img src="{asset(r["logo"])}" alt="" loading="lazy">' if r['logo'] else '<span class="experience-monogram" aria-hidden="true">'+({'EnerSoft':'EN','Strayos':'CV'}.get(r['name'],'AI'))+'</span>'
        out.append(f'''<article class="experience-row"><div class="experience-date">{e(r['date'])}</div><div class="experience-main"><div class="experience-title">{mark}<div><h3>{e(r['name'])}</h3><p>{e(r['role'])}</p></div></div><p class="experience-meta">{e(r['meta'])}</p><p class="experience-summary">{r['body']}</p><ul>{''.join('<li>'+b+'</li>' for b in r['bullets'])}</ul></div></article>''')
    return ''.join(out)

def publications():
    rows=[
      ('Published · PLOS ONE · 2022','Inferring stimulation induced short-term synaptic plasticity dynamics using novel dual optimization algorithm','<strong>A. Ghadimi</strong>, L. A. Steiner, M. R. Popovic, L. Milosevic, M. Lankarany','Computational inference of short-term synaptic dynamics under stimulation.','https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0273699'),
      ('Submitted · IEEE T-BIOM','A Scoping Review of Model Compression for Biometric and Bio-Signal Authentication Systems','<strong>A. Ghadimi</strong>, M. Moodi, A. Ghodsi, T. H. Falk','Connecting efficient models with biometric and biosignal authentication.',None),
      ('Manuscript in preparation','Electroencephalography Foundation Model-Based Soft Biometrics: A Performance Comparison of Age and Biological Sex Prediction','M. Jaberi, M. Moodi, <strong>A. Ghadimi</strong>, A. Jafari, A. Ghodsi, T. H. Falk','Collaborative research on EEG foundation-model representations.',None),
      ('Research in progress','ARMD-QWEN: Fine-tuning large language models for generating multiple tokens during inference','<strong>A. Ghadimi</strong>, M. Karami, A. Jafari, A. Ghodsi','Adapting pretrained language models for masked-diffusion generation.',None)]
    return ''.join(f'''<article class="publication {'published' if i==0 else ''}"><p class="paper-status">{e(status)}</p><div><h3>{f'<a href="{url}" target="_blank" rel="noopener noreferrer">{e(title)}</a>' if url else e(title)}</h3><p class="paper-authors">{authors}</p><p class="paper-summary">{e(summary)}</p>{link('Read paper',url) if url else ''}</div></article>''' for i,(status,title,authors,summary,url) in enumerate(rows))

def education():
    rows=[('University of Waterloo','PhD · Computer Science','2026–present','Efficient language models, agent learning, and GPU-aware research.','waterloo','jpg','Mathematics 3 at the University of Waterloo','https://uwaterloo.ca/'),('University of Toronto','M.Sc. · Biomedical Engineering','2019–2021','Stochastic modeling, machine learning, and neural dynamics.','toronto','png','Convocation Hall at the University of Toronto','https://www.utoronto.ca/'),('Amirkabir University of Technology','B.Sc. · Electrical Engineering','2014–2019','Signal processing and physiological sensing.','amirkabir','png','The entrance of Amirkabir University of Technology','https://aut.ac.ir/')]
    out=[]
    for name,degree,years,focus,key,ext,alt,url in rows:
        logo='institution-'+key+'-logo.'+('svg' if key=='toronto' else 'png')
        out.append(f'''<article class="education-card"><a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Visit {e(name)}"><img class="campus-photo" src="{asset('institution-'+key+'-campus.'+ext)}" alt="{e(alt)}" width="600" height="400" loading="lazy"></a><div class="education-body"><div class="education-top"><img class="education-logo logo-{key}" src="{asset(logo)}" alt="" loading="lazy"><span>{years}</span></div><h3>{e(name)}</h3><p class="degree">{degree}</p><p>{focus}</p></div></article>''')
    return ''.join(out)

def affiliation_logos():
    logos=[('Waterloo','institution-waterloo-logo.png','waterloo'),('University of Toronto','institution-toronto-logo.svg','toronto'),('Amirkabir University','institution-amirkabir-logo.png','amirkabir')]
    logos.extend([('Strayos','company-strayos-logo.svg','strayos'),('Fusion Analytics','company-fusion-logo.png','fusion'),('EnerSoft','company-enersoft-logo.png','enersoft')])
    return ''.join(f'<img src="{asset(file)}" class="logo-{key}" alt="{name}" loading="lazy">' for name,file,key in logos)

def render():
    resume='Alireza-Ghadimi-Resume.pdf'
    pdf=ROOT/'assets'/resume
    version=hashlib.sha256(pdf.read_bytes()).hexdigest()[:12]
    pdf_url=asset(resume)+'?v='+version
    css_hash=hashlib.sha256((ROOT/'styles.css').read_bytes()).hexdigest()[:10]
    js_hash=hashlib.sha256((ROOT/'app.js').read_bytes()).hexdigest()[:10]
    canonical=BASE
    category_json=json.dumps(DATA['categories'])
    bio='I research how language-model agents learn from execution feedback and how generative models can do more with less computation. I’m a Computer Science PhD student at the University of Waterloo, building on experience taking ML systems into production.'
    logo_html=affiliation_logos()
    tabs=''.join(f'<button id="tab-{c["id"]}" type="button" role="tab" aria-selected="{str(i==0).lower()}" aria-controls="work-panel" tabindex="{0 if i==0 else -1}" data-filter="{c["id"]}">{e(c["label"])}</button>' for i,c in enumerate(DATA['categories']))
    structured={'@context':'https://schema.org','@type':'Person','name':'Alireza Ghadimi','url':canonical,'jobTitle':'ML Research Scientist and Computer Science PhD Student','sameAs':['https://github.com/Alireza-Ghadimi','https://www.linkedin.com/in/Alireza-Ghadimi'],'affiliation':{'@type':'CollegeOrUniversity','name':'University of Waterloo'}}
    motion_css_hash = hashlib.sha256((ROOT / 'motion.css').read_bytes()).hexdigest()[:10]
    motion_js_hash = hashlib.sha256((ROOT / 'motion.js').read_bytes()).hexdigest()[:10]
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f7f9f6"><meta name="description" content="Alireza Ghadimi: agentic AI, generative models, and efficient LLM research. Waterloo Computer Science PhD student studying learned agent skills, execution feedback, and multi-token generation."><meta property="og:title" content="Alireza Ghadimi — Agentic AI & Generative Models"><meta property="og:description" content="Efficient models. Adaptive agents. Research on agent learning, compact skills, and generative AI at the University of Waterloo."><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}assets/alireza-portrait-original.jpg"><link rel="canonical" href="{canonical}"><title>Alireza Ghadimi — Motion Edition</title><link rel="icon" href="{asset('favicon.svg')}" type="image/svg+xml"><link rel="preload" href="{asset('fonts/instrument-serif-normal-400.woff')}" as="font" type="font/woff" crossorigin><link rel="stylesheet" href="{asset('fonts/fonts.css')}"><link rel="stylesheet" href="styles.css?v={css_hash}"><script src="app.js?v={js_hash}" defer></script><script type="application/ld+json">{json.dumps(structured)}</script><link rel="stylesheet" href="motion.css?v={motion_css_hash}"><script src="motion.js?v={motion_js_hash}" defer></script></head>
<body class="motion-edition"><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container header-inner"><span class="edition-label">Motion edition</span><a class="brand" href="#about" aria-label="Alireza Ghadimi home">{signature()}</a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav">Menu <span aria-hidden="true">☰</span></button><nav id="main-nav" aria-label="Main navigation"><a href="#work">Work</a><a href="#experience">Experience</a><a href="#research">Research</a><a href="#background">Background</a><a class="nav-contact" href="#contact">Let’s talk</a></nav></div></header>
<div class="reading-progress" aria-hidden="true"><span></span></div><aside class="motion-controls" aria-label="Display options"><button type="button" id="motion-toggle" aria-pressed="false"><span class="motion-symbol" aria-hidden="true"><i></i><i></i><i></i></span><span class="motion-toggle-label">Pause motion</span></button></aside>
<main id="main"><section class="hero container" id="about" aria-labelledby="hero-title"><div class="hero-atmosphere" aria-hidden="true"><div class="hero-orbits"><span></span><span></span><span></span><b></b><b></b><b></b></div></div><div class="hero-copy"><p class="overline hero-overline"><span aria-hidden="true"></span>AGENTIC AI · GENERATIVE AI · LLM RESEARCH</p><h1 id="hero-title"><span class="name-line"><span>Alireza</span></span>
<span class="name-line"><span>Ghadimi<b>.</b></span></span></h1><p class="hero-thesis">Efficient models.<br> <em>Adaptive agents.</em></p><p class="hero-bio">{bio}</p><div class="hero-actions"><a class="button button-green" href="#work">Explore my work</a><a class="button button-outline" href="{pdf_url}" download>Download résumé</a></div><p class="hero-location">Toronto / Waterloo, Canada <span aria-hidden="true">·</span> {link('GitHub','https://github.com/Alireza-Ghadimi')}</p></div><div class="portrait-area"><div class="portrait-frame"><svg class="portrait" viewBox="440 270 1480 1470" preserveAspectRatio="xMidYMin slice" role="img" aria-labelledby="portrait-title"><title id="portrait-title">Alireza Ghadimi in a blue suit, cropped to his head and upper torso</title><image href="{asset('alireza-portrait-original.jpg')}" width="2080" height="3120"/></svg><div class="portrait-caption"><span>ML RESEARCH SCIENTIST · PHD STUDENT</span><span aria-hidden="true">AG / 2026</span></div></div><p class="portrait-note">Learning from feedback.<br>Doing more with less.</p><span class="portrait-outline" aria-hidden="true"></span></div></section>
<section class="affiliations container" aria-label="Academic and industry background"><p class="overline">ACADEMIC & INDUSTRY EXPERIENCE</p><div class="logo-strip">{logo_html}</div></section>
<section class="perspective container" aria-labelledby="perspective-title"><div><p class="overline">MY RESEARCH FOCUS</p><h2 id="perspective-title">Making agents learn.<br><em>Making models efficient.</em></h2></div><div class="perspective-copy"><p>How can an agent turn execution feedback into a reusable skill? How can a generative model make better use of its computation? These questions guide my research.</p><p>I work across <strong>learned agent skills, compact memory, and efficient generation</strong>, connecting model research with the training, inference, and evaluation systems needed to test it.</p></div></section>
<section class="impact-strip container" aria-label="Selected experience highlights"><div><strong>Agent learning</strong><span>Skills and memory that improve<br>through execution feedback</span></div><div><strong>32 vectors</strong><span>Compact learned skills evaluated<br>in my SoftSkill reproduction</span></div><div><strong>Efficient GenAI</strong><span>Masked diffusion, parallel generation,<br>and GPU-aware model research</span></div></section>
<section class="work-section" id="work" aria-labelledby="work-title"><div class="container"><div class="section-heading"><div><p class="overline">RESEARCH & ENGINEERING</p><h2 id="work-title">Agents. Generation.<br><em>Efficient intelligence.</em></h2></div><p class="section-description">Explore my current work in agentic and generative AI, with earlier computer vision and biomedical research in dedicated tabs.</p></div><div class="work-tabs" role="tablist" aria-label="Explore work by domain">{tabs}</div><div class="work-intro"><div><h3 id="domain-title">{DATA['categories'][0]['title']}</h3><p id="domain-description">{DATA['categories'][0]['description']}</p></div><span id="work-count" role="status">6 selected projects</span></div><div id="work-panel" role="tabpanel" aria-labelledby="tab-selected" tabindex="0"><div class="work-grid">{''.join(project_card(p) for p in DATA['projects'])}</div></div><div class="work-footer"><span>Diagrams illustrate the methods, not experimental outputs.</span>{link('More on GitHub','https://github.com/Alireza-Ghadimi?tab=repositories')}</div><noscript><style>.work-card[hidden]{{display:flex!important}}.work-tabs,.case-link,#work-count{{display:none}}.work-intro{{display:none}}</style><p class="noscript-note">All projects are shown. Enable JavaScript for category filters and detailed case studies.</p></noscript></div></section>
<section class="experience-section container" id="experience" aria-labelledby="experience-title"><div class="section-heading"><div><p class="overline">EXPERIENCE & OWNERSHIP</p><h2 id="experience-title">From the research question<br>to the <em>running system.</em></h2></div><p class="section-description">A track record across model research, industrial perception, and the infrastructure that supports them.</p></div><div class="experience-list">{experience()}</div></section>
<section class="research-section" id="research" aria-labelledby="research-title"><div class="container"><div class="section-heading"><div><p class="overline">PUBLICATIONS & MANUSCRIPTS</p><h2 id="research-title">Questions worth<br><em>working on.</em></h2></div><p class="section-description">Published work and ongoing research, with each manuscript’s status kept explicit.</p></div><div class="publication-list">{publications()}</div></div></section>
<section class="background-section container" id="background" aria-labelledby="background-title"><div class="section-heading"><div><p class="overline">THE FOUNDATIONS</p><h2 id="background-title">Signals. Systems.<br><em>Learning.</em></h2></div><p class="section-description">A path from electrical and biomedical engineering to computer science and efficient AI.</p></div><div class="education-grid">{education()}</div><div class="award-note"><span class="award-symbol" aria-hidden="true">✳</span><div><p class="overline">AI IN FINANCE SUMMER SCHOOL · AUGUST 2026</p><h3>Hackathon winner</h3><p>Selected participant in AIFSS, presented by RBC Borealis in Vancouver; winner of the final participant hackathon challenge.</p></div></div></section>
<section class="contact-section" id="contact" aria-labelledby="contact-title"><div class="container contact-inner"><div><p class="overline">LET’S CONNECT</p><h2 id="contact-title">Good work starts<br>with a <em>conversation.</em></h2><p>Working on agents, generative models, or efficient LLMs? I’d love to hear what you’re building or researching.</p><div class="email-row"><a href="mailto:arghadimi.bme@gmail.com">arghadimi.bme@gmail.com</a><button type="button" class="copy-email" aria-label="Copy email address">Copy email</button><span id="copy-status" role="status" class="sr-only"></span></div></div><div class="contact-links">{link('GitHub','https://github.com/Alireza-Ghadimi')}{link('LinkedIn','https://www.linkedin.com/in/Alireza-Ghadimi')}<a href="{pdf_url}" download>Download résumé</a></div></div></section></main>
<footer><div class="container footer-main"><a class="brand" href="#about" aria-label="Back to Alireza Ghadimi’s introduction">{signature()}</a><p>© <span id="year">2026</span> Alireza Ghadimi</p><a href="credits.html">Image credits</a><span>Toronto / Waterloo</span></div><section class="leaflab-section" aria-labelledby="leaflab-title"><div class="container leaflab-inner"><img src="{asset('leaflab-logo-green-puzzle.png')}" width="1706" height="922" alt="LeafLab logo, a leaf formed from interlocking green letters" loading="lazy"><div><p class="overline">AN IDEA TAKING ROOT</p><h2 id="leaflab-title">LeafLab<span>.</span></h2><p>Exploring a research lab for efficient language models.</p></div></div></section></footer>
{''.join(project_dialog(p) for p in DATA['projects'])}<script type="application/json" id="category-data">{category_json}</script></body></html>'''

def credits():
    sources=json.loads((ROOT/'assets/SOURCES-assets.json').read_text())
    rows=''.join(f'<li><strong>{e(item["credit"])}</strong><br>{link("Source",item["source_page"])}</li>' for item in sources if 'source_page' in item)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>Image credits — Alireza Ghadimi</title><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="assets/fonts/fonts.css"><link rel="stylesheet" href="styles.css"></head><body><main class="container credits-page"><a class="brand" href="./" aria-label="Alireza Ghadimi home">{signature()}</a><h1>Image credits</h1><p>Organization imagery identifies my educational and professional affiliations. Copyright and trademarks remain with their respective owners.</p><h2>Organization imagery</h2><ul>{rows}</ul><h2>Personal photographs & signature</h2><p>The portrait, AG signature, and Amirkabir entrance photograph were supplied by Alireza Ghadimi. The original portrait is displayed with a slight brightness increase and a crop to the head and upper torso; the source photograph is unchanged. The signature and campus image are the original supplied files.</p><h2>Project illustrations</h2><p>The diagrams were drawn for this website to illustrate research methods. They are conceptual illustrations, rather than experimental outputs.</p><h2>LeafLab</h2><p>The LeafLab logo was created from Alireza’s original sketch and digitized with Imagegen. The approved green version has subtle shadows between its letter pieces.</p><h2>Typography</h2><p>DM Sans and Instrument Serif are self-hosted under the SIL Open Font License. License files are included with the website’s font assets.</p><h2>Content</h2><p>Experience and project descriptions are based on the supplied résumé sources, reviewed across their variants, and <a href="https://github.com/Alireza-Ghadimi">public project repositories</a>. The published paper links to its <a href="https://doi.org/10.1371/journal.pone.0273699">publisher record</a>.</p><a class="button button-green" href="./">Back to the portfolio</a></main></body></html>'''

def legacy_redirect(destination):
    # JavaScript preserves query strings and fragments. The meta refresh covers
    # readers with JavaScript disabled.
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<title>Alireza Ghadimi</title><link rel="canonical" href="{BASE}{destination}">
<script>location.replace("../{destination}" + location.search + location.hash);</script>
<meta http-equiv="refresh" content="0; url=../{destination}"></head>
<body><a href="../{destination}">Continue to the portfolio</a></body></html>
'''


if __name__ == '__main__':
    (ROOT / 'index.html').write_text(render())
    (ROOT / 'credits.html').write_text(credits())
    legacy = ROOT / 'animated'
    legacy.mkdir(exist_ok=True)
    (legacy / 'index.html').write_text(legacy_redirect(''))
    (legacy / 'credits.html').write_text(legacy_redirect('credits.html'))
    print('Built the public animated homepage and legacy redirects.')
