(function () {
  function init() {
    APF.initCore();
    const grid = document.getElementById('favorites-grid');
    const empty = document.getElementById('favorites-empty');
    const favs = APF.products.filter(p => APF.state.favorites.has(p.id));
    if (!favs.length) { grid?.classList.add('hidden'); empty?.classList.remove('hidden'); return; }
    empty?.classList.add('hidden');
    APF.renderProductGrid(grid, favs);
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
