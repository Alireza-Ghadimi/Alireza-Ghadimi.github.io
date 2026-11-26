// Keep the illustrated index aligned with the section currently being read.
(() => {
  const dock = document.querySelector('.dock');
  const tiles = [...dock.querySelectorAll('a')];
  const sections = tiles.map(tile => ({tile, section: document.getElementById(tile.hash.slice(1))}))
    .filter(item => item.section)
    .sort((a, b) => a.section.compareDocumentPosition(b.section) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1);
  const toggle = document.querySelector('.motion-switch');
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = false;
  try { paused = localStorage.getItem('studio-paused') === 'true'; } catch {}
  function updateMotion() {
    document.body.classList.toggle('still', paused || preference.matches);
    toggle.textContent = preference.matches ? 'Reduced motion' : paused ? 'Play motion' : 'Pause motion';
    toggle.setAttribute('aria-pressed', String(paused || preference.matches));
    toggle.disabled = preference.matches;
  }
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    paused = !paused;
    try { localStorage.setItem('studio-paused', String(paused)); } catch {}
    updateMotion();
  });
  preference.addEventListener('change', updateMotion);
  updateMotion();

  let previous;
  let queued = false;
  function highlight() {
    queued = false;
    const guide = innerHeight * .34;
    let current = sections[0];
    for (const item of sections) {
      if (item.section.getBoundingClientRect().top <= guide) current = item;
    }
    if (scrollY + innerHeight >= document.documentElement.scrollHeight - 3) current = sections.at(-1);
    if (current === previous) return;
    previous?.tile.removeAttribute('aria-current');
    current.tile.setAttribute('aria-current', 'location');
    previous = current;
    const bounds = current.tile.getBoundingClientRect();
    if (bounds.left < 0 || bounds.right > dock.clientWidth) {
      dock.scrollTo({left: dock.scrollLeft + bounds.left - (dock.clientWidth - bounds.width) / 2,
        behavior: document.body.classList.contains('still') ? 'instant' : 'smooth'});
    }
  }
  function schedule() {
    if (!queued) { queued = true; requestAnimationFrame(highlight); }
  }
  window.addEventListener('scroll', schedule, {passive: true});
  window.addEventListener('resize', schedule);
  window.addEventListener('load', schedule);
  highlight();
})();
