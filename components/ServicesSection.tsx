import { Code2, Palette, Globe, CreditCard, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

const services = [
  { icon: Palette, title: 'تعديل الألوان والهوية', desc: 'تغيير ألوان المتجر، الشعار، وهوية العلامة لتتناسب مع علامتك التجارية' },
  { icon: Code2, title: 'إضافة أقسام جديدة', desc: 'إضافة صفحات وميزات مخصصة حسب طبيعة مشروعك' },
  { icon: CreditCard, title: 'ربط بوابة الدفع', desc: 'دمج بوابات دفع عربية وعالمية: تبادل، Stripe، PayPal، وغيرها' },
  { icon: Globe, title: 'تهيئة الدومين والنشر', desc: 'ربط دومينك الخاص ونشر المتجر على Vercel بشكل كامل' },
];

export default function ServicesSection() {
  return (
    <section id="services" className="py-20 px-4 bg-dark-800">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <span className="text-brand-400 text-sm font-semibold tracking-widest uppercase mb-3 block">خدماتنا</span>
          <h2 className="text-4xl font-bold text-white mb-4">خدمة التعديل والتخصيص</h2>
          <p className="text-slate-400 max-w-2xl mx-auto">نقوم بتعديل المتجر الجاهز حسب احتياجاتك بالتفصيل — فقط أخبرنا بمتطلباتك</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          {services.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="bg-dark-700 rounded-2xl p-6 border border-dark-500 hover:border-brand-400/30 transition-colors">
              <div className="w-12 h-12 rounded-xl bg-brand-400/10 flex items-center justify-center mb-4">
                <Icon className="w-6 h-6 text-brand-400" />
              </div>
              <h3 className="text-white font-bold text-lg mb-2">{title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>

        <div className="text-center">
          <div className="inline-block bg-gradient-to-r from-brand-500/10 to-purple-600/10 border border-brand-400/20 rounded-2xl p-8 max-w-2xl">
            <h3 className="text-2xl font-bold text-white mb-3">جاهز للبدء معنا؟</h3>
            <p className="text-slate-400 mb-6">اشترِ متجرك الجاهز وأضف خدمة التعديل لتحصل على متجر مخصص بالكامل</p>
            <Link
              href="/#products"
              className="inline-flex items-center gap-2 bg-gradient-to-r from-brand-500 to-purple-600 text-white font-bold px-8 py-3 rounded-xl hover:opacity-90 transition-opacity"
            >
              <span>ابدأ الآن</span>
              <ArrowLeft className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
