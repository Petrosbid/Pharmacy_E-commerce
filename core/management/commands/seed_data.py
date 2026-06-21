from django.core.management.base import BaseCommand
from products.models import Category, Product, ProductImage, Review
from core.models import FAQ
from blog.models import BlogPost, BlogCategory
from django.utils.text import slugify
from users.models import User
import random

class Command(BaseCommand):
    help = 'Seeds initial data including detailed product information'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        Review.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        FAQ.objects.all().delete()
        BlogPost.objects.all().delete()
        BlogCategory.objects.all().delete()

        self.stdout.write('Seeding users...')
        # Admin user
        admin_user, created = User.objects.get_or_create(
            phone_number='09120000000',
            defaults={'full_name': 'مدیر سیستم', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin1234')
            admin_user.save()

        # Reviewer Users
        reviewers = [
            {'phone': '09121111111', 'name': 'زهرا حسینی'},
            {'phone': '09122222222', 'name': 'علی مرادی'},
            {'phone': '09123333333', 'name': 'مریم رضایی'},
            {'phone': '09124444444', 'name': 'رضا احمدی'},
        ]
        reviewer_instances = []
        for r in reviewers:
            user, created = User.objects.get_or_create(
                phone_number=r['phone'],
                defaults={'full_name': r['name']}
            )
            if created:
                user.set_password('user1234')
                user.save()
            reviewer_instances.append(user)

        self.stdout.write('Seeding categories...')
        # Categories
        categories_data = [
            { 'name': 'داروهای عمومی', 'icon': '💊', 'slug': 'general' },
            { 'name': 'مکمل‌ها', 'icon': '🌿', 'slug': 'supplements' },
            { 'name': 'بهداشت فردی', 'icon': '🧴', 'slug': 'hygiene' },
            { 'name': 'پوست و مو', 'icon': '✨', 'slug': 'skincare' },
            { 'name': 'مراقبت مادر و کودک', 'icon': '👶', 'slug': 'mother-child' },
            { 'name': 'تجهیزات پزشکی', 'icon': '🩺', 'slug': 'medical' },
            { 'name': 'آرایشی', 'icon': '💄', 'slug': 'cosmetics' },
            { 'name': 'محصولات نسخه‌ای', 'icon': '📋', 'slug': 'prescription' },
        ]

        category_map = {}
        for cat_data in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=cat_data['slug'], 
                defaults={'name': cat_data['name'], 'icon': cat_data['icon']}
            )
            category_map[cat_data['slug']] = cat

        self.stdout.write('Seeding products...')
        # Products Data
        products_data = [
            # 1. General (داروهای عمومی - OTC)
            {
                'slug': 'acetaminophen-500',
                'name': 'قرص استامینوفن ۵۰۰ میلی‌گرم آریا',
                'category_slug': 'general',
                'price': 35000,
                'old_price': 40000,
                'badge': 'bestseller',
                'description': 'قرص مسکن و تب‌بر استامینوفن، مناسب برای تسکین سردرد، دندان‌درد، دردهای عضلانی و کاهش تب خفیف تا متوسط.',
                'generic_name': 'استامینوفن (Acetaminophen)',
                'brand': 'داروسازی آریا',
                'dosage_form': 'قرص (Tablet)',
                'dosage_strength': '۵۰۰ میلی‌گرم',
                'usage_instructions': 'بزرگسالان: ۱ تا ۲ قرص هر ۴ تا ۶ ساعت در صورت نیاز. از مصرف بیش از ۸ قرص (۴ گرم) در ۲۴ ساعت خودداری کنید.',
                'warnings': 'مصرف بیش از حد مجاز می‌تواند باعث آسیب جدی کبدی شود. همزمان با سایر داروهای حاوی استامینوفن مصرف نشود.',
                'is_prescription_required': False,
                'image_path': 'products/otc-medicine.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'مسکن خیلی خوبیه، همیشه توی خونه داریم. تأثیرگذاری سریعی هم داره.', 'is_verified': True},
                    {'rating': 4, 'comment': 'کیفیت ساخت قرص‌ها خوبه و قیمتش هم کاملاً مناسبه.', 'is_verified': True}
                ]
            },
            {
                'slug': 'gelofen-400',
                'name': 'کبسول ژلاتینی ژلوفن ۴۰۰ میلی‌گرم دانا',
                'category_slug': 'general',
                'price': 65000,
                'badge': 'popular',
                'description': 'ژلوفن فرم مایع مسکن ایبوپروفن در کپسول ژلاتینی نرم است که جذب سریع‌تر و عوارض گوارشی کمتری نسبت به قرص معمولی دارد. مناسب برای دردهای التهابی، سردرد و دردهای مفصلی.',
                'generic_name': 'ایبوپروفن (Ibuprofen)',
                'brand': 'داروسازی دانا',
                'dosage_form': 'کپسول نرم ژلاتینی (Softgel)',
                'dosage_strength': '۴۰۰ میلی‌گرم',
                'usage_instructions': 'هر ۶ ساعت ۱ عدد همراه با یک لیوان آب ترجیحاً بعد از غذا مصرف شود.',
                'warnings': 'در بیماران مبتلا به زخم معده، بیماری‌های قلبی و آسم با احتیاط مصرف شود. در سه ماهه سوم بارداری ممنوع است.',
                'is_prescription_required': False,
                'image_path': 'products/otc-medicine.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'برای تسکین سردردهای شدید و دندان‌درد فوق‌العاده سریع اثر می‌کنه.', 'is_verified': True},
                    {'rating': 4, 'comment': 'فقط حتما با شکم پر بخورید که معده‌تون اذیت نشه.', 'is_verified': True}
                ]
            },
            {
                'slug': 'adult-cold-abidi',
                'name': 'قرص سرماخوردگی بزرگسالان دکتر عبیدی',
                'category_slug': 'general',
                'price': 45000,
                'old_price': 50000,
                'badge': 'bestseller',
                'description': 'داروی ترکیبی سرماخوردگی حاوی استامینوفن (تب‌بر و مسکن)، فنیل‌افرین (ضد احتقان بینی) و کلرفنیرامین (آنتی‌هیستامین برای کاهش عطسه و آبریزش بینی).',
                'generic_name': 'استامینوفن / فنیل‌افرین / کلرفنیرامین',
                'brand': 'داروسازی دکتر عبیدی',
                'dosage_form': 'قرص (Tablet)',
                'dosage_strength': 'فرمولاسیون استاندارد',
                'usage_instructions': 'هر ۴ تا ۶ ساعت ۱ تا ۲ قرص. بیش از ۶ قرص در روز مصرف نشود.',
                'warnings': 'به دلیل وجود آنتی‌هیستامین ممکن است باعث خواب‌آلودگی شود. در هنگام رانندگی یا کار با ماشین‌آلات احتیاط کنید.',
                'is_prescription_required': False,
                'image_path': 'products/otc-medicine.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'بهترین داروی سرماخوردگی ایرانیه، سریع علائم مثل آبریزش بینی رو کنترل میکنه.', 'is_verified': True}
                ]
            },
            
            # 2. Prescription (محصولات نسخه‌ای - Rx)
            {
                'slug': 'metformin-500',
                'name': 'قرص متفورمین ۵۰۰ میلی‌گرم آریا (نسخه‌ای)',
                'category_slug': 'prescription',
                'price': 85000,
                'badge': None,
                'description': 'داروی کاهنده قند خون و کنترل دیابت نوع ۲. این دارو به بهبود حساسیت بدن به انسولین کمک کرده و میزان قند تولیدی کبد را کاهش می‌دهد.',
                'generic_name': 'متفورمین (Metformin)',
                'brand': 'داروسازی آریا',
                'dosage_form': 'قرص روکش‌دار (Tablet)',
                'dosage_strength': '۵۰۰ میلی‌گرم',
                'usage_instructions': 'دوز دقیق توسط پزشک تعیین می‌شود. معمولا ۱ یا ۲ قرص در روز همراه یا بعد از وعده غذایی اصلی جهت کاهش عوارض گوارشی.',
                'warnings': 'نیازمند نسخه معتبر پزشک. در بیماران کلیوی و قلبی شدید نیاز به پایش مداوم دارد. مصرف الکل همزمان با این دارو خطر اسیدوز لاکتیک را به شدت افزایش می‌دهد.',
                'is_prescription_required': True,
                'image_path': 'products/otc-medicine.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'کیفیت خوبی داره. همیشه از این برند استفاده می‌کنم و قند خونم کاملا تنظییه.', 'is_verified': True}
                ]
            },
            {
                'slug': 'alprazolam-0-5',
                'name': 'قرص آلپرازولام ۰.۵ میلی‌گرم سبحان دارو (نسخه‌ای)',
                'category_slug': 'prescription',
                'price': 95000,
                'badge': None,
                'description': 'داروی آرام‌بخش و ضد اضطراب از گروه بنزودیازپین‌ها. برای درمان اختلال اضطراب، حملات پانیک و اختلالات خواب ناشی از اضطراب تجویز می‌شود.',
                'generic_name': 'آلپرازولام (Alprazolam)',
                'brand': 'سبحان دارو',
                'dosage_form': 'قرص (Tablet)',
                'dosage_strength': '۰.۵ میلی‌گرم',
                'usage_instructions': 'دقیقاً طبق دستور پزشک مصرف شود. معمولا ۱ قرص شب‌ها قبل از خواب یا دوزهای منقسم در روز.',
                'warnings': 'خرید صرفاً با نسخه پزشک. این دارو پتانسیل بالایی برای وابستگی و اعتیاد دارد. از قطع ناگهانی دارو بدون مشورت پزشک خودداری کنید. ایجاد خواب‌آلودگی شدید.',
                'is_prescription_required': True,
                'image_path': 'products/otc-medicine.jpg',
                'reviews': [
                    {'rating': 4, 'comment': 'برای اضطراب فوق‌العاده‌ست اما به نظرم فقط باید در شرایط بحرانی خورد چون خیلی اعتیادآوره.', 'is_verified': True}
                ]
            },
            {
                'slug': 'amoxicillin-500',
                'name': 'کپسول آموکسی‌سیلین ۵۰۰ میلی‌گرم جابرابن‌حیان (نسخه‌ای)',
                'category_slug': 'prescription',
                'price': 120000,
                'badge': None,
                'description': 'آنتی‌بیوتیک از خانواده پنی‌سیلین‌ها، موثر در درمان طیف وسیعی از عفونت‌های باکتریایی مانند عفونت‌های گوش، گلو، سینوس‌ها، مجاری ادراری و پوست.',
                'generic_name': 'آموکسی‌سیلین (Amoxicillin)',
                'brand': 'داروسازی جابر ابن حیان',
                'dosage_form': 'کپسول (Capsule)',
                'dosage_strength': '۵۰۰ میلی‌گرم',
                'usage_instructions': 'معمولاً هر ۸ ساعت ۱ کپسول با مقدار کافی آب. دوره درمان باید به طور کامل به پایان برسد، حتی اگر علائم بیماری زودتر بهبود یابد.',
                'warnings': 'تحویل فقط با ارائه نسخه پزشک. در صورت سابقه حساسیت به پنی‌سیلین‌ها یا سفالوسپورین‌ها پزشک خود را مطلع کنید.',
                'is_prescription_required': True,
                'image_path': 'products/otc-medicine.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'برای عفونت گلو دکتر تجویز کرد و بعد از ۳ روز کاملا خوب شدم. نسخه رو راحت آپلود کردم و تایید شد.', 'is_verified': True}
                ]
            },
            {
                'slug': 'salbutamol-inhaler',
                'name': 'اسپری سالبوتامول ۱۰۰ میکروگرم گلکسو (نسخه‌ای)',
                'category_slug': 'prescription',
                'price': 340000,
                'badge': None,
                'description': 'اسپری تنفسی (اینکالر) گشادکننده برونش سریع‌الاثر. برای پیشگیری و درمان تنگی نفس و خس‌خس سینه ناشی از آسم، برونشیت مزمن و ورزش.',
                'generic_name': 'سالبوتامول (Salbutamol)',
                'brand': 'GlaxoSmithKline',
                'dosage_form': 'اسپری استنشاقی (Inhaler)',
                'dosage_strength': '۱۰۰ میکروگرم در هر پاف',
                'usage_instructions': 'در هنگام حملات آسم، ۱ تا ۲ پاف استنشاق شود. حتماً قبل از استفاده اسپری را به خوبی تکان دهید.',
                'warnings': 'نیازمند نسخه پزشک. مصرف بیش از حد مجاز ممکن است باعث لرزش دست، تپش قلب و اضطراب شود.',
                'is_prescription_required': True,
                'image_path': 'products/otc-medicine.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'تنها اسپری تنفسی که سرفه و تنگی نفسم رو سریع متوقف می‌کنه. برند اصلی و خیلی باکیفیته.', 'is_verified': True}
                ]
            },
            {
                'slug': 'atorvastatin-20',
                'name': 'قرص آتورواستاتین ۲۰ میلی‌گرم دکتر عبیدی (نسخه‌ای)',
                'category_slug': 'prescription',
                'price': 115000,
                'badge': None,
                'description': 'داروی کاهنده چربی خون از گروه استاتین‌ها. این دارو با مهار آنزیم تولیدکننده کلسترول در کبد، کلسترول بد (LDL) را کاهش و کلسترول خوب (HDL) را افزایش می‌دهد.',
                'generic_name': 'آتورواستاتین (Atorvastatin)',
                'brand': 'داروسازی دکتر عبیدی',
                'dosage_form': 'قرص روکش‌دار (Tablet)',
                'dosage_strength': '۲۰ میلی‌گرم',
                'usage_instructions': 'معمولاً ۱ قرص در روز، ترجیحاً شب‌ها همراه یا بدون غذا طبق دستور پزشک.',
                'warnings': 'فروش فقط با نسخه پزشک. در صورت بروز درد یا ضعف عضلانی ناگهانی، فوراً به پزشک مراجعه کنید. مصرف در دوران بارداری اکیداً ممنوع است.',
                'is_prescription_required': True,
                'image_path': 'products/otc-medicine.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'برای چربی خون بالا مصرف می‌کنم و تا الان عوارضی نداشته و آزمایشم خیلی بهتر شده.', 'is_verified': True}
                ]
            },

            # 3. Supplements (مکمل‌ها)
            {
                'slug': 'multivitamin-daily-active',
                'name': 'کپسول مولتی‌ویتامین دیلی اکتیو ویتابیوتیکس',
                'category_slug': 'supplements',
                'price': 295000,
                'old_price': 350000,
                'badge': 'bestseller',
                'description': 'فرمولاسیون کامل حاوی ویتامین‌های گروه B، C، A، D3، روی، آهن و عصاره جینسینگ برای افزایش سطح انرژی روزانه، تقویت سیستم ایمنی و سلامت عمومی بدن.',
                'generic_name': 'مولتی‌ویتامین و مینرال روزانه',
                'brand': 'Vitabiotics',
                'dosage_form': 'کپسول (Capsule)',
                'dosage_strength': '۳۰ عددی',
                'usage_instructions': 'روزانه ۱ کپسول بعد از صبحانه همراه با یک لیوان آب مصرف شود.',
                'warnings': 'از مصرف همزمان با سایر مکمل‌های حاوی آهن یا ویتامین A خودداری کنید. در دوران بارداری مشورت با پزشک لازم است.',
                'is_prescription_required': False,
                'image_path': 'products/vitamin-d3-supplement.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'جنسینگ توش واقعا باعث افزایش انرژی روزانه میشه، عالیه.', 'is_verified': True},
                    {'rating': 4, 'comment': 'کیفیت خیلی بالایی داره و ساخت انگلیسه. من راضی‌ام.', 'is_verified': True}
                ]
            },
            {
                'slug': 'vitamin-d3-5000',
                'name': 'سافت‌ژل ویتامین D3 ۵۰۰۰ واحد زهراوی',
                'category_slug': 'supplements',
                'price': 285000,
                'old_price': 320000,
                'badge': 'sale',
                'description': 'مکمل ویتامین D3 با جذب بالا، بسیار مفید جهت درمان کمبود شدید ویتامین دی، کمک به جذب کلسیم، حفظ سلامت استخوان‌ها و تقویت سیستم دفاعی بدن.',
                'generic_name': 'کوله کلسیفرول (Cholecalciferol)',
                'brand': 'داروسازی زهراوی',
                'dosage_form': 'کپسول نرم ژلاتینی (Softgel)',
                'dosage_strength': '۵۰۰۰ واحد بین‌المللی',
                'usage_instructions': 'طبق دستور پزشک یا معمولا ۱ کپسول به صورت هفتگی یا ماهیانه همراه با وعده غذایی چرب مصرف شود.',
                'warnings': 'از مصرف بیش از حد مجاز خودداری کنید زیرا باعث مسمومیت و رسوب کلسیم در کلیه و عروق می‌شود.',
                'is_prescription_required': False,
                'image_path': 'products/vitamin-d3-supplement.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'دوز ۵۰۰۰ رو دکتر برام نوشته بود، بعد از دو ماه آزمایش دادم و کمبود ویتامین دی بدنم کاملا رفع شد.', 'is_verified': True}
                ]
            },
            {
                'slug': 'protein-isolate-900',
                'name': 'پودر پروتئین ایزوله وی کارن ۹۰۰ گرمی',
                'category_slug': 'supplements',
                'price': 1250000,
                'badge': 'popular',
                'description': 'پروتئین وی خالص شده به روش فیلتراسیون پیشرفته، حاوی درصد بسیار بالا پروتئین، اسیدهای آمینه شاخه‌دار (BCAA) و فاقد لاکتوز. مناسب برای عضله‌سازی و بازسازی عضلانی.',
                'generic_name': 'پروتئین وی ایزوله (Whey Protein Isolate)',
                'brand': 'صنایع دارویی کارن',
                'dosage_form': 'پودر (Powder)',
                'dosage_strength': '۹۰۰ گرم - طعم شکلاتی',
                'usage_instructions': '۱ پیمانه (۳۰ گرم) را در ۲۵۰ میلی‌لیتر آب یا شیر حل کرده و بلافاصله بعد از تمرین یا صبح ناشتا میل کنید.',
                'warnings': 'در افراد مبتلا به نارسایی کلیوی و کبدی مصرف نشود. همراه با آب فراوان مصرف گردد.',
                'is_prescription_required': False,
                'image_path': 'products/vitamin-d3-supplement.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'حلالیت فوق‌العاده و طعم شکلاتی خیلی خوبی داره. از نظر هضم هم عالیه.', 'is_verified': True}
                ]
            },
            {
                'slug': 'calcium-d-karen',
                'name': 'قرص کلسیم دی کارن ۵۰ عددی',
                'category_slug': 'supplements',
                'price': 180000,
                'old_price': 210000,
                'badge': 'sale',
                'description': 'کلسیم کربنات همراه با ویتامین D3 جهت جذب بالاتر. مناسب برای حفظ سلامت استخوان‌ها و دندان‌ها، پیشگیری از پوکی استخوان و تامین نیاز کلسیم روزانه.',
                'generic_name': 'کلسیم + ویتامین دی (Calcium + Vitamin D3)',
                'brand': 'صنایع دارویی کارن',
                'dosage_form': 'قرص (Tablet)',
                'dosage_strength': '۵۰۰ میلی‌گرم کلسیم / ۲۰۰ واحد دی',
                'usage_instructions': 'روزانه ۱ تا ۲ قرص بعد از غذا همراه با یک لیوان آب مصرف شود.',
                'warnings': 'در بیماران مبتلا به سنگ کلیه کلسیمی با احتیاط مصرف شود. با مکمل‌های آهن و آنتی‌بیوتیک‌ها فاصله زمانی ۲ ساعته داشته باشد.',
                'is_prescription_required': False,
                'image_path': 'products/vitamin-d3-supplement.jpg',
                'reviews': [
                    {'rating': 4, 'comment': 'برای درد زانو مادرم خریدم، خوب بوده. قرص‌هاش یکم بزرگه ولی مشکلی نیست.', 'is_verified': True}
                ]
            },
            {
                'slug': 'vitamin-c-effervescent',
                'name': 'قرص جوشان ویتامین C ۱۰۰۰ میلی‌گرم های‌سلامت',
                'category_slug': 'supplements',
                'price': 98000,
                'badge': 'new',
                'description': 'قرص جوشان با طعم پرتقالی دلپذیر، سرشار از ویتامین سی آنتی‌اکسیدان قوی. کمک به کلاژن‌سازی، بهبود سریع زخم‌ها، پیشگیری و بهبود سرماخوردگی.',
                'generic_name': 'اسید اسکوربیک (Ascorbic Acid)',
                'brand': 'های سلامت (Hi Health)',
                'dosage_form': 'قرص جوشان (Effervescent Tablet)',
                'dosage_strength': '۱۰۰۰ میلی‌گرم',
                'usage_instructions': 'روزانه ۱ قرص را در یک لیوان آب حل کرده و پس از انحلال کامل میل کنید.',
                'warnings': 'در صورت ابتلا به سنگ کلیه اگزالاتی یا فاویسم، قبل از مصرف با پزشک مشورت کنید.',
                'is_prescription_required': False,
                'image_path': 'products/vitamin-d3-supplement.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'طعم خیلی خوبی داره و سریع حل میشه. برای مواقعی که سرماخوردگی شروع میشه عالیه.', 'is_verified': True}
                ]
            },

            # 4. Skin & Hair (پوست و مو)
            {
                'slug': 'retinol-serum-30',
                'name': 'سرم ضد چروک رتینول ۰.۲٪ در اسکوالان اوردینری ۳۰ml',
                'category_slug': 'skincare',
                'price': 890000,
                'old_price': 980000,
                'badge': 'new',
                'description': 'سرم جوانساز و ضد پیری رتینول (مشتق ویتامین A) با غلظت ۰.۲٪ جهت کاهش چین و چروک‌های ریز، لک‌های ناشی از آفتاب و بهبود بافت و رنگ پوست.',
                'generic_name': 'رتینول در اسکوالان (Retinol 0.2%)',
                'brand': 'The Ordinary',
                'dosage_form': 'سرم پوستی (Serum)',
                'dosage_strength': '۰.۲ درصد - ۳۰ میلی‌لیتر',
                'usage_instructions': 'شب‌ها چند قطره روی پوست تمیز و خشک صورت بمالید. حتما صبح روز بعد از ضدآفتاب استفاده کنید.',
                'warnings': 'در ابتدای دوره ممکن است باعث قرمزی، پوسته پوسته شدن و حساسیت شود. در دوران بارداری یا شیردهی مصرف نشود.',
                'is_prescription_required': False,
                'image_path': 'products/retinol-serum.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'بعد از یک ماه استفاده منظم، لک‌های پوستی صورتنم خیلی کمرنگ‌تر شده.', 'is_verified': True},
                    {'rating': 4, 'comment': 'کمی چربه ولی اسکوالان داخلش برای پوست‌های خشک خیلی عالیه.', 'is_verified': True}
                ]
            },
            {
                'slug': 'hair-shampoo-400',
                'name': 'شامپو تقویت‌کننده و ضد ریزش مو کافئین آلپسین',
                'category_slug': 'skincare',
                'price': 195000,
                'old_price': 240000,
                'badge': 'sale',
                'description': 'شامپو تخصصی حاوی کمپلکس فعال کافئین، بیوتین و کراتین. کافئین با نفوذ به فولیکول‌های مو، چرخه رشد مو را تحریک کرده و از ریزش ارثی و هورمونی جلوگیری می‌کند.',
                'generic_name': 'شامپو تقویت‌کننده کافئین',
                'brand': 'Alpecin',
                'dosage_form': 'شامپو مایع (Liquid Shampoo)',
                'dosage_strength': '۲۵۰ میلی‌لیتر',
                'usage_instructions': 'موها را خیس کرده، مقدار مناسبی از شامپو را ماساژ دهید و اجازه دهید کف آن حداقل ۲ دقیقه روی پوست سر بماند، سپس آبکشی کنید.',
                'warnings': 'فقط جهت مصرف خارجی. از تماس با چشم‌ها خودداری شود.',
                'is_prescription_required': False,
                'image_path': 'products/retinol-serum.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'بهترین شامپو ضد ریزش، واقعا ریزش موهامو بعد از دو هفته خیلی کم کرد.', 'is_verified': True}
                ]
            },
            {
                'slug': 'sunscreen-lafarrerr-dry',
                'name': 'کرم ضد آفتاب و ضد لک بی‌رنگ لافارر SPF50 مخصوص پوست چرب',
                'category_slug': 'skincare',
                'price': 485000,
                'old_price': 540000,
                'badge': 'popular',
                'description': 'کرم ضد آفتاب و ضد لک فوق‌العاده سبک با فرمولاسیون فاقد چربی و مات‌کننده. حاوی عصاره گیاهان شیرین‌بیان و بیربری جهت پیشگیری و رفع لک‌های پوستی.',
                'generic_name': 'کرم ضد آفتاب ضد لک',
                'brand': 'Lafarrerr',
                'dosage_form': 'کرم پوستی (Cream)',
                'dosage_strength': 'SPF 50+ - ۴۰ میلی‌لیتر',
                'usage_instructions': '۱۵ دقیقه قبل از قرار گرفتن در معرض آفتاب روی پوست بمالید و هر ۲ تا ۳ ساعت یکبار تمدید کنید.',
                'warnings': 'از مالیدن کرم به دور چشم‌ها خودداری شود. در صورت بروز هرگونه حساسیت مصرف را قطع کنید.',
                'is_prescription_required': False,
                'image_path': 'products/retinol-serum.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'بافت بسیار سبک و جذب سریع، اصلا رد سفید روی صورت باقی نمیذاره.', 'is_verified': True}
                ]
            },

            # 5. Hygiene (بهداشت فردی)
            {
                'slug': 'sensodyne-toothpaste',
                'name': 'خمیر دندان ترمیم و محافظت سنسوداین ۷۵ml',
                'category_slug': 'hygiene',
                'price': 220000,
                'badge': 'bestseller',
                'description': 'خمیردندان تخصصی برای دندان‌های حساس حاوی کلسیم مایع. این فناوری نواحی آسیب‌دیده و حساس دندان را با مواد معدنی مشابه مینای دندان پوشانده و درد ناشی از حسگرهای سرما و گرما را متوقف می‌کند.',
                'generic_name': 'خمیردندان تخصصی دندان حساس',
                'brand': 'Sensodyne',
                'dosage_form': 'خمیر دندان (Toothpaste)',
                'dosage_strength': '۷۵ میلی‌لیتر',
                'usage_instructions': 'روزانه دو بار با مسواک نرم روی دندان‌ها بکشید. بلعیده نشود.',
                'warnings': 'برای کودکان زیر ۱۲ سال بدون دستور دندان‌پزشک توصیه نمی‌شود.',
                'is_prescription_required': False,
                'image_path': 'products/retinol-serum.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'من دندونام خیلی به آب سرد حساس بود، این خمیر دندون معجزه کرد.', 'is_verified': True}
                ]
            },
            {
                'slug': 'irsha-mouthwash',
                'name': 'دهان‌شویه کامل بدون الکل ۷ در ۱ ایرشا',
                'category_slug': 'hygiene',
                'price': 75000,
                'badge': None,
                'description': 'دهان‌شویه کامل با فرمولاسیون فاقد الکل (بدون ایجاد سوزش دهان). ضد پلاک، ضد جرم، سفیدکننده ملایم، محافظت از لثه و خوشبوکننده قوی دهان.',
                'generic_name': 'دهان‌شویه بدون الکل',
                'brand': 'Irsha',
                'dosage_form': 'مایع دهان‌شویه (Mouthwash)',
                'dosage_strength': '۲۵۰ میلی‌لیتر',
                'usage_instructions': 'روزی دو بار بعد از مسواک، دهان را با یک درب پر از مایع به مدت ۳۰ ثانیه شستشو داده و بیرون بریزید.',
                'warnings': 'حداقل تا ۳۰ دقیقه بعد از مصرف دهان‌شویه، از خوردن و آشامیدن خودداری کنید. بلعیده نشود.',
                'is_prescription_required': False,
                'image_path': 'products/retinol-serum.jpg',
                'reviews': [
                    {'rating': 4, 'comment': 'چون بدون الکله اصلا دهنو نمیسوزونه. حس تازگی خوبی به دهان میده.', 'is_verified': True}
                ]
            },

            # 6. Mother & Child (مراقبت مادر و کودک)
            {
                'slug': 'nan-1-formula',
                'name': 'شیر خشک نان ۱ نستله ۴۰۰ گرمی',
                'category_slug': 'mother-child',
                'price': 178000,
                'badge': 'bestseller',
                'description': 'شیر خشک آغازین مناسب برای شیرخواران از بدو تولد تا ۶ ماهگی که با شیر مادر تغذیه نمی‌شوند. حاوی آهن، امگا ۳ و ۶، و پروبیوتیک فعال جهت سلامت گوارش نوزاد.',
                'generic_name': 'شیر خشک نوزاد',
                'brand': 'Nestle',
                'dosage_form': 'پودر (Powder)',
                'dosage_strength': '۴۰۰ گرم',
                'usage_instructions': 'طبق جدول تغذیه روی قوطی، تعداد پیمانه‌های مشخص را در آب جوشیده ولرم حل کرده و بلافاصله به نوزاد بدهید.',
                'warnings': 'آب نجوشیده یا شیشه شیر استریل نشده می‌تواند نوزاد را بیمار کند. باقی‌مانده شیر را در شیشه دور بریزید.',
                'is_prescription_required': False,
                'image_path': 'products/vitamin-d3-supplement.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'پسرم خیلی راحت این شیر خشک رو هضم می‌کنه و بهش میسازه.', 'is_verified': True}
                ]
            },
            {
                'slug': 'baby-powder-firooz',
                'name': 'پودر بچه کلاسیک فیروز ۲۰۰ گرمی',
                'category_slug': 'mother-child',
                'price': 38000,
                'badge': None,
                'description': 'پودر تالک طبیعی و استریل شده با رایحه ملایم. جاذب رطوبت اضافی پوست نوزاد، پیشگیری از عرق‌سوز شدن و اصطکاک پوستی در نواحی چین‌خورده بدن نوزاد.',
                'generic_name': 'پودر تالک بچه',
                'brand': 'فیروز (Firooz)',
                'dosage_form': 'پودر خشک (Powder)',
                'dosage_strength': '۲۰۰ گرم',
                'usage_instructions': 'پوست را کاملا تمیز و خشک کرده، پودر را به آرامی روی دست خود ریخته و سپس روی پوست کودک بمالید.',
                'warnings': 'پودر را دور از دهان و بینی نوزاد نگه دارید تا از استنشاق ریوی جلوگیری شود.',
                'is_prescription_required': False,
                'image_path': 'products/vitamin-d3-supplement.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'برند قدیمی و باکیفیت ایرانی. عطر نوستالژیک و خیلی خوبی هم داره.', 'is_verified': True}
                ]
            },

            # 7. Medical (تجهیزات پزشکی)
            {
                'slug': 'beurer-bm28-monitor',
                'name': 'فشارسنج دیجیتال بازویی بیورر مدل BM28',
                'category_slug': 'medical',
                'price': 2450000,
                'old_price': 2700000,
                'badge': 'popular',
                'description': 'دستگاه سنجش فشار خون کاملا اتوماتیک با کاف بازویی سخنگو و حافظه داخلی برای ۴ کاربر. دارای هشدار آریتمی قلبی و منبع تغذیه باتری و آداپتور.',
                'generic_name': 'دستگاه فشارسنج دیجیتال',
                'brand': 'Beurer (آلمان)',
                'dosage_form': 'دستگاه پزشکی (Device)',
                'dosage_strength': 'مدل بازویی BM28',
                'usage_instructions': 'کاف را روی بازوی چپ، ۲ سانتی‌متر بالاتر از چین آرنج ببندید. در حالت نشسته بدون صحبت کردن دکمه استارت را بزنید.',
                'warnings': 'در زمان اندازه‌گیری کاملاً آرام باشید و پاها را روی هم نیندازید. ضربه به دستگاه وارد نشود.',
                'is_prescription_required': False,
                'image_path': 'products/blood-pressure-monitor.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'سنجش‌های خیلی دقیق و منظمی داره. کار باهاش برای افراد مسن هم خیلی راحته.', 'is_verified': True},
                    {'rating': 4, 'comment': 'قیمتش بالاست ولی ارزش خرید داره. بیورر برند عالیه.', 'is_verified': True}
                ]
            },
            {
                'slug': 'accuchek-instant-glucometer',
                'name': 'دستگاه تست قند خون اکیو چک مدل Instant',
                'category_slug': 'medical',
                'price': 780000,
                'badge': 'bestseller',
                'description': 'دستگاه اندازه‌گیری قند خون سریع و دقیق با حداقل خون مورد نیاز. اتصال بلوتوثی به گوشی همراه برای پایش اطلاعات و رسم نمودارهای سلامتی.',
                'generic_name': 'دستگاه سنجش قند خون',
                'brand': 'Accu-Chek',
                'dosage_form': 'دستگاه دیجیتال',
                'dosage_strength': 'مدل Instant',
                'usage_instructions': 'نوار تست را وارد دستگاه کنید، با قلم لانست انگشت خود را سوراخ کرده و قطره خون را به انتهای نوار متصل کنید.',
                'warnings': 'نوارها را در جای خشک و خنک نگهداری کنید و بلافاصله پس از برداشتن نوار، درب قوطی را ببندید.',
                'is_prescription_required': False,
                'image_path': 'products/blood-pressure-monitor.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'دقت بسیار بالا و سرعت عالی توی نمایش نتیجه. اتصال به برنامه موبایلش هم خیلی خوب کار می‌کنه.', 'is_verified': True}
                ]
            },

            # 8. Cosmetics (آرایشی)
            {
                'slug': 'hydroderm-lip-balm',
                'name': 'بالم لب بازسازی‌کننده و ویتامینه هیدرودرم',
                'category_slug': 'cosmetics',
                'price': 54000,
                'old_price': 65000,
                'badge': 'sale',
                'description': 'بالم لب غنی شده با ویتامین A و E، روغن کالاندولا و کرچک. ترمیم‌کننده ترک‌های لب، مرطوب‌کننده قوی و محافظت در برابر خشکی هوا و باد.',
                'generic_name': 'بالم لب مرطوب‌کننده',
                'brand': 'Hydroderm',
                'dosage_form': 'ماتیک استیک (Balm)',
                'dosage_strength': '۴.۵ گرم',
                'usage_instructions': 'در طول روز در صورت احساس خشکی روی لب‌ها مالیده شود.',
                'warnings': 'دور از تابش مستقیم آفتاب و در دمای زیر ۳۰ درجه نگهداری شود.',
                'is_prescription_required': False,
                'image_path': 'products/retinol-serum.jpg',
                'reviews': [
                    {'rating': 4, 'comment': 'برای پوست لب‌های خیلی خشک و ترک‌خورده کارسازه و بوی خوبی هم داره.', 'is_verified': True}
                ]
            },
            {
                'slug': 'bioderma-micellar-water',
                'name': 'میسلار واتر پوست حساس بایودرما ۲۵۰ml',
                'category_slug': 'cosmetics',
                'price': 620000,
                'badge': 'popular',
                'description': 'محلول پاک‌کننده ملایم پوست صورت و چشم‌ها از مواد آرایشی و آلودگی‌ها بدون نیاز به آبکشی. التیام‌بخش پوست حساس و محافظ چربی طبیعی پوست.',
                'generic_name': 'محلول میسلار واتر',
                'brand': 'Bioderma',
                'dosage_form': 'محلول پاک‌کننده (Liquid)',
                'dosage_strength': '۲۵۰ میلی‌لیتر',
                'usage_instructions': 'پد پنبه‌ای را به محلول آغشته کرده و به آرامی روی پوست صورت و دور چشم بکشید تا پاک شود.',
                'warnings': 'فقط جهت مصرف خارجی. در صورت تماس مستقیم با داخل چشم با آب شستشو دهید.',
                'is_prescription_required': False,
                'image_path': 'products/retinol-serum.jpg',
                'reviews': [
                    {'rating': 5, 'comment': 'آرایش‌های ضد آب رو هم خیلی راحت پاک می‌کنه و اصلا چشم رو نمی‌سوزونه.', 'is_verified': True}
                ]
            }
        ]

        for p_data in products_data:
            cat = category_map.get(p_data['category_slug'])
            if not cat:
                self.stdout.write(f"Category {p_data['category_slug']} not found! Skipping {p_data['name']}")
                continue

            product, created = Product.objects.get_or_create(
                slug=p_data['slug'],
                defaults={
                    'name': p_data['name'],
                    'category': cat,
                    'price': p_data['price'],
                    'old_price': p_data.get('old_price'),
                    'badge': p_data['badge'],
                    'description': p_data['description'],
                    'generic_name': p_data.get('generic_name'),
                    'brand': p_data.get('brand'),
                    'dosage_form': p_data.get('dosage_form'),
                    'dosage_strength': p_data.get('dosage_strength'),
                    'usage_instructions': p_data.get('usage_instructions'),
                    'warnings': p_data.get('warnings'),
                    'is_prescription_required': p_data.get('is_prescription_required', False),
                    'quantity': random.randint(15, 120),
                    'in_stock': True,
                }
            )

            # Product Image
            ProductImage.objects.get_or_create(
                product=product,
                image=p_data['image_path'],
                defaults={'is_main': True}
            )

            # Recalculate rating and reviews based on seeded reviews
            p_reviews = p_data.get('reviews', [])
            total_rating = 0
            for idx, r_data in enumerate(p_reviews):
                user = reviewer_instances[idx % len(reviewer_instances)]
                Review.objects.create(
                    product=product,
                    user=user,
                    rating=r_data['rating'],
                    comment=r_data['comment'],
                    is_verified_purchase=r_data['is_verified']
                )
                total_rating += r_data['rating']
            
            if p_reviews:
                product.rating = round(total_rating / len(p_reviews), 1)
                product.review_count = len(p_reviews)
                product.save()
            else:
                product.rating = 4.5
                product.review_count = random.randint(3, 15)
                product.save()

        # FAQs
        self.stdout.write('Seeding FAQs...')
        faqs_data = [
            { 'q': 'آیا خرید دارو بدون نسخه از داروخانه آنلاین مجاز است؟', 'a': 'داروهای OTC (بدون نسخه) مانند مسکن‌ها، مکمل‌ها و محصولات بهداشتی بدون محدودیت قابل خرید هستند. اما داروهای نسخه‌ای نیازمند بارگذاری تصویر نسخه معتبر پزشک می‌باشند.' },
            { 'q': 'چگونه نسخه پزشک خود را جهت بررسی و ارسال دارو ارسال کنم؟', 'a': 'کافیست وارد بخش «ثبت نسخه» در منوی بالایی سایت شده، اطلاعات خود و تصویر نسخه پزشک را بارگذاری نمایید. داروسازان ما پس از بررسی نسخه با شما تماس خواهند گرفت.' },
            { 'q': 'چگونه از اصالت داروها اطمینان حاصل کنم؟', 'a': 'تمام محصولات ارائه شده در آرمان فارما از توزیع‌کنندگان مجاز و دارای پروانه معتبر سازمان غذا و دارو تامین می‌شوند و همگی دارای برچسب اصالت کالا می‌باشند.' },
            { 'q': 'مدت زمان ارسال سفارشات چقدر است؟', 'a': 'سفارشات داخل تهران توسط پیک اختصاصی در کمتر از ۴ ساعت ارسال می‌شوند. سفارشات شهرستان توسط پست پیشتاز ظرف ۲ الی ۴ روز کاری تحویل می‌گردند.' },
        ]

        for faq_data in faqs_data:
            FAQ.objects.get_or_create(question=faq_data['q'], defaults={'answer': faq_data['a']})

        # Blog
        self.stdout.write('Seeding blog...')
        blog_cats = ['مکمل‌ها', 'داروها', 'پوست و مو', 'مراقبت‌های بهداشتی']
        blog_cat_instances = {}
        for cat_name in blog_cats:
            cat, _ = BlogCategory.objects.get_or_create(name=cat_name, slug=slugify(cat_name, allow_unicode=True))
            blog_cat_instances[cat_name] = cat

        blog_posts_data = [
            {
                'slug': 'vitamin-d-guide',
                'title': 'راهنمای کامل مصرف ویتامین D3 — چه زمانی و چقدر مصرف کنیم؟',
                'category_name': 'مکمل‌ها',
                'excerpt': 'بررسی علمی دوز مناسب ویتامین D3، تداخلات دارویی، اهمیت آن در جذب کلسیم و نحوه تشخیص کمبود ویتامین D در بدن.',
                'content': 'ویتامین D3 یکی از مهم‌ترین ویتامین‌های محلول در چربی است که نقش حیاتی در حفظ سلامت استخوان‌ها، تقویت سیستم ایمنی و تنظیم کلسیم و فسفر بدن ایفا می‌کند. کمبود این ویتامین بسیار شایع است و می‌تواند منجر به پوکی استخوان، خستگی مفرط و تضعیف دفاع طبیعی بدن شود.\n\nدوز مناسب مصرف:\nبرای بزرگسالان به صورت عمومی دوز روزانه ۱۰۰۰ تا ۲۰۰۰ واحد بین‌المللی توصیه می‌شود. اما دوزهای درمانی مثل ۵۰۰۰۰ واحد باید حتماً تحت نظارت پزشک و معمولاً به صورت هفتگی یا ماهیانه مصرف شوند.\n\nبهترین زمان مصرف:\nاز آنجا که ویتامین D یک ویتامین محلول در چربی است، بهترین زمان برای مصرف آن همراه با وعده غذایی اصلی (نهار یا شام) است که حاوی چربی‌های سالم باشد تا جذب آن به حداکثر برسد.\n\nتداخلات دارویی:\nبرخی از داروهای ضد صرع و کاهش وزن ممکن است جذب ویتامین D را کاهش دهند. همواره قبل از شروع مصرف مکمل با داروساز یا پزشک مشورت کنید.',
                'read_time': 6,
                'icon': '🌿'
            },
            {
                'slug': 'retinol-skincare-routine',
                'title': 'جوانی و شادابی پوست با سرم رتینول: راهنمای گام‌به‌گام روتین شبانه',
                'category_name': 'پوست و مو',
                'excerpt': 'سرم رتینول چگونه باعث جوانسازی پوست می‌شود؟ بررسی نحوه مصرف صحیح، عوارض اولیه و نکات ضروری برای جلوگیری از حساسیت پوستی.',
                'content': 'رتینول، یکی از قوی‌ترین مشتقات ویتامین A است که به دلیل توانایی بی‌نظیرش در تسریع بازسازی سلولی، تحریک تولید کلاژن و کاهش لک‌ها و چروک‌ها شناخته می‌شود. استفاده از این ماده در روتین پوستی می‌تواند تفاوت شگرفی ایجاد کند.\n\nچگونه رتینول را شروع کنیم؟\nاگر برای اولین بار از رتینول استفاده می‌کنید، با غلظت‌های کم (مثل ۰.۲٪) شروع کنید. در هفته‌های اول فقط ۲ شب در هفته از آن استفاده کنید تا پوستتان به آن عادت کند، سپس به آرامی دفعات مصرف را افزایش دهید.\n\nمراحل روتین شبانه رتینول:\n۱. پوست خود را با یک شوینده ملایم تمیز کرده و کاملاً خشک کنید.\n۲. چند قطره سرم رتینول روی پوست بمالید (از تماس با دور چشم و لب‌ها خودداری شود).\n۳. پس از جذب، حتماً از یک کرم مرطوب‌کننده قوی استفاده کنید تا سد دفاعی پوست تقویت شود.\n\nنکته بسیار مهم:\nرتینول پوست را به شدت به نور آفتاب حساس می‌کند. بنابراین، مصرف ضد آفتاب با SPF بالا در طول روز بعد از شب‌های مصرف رتینول الزامی است.',
                'read_time': 5,
                'icon': '✨'
            },
            {
                'slug': 'metformin-diabetes-control',
                'title': 'کنترل دیابت نوع ۲ با متفورمین: مکانیسم اثر، دوز و عوارض جانبی',
                'category_name': 'داروها',
                'excerpt': 'متفورمین چگونه قند خون را تنظیم می‌کند؟ راهکارهای کاهش عوارض گوارشی و اهمیت مصرف منظم این دارو در کنترل قند خون.',
                'content': 'متفورمین خط اول درمان دارویی در دیابت نوع ۲ است. این دارو به بدن کمک می‌کند تا به انسولین تولیدی خود بهتر پاسخ دهد، قند کمتری از کبد آزاد شود و جذب قند از روده کاهش یابد.\n\nبهترین زمان مصرف متفورمین:\nشایع‌ترین عارضه متفورمین مشکلات گوارشی مانند نفخ، تهوع و اسهال است. برای کاهش این عوارض، توصیه می‌شود متفورمین را حتماً همراه یا بلافاصله بعد از غذا میل کنید. همچنین معمولاً پزشک درمان را با دوزهای پایین شروع کرده و به تدریج افزایش می‌دهد.\n\nنکات مهم در حین درمان:\n۱. پایش منظم قند خون ناشتا و تست HbA1c اهمیت زیادی دارد.\n۲. در صورت نیاز به تصویربرداری پزشکی با ماده حاجب، مصرف متفورمین باید با دستور پزشک موقتاً قطع شود.\n۳. مصرف الکل در طول درمان با متفورمین ریسک اسیدوز لاکتیک (یک وضعیت اورژانسی شدید) را به شدت بالا می‌برد.',
                'read_time': 7,
                'icon': '💊'
            },
            {
                'slug': 'otc-vs-rx-medicines',
                'title': 'تفاوت داروهای بدون نسخه (OTC) و داروهای نسخه‌ای (Rx): قوانین و ایمنی',
                'category_name': 'مراقبت‌های بهداشتی',
                'excerpt': 'کدام داروها را می‌توان بدون نسخه تهیه کرد؟ چرا برخی داروها فقط با نسخه پزشک تحویل داده می‌شوند و خطرات خوددرمانی چیست؟',
                'content': 'داروها بر اساس میزان ایمنی، پتانسیل عوارض جانبی و سوءمصرف به دو دسته کلی تقسیم می‌شوند: داروهای بدون نسخه (OTC) و داروهای نسخه‌ای (Rx).\n\nداروهای بدون نسخه (OTC):\nاین داروها شامل مسکن‌های خفیف (مانند استامینوفن و ایبوپروفن)، برخی آنتی‌هیستامین‌ها، داروهای سرماخوردگی و مکمل‌های مولتی‌ویتامین هستند. این داروها برای درمان بیماری‌های خود محدود شونده و ساده تحت نظر داروساز قابل تهیه می‌باشند.\n\nداروهای نسخه‌ای (Rx):\nداروهایی مانند آنتی‌بیوتیک‌ها، داروهای آرام‌بخش، داروهای فشار خون و دیابت جزو این دسته هستند. این داروها به دلیل نیاز به تشخیص دقیق پزشکی، پتانسیل عوارض شدید یا خطر ایجاد مقاومت دارویی (مانند آنتی‌بیوتیک‌ها) فقط با نسخه معتبر پزشک تحویل داده می‌شوند.\n\nچرا خوددرمانی با داروهای نسخه‌ای خطرناک است؟\nمصرف خودسرانه آنتی‌بیوتیک‌ها باعث ایجاد مقاومت باکتریایی شده و در آینده درمان عفونت‌های ساده را غیرممکن می‌سازد. همچنین تداخلات دارویی در خوددرمانی می‌تواند عوارض جبران‌ناپذیری بر کبد و کلیه بگذارد.',
                'read_time': 6,
                'icon': '📋'
            },
            {
                'slug': 'asthma-inhaler-guide',
                'title': 'راهنمای استفاده صحیح از اسپری‌های استنشاقی آسم (سالبوتامول)',
                'category_name': 'داروها',
                'excerpt': 'آموزش گام‌به‌گام نحوه استفاده صحیح از اسپری آسم برای اثربخشی بیشتر دارو و کاهش عوارض جانبی مانند لرزش دست و تپش قلب.',
                'content': 'اسپری‌های تنفسی مانند سالبوتامول ابزاری حیاتی برای باز کردن سریع مجاری هوایی در بیماران مبتلا به آسم و تنگی نفس هستند. با این حال، درصد زیادی از بیماران به دلیل تکنیک نادرست، مقدار کافی از دارو را دریافت نمی‌کنند.\n\nمراحل استفاده صحیح از اسپری:\n۱. اسپری را به مدت ۵ تا ۱۰ ثانیه به خوبی تکان دهید.\n۲. درپوش را بردارید و یک بازدم عمیق انجام دهید تا ریه‌ها خالی شوند.\n۳. دهانه اسپری را بین دندان‌ها قرار داده و لب‌ها را دور آن محکم ببندید.\n۴. همزمان با شروع یک دم عمیق و کند، بالای اسپری را فشار دهید تا دارو آزاد شود.\n۵. دم را تا پایان ادامه داده، سپس دهان را بسته و نفس خود را به مدت ۱۰ ثانیه حبس کنید.\n\nنکته طلایی:\nدر صورتی که پزشک دو پاف تجویز کرده است، بین پاف اول و دوم حداقل ۱ دقیقه فاصله بیندازید. همچنین در صورت استفاده از اسپری‌های حاوی کورتون، پس از مصرف حتماً دهان خود را با آب بشویید تا دچار برفک دهان نشوید.',
                'read_time': 5,
                'icon': '🫁'
            },
            {
                'slug': 'baby-formula-guide',
                'title': 'راهنمای انتخاب شیر خشک مناسب نوزاد و اصول تهیه بهداشتی آن',
                'category_name': 'مراقبت‌های بهداشتی',
                'excerpt': 'تفاوت انواع شیر خشک نوزاد، روش صحیح آماده‌سازی و استریل کردن شیشه شیر جهت پیشگیری از عفونت‌های گوارشی در نوزادان.',
                'content': 'تغذیه نوزاد در ماه‌های اولیه زندگی از اهمیت فوق‌العاده‌ای برخوردار است. اگرچه شیر مادر بهترین گزینه است، اما در صورت عدم امکان تغذیه با شیر مادر، شیر خشک‌های فرموله شده استاندارد جایگزین مناسبی هستند.\n\nانواع شیر خشک بر اساس سن نوزاد:\n- شیر خشک شماره ۱: مناسب از بدو تولد تا ۶ ماهگی.\n- شیر خشک شماره ۲: مناسب از ۶ ماهگی تا ۱ سالگی.\n- شیر خشک شماره ۳: مناسب برای کودکان بالای ۱ سال.\n\nاصول بهداشتی تهیه شیر خشک:\n۱. همیشه دست‌های خود را قبل از آماده‌سازی شیشه شیر با آب و صابون بشویید.\n۲. شیشه شیر، پستانک و حلقه‌ها را در آب جوش استریل کنید.\n۳. آب را بجوشانید و اجازه دهید تا دمای حدود ۴۰ درجه سانتی‌گراد (ولرم) خنک شود.\n۴. طبق دستور روی قوطی، دقیقاً به تعداد پیمانه‌های مشخص شده پودر اضافه کنید (رقیق یا غلیظ کردن خودسرانه شیر خشک می‌تواند به کلیه نوزاد آسیب بزند یا باعث سوءتغذیه شود).\n۵. شیشه را خوب تکان دهید و قبل از شیردهی، دمای شیر را روی پوست مچ دست خود تست کنید.',
                'read_time': 8,
                'icon': '👶'
            },
            {
                'slug': 'cholesterol-control-atorvastatin',
                'title': 'آتورواستاتین و کنترل چربی خون: زمان طلایی مصرف و عوارض عضلانی',
                'category_name': 'داروها',
                'excerpt': 'آتورواستاتین چگونه کلسترول بد را کاهش می‌دهد؟ اهمیت زمان مصرف شبانه و علائم هشداردهنده دردهای عضلانی که باید جدی گرفته شوند.',
                'content': 'کلسترول بالا یکی از عوامل اصلی بیماری‌های قلبی و عروقی است. آتورواستاتین با مهار آنزیم کلیدی تولید کلسترول در کبد، به طرز موثری میزان کلسترول مضر (LDL) را کاهش می‌دهد.\n\nچرا آتورواستاتین معمولاً شب‌ها مصرف می‌شود؟\nکبد انسان بیشترین میزان کلسترول را در طول شب و ساعات اولیه صبح سنتز می‌کند. به همین دلیل، مصرف داروهای کاهنده چربی خون در شب اثربخشی آن‌ها را به حداکثر می‌رساند.\n\nعوارض جانبی و مراقبت‌ها:\nیکی از عوارض نادر اما جدی استاتین‌ها، ایجاد دردهای عضلانی شدید (میوپاتی) است. در صورت بروز دردهای مبهم عضلانی، ضعف یا خستگی شدید غیر توجیه بدون فعالیت بدنی، فوراً پزشک خود را مطلع کنید. همچنین در طول درمان با آتورواستاتین از مصرف گریپ‌فروت خودداری کنید زیرا باعث افزایش غلظت دارو در خون و افزایش خطر عوارض جانبی می‌شود.',
                'read_time': 6,
                'icon': '❤️'
            },
            {
                'slug': 'digital-blood-pressure-monitor',
                'title': 'راهنمای کامل خرید و روش صحیح اندازه‌گیری فشار خون با دستگاه دیجیتال',
                'category_name': 'مراقبت‌های بهداشتی',
                'excerpt': 'نکات کلیدی در انتخاب دستگاه فشارسنج دیجیتال بازویی و دستورالعمل‌های لازم برای اندازه‌گیری دقیق فشار خون در منزل.',
                'content': 'کنترل فشار خون در خانه برای پیشگیری از بیماری‌های قلبی و مغزی بسیار مهم است. دستگاه‌های فشارسنج دیجیتال بازویی به دلیل کاربری آسان و دقت بالا، بهترین گزینه برای پایش خانگی هستند.\n\nاصول اندازه‌گیری صحیح فشار خون:\n۱. حداقل ۳۰ دقیقه قبل از اندازه‌گیری از مصرف چای، قهوه، سیگار و فعالیت بدنی شدید خودداری کنید.\n۲. قبل از سنجش، ۵ دقیقه در آرامش روی صندلی بنشینید و تکیه دهید.\n۳. کاف دستگاه را روی بازوی برهنه (ترجیحاً بازوی چپ)، حدود ۲ سانتی‌متر بالاتر از خم آرنج ببندید. کاف باید هم‌سطح قلب شما باشد.\n۴. در حین اندازه‌گیری صحبت نکنید، پاهای خود را روی هم نیندازید و دست خود را شل نگه دارید.\n\nتفسیر نتایج:\nفشار خون طبیعی معمولاً کمتر از ۱۲۰ روی ۸۰ میلی‌متر جیوه است. در صورت مشاهده اعداد بالاتر به صورت مستمر، از تغییر دوز داروهای خود به صورت خودسرانه پرهیز کرده و با پزشک معالج مشورت نمایید.',
                'read_time': 5,
                'icon': '🩺'
            }
        ]

        for p_data in blog_posts_data:
            cat = blog_cat_instances.get(p_data['category_name'])
            BlogPost.objects.get_or_create(
                slug=p_data['slug'],
                defaults={
                    'title': p_data['title'],
                    'category': cat,
                    'author': admin_user,
                    'excerpt': p_data['excerpt'],
                    'content': p_data['content'],
                    'read_time': p_data['read_time'],
                    'icon': p_data['icon']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded all pharmacy data!'))
