# Alireza Ghadimi

Personal website for Alireza Ghadimi: research, projects, work experience, education, and LeafLab.

Main profile: https://alireza-ghadimi.github.io/

Full profile: https://alireza-ghadimi.github.io/full-profile/

Animated edition: https://alireza-ghadimi.github.io/animated/

Animated full profile: https://alireza-ghadimi.github.io/animated/full-profile/

[Research Studio](https://alireza-ghadimi.github.io/studio/) and its [full profile](https://alireza-ghadimi.github.io/studio/full-profile/) use the same project catalog, case studies, and résumés. Its templates are in `scripts/build-studio.py` and `scripts/studio_work.py`. Styles, navigation, and animated research symbols live in `studio/`.

The homepage presents the recent agent research as industry projects without naming its employer. The separate full profile includes the Huawei internship and OpenJiuwen team. Each profile downloads its matching résumé. The full profile is publicly accessible but uses `noindex`; this is an editorial presentation choice, not access control.

## Hosting

GitHub Pages serves the generated HTML, CSS, and JavaScript from the root of the `main` branch. The `.nojekyll` file disables Jekyll processing. Changes pushed to `main` are deployed by GitHub Pages. Hosting requires no dependencies or server runtime.

## Edit the site

- `content/portfolio.json`: shared project descriptions, categories, evidence, and links.
- `scripts/build-site.py`: shared templates for both profile and credit pages.
- `index.html` and `full-profile/index.html`: generated pages; edit their sources above.
- `app.js`: keyboard-accessible project tabs, native case-study dialogs, mobile menu, and email copying.
- `styles.css`: responsive layout, print styles, and reduced-motion support.
- `motion.css` and `motion.js`: separate animated edition with scroll reveals, portrait parallax, an unfolding timeline, card transitions, and a persistent pause control.
- `animated/`: generated motion pages, using the same content and matching résumé variants as the classic edition.
- `assets/project-motion/`: 15 original conceptual GIFs and static PNG posters; GIFs only play while visible and motion is enabled.
- `assets/`: the website’s images, logos, and downloadable résumé.
- `credits.html` and `assets/SOURCES-assets.json`: image sources and credits.

After editing the content, templates, CSS, JavaScript, or résumé PDFs:

```sh
python3 scripts/build-site.py
python3 scripts/check-site.py
node --check app.js
node --check motion.js
```

The generator updates cache keys for styles, scripts, and résumé downloads. All fonts and visible assets are hosted locally. Static content is readable without JavaScript; JavaScript adds category filtering and detailed case studies.

The hero uses the original supplied portrait. An SVG viewport crops out the chair and feet, and CSS applies a slight brightness increase. The face, clothes, and pose are not regenerated or reshaped.

The animated edition respects the device's reduced-motion setting. Its pause control replaces GIFs with static posters, disables ambient motion and scroll transitions, and remembers the choice. Offscreen animations use posters to limit decoding work. Without JavaScript, the full project collection and static posters remain readable. Both animated pages use `noindex` and point to the matching classic page as canonical.

To regenerate the 600×260 conceptual project GIFs (requires Python and Pillow):

```sh
python3 scripts/build-project-motion.py
```

Each animation has 48 frames and a 3.84-second loop. These are illustrative methods, not recordings or experimental results. The whole GIF set is about 2 MB. The script selects local system fonts; the committed rendered assets are ready to serve without installing anything.

For the motion interaction checks, run a local server and use Node with Playwright installed:

```sh
node scripts/check-motion.cjs
```

`SITE_URL` can override `http://127.0.0.1:4173`; `CHROMIUM_PATH` can point to a local Chrome executable.

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
