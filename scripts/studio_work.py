"""Build the studio edition's project index and illustrated research chapters."""
from html import escape


# Lead with a different project in each chapter. All other projects retain their
# source order, including projects that belong to more than one research area.
LEAD_PROJECTS = {
    'agents': 'edgealign',
    'genai': 'document-rag',
    'llm': 'armd',
}


def chapter_projects(category, projects):
    if category == 'selected':
        return [p for p in projects if p['featured']]
    matches = [p for p in projects if category in p['categories']]
    lead = LEAD_PROJECTS.get(category)
    return sorted(matches, key=lambda p: p['id'] != lead)


def project_panel(project, prefix, chapter):
    project_id = project['id']
    panel_id = f'study-{chapter}-{project_id}'
    art = f'{prefix}assets/project-motion/{project_id}'
    links = ''.join(
        f'<a href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a>'
        for link in project['links']
    )
    tags = ''.join(f'<li>{escape(tag)}</li>' for tag in project['tags'])
    contributions = ''.join(f'<li>{escape(item)}</li>' for item in project['contributions'])
    return f'''<article class="sw-study" id="{panel_id}" data-study="{project_id}">
      <div class="sw-image"><img src="{art}.png" data-poster="{art}.png" data-gif="{art}.gif" width="600" height="260" alt="" loading="lazy" decoding="async"></div>
      <div class="sw-meta"><span>{escape(project['context'])}</span><span>{escape(project['status'])}</span></div>
      <h4>{escape(project['title'])}</h4>
      <p class="sw-summary">{project['summary']}</p>
      <ul class="sw-tags" aria-label="Methods">{tags}</ul>
      <div class="sw-links"><button type="button" data-case="{project_id}" aria-haspopup="dialog" aria-label="Read case study for {escape(project['short'], quote=True)}">Read case study</button>{links}</div>
      <noscript><details class="sw-fallback"><summary>Read case study</summary><p>{escape(project['problem'])}</p><ul>{contributions}</ul><p>{escape(project['evidence'])}</p><p>{escape(project['note'])}</p></details></noscript>
    </article>'''


def work_chapter(category, projects, prefix):
    chapter = category['id']
    tabs = ''.join(
        f'<li><a id="choose-{chapter}-{p["id"]}" data-choose="{p["id"]}" href="#study-{chapter}-{p["id"]}"><span>{escape(p["short"])}</span></a></li>'
        for p in projects
    )
    panels = ''.join(project_panel(p, prefix, chapter) for p in projects)
    return f'''<section class="sw-chapter" id="work-{chapter}" aria-labelledby="heading-{chapter}">
      <div class="sw-inset">
        <div class="sw-chapter-heading"><h3 id="heading-{chapter}">{escape(category['label'])}</h3>
          <div><p class="sw-deck">{escape(category['title'])}</p><p class="sw-intro">{escape(category['description'])}</p></div>
        </div>
        <div class="sw-gallery"><ol class="sw-chooser" aria-label="{escape(category['label'])} projects">{tabs}</ol>
          <div class="sw-display">{panels}</div>
        </div>
        <a class="sw-return" href="#work-index">Project index</a>
      </div>
    </section>'''


def render_work(data, prefix):
    rows = []
    chapters = []
    for category in data['categories']:
        chapter = category['id']
        projects = chapter_projects(chapter, data['projects'])
        rows.append(f'''<li><a href="#work-{chapter}" data-field="{chapter}"><span>{escape(category['label'])}</span><span>{escape(category['title'])}</span><span>{len(projects):02d}</span></a></li>''')
        chapters.append(work_chapter(category, projects, prefix))
    return f'''<section id="work" aria-labelledby="work-title">
      <noscript><style>#work .sw-links button {{ display: none }}</style></noscript>
      <div class="sw-directory" id="work-index"><div class="sw-inset">
        <h2 id="work-title">Research &amp; engineering</h2>
        <p>Explore my current work in agentic and generative AI, with earlier computer vision and biomedical research.</p>
        <nav aria-label="Project index"><ol>{''.join(rows)}</ol></nav>
      </div></div>
      {''.join(chapters)}
      <div class="sw-end"><div class="sw-inset"><p>Diagrams illustrate the methods, not experimental outputs.</p><a href="https://github.com/Alireza-Ghadimi?tab=repositories">More on GitHub</a></div></div>
    </section>'''
