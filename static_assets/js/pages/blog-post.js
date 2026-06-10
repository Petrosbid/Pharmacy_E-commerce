(function () {
  function init() {
    APF.initCore();
    const slug = new URLSearchParams(location.search).get('slug');
    const post = APF_DATA.blogPosts.find(p => p.slug === slug);
    if (!post) return;
    document.title = `${post.title} | آرمان فارما`;
    document.getElementById('post-title').textContent = post.title;
    document.getElementById('post-tag').textContent = post.tag;
    document.getElementById('post-date').textContent = post.date;
    document.getElementById('post-author').textContent = post.author;
    document.getElementById('post-read').textContent = post.readTime;
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
