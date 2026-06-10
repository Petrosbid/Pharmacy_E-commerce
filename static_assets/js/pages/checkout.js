(function () {
  function init() {
    APF.initCore();
    const list = document.getElementById('checkout-items');
    if (list && APF.state.cart.length) {
      list.innerHTML = APF.state.cart.map(item => `
        <div class="flex justify-between py-2 text-sm"><span>${item.name} × ${item.qty.toLocaleString('fa-IR')}</span><span>${APF.formatPrice(item.price * item.qty)}</span></div>`).join('');
    }
    APF.updateCartUI();
    const shipping = 45000;
    const totalEl = document.getElementById('checkout-total');
    if (totalEl) totalEl.textContent = APF.formatPrice(APF.getCartTotal() + shipping);
    document.getElementById('checkout-form')?.addEventListener('submit', e => {
      // Allow Django to handle POST
      APF.showToast('در حال ثبت سفارش...');
      // We don't preventDefault here
    });
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
