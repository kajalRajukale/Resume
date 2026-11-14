// Typewriter for hero roles
const typed = document.querySelector('[data-typed]');
if (typed) {
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

// Reveal on scroll
const io = new IntersectionObserver(entries => entries.forEach(e => {
  if (!e.isIntersecting) return;
  e.target.classList.add('in'); io.unobserve(e.target);
  e.target.addEventListener('transitionend', () => { e.target.style.transitionDelay = ''; }, { once: true });
}), { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((el, n) => {
  el.style.transitionDelay = `${(n % 4) * 70}ms`;
  io.observe(el);
});

// Project filter
document.querySelectorAll('[data-filter]').forEach(btn => btn.addEventListener('click', () => {
  const f = btn.dataset.filter;
  document.querySelectorAll('[data-filter]').forEach(b => b.setAttribute('aria-pressed', b === btn));
  document.querySelectorAll('.card[data-tags]').forEach(c => {
    c.hidden = f !== 'all' && !c.dataset.tags.split(' ').includes(f);
  });
}));

// Animated counters
document.querySelectorAll('[data-count]').forEach(el => {
  const end = +el.dataset.count, t0 = performance.now();
  const step = t => {
    const k = Math.min((t - t0) / 1200, 1);
    el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3)));
    if (k < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
});
