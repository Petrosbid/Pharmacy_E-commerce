(function () {
  function init() {
    APF.initCore();
    const ordersEl = document.getElementById('orders-list');
    if (ordersEl) {
      ordersEl.innerHTML = APF_DATA.orders.map(o => `
        <div class="order-card reveal">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
            <strong>${o.id}</strong>
            <span class="order-status order-status-${o.status}">${o.statusLabel}</span>
          </div>
          <div class="text-sm" style="color:var(--color-text-muted)">${o.date} · ${o.items.toLocaleString('fa-IR')} قلم · ${APF.formatPrice(o.total)}</div>
          <a href="/orders/history/" class="btn btn-ghost text-sm mt-2">جزئیات سفارش</a>
        </div>`).join('');
      APF.initScrollReveal();
    }
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
