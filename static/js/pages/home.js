(function () {
  function init() {
    APF.initCore();
    APF.initCounters();
    APF.initHeroParallax();
    APF.initFAQ();
    const grid = document.getElementById('product-grid');
    const render = (filter) => {
      const list = filter === 'all' ? APF.products : APF.products.filter(p => p.tab === filter);
      APF.renderProductGrid(grid, list.slice(0, 8));
    };
    render('all');
    document.querySelectorAll('.tab-btn').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        render(tab.dataset.tab);
      });
    });
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
