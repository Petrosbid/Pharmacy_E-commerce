/**
 * آرمان فارما — Shared layout injection (Django: replace with {% include %})
 */
(function () {
  'use strict';

  const page = document.body.dataset.page || 'home';
  const isHome = page === 'home';

  const navLinks = [
    { href: '/products/categories/', label: 'دسته‌بندی‌ها', key: 'categories' },
    { href: '/products/', label: 'محصولات', key: 'products' },
    { href: '/prescriptions/submit/', label: 'نسخه', key: 'prescription' },
    { href: '/consultation/', label: 'مشاوره', key: 'consultation' },
  ];

  function navClass(key) {
    return page === key ? 'text-[var(--color-primary)]' : '';
  }

  const headerHTML = `
  <a href="#main-content" class="skip-link">رفتن به محتوای اصلی</a>
  <header id="site-header" class="site-header${isHome ? '' : ' scrolled'}">
    <div class="container-main header-inner flex items-center justify-between gap-4">
      <a href="/" class="brand-logo shrink-0">
        <div class="brand-icon" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M12 2v20M2 12h20"/></svg></div>
        <div><div class="brand-name">آرمان فارما</div><div class="brand-tagline hidden sm:block">سلامت، اعتماد، کیفیت</div></div>
      </a>
      <div class="search-bar hidden lg:block">
        <input type="search" placeholder="جستجوی دارو، مکمل یا محصول بهداشتی..." aria-label="جستجو">
        <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      </div>
      <nav class="hidden lg:flex items-center gap-1" aria-label="ناوبری اصلی">
        ${navLinks.map(n => {
          const active = page === n.key;
          return `<a href="${n.href}" class="px-3 py-2 text-sm font-semibold rounded-lg hover:text-[var(--color-primary)] transition-colors" style="color:${active ? 'var(--color-primary)' : 'var(--color-text-secondary)'}">${n.label}</a>`;
        }).join('')}
      </nav>
      <div class="flex items-center gap-2">
        <button id="theme-toggle" class="theme-toggle" aria-label="تغییر تم"><span class="theme-toggle-thumb"><svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg><svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></span></button>
        <a href="/products/favorites/" id="favorites-link" class="nav-action hidden sm:flex" aria-label="علاقه‌مندی‌ها"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg></a>
        <a href="/users/profile/" id="account-link" class="nav-action hidden sm:flex" aria-label="حساب کاربری"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></a>
        <button id="cart-open" class="nav-action" aria-label="سبد خرید"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg><span id="cart-badge" class="badge" style="display:none">۰</span></button>
        <button id="mobile-menu-open" class="nav-action lg:hidden" aria-label="منوی موبایل" aria-expanded="false"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg></button>
      </div>
    </div>
  </header>
  <div id="mobile-menu" class="mobile-menu" aria-hidden="true">
    <div id="mobile-menu-backdrop" class="mobile-menu-backdrop"></div>
    <div class="mobile-menu-panel">
      <div class="flex items-center justify-between mb-6"><span class="font-bold text-lg">منو</span><button id="mobile-menu-close" class="nav-action" aria-label="بستن"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg></button></div>
      <div class="search-bar mb-6"><input type="search" placeholder="جستجو..." aria-label="جستجو"><svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg></div>
      <nav class="flex flex-col gap-1">
        ${navLinks.map(n => `<a href="${n.href}" class="mobile-nav-link px-4 py-3 rounded-lg font-semibold hover:bg-[var(--color-bg-muted)]">${n.label}</a>`).join('')}
        <a href="/blog/" class="mobile-nav-link px-4 py-3 rounded-lg font-semibold hover:bg-[var(--color-bg-muted)]">مجله سلامت</a>
        <a href="/faq/" class="mobile-nav-link px-4 py-3 rounded-lg font-semibold hover:bg-[var(--color-bg-muted)]">سوالات متداول</a>
        <a href="/users/login/" class="mobile-nav-link px-4 py-3 rounded-lg font-semibold hover:bg-[var(--color-bg-muted)]">ورود / ثبت‌نام</a>
      </nav>
    </div>
  </div>`;

  const footerHTML = `
  <footer class="site-footer">
    <div class="container-main">
      <div class="footer-grid">
        <div>
          <a href="/" class="brand-logo"><div class="brand-icon" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M12 2v20M2 12h20"/></svg></div><div><div class="brand-name">آرمان فارما</div><div class="brand-tagline">سلامت، اعتماد، کیفیت</div></div></a>
          <p class="footer-brand-desc">داروخانه آنلاین مدرن با بیش از ۱۵ سال سابقه. ارائه دارو، مکمل و محصولات بهداشتی اصل با مشاوره تخصصی و ارسال سریع.</p>
          <div class="footer-social">
            <a href="#" aria-label="اینستاگرام"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/></svg></a>
            <a href="#" aria-label="تلگرام"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg></a>
            <a href="#" aria-label="واتساپ"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></a>
          </div>
        </div>
        <div><h4 class="footer-heading">دسترسی سریع</h4><ul class="footer-links"><li><a href="/products/">محصولات</a></li><li><a href="/products/categories/">دسته‌بندی‌ها</a></li><li><a href="/prescriptions/submit/">ثبت نسخه</a></li><li><a href="/consultation/">مشاوره داروساز</a></li><li><a href="/blog/">مجله سلامت</a></li></ul></div>
        <div><h4 class="footer-heading">پشتیبانی</h4><ul class="footer-links"><li><a href="/faq/">سوالات متداول</a></li><li><a href="/orders/history/">پیگیری سفارش</a></li><li><a href="/returns/">شرایط مرجوعی</a></li><li><a href="/privacy/">حریم خصوصی</a></li><li><a href="/contact/">تماس با ما</a></li></ul></div>
        <div><h4 class="footer-heading">خبرنامه سلامت</h4><p class="text-sm" style="color:var(--color-text-secondary)">تخفیف‌ها و مطالب سلامت را در ایمیل خود دریافت کنید</p>
          <form id="newsletter-form" class="newsletter-form"><input type="email" placeholder="ایمیل شما" required aria-label="ایمیل"><button type="submit">عضویت</button></form>
          <div class="mt-4 text-sm" style="color:var(--color-text-muted)"><div class="flex items-center gap-2 mb-1"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>۰۲۱-۹۱۰۰۱۰۰۰</div><div class="flex items-center gap-2"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>support@armanpharma.ir</div></div>
        </div>
      </div>
      <div class="footer-bottom"><span>© ۱۴۰۴ آرمان فارما — تمامی حقوق محفوظ است</span><div class="footer-badges"><span class="footer-badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>مجوز سازمان غذا و دارو</span><span class="footer-badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>پرداخت امن شاپرک</span></div></div>
    </div>
  </footer>`;

  const overlaysHTML = `
  <div id="cart-drawer" class="cart-drawer" aria-hidden="true">
    <div id="cart-backdrop" class="cart-drawer-backdrop"></div>
    <div class="cart-drawer-panel" role="dialog" aria-label="سبد خرید">
      <div class="cart-drawer-header"><h2 class="font-bold text-lg">سبد خرید</h2><button id="cart-close" class="nav-action" aria-label="بستن"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg></button></div>
      <div id="cart-drawer-body" class="cart-drawer-body"><div class="cart-empty"><p>سبد خرید شما خالی است</p></div></div>
      <div class="cart-drawer-footer"><div class="cart-total"><span>جمع کل</span><span id="cart-total-price">۰ تومان</span></div><button id="cart-checkout-btn" class="btn btn-primary w-full">تکمیل خرید</button></div>
    </div>
  </div>
  <div id="toast-container" class="toast-container" aria-live="polite"></div>`;

  function inject() {
    // HTML injection removed as it's now handled by Django templates.
  }

  inject();
})();
