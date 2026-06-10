(function () {
  function init() {
    APF.initCore();
    const q = new URLSearchParams(location.search).get('q') || '';
    const title = document.getElementById('search-query');
    const grid = document.getElementById('search-results');
    const count = document.getElementById('search-count');
    if (title) title.textContent = q ? `نتایج جستجو برای «${q}»` : 'جستجو';
    const results = q ? APF.products.filter(p => p.name.includes(q) || p.category.includes(q) || p.desc.includes(q)) : APF.products;
    if (count) count.textContent = results.length.toLocaleString('fa-IR') + ' نتیجه';
    APF.renderProductGrid(grid, results);
    document.querySelector('.search-bar input')?.setAttribute('value', q);
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
