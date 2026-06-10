(function () {
  function init() {
    APF.initCore();
    APF_DATA.categories.forEach(cat => {
      const grid = document.getElementById('category-grid');
      if (!grid) return;
    });
    const grid = document.getElementById('category-grid');
    if (grid) {
      grid.innerHTML = APF_DATA.categories.map(cat => `
        <a href="/products/category/${cat.slug}/" class="category-card reveal">
          <div class="category-icon">${cat.icon}</div>
          <div class="category-name">${cat.name}</div>
          <div class="category-count">+${cat.count.toLocaleString('fa-IR')} محصول</div>
        </a>`).join('');
      APF.initScrollReveal();
    }
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
