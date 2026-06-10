(function () {
  function init() {
    APF.initCore();
    const grid = document.getElementById('blog-grid');
    if (grid) {
      grid.innerHTML = APF_DATA.blogPosts.map((post, i) => `
        <a href="/blog/${post.slug}/" class="blog-card reveal${i ? ' reveal-delay-' + Math.min(i, 4) : ''}">
          <div class="blog-card-image">${post.icon}</div>
          <div class="blog-card-body"><div class="blog-tag">${post.tag}</div><h3 class="blog-title">${post.title}</h3><p class="blog-excerpt">${post.excerpt}</p></div>
        </a>`).join('');
      APF.initScrollReveal();
    }
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
