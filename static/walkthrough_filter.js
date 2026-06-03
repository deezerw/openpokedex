// "Only show uncaught" toggle for the walkthrough guide + afterward pages.
// State is remembered in localStorage and shared across both pages.
(function () {
  var KEY = 'wt_only_uncaught';
  var btn = document.getElementById('wt-uncaught-toggle');
  if (!btn) return;

  function apply(on) {
    // Hide caught Pokémon (leave e-Card-only cards to their own toggle).
    document.querySelectorAll('.wt-mon-caught:not(.wt-ecard-only)').forEach(function (el) {
      el.style.display = on ? 'none' : '';
    });
    // Collapse sections that have no uncaught Pokémon left to show.
    document.querySelectorAll('.wt-section').forEach(function (sec) {
      sec.style.display = (on && !sec.querySelector('.wt-mon:not(.wt-mon-caught)')) ? 'none' : '';
    });
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    btn.classList.toggle('is-active', on);
    btn.textContent = on ? '✓ Only uncaught — click to show all' : 'Show only uncaught';
  }

  apply(localStorage.getItem(KEY) === '1');

  btn.addEventListener('click', function () {
    var on = localStorage.getItem(KEY) !== '1';
    localStorage.setItem(KEY, on ? '1' : '0');
    apply(on);
  });
})();
