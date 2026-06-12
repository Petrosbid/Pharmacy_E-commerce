/**
 * آرمان فارما — Core Application
 */
window.APF = (function () {
  'use strict';

  const STORAGE_CART = 'arman-pharma-cart';
  const STORAGE_FAVS = 'arman-pharma-favorites';
  const STORAGE_THEME = 'arman-pharma-theme';

  const products = APF_DATA.products;
  const badgeLabels = APF_DATA.badgeLabels;

  const state = {
    cart: JSON.parse(localStorage.getItem(STORAGE_CART) || '[]'),
    favorites: new Set(JSON.parse(localStorage.getItem(STORAGE_FAVS) || '[]')),
    theme: localStorage.getItem(STORAGE_THEME) || 'light',
  };

  function saveCart() {
    localStorage.setItem(STORAGE_CART, JSON.stringify(state.cart));
  }

  function saveFavorites() {
    localStorage.setItem(STORAGE_FAVS, JSON.stringify([...state.favorites]));
  }

  function formatPrice(num) {
    const farsiDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    return num.toLocaleString('en-US').replace(/\d/g, x => farsiDigits[x]) + ' تومان';
  }

  function $(s, p = document) { return p.querySelector(s); }
  function $$(s, p = document) { return [...p.querySelectorAll(s)]; }

  function createElement(tag, cls, html) {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (html !== undefined) el.innerHTML = html;
    return el;
  }

  function getProduct(id) {
    return products.find(p => p.id === id || p.slug === id);
  }

  function renderStars(rating) {
    const full = Math.floor(rating);
    const half = rating % 1 >= 0.5;
    let html = '';
    for (let i = 0; i < 5; i++) {
      if (i < full) {
        html += '<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>';
      } else if (i === full && half) {
        html += '<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" opacity="0.5"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>';
      } else {
        html += '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>';
      }
    }
    return html;
  }

  function productCardHTML(product, opts = {}) {
    const link = opts.link !== false;
    const badgeHtml = product.badge ? `<span class="product-badge product-badge-${product.badge}">${badgeLabels[product.badge]}</span>` : '';
    const oldPriceHtml = product.oldPrice ? `<span class="product-price-old">${formatPrice(product.oldPrice)}</span>` : '';
    const isFav = state.favorites.has(product.id);
    const nameTag = link ? 'a' : 'h3';
    const nameAttrs = link ? `href="/products/${product.slug}/" class="product-name"` : 'class="product-name"';

    return `
      <article class="product-card reveal" data-product-id="${product.id}">
        <div class="product-card-image">
          ${badgeHtml}
          <button class="product-favorite ${isFav ? 'active' : ''}" aria-label="افزودن به علاقه‌مندی‌ها" data-fav-id="${product.id}">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          </button>
          ${link ? `<a href="/products/${product.slug}/" class="block w-full h-full flex items-center justify-center">` : ''}
          <div class="product-visual"></div>
          ${link ? '</a>' : ''}
        </div>
        <div class="product-card-body">
          <div class="product-category-tag">${product.category}</div>
          <${nameTag} ${nameAttrs}>${product.name}</${nameTag}>
          <div class="product-rating">
            <div class="product-stars">${renderStars(product.rating)}</div>
            <span class="product-rating-count">(${product.reviews.toLocaleString('fa-IR')})</span>
          </div>
          <div class="product-footer">
            <div class="product-price-wrap">
              <span class="product-price">${formatPrice(product.price)}</span>
              ${oldPriceHtml}
            </div>
            <button class="product-add-btn" aria-label="افزودن به سبد خرید" data-add-id="${product.id}">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
            </button>
          </div>
        </div>
      </article>`;
  }

  function renderProductGrid(container, list) {
    if (!container) return;
    container.innerHTML = list.map(p => productCardHTML(p)).join('');
    bindProductEvents(container);
    initScrollReveal();
  }

  function bindProductEvents(container) {
    container.addEventListener('click', e => {
      const addBtn = e.target.closest('[data-add-id]');
      if (addBtn) { addToCart(parseInt(addBtn.dataset.addId, 10)); rippleEffect(addBtn, e); return; }
      const favBtn = e.target.closest('[data-fav-id]');
      if (favBtn) toggleFavorite(parseInt(favBtn.dataset.favId, 10), favBtn);
    });
  }

  function rippleEffect(btn, e) {
    const rect = btn.getBoundingClientRect();
    const ripple = createElement('span');
    ripple.style.cssText = `position:absolute;border-radius:50%;background:rgba(255,255,255,0.4);width:40px;height:40px;pointer-events:none;left:${e.clientX - rect.left - 20}px;top:${e.clientY - rect.top - 20}px;animation:rippleAnim 0.5s ease forwards;`;
    btn.style.position = 'relative';
    btn.style.overflow = 'hidden';
    btn.appendChild(ripple);
    setTimeout(() => ripple.remove(), 500);
  }

  /* Theme */
  function initTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
    const btn = $('#theme-toggle');
    if (btn) btn.setAttribute('aria-label', state.theme === 'light' ? 'فعال‌سازی حالت تاریک' : 'فعال‌سازی حالت روشن');
  }

  function toggleTheme() {
    document.documentElement.classList.add('theme-transitioning');
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', state.theme);
    localStorage.setItem(STORAGE_THEME, state.theme);
    initTheme();
    setTimeout(() => document.documentElement.classList.remove('theme-transitioning'), 600);
  }

  /* Header */
  function initHeaderScroll() {
    const header = $('#site-header');
    if (!header) return;
    const fn = () => header.classList.toggle('scrolled', window.scrollY > 20);
    window.addEventListener('scroll', fn, { passive: true });
    fn();
  }

  function initMobileMenu() {
    const menu = $('#mobile-menu');
    const openBtn = $('#mobile-menu-open');
    const closeBtn = $('#mobile-menu-close');
    const backdrop = $('#mobile-menu-backdrop');
    if (!menu || !openBtn) return;

    const open = () => { menu.classList.add('open'); openBtn.setAttribute('aria-expanded', 'true'); document.body.style.overflow = 'hidden'; };
    const close = () => { menu.classList.remove('open'); openBtn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; };

    openBtn.addEventListener('click', open);
    closeBtn?.addEventListener('click', close);
    backdrop?.addEventListener('click', close);
    $$('.mobile-nav-link', menu).forEach(l => l.addEventListener('click', close));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.classList.contains('open')) close(); });
  }

  /* Scroll reveal */
  function initScrollReveal() {
    const reveals = $$('.reveal:not(.revealed)');
    if (!reveals.length) return;
    const obs = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('revealed'); obs.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(el => obs.observe(el));
  }

  /* Counters */
  function initCounters() {
    $$('[data-counter]').forEach(el => {
      const obs = new IntersectionObserver(entries => {
        if (!entries[0].isIntersecting) return;
        const target = parseInt(el.dataset.counter, 10);
        const suffix = el.dataset.suffix || '';
        const start = performance.now();
        const step = now => {
          const p = Math.min((now - start) / 2000, 1);
          el.textContent = Math.floor((1 - Math.pow(1 - p, 3)) * target).toLocaleString('fa-IR') + suffix;
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
        obs.disconnect();
      }, { threshold: 0.5 });
      obs.observe(el);
    });
  }

  /* Cart */
  function addToCart(productId, qty = 1) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    const existing = state.cart.find(i => i.id === productId);
    if (existing) existing.qty += qty;
    else state.cart.push({ id: product.id, name: product.name, price: product.price, qty });
    saveCart();
    updateCartUI();
    showToast(`${product.name} به سبد خرید اضافه شد`);
  }

  function updateCartQty(productId, delta) {
    const item = state.cart.find(i => i.id === productId);
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) state.cart = state.cart.filter(i => i.id !== productId);
    saveCart();
    updateCartUI();
  }

  function getCartTotal() { return state.cart.reduce((s, i) => s + i.price * i.qty, 0); }
  function getCartCount() { return state.cart.reduce((s, i) => s + i.qty, 0); }

  function updateCartUI() {
    const badge = $('#cart-badge');
    const count = getCartCount();
    if (badge) {
      badge.textContent = count.toLocaleString('fa-IR');
      badge.style.display = count > 0 ? 'flex' : 'none';
    }
    renderCartItems();
    const checkoutTotal = $('#checkout-total');
    if (checkoutTotal) checkoutTotal.textContent = formatPrice(getCartTotal());
    const checkoutSubtotal = $('#checkout-subtotal');
    if (checkoutSubtotal) checkoutSubtotal.textContent = formatPrice(getCartTotal());
  }

  function renderCartItems() {
    const body = $('#cart-drawer-body');
    const totalEl = $('#cart-total-price');
    if (!body) return;

    if (!state.cart.length) {
      body.innerHTML = `<div class="cart-empty"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="opacity:0.3;margin-bottom:1rem"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg><p>سبد خرید شما خالی است</p></div>`;
    } else {
      body.innerHTML = state.cart.map(item => `
        <div class="cart-item"><div class="cart-item-image"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/></svg></div>
        <div class="cart-item-info"><div class="cart-item-name">${item.name}</div><div class="cart-item-price">${formatPrice(item.price)}</div>
        <div class="cart-item-qty"><button aria-label="کاهش" data-qty-minus="${item.id}">−</button><span>${item.qty.toLocaleString('fa-IR')}</span><button aria-label="افزایش" data-qty-plus="${item.id}">+</button></div></div></div>`).join('');
    }
    if (totalEl) totalEl.textContent = formatPrice(getCartTotal());
  }

  function initCartDrawer() {
    const drawer = $('#cart-drawer');
    const openBtn = $('#cart-open');
    if (!drawer || !openBtn) return;
    const close = () => { drawer.classList.remove('open'); document.body.style.overflow = ''; };
    openBtn.addEventListener('click', () => { drawer.classList.add('open'); document.body.style.overflow = 'hidden'; });
    $('#cart-close')?.addEventListener('click', close);
    $('#cart-backdrop')?.addEventListener('click', close);
    $('#cart-drawer-body')?.addEventListener('click', e => {
      if (e.target.closest('[data-qty-minus]')) updateCartQty(parseInt(e.target.closest('[data-qty-minus]').dataset.qtyMinus, 10), -1);
      if (e.target.closest('[data-qty-plus]')) updateCartQty(parseInt(e.target.closest('[data-qty-plus]').dataset.qtyPlus, 10), 1);
    });
    $('#cart-checkout-btn')?.addEventListener('click', () => { if (state.cart.length) window.location.href = '/orders/checkout/'; });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && drawer.classList.contains('open')) close(); });
  }

  function toggleFavorite(id, btn) {
    if (state.favorites.has(id)) { state.favorites.delete(id); btn?.classList.remove('active'); }
    else { state.favorites.add(id); btn?.classList.add('active'); showToast('به علاقه‌مندی‌ها اضافه شد'); }
    saveFavorites();
  }

  function initFAQ() {
    $$('.faq-item').forEach(item => {
      $('.faq-question', item)?.addEventListener('click', () => {
        const open = item.classList.contains('open');
        $$('.faq-item').forEach(i => { i.classList.remove('open'); $('.faq-question', i)?.setAttribute('aria-expanded', 'false'); });
        if (!open) { item.classList.add('open'); $('.faq-question', item)?.setAttribute('aria-expanded', 'true'); }
      });
    });
  }

  function showToast(message) {
    const container = $('#toast-container');
    if (!container) return;
    const toast = createElement('div', 'toast', `<span class="toast-icon"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M20 6L9 17l-5-5"/></svg></span><span>${message}</span>`);
    container.appendChild(toast);
    setTimeout(() => { toast.classList.add('toast-out'); setTimeout(() => toast.remove(), 300); }, 3000);
  }

  function initSearch() {
    $$('.search-bar input').forEach(input => {
      input.addEventListener('keydown', e => {
        if (e.key === 'Enter' && input.value.trim()) window.location.href = `/products/search/?q=${encodeURIComponent(input.value.trim())}`;
      });
    });
  }

  function initNewsletter() {
    $('#newsletter-form')?.addEventListener('submit', e => {
      e.preventDefault();
      const input = $('input', e.target);
      if (input?.value.trim()) { showToast('عضویت شما با موفقیت ثبت شد'); input.value = ''; }
    });
  }

  function initHeroParallax() {
    const hero = $('#hero-section');
    if (!hero || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    window.addEventListener('scroll', () => {
      const rect = hero.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > window.innerHeight) return;
      const p = -rect.top / rect.height;
      $$('.hero-orb', hero).forEach((o, i) => { o.style.transform = `translateY(${p * (20 + i * 15)}px)`; });
    }, { passive: true });
  }

  function injectRippleKeyframes() {
    if ($('#ripple-styles')) return;
    const s = createElement('style');
    s.id = 'ripple-styles';
    s.textContent = '@keyframes rippleAnim { to { transform: scale(4); opacity: 0; } }';
    document.head.appendChild(s);
  }

  function initCore() {
    injectRippleKeyframes();
    initTheme();
    initHeaderScroll();
    initMobileMenu();
    initScrollReveal();
    initCartDrawer();
    initSearch();
    initNewsletter();
    updateCartUI();
    $('#theme-toggle')?.addEventListener('click', toggleTheme);
    document.body.classList.add('page-enter');
  }

  return {
    state, products, formatPrice, getProduct, renderStars, productCardHTML,
    renderProductGrid, bindProductEvents, addToCart, updateCartQty, toggleFavorite,
    initCore, initScrollReveal, initCounters, initFAQ, initHeroParallax, showToast,
    getCartTotal, getCartCount, updateCartUI,
  };
})();
