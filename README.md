# Alireza Ghadimi

Personal website for Alireza Ghadimi: research, projects, work experience, education, and LeafLab.

Main profile: https://alireza-ghadimi.github.io/

Full profile: https://alireza-ghadimi.github.io/full-profile/

The homepage presents the recent agent research as industry projects without naming its employer. The separate full profile includes the Huawei internship and OpenJiuwen team. Each profile downloads its matching résumé. The full profile is publicly accessible but uses `noindex`; this is an editorial presentation choice, not access control.

## Hosting

GitHub Pages serves the generated HTML, CSS, and JavaScript from the root of the `main` branch. The `.nojekyll` file disables Jekyll processing. Changes pushed to `main` are deployed by GitHub Pages. Hosting requires no dependencies or server runtime.

## Edit the site

- `content/portfolio.json`: shared project descriptions, categories, evidence, and links.
- `scripts/build-site.py`: shared templates for both profile and credit pages.
- `index.html` and `full-profile/index.html`: generated pages; edit their sources above.
- `app.js`: keyboard-accessible project tabs, native case-study dialogs, mobile menu, and email copying.
- `styles.css`: responsive layout, print styles, and reduced-motion support.
- `assets/`: the website’s images, logos, and downloadable résumé.
- `credits.html` and `assets/SOURCES-assets.json`: image sources and credits.

After editing the content, templates, CSS, JavaScript, or résumé PDFs:

```sh
python3 scripts/build-site.py
python3 scripts/check-site.py
node --check app.js
```

The generator updates cache keys for styles, scripts, and résumé downloads. All fonts and visible assets are hosted locally. Static content is readable without JavaScript; JavaScript adds category filtering and detailed case studies.

The hero uses the original supplied portrait. An SVG viewport crops out the chair and feet, and CSS applies a slight brightness increase. The face, clothes, and pose are not regenerated or reshaped.

## Preview locally

From this directory, run:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173/ in your browser.

Organization logos, photographs, and trademarks retain their respective owners’ rights. See the image credits for provenance.

## Content review

The November 2026 revision reviewed active and commented résumé material on `agentic`, `bio`, `efficiency`, `efficeincy`, `efficiency-no-huawei`, and `main`. Current dates took precedence over older variants. Public project repositories and the PLOS ONE publisher record supported artifact links and research claims.

SoftSkill's SearchQA reproduction result is attributed to that project, separately from the EdgeAlign prototype. Ongoing research and submitted manuscripts are labeled by status. Beyond Kernel Dynamics remains excluded. Application-specific résumé language and unsupported historical metrics were not carried into the site.

Design references included [Jon Barron](https://jonbarron.info/) for concise research summaries, [Eugene Yan](https://eugeneyan.com/start-here/) for topic navigation, and the portfolios of [Andrej Karpathy](https://karpathy.ai/), [Chip Huyen](https://huyenchip.com/), [Lilian Weng](https://lilianweng.github.io/), and [Chelsea Finn](https://ai.stanford.edu/~cbfinn/). The visual design, illustrations, and implementation are specific to this portfolio.
