(function () {
  function init() {
    APF.initCore();
    const params = new URLSearchParams(location.search);
    const slug = params.get('slug');
    const cat = APF_DATA.categories.find(c => c.slug === slug);
    const title = document.getElementById('page-title-heading');
    const subtitle = document.getElementById('page-subtitle');
    const breadcrumbTitle = document.getElementById('breadcrumb-cat');
    if (cat && title) {
      title.textContent = cat.name;
      subtitle.textContent = `${cat.count.toLocaleString('fa-IR')} محصول در این دسته`;
      if (breadcrumbTitle) breadcrumbTitle.textContent = cat.name;
    }
    const grid = document.getElementById('product-grid');
    const list = slug ? APF.products.filter(p => p.categorySlug === slug) : APF.products;
    APF.renderProductGrid(grid, list);
    document.getElementById('catalog-count').textContent = list.length.toLocaleString('fa-IR') + ' محصول';
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
