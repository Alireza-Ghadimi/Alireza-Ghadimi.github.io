/* Progressive enhancement, isolated from the original portfolio's behavior. */
(() => {
  'use strict';
  const body = document.body;
  if (!body.classList.contains('motion-edition')) return;
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const hero = document.querySelector('.hero');
  const timeline = document.querySelector('.experience-list');
  const progress = document.querySelector('.reading-progress > span');
  const motionCards = [...document.querySelectorAll('.work-card')];
  const diagrams = [...document.querySelectorAll('.project-motion')];
  const visibleDiagrams = new Set();
  const activeAnimations = new Set();
  const revealTargets = [];
  let enabled = false;
  let frame = 0;

  function animate(element, keyframes, options) {
    if (!enabled || !element?.animate) return;
    const animation = element.animate(keyframes, options);
    activeAnimations.add(animation);
    animation.finished.catch(() => {}).finally(() => activeAnimations.delete(animation));
    return animation;
  }

  // Wrap words without replacing headings with images or changing their text.
  document.querySelectorAll('main h2').forEach(heading => {
    let index = 0;
    const walker = document.createTreeWalker(heading, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(node => {
      const fragment = document.createDocumentFragment();
      node.textContent.split(/(\s+)/).forEach(part => {
        if (!part.trim()) { fragment.append(document.createTextNode(part)); return; }
        const mask = document.createElement('span');
        const word = document.createElement('span');
        mask.className = 'word-mask'; word.className = 'word-reveal';
        word.style.setProperty('--word-index', String(index++));
        word.textContent = part; mask.append(word); fragment.append(mask);
      });
      node.replaceWith(fragment);
    });
    heading.classList.add('motion-heading');
    revealTargets.push(heading);
  });

  const revealSelectors = '.section-heading .overline, .section-description, .perspective-copy, .logo-strip img, .impact-strip > div, .work-card, .experience-row, .publication, .education-card, .award-note, .contact-section h2 + p, .email-row, .contact-links, .leaflab-inner';
  document.querySelectorAll(revealSelectors).forEach(element => {
    element.dataset.reveal = '';
    const index = [...element.parentElement.children].indexOf(element);
    const staggered = element.matches('.work-card, .education-card, .logo-strip img, .impact-strip > div');
    element.style.setProperty('--reveal-delay', `${staggered ? (index % 3) * 90 : 0}ms`);
    revealTargets.push(element);
  });

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, {threshold: 0.06, rootMargin: '0px 0px -35px 0px'});
  revealTargets.forEach(element => revealObserver.observe(element));
  document.addEventListener('focusin', event => {
    event.target.closest('[data-reveal]')?.classList.add('is-visible');
  });

  const ambientObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => entry.target.classList.toggle('in-view', entry.isIntersecting));
  });
  [hero, document.querySelector('.contact-section'), document.querySelector('.leaflab-section')].forEach(element => ambientObserver.observe(element));

  function syncDiagram(img) {
    const shouldPlay = enabled && !document.hidden && !img.closest('.work-card').hidden && visibleDiagrams.has(img);
    const next = shouldPlay ? img.dataset.gif : img.dataset.poster;
    if (img.getAttribute('src') !== next) img.setAttribute('src', next);
  }
  const diagramObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) visibleDiagrams.add(entry.target);
      else visibleDiagrams.delete(entry.target);
      syncDiagram(entry.target);
    });
  }, {threshold: 0.03});
  diagrams.forEach(img => {
    diagramObserver.observe(img);
    img.addEventListener('error', () => {
      // Keep the readable poster when an animation cannot be loaded.
      if (img.getAttribute('src') !== img.dataset.poster) img.src = img.dataset.poster;
    });
  });

  function updateScroll() {
    frame = 0;
    const height = document.documentElement.scrollHeight - innerHeight;
    const fraction = height > 0 ? Math.min(1, Math.max(0, scrollY / height)) : 0;
    progress.style.transform = `scaleX(${fraction})`;
    if (!enabled) return;
    const bounds = hero.getBoundingClientRect();
    const heroFraction = Math.min(1, Math.max(0, -bounds.top / bounds.height));
    body.style.setProperty('--hero-scroll', heroFraction.toFixed(3));
    const career = timeline.getBoundingClientRect();
    const careerFraction = Math.min(1, Math.max(0, (innerHeight * .68 - career.top) / career.height));
    timeline.style.setProperty('--timeline-progress', careerFraction.toFixed(3));
  }
  function requestScrollUpdate() {
    if (!frame) frame = requestAnimationFrame(updateScroll);
  }
  addEventListener('scroll', requestScrollUpdate, {passive: true});
  addEventListener('resize', requestScrollUpdate, {passive: true});

  function updateMotion() {
    enabled = !preference.matches;
    body.classList.toggle('motion-enabled', enabled);
    body.classList.toggle('motion-paused', !enabled);
    if (!enabled) {
      activeAnimations.forEach(animation => animation.cancel());
      activeAnimations.clear();
      revealTargets.forEach(element => element.classList.add('is-visible'));
      motionCards.forEach(card => {
        card.style.setProperty('--tilt-x', '0deg'); card.style.setProperty('--tilt-y', '0deg');
      });
    }
    diagrams.forEach(syncDiagram);
    requestScrollUpdate();
  }
  preference.addEventListener('change', updateMotion);
  document.addEventListener('visibilitychange', () => {
    diagrams.forEach(syncDiagram);
    body.classList.toggle('page-hidden', document.hidden);
  });

  // Animate newly selected project cards without changing the shared tab logic.
  const filterObserver = new MutationObserver(records => {
    const revealed = [...new Set(records.map(record => record.target))].filter(card => !card.hidden);
    records.forEach(record => syncDiagram(record.target.querySelector('.project-motion')));
    revealed.forEach((card, index) => {
      card.classList.add('is-visible');
      animate(card, [{opacity: 0, transform: 'translateY(25px) scale(.98)'}, {opacity: 1, transform: 'translateY(0) scale(1)'}], {duration: 550, delay: Math.min(index, 4) * 65, easing: 'cubic-bezier(.2,.75,.25,1)'});
    });
    requestScrollUpdate();
  });
  motionCards.forEach(card => {
    filterObserver.observe(card, {attributes: true, attributeFilter: ['hidden']});
    card.addEventListener('pointermove', event => {
      if (!enabled || !finePointer.matches || event.pointerType === 'touch') return;
      const bounds = card.getBoundingClientRect();
      card.style.setProperty('--tilt-x', `${((.5 - (event.clientY - bounds.top) / bounds.height) * 3).toFixed(2)}deg`);
      card.style.setProperty('--tilt-y', `${(((event.clientX - bounds.left) / bounds.width - .5) * 3).toFixed(2)}deg`);
    });
    card.addEventListener('pointerleave', () => {
      card.style.setProperty('--tilt-x', '0deg'); card.style.setProperty('--tilt-y', '0deg');
    });
  });

  const dialogObserver = new MutationObserver(records => {
    records.forEach(({target}) => {
      if (target.open) animate(target, [{opacity: 0, transform: 'translateY(25px) scale(.96)'}, {opacity: 1, transform: 'translateY(0) scale(1)'}], {duration: 380, easing: 'cubic-bezier(.2,.75,.25,1)'});
    });
  });
  document.querySelectorAll('.case-dialog').forEach(dialog => dialogObserver.observe(dialog, {attributes: true, attributeFilter: ['open']}));

  body.classList.add('motion-ready');
  updateMotion();
  // The hero is a one-time entrance; no looping text that disrupts reading.
  if (enabled) {
    document.querySelectorAll('.name-line > span').forEach((line, index) => animate(line, [{transform: 'translateY(112%) rotate(3deg)'}, {transform: 'translateY(0) rotate(0)'}], {duration: 1150, delay: 80 + index * 150, easing: 'cubic-bezier(.18,.8,.2,1)'}));
    document.querySelectorAll('.hero-overline,.hero-thesis,.hero-bio,.hero-actions,.hero-location,.portrait-note').forEach((element, index) => animate(element, [{opacity: 0, transform: 'translateY(20px)'}, {opacity: 1, transform: 'translateY(0)'}], {duration: 850, delay: 100 + index * 90, easing: 'cubic-bezier(.2,.75,.25,1)'}));
    animate(document.querySelector('.portrait-frame'), [{opacity: 0, clipPath: 'inset(15% 8% 40% 8% round 14px)', transform: 'translateY(35px)'}, {opacity: 1, clipPath: 'inset(0 0 0 0 round 8px)', transform: 'translateY(0)'}], {duration: 1300, delay: 180, easing: 'cubic-bezier(.18,.8,.2,1)'});
  }
})();
