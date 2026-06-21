(function () {
  function init() {
    APF.initCore();
    const grid = document.getElementById('product-grid');
    const countEl = document.getElementById('catalog-count');
    
    let filtered = [...(window.APF_DATA?.products || [])];

    function applyFilters() {
      const cats = [...document.querySelectorAll('.filter-cat:checked')].map(c => c.value);
      const sort = document.getElementById('sort-select')?.value || 'popular';
      
      filtered = (window.APF_DATA?.products || []).filter(p => !cats.length || cats.includes(p.categorySlug));
      
      if (sort === 'price-asc') filtered.sort((a, b) => a.price - b.price);
      else if (sort === 'price-desc') filtered.sort((a, b) => b.price - a.price);
      else if (sort === 'rating') filtered.sort((a, b) => b.rating - a.rating);
      
      APF.renderProductGrid(grid, filtered);
      if (countEl) countEl.textContent = filtered.length.toLocaleString('fa-IR') + ' محصول';
    }

    document.querySelectorAll('.filter-cat, .filter-stock').forEach(el => el.addEventListener('change', applyFilters));
    document.getElementById('sort-select')?.addEventListener('change', applyFilters);
    applyFilters();


  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();