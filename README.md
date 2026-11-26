# Alireza Ghadimi

[Personal portfolio](https://alireza-ghadimi.github.io/) featuring research on agentic AI, generative models and efficient language models. The animated homepage includes 15 project case studies, experience, publications, education, a downloadable résumé and LeafLab.

## Build and preview

GitHub Pages serves the static files from the root of the main branch. To rebuild the site and verify the local assets, run:

```sh
python3 scripts/build-site.py
python3 scripts/check-site.py
python3 -m http.server 4173 --bind 127.0.0.1
```

Visit http://127.0.0.1:4173/. Bookmarks to the older `/animated/` address redirect to the homepage.

## Content and presentation

- `content/portfolio.json` contains project descriptions, categories, evidence and links.
- `scripts/build-site.py` generates the homepage and image credits.
- `app.js` handles project tabs, case studies, navigation and copying the contact email.
- `motion.js` and `motion.css` control scroll effects and project animations. The page follows the visitor’s device setting for reduced motion.
- `assets/project-motion/` contains illustrative GIFs and static posters. Rebuild them with `python3 scripts/build-project-motion.py` and Pillow.
- `credits.html` lists the sources of images, organization logos and fonts.
