#!/usr/bin/env python3
"""Build both static portfolio profiles from the shared, reviewed content."""
from pathlib import Path
from html import escape as e
import json, hashlib, math

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/portfolio.json').read_text())
BASE = 'https://alireza-ghadimi.github.io/'

def asset(prefix, name):
    return prefix + 'assets/' + name

def link(label, url, cls='text-link'):
    return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)}</a>'

def signature(prefix, light=False):
    return f'<span class="signature-mark"><img src="{asset(prefix, "ag-signature.png")}" width="1254" height="1254" alt=""></span>'

def art(project):
    """Conceptual, code-native diagrams. No charts imply measured output."""
    kind = project['visual']; pid = project['id']
    palettes = {'skills':('#e5eee6','#236549'), 'spectra':('#e9e7f0','#695389'), 'signals':('#e7edf1','#466c80'), 'tokens':('#e9e8f1','#766399'), 'retrieval':('#f0ece3','#8d7349'), 'feedback':('#e2edeb','#24706b'), 'roads':('#e8ece8','#456452'), 'eeg':('#e9edf3','#536e98'), 'ecg':('#e6eeee','#397775')}
    bg, ink = palettes.get(kind, ('#e9eee8','#507456'))
    shapes = []
    def text(x,y,value,size=12,opacity=1):
        return f'<text x="{x}" y="{y}" font-size="{max(size,14)}" fill="{ink}" opacity="{opacity}" font-family="Arial,sans-serif" letter-spacing="1">{e(value)}</text>'
    if kind == 'skills':
        shapes += [f'<rect x="66" y="57" width="104" height="139" rx="6" fill="white" fill-opacity=".55" stroke="{ink}" stroke-opacity=".3"/>']
        shapes += [f'<path d="M85 {82+i*17}h{62-(i%3)*10}" stroke="{ink}" opacity=".4" stroke-width="3" stroke-linecap="round"/>' for i in range(6)]
        shapes += [f'<path d="M191 128h54m-8-5 8 5-8 5" fill="none" stroke="{ink}" stroke-width="1.5"/>']
        shapes += [f'<rect x="{274+(i%8)*25}" y="{79+(i//8)*28}" width="18" height="20" rx="3" fill="{ink}" opacity="{.25+(i%4)*.2}"/>' for i in range(32)]
        shapes += [text(66,224,'TEXT INSTRUCTIONS',10),text(274,224,'LEARNED REPRESENTATIONS',10)]
    elif kind=='feedback':
        for x,label in [(58,'AGENT'),(239,'TOOLS'),(420,'FEEDBACK')]:
            shapes += [f'<rect x="{x}" y="70" width="122" height="106" rx="9" fill="white" fill-opacity=".5" stroke="{ink}" stroke-opacity=".3"/>',text(x+11,197,label,14)]
        for row in range(3):
            for col in range(3): shapes.append(f'<rect x="{88+col*23}" y="{96+row*20}" width="14" height="12" rx="2" fill="{ink}" opacity="{.3+row*.25}"/>')
        shapes += [f'<path d="m279 107-16 17 16 16m42-33 16 17-16 16m-17-39-11 48" fill="none" stroke="{ink}" stroke-width="2.5" stroke-linecap="round"/>',f'<path d="m451 122 17 18 34-37" fill="none" stroke="{ink}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',f'<path d="M181 124h56m125 0h56M482 210v13H119v-13" fill="none" stroke="{ink}" stroke-dasharray="4 5" opacity=".7"/>']
    elif kind=='memory':
        for i,(x,label) in enumerate([(68,'CAPTURE'),(249,'UPDATE'),(430,'REUSE')]):
            shapes += [f'<rect x="{x}" y="74" width="104" height="110" rx="7" fill="white" fill-opacity=".5" stroke="{ink}" stroke-opacity=".4"/>',text(x+10,216,label,14)]
            for row in range(3):
                for col in range(3): shapes.append(f'<rect x="{x+21+col*23}" y="{96+row*23}" width="16" height="16" rx="3" fill="{ink}" opacity="{.2+((row+col+i)%4)*.2}"/>')
        shapes += [f'<path d="M174 127h72m109 0h72M301 74V39h180v35" fill="none" stroke="{ink}" stroke-width="1.5" stroke-dasharray="4 4"/>',f'<circle cx="300" cy="40" r="8" fill="{ink}"/>']
    elif kind in ['spectra','generation']:
        for row in range(6):
            for col in range(7):
                hue=['#5d8772','#9eb39a','#c5c9a3','#6b6b91','#a18eb2','#d8cbb5'][(row+col*3)%6]
                shapes.append(f'<rect x="{65+col*21}" y="{63+row*23}" width="18" height="20" rx="2" fill="{hue}"/>')
        shapes += [f'<path d="M247 128h44" stroke="{ink}" opacity=".5"/>']
        for j in range(3):
            points=' '.join(f'{320+x},{138+math.sin(x/28+j*1.4)*31+math.cos(x/11)*8+j*11}' for x in range(0,202,3))
            shapes.append(f'<polyline points="{points}" fill="none" stroke="{ink}" stroke-width="2" opacity="{.35+j*.3}"/>')
        shapes += [text(65,226,'MULTIMODAL INPUT',10),text(319,226,'SPECTRAL REPRESENTATION',10)]
    elif kind in ['signals','eeg','ecg']:
        for j in range(3):
            pts=[]
            for x in range(470):
                spike=(x+37*j)%94
                value=(-32 if spike in range(39,44) else 21 if spike in range(44,49) else 0)
                pts.append(f'{65+x},{72+j*59+math.sin(x/14+j)*5+value}')
            shapes.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{ink}" stroke-width="1.8" opacity="{.4+j*.25}"/>')
        shapes += [text(65,238,'SIGNALS · MODELS · INFERENCE',10)]
    elif kind in ['tokens','attention']:
        for row in range(4):
            for col in range(12):
                active=col<=row*3 if kind=='attention' else (col+row)%4!=0
                shapes.append(f'<rect x="{66+col*39}" y="{58+row*39}" width="30" height="29" rx="4" fill="{ink if active else "white"}" fill-opacity="{.25+row*.15 if active else .6}" stroke="{ink}" stroke-opacity=".22"/>')
        shapes += [text(66,239,'CONTEXT',10),text(368,239,'PARALLEL COMPUTATION',10)]
    elif kind in ['retrieval','service']:
        for x,label in [(62,'DOCUMENTS'),(246,'RETRIEVAL'),(432,'CONTEXT')]:
            shapes += [f'<rect x="{x}" y="76" width="112" height="103" rx="8" fill="white" fill-opacity=".55" stroke="{ink}" stroke-opacity=".4"/>',text(x+11,210,label,10)]
        shapes += [f'<path d="M175 126h70m113 0h74" stroke="{ink}" stroke-dasharray="3 5"/>']
        for x in [81,267,452]: shapes += [f'<path d="M{x} {103+j*19}h71" stroke="{ink}" stroke-width="3" opacity="{.25+j*.2}"/>' for j in range(3)]
    elif kind=='roads':
        shapes += [f'<path d="M204 260 282 0h58l100 260Z" fill="{ink}" fill-opacity=".25"/>',f'<path d="M297 260 311 0" stroke="white" stroke-width="3" stroke-dasharray="12 13"/>',f'<path d="M204 260 282 0M440 260 340 0" fill="none" stroke="{ink}" stroke-width="2"/>']
        shapes += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="none" stroke="{ink}" stroke-dasharray="5 4"/>' for x,y,w,h in [(237,125,55,35),(333,180,61,40),(292,54,34,22)]]
        shapes += [text(38,40,'SEGMENT',10),text(427,227,'REFINE',10)]
    elif kind=='landmarks':
        shapes += [f'<ellipse cx="300" cy="121" rx="76" ry="93" fill="none" stroke="{ink}" opacity=".5"/>',f'<path d="M260 115 280 105 300 140 320 105 340 115M276 165q24 14 48 0" fill="none" stroke="{ink}"/>']
        shapes += [f'<circle cx="{x}" cy="{y}" r="7" fill="{ink}"/>' for x,y in [(263,113),(336,113),(300,143),(277,165),(324,165),(300,211)]]
        shapes += [text(52,231,'RGB + LANDMARK HEATMAPS',10)]
    else:
        for i in range(13): shapes.append(f'<rect x="{67+i*36}" y="{55+(i%4)*9}" width="29" height="{148-(i%4)*18}" rx="7" fill="hsl({125+i*15} 23% {35+i*3}%)"/>')
        shapes += [text(67,233,'CONDITION · GENERATE · EVALUATE',10)]
    return f'<svg viewBox="0 0 600 260" aria-hidden="true" focusable="false"><rect width="600" height="260" fill="{bg}"/>{"".join(shapes)}</svg>'

