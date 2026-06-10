(function () {
  function init() { APF.initCore(); APF.initFAQ(); }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
