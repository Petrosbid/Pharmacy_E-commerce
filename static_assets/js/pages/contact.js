(function () {
  function init() {
    APF.initCore();
    document.getElementById('contact-form')?.addEventListener('submit', e => {
      e.preventDefault();
      APF.showToast('پیام شما ارسال شد. به‌زودی پاسخ می‌دهیم.');
    });
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