def project_card(p, motion=False, prefix=''):
    visual=art(p)
    if motion:
        poster=asset(prefix,'project-motion/'+p['id']+'.png')
        gif=asset(prefix,'project-motion/'+p['id']+'.gif')
        visual=f'<img class="project-motion" src="{poster}" data-poster="{poster}" data-gif="{gif}" width="600" height="260" alt="" loading="lazy" decoding="async">'
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

def experience(full,prefix):
    if full:
        first={'date':'Sep 2026–present','name':'Huawei','role':'ML Research Scientist Intern · Agent Evolution','meta':'OpenJiuwen Team · Markham, ON','logo':None,'body':'Researching how agents improve through <strong>learned skills and execution feedback</strong>, under constraints on compute and context.','bullets':['Designed the <strong>EdgeAlign research prototype</strong> around forward-only skill optimization.','Built evaluation and runtime support; investigated soft-token skills and contributed to the OpenJiuwen framework.']}
    else:
        first={'date':'Sep 2026–present','name':'Agentic AI research & engineering','role':'Industry project experience','meta':'Learned skills · Execution feedback · Evaluation','logo':None,'body':'Researching how agents improve through <strong>learned skills and execution feedback</strong>, under constraints on compute and context.','bullets':['Designed the <strong>EdgeAlign research prototype</strong> around forward-only skill optimization.','Built prompt-embedding and sandboxed evaluation support, and investigated feedback from tool execution.']}
    rows=[first,
      {'date':'Jan–Jul 2026','name':'Strayos','role':'AI Engineer · Computer Vision','meta':'Toronto, ON','logo':'company-strayos-logo.svg','body':'Owned <strong>road-scene segmentation and anomaly detection</strong> from data curation through training, evaluation, and deployment.','bullets':['Built a <strong>human-in-the-loop active-learning pipeline</strong> to turn corrected annotations into model improvements.','Analyzed failures, prioritized difficult cases, and improved the retraining workflow.']},
      {'date':'May 2022–Dec 2024','name':'EnerSoft','role':'Lead Data Scientist · Computer Vision','meta':'Toronto, ON','logo':'company-enersoft-logo.png','body':'Built and deployed <strong>RGB–hyperspectral perception systems</strong> that reduced manual-review costs by <strong>$200K annually</strong>.','bullets':['Led production troubleshooting for <strong>6+ months</strong>, coordinating model-failure analysis and fixes.','Built scalable training, inference, and distributed evaluation workflows; improved legacy-code reliability.']},
      {'date':'Feb–May 2022','name':'Fusion Analytics','role':'Data Engineer','meta':'Toronto, ON','logo':'company-fusion-logo.png','body':'Built the data infrastructure behind analytical workflows: <strong>Azure and SQL ETL pipelines</strong>, large-scale auditing, and Python dashboards.','bullets':['Used <strong>PySpark and SQL</strong> to audit and balance datasets for downstream analysis.']}]
    out=[]
    for r in rows:
        mark=f'<img src="{asset(prefix,r["logo"])}" alt="" loading="lazy">' if r['logo'] else '<span class="experience-monogram" aria-hidden="true">'+({'EnerSoft':'EN','Strayos':'CV'}.get(r['name'],'AI'))+'</span>'
        out.append(f'''<article class="experience-row"><div class="experience-date">{e(r['date'])}</div><div class="experience-main"><div class="experience-title">{mark}<div><h3>{e(r['name'])}</h3><p>{e(r['role'])}</p></div></div><p class="experience-meta">{e(r['meta'])}</p><p class="experience-summary">{r['body']}</p><ul>{''.join('<li>'+b+'</li>' for b in r['bullets'])}</ul></div></article>''')
    return ''.join(out)

