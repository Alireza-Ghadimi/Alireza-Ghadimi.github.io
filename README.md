# Alireza Ghadimi

Personal website for Alireza Ghadimi: research, projects, work experience, education, and LeafLab.

Website: https://alireza-ghadimi.github.io/

## Hosting

GitHub Pages serves this repository from the root of the `main` branch. The site is plain HTML, CSS, and JavaScript; no build step is required. The `.nojekyll` file disables Jekyll processing. Changes pushed to `main` are deployed by GitHub Pages.

## Edit the site

- `index.html`: introduction, research, contact details, and page structure.
- `app.js`: project tabs, work history, education, and interactions.
- `styles.css`: responsive layout and visual styling.
- `assets/`: the website’s images, logos, and downloadable résumé.
- `credits.html` and `assets/SOURCES-assets.json`: image sources and credits.

The hero uses the original supplied portrait. An SVG viewport crops out the chair and feet, and CSS applies a slight brightness increase. The face, clothes, and pose are not regenerated or reshaped.

## Preview locally

From this directory, run:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173/ in your browser.

Organization logos, photographs, and trademarks retain their respective owners’ rights. See the image credits for provenance.
