(function () {
  function init() {
    APF.initCore();
    document.querySelectorAll('.auth-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.auth-panel').forEach(p => p.classList.add('hidden'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.panel)?.classList.remove('hidden');
      });
    });
    document.getElementById('login-form')?.addEventListener('submit', e => { e.preventDefault(); window.location.href = '/users/profile/'; });
    document.getElementById('register-form')?.addEventListener('submit', e => { e.preventDefault(); window.location.href = '/users/profile/'; });
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