def publications():
    rows=[
      ('Published · PLOS ONE · 2022','Inferring stimulation induced short-term synaptic plasticity dynamics using novel dual optimization algorithm','<strong>A. Ghadimi</strong>, L. A. Steiner, M. R. Popovic, L. Milosevic, M. Lankarany','Computational inference of short-term synaptic dynamics under stimulation.','https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0273699'),
      ('Submitted · IEEE T-BIOM','A Scoping Review of Model Compression for Biometric and Bio-Signal Authentication Systems','<strong>A. Ghadimi</strong>, M. Moodi, A. Ghodsi, T. H. Falk','Connecting efficient models with biometric and biosignal authentication.',None),
      ('Manuscript in preparation','Electroencephalography Foundation Model-Based Soft Biometrics: A Performance Comparison of Age and Biological Sex Prediction','M. Jaberi, M. Moodi, <strong>A. Ghadimi</strong>, A. Jafari, A. Ghodsi, T. H. Falk','Collaborative research on EEG foundation-model representations.',None),
      ('Research in progress','ARMD-QWEN: Fine-tuning large language models for generating multiple tokens during inference','<strong>A. Ghadimi</strong>, M. Karami, A. Jafari, A. Ghodsi','Adapting pretrained language models for masked-diffusion generation.',None)]
    return ''.join(f'''<article class="publication {'published' if i==0 else ''}"><p class="paper-status">{e(status)}</p><div><h3>{f'<a href="{url}" target="_blank" rel="noopener noreferrer">{e(title)}</a>' if url else e(title)}</h3><p class="paper-authors">{authors}</p><p class="paper-summary">{e(summary)}</p>{link('Read paper',url) if url else ''}</div></article>''' for i,(status,title,authors,summary,url) in enumerate(rows))

