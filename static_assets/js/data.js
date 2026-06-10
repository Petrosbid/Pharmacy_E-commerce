/**
 * آرمان فارما — Shared mock data (replace with Django context)
 */
window.APF_DATA = window.APF_DATA || {};
Object.assign(window.APF_DATA, {
  categories: window.APF_DATA.categories || [
    { id: 'general', name: 'داروهای عمومی', icon: '💊', count: 2400, slug: 'general' },
    { id: 'supplements', name: 'مکمل‌ها', icon: '🌿', count: 850, slug: 'supplements' },
    { id: 'hygiene', name: 'بهداشت فردی', icon: '🧴', count: 620, slug: 'hygiene' },
    { id: 'skincare', name: 'پوست و مو', icon: '✨', count: 1100, slug: 'skincare' },
    { id: 'mother-child', name: 'مراقبت مادر و کودک', icon: '👶', count: 430, slug: 'mother-child' },
    { id: 'medical', name: 'تجهیزات پزشکی', icon: '🩺', count: 320, slug: 'medical' },
    { id: 'cosmetics', name: 'آرایشی', icon: '💄', count: 780, slug: 'cosmetics' },
    { id: 'prescription', name: 'محصولات نسخه‌ای', icon: '📋', count: 1500, slug: 'prescription' },
  ],

  products: [
    { id: 1, slug: 'vitamin-d3-5000', name: 'ویتامین D3 ۵۰۰۰ واحد', category: 'مکمل‌ها', categorySlug: 'supplements', price: 285000, oldPrice: 320000, rating: 4.8, reviews: 124, badge: 'sale', tab: 'special', inStock: true, desc: 'مکمل ویتامین D3 با جذب بالا، مناسب تقویت سیستم ایمنی و سلامت استخوان.' },
    { id: 2, slug: 'retinol-serum-30', name: 'سرم ضد چروک رتینول ۳۰ml', category: 'پوست و مو', categorySlug: 'skincare', price: 890000, oldPrice: null, rating: 4.9, reviews: 89, badge: 'new', tab: 'new', inStock: true, desc: 'سرم رتینول ۰.۳٪ برای کاهش چروک و یکنواخت‌سازی رنگ پوست.' },
    { id: 3, slug: 'multivitamin-adult', name: 'مولتی‌ویتامین کامل بزرگسال', category: 'مکمل‌ها', categorySlug: 'supplements', price: 420000, oldPrice: null, rating: 4.7, reviews: 256, badge: 'bestseller', tab: 'popular', inStock: true, desc: 'فرمول کامل ۲۳ ویتامین و م mineral برای بزرگسالان.' },
    { id: 4, slug: 'hair-shampoo-400', name: 'شامپو تقویت‌کننده مو ۴۰۰ml', category: 'پوست و مو', categorySlug: 'skincare', price: 195000, oldPrice: 240000, rating: 4.5, reviews: 67, badge: 'sale', tab: 'special', inStock: true, desc: 'شامپو تقویت‌کننده با بیوتین و کراتین برای موهای آسیب‌دیده.' },
    { id: 5, slug: 'protein-isolate-900', name: 'پودر پروتئین ایزوله ۹۰۰g', category: 'مکمل‌ها', categorySlug: 'supplements', price: 1250000, oldPrice: null, rating: 4.6, reviews: 43, badge: 'popular', tab: 'popular', inStock: true, desc: 'پروتئین وی ایزوله ۹۰٪ با طعم وانیل، مناسب ورزشکاران.' },
    { id: 6, slug: 'sensitive-moisturizer', name: 'کرم مرطوب‌کننده پوست حساس', category: 'پوست و مو', categorySlug: 'skincare', price: 340000, oldPrice: null, rating: 4.8, reviews: 178, badge: 'new', tab: 'new', inStock: true, desc: 'کرم سبک بدون عطر برای پوست حساس و مستعد قرمزی.' },
    { id: 7, slug: 'omega3-1000', name: 'قرص امگا ۳ ۱۰۰۰mg', category: 'مکمل‌ها', categorySlug: 'supplements', price: 380000, oldPrice: 450000, rating: 4.7, reviews: 312, badge: 'bestseller', tab: 'popular', inStock: true, desc: 'امگا ۳ با غلظت EPA/DHA بالا برای سلامت قلب و مغز.' },
    { id: 8, slug: 'hand-sanitizer', name: 'اسپری ضدعفونی‌کننده دست', category: 'بهداشت فردی', categorySlug: 'hygiene', price: 85000, oldPrice: null, rating: 4.4, reviews: 95, badge: null, tab: 'popular', inStock: true, desc: 'ضدعفونی‌کننده ۷۰٪ الکل با آلوئه‌ورا، بدون خشکی پوست.' },
    { id: 9, slug: 'baby-diaper-cream', name: 'کرم سوختگی نوزاد ۱۰۰g', category: 'مراقبت مادر و کودک', categorySlug: 'mother-child', price: 125000, oldPrice: null, rating: 4.9, reviews: 201, badge: 'bestseller', tab: 'popular', inStock: true, desc: 'کرم زینک اکساید برای پیشگیری و درمان سوختگی پوشک.' },
    { id: 10, slug: 'blood-pressure-monitor', name: 'فشارسنج دیجیتال بازویی', category: 'تجهیزات پزشکی', categorySlug: 'medical', price: 1850000, oldPrice: 2100000, rating: 4.6, reviews: 54, badge: 'sale', tab: 'special', inStock: true, desc: 'فشارسنج اتوماتیک با حافظه ۹۹ اندازه‌گیری و صفحه بزرگ.' },
    { id: 11, slug: 'sunscreen-spf50', name: 'ضدآفتاب SPF50+ ۵۰ml', category: 'آرایشی', categorySlug: 'cosmetics', price: 520000, oldPrice: null, rating: 4.8, reviews: 143, badge: 'new', tab: 'new', inStock: true, desc: 'فلوئید سبک با محافظت UVA/UVB، مناسب انواع پوست.' },
    { id: 12, slug: 'calcium-magnesium', name: 'قرص کلسیم + منیزium', category: 'مکمل‌ها', categorySlug: 'supplements', price: 210000, oldPrice: null, rating: 4.5, reviews: 88, badge: null, tab: 'popular', inStock: false, desc: 'ترکیب کلسیم، منیزium و ویتامین D3 برای استخوان‌ها.' },
  ],

  badgeLabels: { new: 'جدید', sale: 'تخفیف ویژه', popular: 'محبوب', bestseller: 'پرفروش' },

  blogPosts: [
    { slug: 'vitamin-d-guide', tag: 'مکمل‌ها', icon: '🌿', title: 'راهنمای کامل انتخاب ویتامین D — چه زمانی و چقدر مصرف کنیم؟', excerpt: 'بررسی علمی دوز مناسب، تداخلات دارویی و علائم کمبود...', date: '۱۵ اردیبهشت ۱۴۰۴', readTime: '۸ دقیقه', author: 'دکتر سارا محمدی' },
    { slug: 'antibiotic-mistakes', tag: 'دارو', icon: '💊', title: '۵ اشتباه رایج در مصرف آنتی‌بیotic که باید بدانید', excerpt: 'مصرف ناقص دوره درمان و خوددرمانی — خطراتی که جدی بگیرید...', date: '۸ اردیبهشت ۱۴۰۴', readTime: '۶ دقیقه', author: 'دکتر علی رضایی' },
    { slug: 'autumn-skincare', tag: 'پوست', icon: '✨', title: 'روتین پوستی پاییزه: محصولات ضروری برای پوست خشک', excerpt: 'از سرم هیالورونیک تا کرم مرطوب‌کننده — پیشنهاد داروساز...', date: '۱ اردیبهشت ۱۴۰۴', readTime: '۱۰ دقیقه', author: 'دکتر مریم حسینی' },
    { slug: 'immune-boost', tag: 'سلامت', icon: '🛡️', title: 'تقویت سیستم ایمنی: واقعیت‌ها در برابر شایعات', excerpt: 'چه مکمل‌هایی واقعاً موثرند و چه چیزهایی فقط تبلیغات‌اند...', date: '۲۵ فروردین ۱۴۰۴', readTime: '۷ دقیقه', author: 'دکتر سارا محمدی' },
    { slug: 'sleep-hygiene', tag: 'سبک زندگی', icon: '😴', title: 'بهداشت خواب: ۷ عادت ساده برای شب‌های بهتر', excerpt: 'بدون دارو خوابتان را تنظیم کنید — توصیه‌های مبتنی بر شواهد...', date: '۱۸ فروردین ۱۴۰۴', readTime: '۵ دقیقه', author: 'دکتر علی رضایی' },
    { slug: 'child-vitamins', tag: 'کودک', icon: '👶', title: 'ویتامین‌های ضروری کودکان: راهنمای والدین', excerpt: 'کدام مکمل‌ها لازم است و از چه سنی — نظر داروساز کودک...', date: '۱۰ فروردین ۱۴۰۴', readTime: '۹ دقیقه', author: 'دکتر مریم حسینی' },
  ],

  orders: [
    { id: 'AP-1404-8842', date: '۳ خرداد ۱۴۰۴', status: 'delivered', statusLabel: 'تحویل شده', total: 705000, items: 2 },
    { id: 'AP-1404-8710', date: '۲۸ اردیبهشت ۱۴۰۴', status: 'shipping', statusLabel: 'در حال ارسال', total: 1250000, items: 1 },
    { id: 'AP-1404-8655', date: '۲۰ اردیبهشت ۱۴۰۴', status: 'processing', statusLabel: 'در حال آماده‌سازی', total: 420000, items: 3 },
  ],
};
