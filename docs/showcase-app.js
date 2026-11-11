/* Showcase state: one appearance, one preview, native document navigation. */
(() => {
  const root = document.documentElement;
  const system = matchMedia('(prefers-color-scheme: dark)');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let choice = 'system', view = 'editor', frame = 0;
  try { choice = localStorage.getItem('ma-appearance') || 'system'; } catch {}
  if (!['system', 'dark', 'light'].includes(choice)) choice = 'system';
  const flavor = () => (choice === 'dark' || (choice === 'system' && system.matches)) ? IDS[0] : IDS[1];
  const notes = document.getElementById('notes-dialog');
  const paletteDialog = document.getElementById('palette-dialog');
  const table = document.getElementById('palette-table');
  const search = document.getElementById('palette-search');
  let paletteFlavor = flavor();

  // Diagram geometry stays scientific; only its display inks follow the flavour.
  const inks = {};
  for (const key of Object.keys(K)) if (B[key]) inks[K[key].hex.toLowerCase()] = B[key].hex;
  for (const group of ['normal', 'bright']) for (const key of Object.keys(F[IDS[0]].ansi[group])) {
    inks[F[IDS[0]].ansi[group][key].hex.toLowerCase()] = F[IDS[1]].ansi[group][key].hex;
  }
  function recolor(id) {
    if (flavor() === IDS[0]) return;
    const node = document.getElementById(id);
    node.innerHTML = node.innerHTML.replace(/#[0-9a-f]{6}/gi, hex => inks[hex.toLowerCase()] || hex);
  }
  function renderPreview() {
    const id = flavor();
    const pane = view === 'editor' ? editor(id, 1, 20) : view === 'diff' ? diffView(id) : terminal(id);
    document.getElementById('preview').replaceChildren(pane);
    document.getElementById('flavour-label').textContent = id === IDS[0]
      ? '黒紫 / Kuromurasaki — black-purple, with a green seed'
      : '白緑 / Byakuroku — white-green, with a purple seed';
  }
  function turnCube() {
    const section = document.getElementById('model').getBoundingClientRect();
    const t = motion.matches ? 1 : Math.max(0, Math.min(1, (innerHeight * .85 - section.top) / (section.height * .65)));
    drawCube(t); recolor('fig-cube');
  }
  function diagrams() {
    drawEye(); drawCIE(); drawMix(flavor() === IDS[0] ? K : B); turnCube();
    recolor('fig-eye'); recolor('fig-cie');
    // Mixing ramps remain computed in linear light; their labels use page tokens.
  }
  function applyAppearance() {
    if (choice === 'system') delete root.dataset.theme;
    else root.dataset.theme = choice;
    root.style.colorScheme = flavor() === IDS[0] ? 'dark' : 'light';
    document.querySelectorAll('[data-theme-choice]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.themeChoice === choice));
    });
    renderPreview(); diagrams();
  }
  document.querySelectorAll('[data-theme-choice]').forEach(button => button.addEventListener('click', () => {
    choice = button.dataset.themeChoice;
    try { localStorage.setItem('ma-appearance', choice); } catch {}
    applyAppearance();
  }));
  system.addEventListener('change', () => { if (choice === 'system') applyAppearance(); });
  motion.addEventListener('change', turnCube);
  const tabs = [...document.querySelectorAll('[data-view]')];
  function selectTab(button, focus = false) {
    view = button.dataset.view;
    tabs.forEach(tab => { tab.setAttribute('aria-selected', String(tab === button)); tab.tabIndex = tab === button ? 0 : -1; });
    document.getElementById('preview').setAttribute('aria-labelledby', button.id);
    renderPreview();
    if (focus) button.focus();
  }
  tabs.forEach((button, index) => {
    button.addEventListener('click', () => selectTab(button));
    button.addEventListener('keydown', e => {
      let next;
      if (e.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (e.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (e.key === 'Home') next = 0;
      if (e.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { e.preventDefault(); selectTab(tabs[next], true); }
    });
  });
  function filter() {
    const q = search.value.trim().toLowerCase();
    table.querySelectorAll('tbody tr:not(.grp)').forEach(row => row.hidden = !row.textContent.toLowerCase().includes(q));
    table.querySelectorAll('.grp').forEach(row => {
      let next = row.nextElementSibling, any = false;
      while (next && !next.classList.contains('grp')) { any ||= !next.hidden; next = next.nextElementSibling; }
      row.hidden = !any;
    });
  }
  function renderPalette(id) {
    paletteFlavor = id; table.replaceChildren(palette(id)); filter();
    document.querySelectorAll('[data-flavour]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.flavour === id)));
  }
  document.getElementById('open-palette').addEventListener('click', () => { renderPalette(flavor()); paletteDialog.showModal(); });
  document.getElementById('close-palette').addEventListener('click', () => paletteDialog.close());
  document.getElementById('open-notes').addEventListener('click', () => notes.showModal());
  document.getElementById('close-notes').addEventListener('click', () => notes.close());
  document.querySelectorAll('[data-flavour]').forEach(b => b.addEventListener('click', () => renderPalette(b.dataset.flavour)));
  search.addEventListener('input', filter);
  table.addEventListener('click', async e => {
    const button = e.target.closest('.copy'); if (!button) return;
    try { await navigator.clipboard.writeText(button.dataset.hex); document.getElementById('copy-live').textContent = `Copied ${button.dataset.hex}`; }
    catch { document.getElementById('copy-live').textContent = `Copy this value: ${button.dataset.hex}`; }
  });
  function onScroll() {
    if (frame) return;
    frame = requestAnimationFrame(() => { frame = 0; const r = document.getElementById('model').getBoundingClientRect(); if (r.bottom > 0 && r.top < innerHeight) turnCube(); });
  }
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);
  const observer = new IntersectionObserver(entries => entries.forEach(e => e.target.classList.toggle('visible', e.isIntersecting)), { threshold: .1 });
  document.querySelectorAll('.exchange').forEach(node => observer.observe(node));
  applyAppearance(); renderPalette(paletteFlavor);
})();