def education(prefix):
    rows=[('University of Waterloo','PhD · Computer Science','2026–present','Efficient language models, agent learning, and GPU-aware research.','waterloo','jpg','Mathematics 3 at the University of Waterloo','https://uwaterloo.ca/'),('University of Toronto','M.Sc. · Biomedical Engineering','2019–2021','Stochastic modeling, machine learning, and neural dynamics.','toronto','png','Convocation Hall at the University of Toronto','https://www.utoronto.ca/'),('Amirkabir University of Technology','B.Sc. · Electrical Engineering','2014–2019','Signal processing and physiological sensing.','amirkabir','png','The entrance of Amirkabir University of Technology','https://aut.ac.ir/')]
    out=[]
    for name,degree,years,focus,key,ext,alt,url in rows:
        logo='institution-'+key+'-logo.'+('svg' if key=='toronto' else 'png')
        out.append(f'''<article class="education-card"><a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Visit {e(name)}"><img class="campus-photo" src="{asset(prefix,'institution-'+key+'-campus.'+ext)}" alt="{e(alt)}" width="600" height="400" loading="lazy"></a><div class="education-body"><div class="education-top"><img class="education-logo logo-{key}" src="{asset(prefix,logo)}" alt="" loading="lazy"><span>{years}</span></div><h3>{e(name)}</h3><p class="degree">{degree}</p><p>{focus}</p></div></article>''')
    return ''.join(out)

