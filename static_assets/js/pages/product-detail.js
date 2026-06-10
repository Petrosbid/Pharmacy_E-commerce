(function () {
  function init() {
    APF.initCore();
    // Get product from the first item in APF_DATA.products which is populated by the Django template
    const product = APF_DATA.products[0];
    if (!product) return;

    // The template already renders most of this, but we keep the logic for any dynamic updates
    let qty = 1;
    const qtyEl = document.getElementById('qty-value');
    if (qtyEl) {
        document.getElementById('qty-minus')?.addEventListener('click', () => { if (qty > 1) { qty--; qtyEl.textContent = qty.toLocaleString('fa-IR'); } });
        document.getElementById('qty-plus')?.addEventListener('click', () => { qty++; qtyEl.textContent = qty.toLocaleString('fa-IR'); });
    }
    
    document.getElementById('add-to-cart')?.addEventListener('click', () => { for (let i = 0; i < qty; i++) APF.addToCart(product.id); });
    document.getElementById('add-favorite')?.addEventListener('click', function () { APF.toggleFavorite(product.id, this); this.classList.toggle('active'); });

    document.querySelectorAll('.info-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.info-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.info-panel').forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.panel)?.classList.add('active');
      });
    });

    const related = APF_DATA.products.slice(1, 5);
    APF.renderProductGrid(document.getElementById('related-products'), related);
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
