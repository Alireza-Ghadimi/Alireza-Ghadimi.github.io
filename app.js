'use strict';

const categoryData = document.querySelector('#category-data');
const categories = categoryData ? JSON.parse(categoryData.textContent) : [];
const tabs = [...document.querySelectorAll('[data-filter]')];
const cards = [...document.querySelectorAll('.work-card')];

function selectCategory(id, moveFocus = false) {
  const category = categories.find(item => item.id === id);
  if (!category) return;
  tabs.forEach(tab => {
    const selected = tab.dataset.filter === id;
    tab.setAttribute('aria-selected', String(selected));
    tab.tabIndex = selected ? 0 : -1;
    if (selected && moveFocus) {
      tab.focus({preventScroll: true});
      tab.scrollIntoView({block: 'nearest', inline: 'nearest', behavior: 'instant'});
    }
  });
  let count = 0;
  cards.forEach(card => {
    const visible = id === 'selected' ? card.dataset.featured === 'true' : card.dataset.category.split(' ').includes(id);
    card.hidden = !visible;
    if (visible) count += 1;
  });
  document.querySelector('#domain-title').textContent = category.title;
  document.querySelector('#domain-description').textContent = category.description;
  document.querySelector('#work-count').textContent = `${count} ${id === 'selected' ? 'selected ' : ''}project${count === 1 ? '' : 's'}`;
  document.querySelector('#work-panel').setAttribute('aria-labelledby', `tab-${id}`);
}

tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectCategory(tab.dataset.filter));
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    else return;
    event.preventDefault();
    selectCategory(tabs[next].dataset.filter, true);
  });
});

const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
function closeMenu() {
  menu?.setAttribute('aria-expanded', 'false');
  nav?.classList.remove('is-open');
}
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('is-open', open);
});
nav?.querySelectorAll('a').forEach(anchor => anchor.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
    closeMenu(); menu.focus();
  }
});
window.matchMedia('(min-width: 641px)').addEventListener('change', event => {
  if (event.matches) closeMenu();
});

document.querySelectorAll('[data-case]').forEach(trigger => {
  trigger.addEventListener('click', () => {
    const dialog = document.getElementById(`case-${trigger.dataset.case}`);
    if (!dialog) return;
    closeMenu(); dialog.showModal(); dialog.scrollTop = 0;
    document.body.classList.add('dialog-open');
  });
});
document.querySelectorAll('.case-dialog').forEach(dialog => {
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => document.body.classList.remove('dialog-open'));
});

const copyEmail = document.querySelector('.copy-email');
let copyTimeout;
copyEmail?.addEventListener('click', async () => {
  const status = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText('arghadimi.bme@gmail.com');
    copyEmail.textContent = 'Copied';
    status.textContent = 'Email address copied to clipboard.';
  } catch {
    const range = document.createRange();
    range.selectNodeContents(document.querySelector('.email-row a'));
    const selection = window.getSelection();
    selection.removeAllRanges(); selection.addRange(range);
    copyEmail.textContent = 'Email selected';
    status.textContent = 'Email selected. Use your device’s copy command.';
  }
  clearTimeout(copyTimeout);
  copyTimeout = setTimeout(() => {copyEmail.textContent = 'Copy email';}, 2800);
});

const year = document.querySelector('#year');
if (year) year.textContent = new Date().getFullYear();
