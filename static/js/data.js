/**
 * آرمان فارما — Shared data (populated by Django context)
 */
window.APF_DATA = window.APF_DATA || {};
Object.assign(window.APF_DATA, {
  categories: window.APF_DATA.categories || [],
  products: window.APF_DATA.products || [],
  badgeLabels: { new: 'جدید', sale: 'تخفیف ویژه', popular: 'محبوب', bestseller: 'پرفروش' },

  blogPosts: [
    { slug: 'vitamin-d-guide', tag: 'مکمل‌ها', icon: '🌿', title: 'راهنمای کامل انتخاب ویتامین D — چه زمانی و چقدر مصرف کنیم؟', excerpt: 'بررسی علمی دوز مناسب، تداخلات دارویی و علائم کمبود...', date: '۱۵ اردیبهشت ۱۴۰۴', readTime: '۸ دقیقه', author: 'دکتر سارا محمدی' },
    { slug: 'antibiotic-mistakes', tag: 'دارو', icon: '💊', title: '۵ اشتباه رایج در مصرف آنتی‌بیotic که باید بدانید', excerpt: 'مصرف ناقص دوره درمان و خوددرمانی — خطراتی که جدی بگیرید...', date: '۸ اردیبهشت ۱۴۰۴', readTime: '۶ دقیقه', author: 'دکتر علی رضایی' },
    { slug: 'autumn-skincare', tag: 'پوست', icon: '✨', title: 'روتین پوستی پاییزه: محصولات ضروری برای پوست خشک', excerpt: 'از سرم هیالورونیک تا کرم مرطوب‌کننده — پیشنهاد داروساز...', date: '۱ اردیبهشت ۱۴۰۴', readTime: '۱۰ دقیقه', author: 'دکتر مریم حسینی' },
  ],
});
