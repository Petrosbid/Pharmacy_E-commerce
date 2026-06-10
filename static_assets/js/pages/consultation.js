(function () {
  function init() {
    APF.initCore();
    document.getElementById('consultation-form')?.addEventListener('submit', e => {
      e.preventDefault();
      APF.showToast('درخواست مشاوره ثبت شد. ظرف ۳۰ دقیقه با شما تماس می‌گیریم.');
    });
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