def render(full=False, motion=False):
    prefix=('../../' if full else '../') if motion else ('../' if full else '')
    resume='Alireza-Ghadimi-Resume-Full.pdf' if full else 'Alireza-Ghadimi-Resume.pdf'
    pdf=ROOT/'assets'/resume
    version=hashlib.sha256(pdf.read_bytes()).hexdigest()[:12] if pdf.exists() else 'preview'
    pdf_url=asset(prefix,resume)+'?v='+version
    css_hash=hashlib.sha256((ROOT/'styles.css').read_bytes()).hexdigest()[:10]
    js_hash=hashlib.sha256((ROOT/'app.js').read_bytes()).hexdigest()[:10]
    canonical=BASE+('full-profile/' if full else '')
    category_json=json.dumps(DATA['categories'])
    bio='I research how language-model agents learn from execution feedback and how generative models can do more with less computation. I’m a Computer Science PhD student at the University of Waterloo and an ML Research Scientist Intern at Huawei.' if full else 'I research how language-model agents learn from execution feedback and how generative models can do more with less computation. I’m a Computer Science PhD student at the University of Waterloo, building on experience taking ML systems into production.'
    logos=[('Waterloo','institution-waterloo-logo.png','waterloo'),('University of Toronto','institution-toronto-logo.svg','toronto'),('Amirkabir University','institution-amirkabir-logo.png','amirkabir')]
    logos.extend([('Strayos','company-strayos-logo.svg','strayos'),('Fusion Analytics','company-fusion-logo.png','fusion'),('EnerSoft','company-enersoft-logo.png','enersoft')])
    logo_html=''.join(f'<img src="{asset(prefix,file)}" class="logo-{key}" alt="{name}" loading="lazy">' for name,file,key in logos)
    tabs=''.join(f'<button id="tab-{c["id"]}" type="button" role="tab" aria-selected="{str(i==0).lower()}" aria-controls="work-panel" tabindex="{0 if i==0 else -1}" data-filter="{c["id"]}">{e(c["label"])}</button>' for i,c in enumerate(DATA['categories']))
    structured={'@context':'https://schema.org','@type':'Person','name':'Alireza Ghadimi','url':canonical,'jobTitle':'ML Research Scientist and Computer Science PhD Student','sameAs':['https://github.com/Alireza-Ghadimi','https://www.linkedin.com/in/Alireza-Ghadimi'],'affiliation':{'@type':'CollegeOrUniversity','name':'University of Waterloo'}}
    page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f7f9f6"><meta name="description" content="Alireza Ghadimi: agentic AI, generative models, and efficient LLM research. Waterloo Computer Science PhD student studying learned agent skills, execution feedback, and multi-token generation."><meta property="og:title" content="Alireza Ghadimi — Agentic AI & Generative Models"><meta property="og:description" content="Efficient models. Adaptive agents. Research on agent learning, compact skills, and generative AI at the University of Waterloo."><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}assets/alireza-portrait-original.jpg"><link rel="canonical" href="{canonical}">{'<meta name="robots" content="noindex,follow">' if full else ''}<title>Alireza Ghadimi — Agentic AI & Generative Models</title><link rel="icon" href="{asset(prefix,'favicon.svg')}" type="image/svg+xml"><link rel="preload" href="{asset(prefix,'fonts/instrument-serif-normal-400.woff')}" as="font" type="font/woff" crossorigin><link rel="stylesheet" href="{asset(prefix,'fonts/fonts.css')}"><link rel="stylesheet" href="{prefix}styles.css?v={css_hash}"><script src="{prefix}app.js?v={js_hash}" defer></script><script type="application/ld+json">{json.dumps(structured)}</script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="#about" aria-label="Alireza Ghadimi home">{signature(prefix)}</a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav">Menu <span aria-hidden="true">☰</span></button><nav id="main-nav" aria-label="Main navigation"><a href="#work">Work</a><a href="#experience">Experience</a><a href="#research">Research</a><a href="#background">Background</a><a class="nav-contact" href="#contact">Let’s talk</a></nav></div></header>
