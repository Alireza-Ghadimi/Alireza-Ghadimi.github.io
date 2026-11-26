/* Project chapters keep native hash navigation and readable posters without JS. */
(() => {
  const work = document.getElementById('work');
  if (!work) return;

  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const visibleArt = new Set();
  const selectedStudy = new Map();
  const arts = work.querySelectorAll('.sw-image img');
  const animations = new Set();

  function motionEnabled() {
    return !preference.matches && !document.hidden && !document.body.classList.contains('still');
  }

  function updateArt(image) {
    const visible = visibleArt.has(image) && !image.closest('.sw-study').hidden;
    const play = motionEnabled() && visible && !image.hasAttribute('data-unavailable');
    const next = play ? image.dataset.gif : image.dataset.poster;
    if (image.getAttribute('src') !== next) image.setAttribute('src', next);
  }

  function syncMotion() {
    arts.forEach(updateArt);
    if (!motionEnabled()) animations.forEach(animation => animation.cancel());
  }

  const inView = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting) visibleArt.add(entry.target);
      else visibleArt.delete(entry.target);
      updateArt(entry.target);
    }
  });
  for (const image of arts) {
    inView.observe(image);
    image.addEventListener('error', () => {
      if (image.getAttribute('src') === image.dataset.gif) {
        image.dataset.unavailable = '';
        updateArt(image);
      }
    });
  }
  new MutationObserver(syncMotion).observe(document.body, {attributes: true, attributeFilter: ['class']});
  preference.addEventListener('change', syncMotion);
  document.addEventListener('visibilitychange', syncMotion);

  for (const chapter of work.querySelectorAll('.sw-chapter')) {
    const list = chapter.querySelector('.sw-chooser');
    const tabs = [...list.querySelectorAll('[data-choose]')];
    const panels = [...chapter.querySelectorAll('[data-study]')];
    let active;

    function select(id, animate) {
      if (active === id) return;
      active = id;
      for (const tab of tabs) {
        const selected = tab.dataset.choose === id;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
      }
      for (const panel of panels) {
        panel.hidden = panel.dataset.study !== id;
        updateArt(panel.querySelector('img'));
        if (!panel.hidden && animate && motionEnabled() && panel.animate) {
          const entrance = panel.animate([{opacity: .35, transform: 'translateY(8px)'}, {opacity: 1, transform: 'none'}],
            {duration: 260, easing: 'ease-out'});
          animations.add(entrance);
          entrance.finished.catch(() => {}).finally(() => animations.delete(entrance));
        }
      }
    }

    list.setAttribute('role', 'tablist');
    chapter.classList.add('sw-enhanced');
    tabs.forEach((tab, i) => {
      const panel = panels[i];
      tab.parentElement.setAttribute('role', 'presentation');
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panel.id);
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tab.id);
      panel.tabIndex = 0;
      tab.addEventListener('click', event => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        select(tab.dataset.choose, true);
      });
      tab.addEventListener('keydown', event => {
        let next;
        switch (event.key) {
          case 'ArrowDown': case 'ArrowRight': next = tabs[(i + 1) % tabs.length]; break;
          case 'ArrowUp': case 'ArrowLeft': next = tabs[(i + tabs.length - 1) % tabs.length]; break;
          case 'Home': next = tabs[0]; break;
          case 'End': next = tabs[tabs.length - 1]; break;
          case ' ': next = tab; break;
          default: return;
        }
        event.preventDefault();
        select(next.dataset.choose, true);
        next.focus({preventScroll: true});
      });
    });
    select(tabs[0].dataset.choose, false);
    selectedStudy.set(chapter, select);
  }

  function restoreStudyLink() {
    const target = document.getElementById(location.hash.slice(1));
    if (!target?.matches('#work .sw-study')) return;
    selectedStudy.get(target.closest('.sw-chapter'))(target.dataset.study, false);
    target.scrollIntoView({block: 'start', behavior: 'instant'});
  }
  addEventListener('hashchange', restoreStudyLink);
  restoreStudyLink();
})();
