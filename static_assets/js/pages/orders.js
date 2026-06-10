(function () {
  function init() {
    APF.initCore();
    const form = document.getElementById('track-form');
    form?.addEventListener('submit', e => {
      e.preventDefault();
      const id = document.getElementById('order-id').value.trim();
      const result = document.getElementById('track-result');
      const order = APF_DATA.orders.find(o => o.id === id) || APF_DATA.orders[0];
      if (result) {
        result.classList.remove('hidden');
        result.innerHTML = `<div class="order-card"><strong>${order.id}</strong><span class="order-status order-status-${order.status} mr-3">${order.statusLabel}</span><p class="text-sm mt-2" style="color:var(--color-text-muted)">${order.date} — ${APF.formatPrice(order.total)}</p></div>`;
      }
    });
    APF_DATA.orders.forEach(o => {
      const list = document.getElementById('orders-list');
      if (!list) return;
      list.innerHTML += `<div class="order-card reveal"><div class="flex justify-between"><strong>${o.id}</strong><span class="order-status order-status-${o.status}">${o.statusLabel}</span></div><p class="text-sm mt-1" style="color:var(--color-text-muted)">${o.date}</p></div>`;
    });
    APF.initScrollReveal();
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
