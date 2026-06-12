(function () {
  function init() {
    APF.initCore();
    // Wait for the cart API call to finish before rendering items
    setTimeout(() => {
        const list = document.getElementById('checkout-items');
        if (list && APF.state.cartData && APF.state.cartData.length) {
          list.innerHTML = APF.state.cartData.map(item => `
            <div class="flex justify-between py-2 text-sm"><span>${item.name} × ${item.quantity.toLocaleString('fa-IR')}</span><span>${APF.formatPrice(item.total)}</span></div>`).join('');
        }
        
        const shipping = window.APF_DATA?.expressShippingCost || 45000;
        const totalEl = document.getElementById('checkout-total');
        if (totalEl) totalEl.textContent = APF.formatPrice(APF.getCartTotal() + shipping);
    }, 300);

    document.getElementById('checkout-form')?.addEventListener('submit', e => {
      // Allow Django to handle POST
      APF.showToast('در حال ثبت سفارش...');
      // We don't preventDefault here
    });
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
