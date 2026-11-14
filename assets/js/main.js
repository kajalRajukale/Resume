const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const root = document.documentElement;
const calm = matchMedia('(prefers-reduced-motion: reduce)').matches || root.dataset.motion === 'off';

// Theme toggle (initial theme is set inline in <head> to avoid a flash)
$('.theme-btn')?.addEventListener('click', () => {
  const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
  root.dataset.theme = next;
  try { localStorage.setItem('theme', next); } catch (e) {}
});

// Mobile menu
const menuBtn = $('.menu-btn'), nav = $('#site-nav');
menuBtn?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menuBtn.setAttribute('aria-expanded', open);
});

// Back to top
const toTop = $('.to-top');
addEventListener('scroll', () => { toTop.hidden = scrollY < 600; }, { passive: true });
toTop.addEventListener('click', () => scrollTo({ top: 0, behavior: calm ? 'auto' : 'smooth' }));

// Typewriter
const typed = $('[data-typed]');
if (typed && !calm) {
  const words = JSON.parse(typed.dataset.typed);
  let w = 0, i = 0, del = false;
  const tick = () => {
    const word = words[w];
    i += del ? -1 : 1;
    typed.textContent = word.slice(0, i);
    if (!del && i === word.length) { del = true; return setTimeout(tick, 1600); }
    if (del && i === 0) { del = false; w = (w + 1) % words.length; }
    setTimeout(tick, del ? 40 : 85);
  };
  tick();
}

// Reveal on scroll (also starts skill bars and counters)
const io = new IntersectionObserver(entries => entries.forEach(e => {
  if (!e.isIntersecting) return;
  e.target.classList.add('in');
  io.unobserve(e.target);
  e.target.addEventListener('transitionend', () => { e.target.style.transitionDelay = ''; }, { once: true });
  $$('[data-count]', e.target).forEach(count);
}), { threshold: 0.12 });
$$('.reveal').forEach((el, n) => {
  if (!calm) el.style.transitionDelay = `${(n % 4) * 70}ms`;
  io.observe(el);
});

function count(el) {
  const end = +el.dataset.count, t0 = performance.now();
  if (calm || !end) return;
  const step = t => {
    const k = Math.min((t - t0) / 1200, 1);
    el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3)));
    if (k < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// Project filters: topic buttons + language select + search
const cards = $$('.card[data-tags]');
const state = { tag: 'all', lang: '', q: '' };
const apply = () => {
  let shown = 0;
  cards.forEach(c => {
    const ok = (state.tag === 'all' || c.dataset.tags.split(' ').includes(state.tag))
      && (!state.lang || c.dataset.langs.split('|').includes(state.lang))
      && (!state.q || c.dataset.text.includes(state.q));
    c.hidden = !ok;
    if (ok) { shown++; c.classList.add('in'); }
  });
  const empty = $('.empty');
  if (empty) empty.hidden = shown > 0;
};
$$('[data-filter]').forEach(btn => btn.addEventListener('click', () => {
  state.tag = btn.dataset.filter;
  $$('[data-filter]').forEach(b => b.setAttribute('aria-pressed', b === btn));
  apply();
}));
$('#lang-filter')?.addEventListener('change', e => { state.lang = e.target.value; apply(); });
$('#search')?.addEventListener('input', e => { state.q = e.target.value.trim().toLowerCase(); apply(); });

// Card tilt + hero parallax (pointer devices only)
if (!calm && matchMedia('(hover: hover)').matches) {
  $$('.tilt').forEach(card => {
    card.addEventListener('pointermove', e => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--ry', `${((e.clientX - r.left) / r.width - .5) * 8}deg`);
      card.style.setProperty('--rx', `${((e.clientY - r.top) / r.height - .5) * -8}deg`);
    });
    card.addEventListener('pointerleave', () => { card.style.removeProperty('--rx'); card.style.removeProperty('--ry'); });
  });
  const layers = $$('.parallax');
  if (layers.length) addEventListener('pointermove', e => {
    const x = e.clientX - innerWidth / 2, y = e.clientY - innerHeight / 2;
    layers.forEach(l => { l.style.transform = `translate(${x * l.dataset.depth}px, ${y * l.dataset.depth}px)`; });
  }, { passive: true });
}

// Lazy-play terminal videos only while visible
const vio = new IntersectionObserver(entries => entries.forEach(e => {
  const v = e.target;
  if (e.isIntersecting) { if (v.preload === 'none') { v.preload = 'auto'; v.load(); } if (!calm) v.play().catch(() => {}); }
  else v.pause();
}), { threshold: 0.25 });
$$('.term-video video').forEach(v => { v.removeAttribute('autoplay'); vio.observe(v); });

// 404: show the requested path
const path = $('.err .path');
if (path) path.textContent = location.pathname;