<main id="main"><section class="hero container" id="about" aria-labelledby="hero-title"><div class="hero-copy"><p class="overline hero-overline"><span aria-hidden="true"></span>AGENTIC AI · GENERATIVE AI · LLM RESEARCH</p><h1 id="hero-title">Alireza<br>Ghadimi<span>.</span></h1><p class="hero-thesis">Efficient models.<br> <em>Adaptive agents.</em></p><p class="hero-bio">{bio}</p><div class="hero-actions"><a class="button button-green" href="#work">Explore my work</a><a class="button button-outline" href="{pdf_url}" download>Download résumé</a></div><p class="hero-location">Toronto / Waterloo, Canada <span aria-hidden="true">·</span> {link('GitHub','https://github.com/Alireza-Ghadimi')}</p></div><div class="portrait-area"><div class="portrait-frame"><svg class="portrait" viewBox="440 270 1480 1470" preserveAspectRatio="xMidYMin slice" role="img" aria-labelledby="portrait-title"><title id="portrait-title">Alireza Ghadimi in a blue suit, cropped to his head and upper torso</title><image href="{asset(prefix,'alireza-portrait-original.jpg')}" width="2080" height="3120"/></svg><div class="portrait-caption"><span>ML RESEARCH SCIENTIST · PHD STUDENT</span><span aria-hidden="true">AG / 2026</span></div></div><p class="portrait-note">Learning from feedback.<br>Doing more with less.</p><span class="portrait-outline" aria-hidden="true"></span></div></section>
<section class="affiliations container" aria-label="Academic and industry background"><p class="overline">ACADEMIC & INDUSTRY EXPERIENCE</p><div class="logo-strip">{logo_html}</div></section>
<section class="perspective container" aria-labelledby="perspective-title"><div><p class="overline">MY RESEARCH FOCUS</p><h2 id="perspective-title">Making agents learn.<br><em>Making models efficient.</em></h2></div><div class="perspective-copy"><p>How can an agent turn execution feedback into a reusable skill? How can a generative model make better use of its computation? These questions guide my research.</p><p>I work across <strong>learned agent skills, compact memory, and efficient generation</strong>, connecting model research with the training, inference, and evaluation systems needed to test it.</p></div></section>
<section class="impact-strip container" aria-label="Selected experience highlights"><div><strong>Agent learning</strong><span>Skills and memory that improve<br>through execution feedback</span></div><div><strong>32 vectors</strong><span>Compact learned skills evaluated<br>in my SoftSkill reproduction</span></div><div><strong>Efficient GenAI</strong><span>Masked diffusion, parallel generation,<br>and GPU-aware model research</span></div></section>
<section class="work-section" id="work" aria-labelledby="work-title"><div class="container"><div class="section-heading"><div><p class="overline">RESEARCH & ENGINEERING</p><h2 id="work-title">Agents. Generation.<br><em>Efficient intelligence.</em></h2></div><p class="section-description">Explore my current work in agentic and generative AI, with earlier computer vision and biomedical research in dedicated tabs.</p></div><div class="work-tabs" role="tablist" aria-label="Explore work by domain">{tabs}</div><div class="work-intro"><div><h3 id="domain-title">{DATA['categories'][0]['title']}</h3><p id="domain-description">{DATA['categories'][0]['description']}</p></div><span id="work-count" role="status">6 selected projects</span></div><div id="work-panel" role="tabpanel" aria-labelledby="tab-selected" tabindex="0"><div class="work-grid">{''.join(project_card(p,motion,prefix) for p in DATA['projects'])}</div></div><div class="work-footer"><span>Diagrams illustrate the methods, not experimental outputs.</span>{link('More on GitHub','https://github.com/Alireza-Ghadimi?tab=repositories')}</div><noscript><style>.work-card[hidden]{{display:flex!important}}.work-tabs,.case-link,#work-count{{display:none}}.work-intro{{display:none}}</style><p class="noscript-note">All projects are shown. Enable JavaScript for category filters and detailed case studies.</p></noscript></div></section>
<section class="experience-section container" id="experience" aria-labelledby="experience-title"><div class="section-heading"><div><p class="overline">EXPERIENCE & OWNERSHIP</p><h2 id="experience-title">From the research question<br>to the <em>running system.</em></h2></div><p class="section-description">A track record across model research, industrial perception, and the infrastructure that supports them.</p></div><div class="experience-list">{experience(full,prefix)}</div></section>
<section class="research-section" id="research" aria-labelledby="research-title"><div class="container"><div class="section-heading"><div><p class="overline">PUBLICATIONS & MANUSCRIPTS</p><h2 id="research-title">Questions worth<br><em>working on.</em></h2></div><p class="section-description">Published work and ongoing research, with each manuscript’s status kept explicit.</p></div><div class="publication-list">{publications()}</div></div></section>
<section class="background-section container" id="background" aria-labelledby="background-title"><div class="section-heading"><div><p class="overline">THE FOUNDATIONS</p><h2 id="background-title">Signals. Systems.<br><em>Learning.</em></h2></div><p class="section-description">A path from electrical and biomedical engineering to computer science and efficient AI.</p></div><div class="education-grid">{education(prefix)}</div><div class="award-note"><span class="award-symbol" aria-hidden="true">✳</span><div><p class="overline">AI IN FINANCE SUMMER SCHOOL · AUGUST 2026</p><h3>Hackathon winner</h3><p>Selected participant in AIFSS, presented by RBC Borealis in Vancouver; winner of the final participant hackathon challenge.</p></div></div></section>
<section class="contact-section" id="contact" aria-labelledby="contact-title"><div class="container contact-inner"><div><p class="overline">LET’S CONNECT</p><h2 id="contact-title">Good work starts<br>with a <em>conversation.</em></h2><p>Working on agents, generative models, or efficient LLMs? I’d love to hear what you’re building or researching.</p><div class="email-row"><a href="mailto:arghadimi.bme@gmail.com">arghadimi.bme@gmail.com</a><button type="button" class="copy-email" aria-label="Copy email address">Copy email</button><span id="copy-status" role="status" class="sr-only"></span></div></div><div class="contact-links">{link('GitHub','https://github.com/Alireza-Ghadimi')}{link('LinkedIn','https://www.linkedin.com/in/Alireza-Ghadimi')}<a href="{pdf_url}" download>Download résumé</a></div></div></section></main>
<footer><div class="container footer-main"><a class="brand" href="#about" aria-label="Back to Alireza Ghadimi’s introduction">{signature(prefix)}</a><p>© <span id="year">2026</span> Alireza Ghadimi</p><a href="credits.html">Image credits</a><span>Toronto / Waterloo</span></div><section class="leaflab-section" aria-labelledby="leaflab-title"><div class="container leaflab-inner"><img src="{asset(prefix,'leaflab-logo-green-puzzle.png')}" width="1706" height="922" alt="LeafLab logo, a leaf formed from interlocking green letters" loading="lazy"><div><p class="overline">AN IDEA TAKING ROOT</p><h2 id="leaflab-title">LeafLab<span>.</span></h2><p>Exploring a research lab for efficient language models.</p></div></div></section></footer>
{''.join(project_dialog(p) for p in DATA['projects'])}<script type="application/json" id="category-data">{category_json}</script></body></html>'''
    return add_motion(page,full,prefix) if motion else page

def add_motion(page, full, prefix):
    """Enhance the separate motion edition; keep classic output unchanged."""
    css_hash=hashlib.sha256((ROOT/'motion.css').read_bytes()).hexdigest()[:10]
    js_hash=hashlib.sha256((ROOT/'motion.js').read_bytes()).hexdigest()[:10]
    extra=f'<link rel="stylesheet" href="{prefix}motion.css?v={css_hash}"><script src="{prefix}motion.js?v={js_hash}" defer></script>'
    if not full:
        extra+='<meta name="robots" content="noindex,follow">'
    page=page.replace('</head>',extra+'</head>')
    page=page.replace('<body>','<body class="motion-edition">')
    page=page.replace('<title>Alireza Ghadimi — Agentic AI & Generative Models</title>','<title>Alireza Ghadimi — Motion Edition</title>')
    classic=prefix+('full-profile/' if full else '')
    controls=f'''<div class="reading-progress" aria-hidden="true"><span></span></div><aside class="motion-controls" aria-label="Display options"><a href="{classic}">Classic view</a><button type="button" id="motion-toggle" aria-pressed="false"><span class="motion-symbol" aria-hidden="true"><i></i><i></i><i></i></span><span class="motion-toggle-label">Pause motion</span></button></aside>'''
    page=page.replace('</header>','</header>'+controls,1)
    page=page.replace('<div class="hero-copy">','<div class="hero-atmosphere" aria-hidden="true"><div class="hero-orbits"><span></span><span></span><span></span><b></b><b></b><b></b></div></div><div class="hero-copy">',1)
    page=page.replace('<h1 id="hero-title">Alireza<br>Ghadimi<span>.</span></h1>','<h1 id="hero-title"><span class="name-line"><span>Alireza</span></span>\n<span class="name-line"><span>Ghadimi<b>.</b></span></span></h1>')
    page=page.replace('<div class="container header-inner">','<div class="container header-inner"><span class="edition-label">Motion edition</span>',1)
    return page

def credits(full=False, motion=False):
    prefix=('../../' if full else '../') if motion else ('../' if full else '')
    sources=json.loads((ROOT/'assets/SOURCES-assets.json').read_text())
    rows=''.join(f'<li><strong>{e(item["credit"])}</strong><br>{link("Source",item["source_page"])}</li>' for item in sources if 'source_page' in item and (full or item['file']!='company-huawei-logo.png'))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>Image credits — Alireza Ghadimi</title><link rel="icon" href="{prefix}assets/favicon.svg"><link rel="stylesheet" href="{prefix}assets/fonts/fonts.css"><link rel="stylesheet" href="{prefix}styles.css"></head><body><main class="container credits-page"><a class="brand" href="./" aria-label="Alireza Ghadimi home">{signature(prefix)}</a><h1>Image credits</h1><p>Organization imagery identifies my educational and professional affiliations. Copyright and trademarks remain with their respective owners.</p><h2>Organization imagery</h2><ul>{rows}</ul><h2>Personal photographs & signature</h2><p>The portrait, AG signature, and Amirkabir entrance photograph were supplied by Alireza Ghadimi. The original portrait is displayed with a slight brightness increase and a crop to the head and upper torso; the source photograph is unchanged. The signature and campus image are the original supplied files.</p><h2>Project illustrations</h2><p>The diagrams were drawn for this website to illustrate research methods. They are conceptual illustrations, rather than experimental outputs.</p><h2>LeafLab</h2><p>The LeafLab logo was created from Alireza’s original sketch and digitized with Imagegen. The approved green version has subtle shadows between its letter pieces.</p><h2>Typography</h2><p>DM Sans and Instrument Serif are self-hosted under the SIL Open Font License. License files are included with the website’s font assets.</p><h2>Content</h2><p>Experience and project descriptions are based on the supplied résumé sources, reviewed across their variants, and <a href="https://github.com/Alireza-Ghadimi">public project repositories</a>. The published paper links to its <a href="https://doi.org/10.1371/journal.pone.0273699">publisher record</a>.</p><a class="button button-green" href="./">Back to the portfolio</a></main></body></html>'''

if __name__=='__main__':
    (ROOT/'index.html').write_text(render(False))
    (ROOT/'full-profile').mkdir(exist_ok=True)
    (ROOT/'full-profile/index.html').write_text(render(True))
    (ROOT/'credits.html').write_text(credits(False))
    (ROOT/'full-profile/credits.html').write_text(credits(True))
    for full in (False,True):
        folder=ROOT/'animated'/('full-profile' if full else '')
        folder.mkdir(parents=True,exist_ok=True)
        (folder/'index.html').write_text(render(full,motion=True))
        (folder/'credits.html').write_text(credits(full,motion=True))
    print('Built classic and animated editions, each with neutral and full profiles.')
