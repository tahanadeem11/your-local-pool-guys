// Your Local Pool Guys — menu toggle + before/after slider
(function () {
  // Mobile menu
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  // Before / after slider
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-ba]').forEach(function (el) {
    var range = el.querySelector('input[type="range"]');
    if (!range) return;
    var touched = false;
    function set(v) {
      el.style.setProperty('--pos', v + '%');
      range.setAttribute('aria-valuetext', Math.round(v) + '% before, ' + Math.round(100 - v) + '% after');
    }
    range.addEventListener('input', function () { touched = true; set(range.value); });
    set(range.value);

    // One reveal when the slider first scrolls into view: green sweeps away to show the clean pool.
    if (reduce || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.disconnect();
        var from = 92, to = Number(range.value), start = null, dur = 1400;
        function step(t) {
          if (touched) return;
          if (start === null) start = t;
          var p = Math.min(1, (t - start) / dur);
          var e = 1 - Math.pow(1 - p, 3);
          var v = from + (to - from) * e;
          set(v);
          if (p < 1) requestAnimationFrame(step); else set(to);
        }
        set(from);
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    io.observe(el);
  });
})();
