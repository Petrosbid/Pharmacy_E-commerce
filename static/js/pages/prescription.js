(function () {
  function init() {
    APF.initCore();
    APF.initFAQ();
    const zone = document.getElementById('upload-zone');
    const input = document.getElementById('file-input');
    if (zone && input) {
      zone.addEventListener('click', () => input.click());
      zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
      zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
      zone.addEventListener('drop', e => { e.preventDefault(); zone.classList.remove('dragover'); if (e.dataTransfer.files.length) APF.showToast('نسخه با موفقیت آپلود شد — در حال بررسی'); });
      input.addEventListener('change', () => { if (input.files.length) APF.showToast('نسخه با موفقیت آپلود شد — در حال بررسی'); });
    }
    document.getElementById('prescription-form')?.addEventListener('submit', e => {
      e.preventDefault();
      APF.showToast('درخواست شما ثبت شد. داروساز به‌زودی با شما تماس می‌گیرد.');
    });
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
