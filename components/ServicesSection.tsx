import { Code2, Palette, Globe, CreditCard, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

const services = [
  { icon: Palette, title: 'تعديل الألوان والهوية', desc: 'تغيير ألوان المتجر، الشعار، وهوية العلامة التجارية لتتناسب مع علامتك' },
  { icon: Code2, title: 'إضافة أقسام جديدة', desc: 'إضافة صفحات وميزات مخصصة حسب طبيعة مشروعك' },
  { icon: CreditCard, title: 'ربط بوابة الدفع', desc: 'دمج بوابات دفع عربية وعالمية: تبادل، Stripe، PayPal وغيرها' },
  { icon: Globe, title: 'تهيئة الدومين والنشر', desc: 'ربط دومينك الخاص ونشر المتجر على Vercel بشكل كامل' },
];

export default function ServicesSection() {
  return (
    <section id="services" className="py-20 px-4 bg-[#0e0e1a]">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <span className="text-cyan-400 text-sm font-semibold tracking-widest uppercase mb-2 block">خدماتنا</span>
          <h2 className="text-4xl font-bold text-white mb-3">خدمة التعديل والتخصيص</h2>
          <p className="text-slate-400 max-w-xl mx-auto">نقوم بتعديل المتجر الجاهز حسب احتياجاتك بالتفصيل</p>
        </div>
        <div className="grid md:grid-cols-2 gap-6 mb-10">
          {services.map(({icon:Icon,title,desc})=>(
            <div key={title} className="bg-[#16162a] rounded-2xl p-6 border border-[#2a2a4a] hover:border-cyan-400/30 transition-colors">
              <div className="w-12 h-12 rounded-xl bg-cyan-400/10 flex items-center justify-center mb-4"><Icon className="w-6 h-6 text-cyan-400" /></div>
              <h3 className="text-white font-bold text-lg mb-2">{title}</h3>
              <p className="text-slate-400 text-sm">{desc}</p>
            </div>
          ))}
        </div>
        <div className="text-center">
          <div className="inline-block bg-gradient-to-r from-cyan-500/10 to-purple-600/10 border border-cyan-400/20 rounded-2xl p-8 max-w-2xl">
            <h3 className="text-2xl font-bold text-white mb-3">جاهز للبدء معنا؟</h3>
            <p className="text-slate-400 mb-6">اشترِ متجرك الجاهز وأضف خدمة التعديل للحصول على متجر مخصص بالكامل</p>
            <Link href="/#products" className="inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-bold px-8 py-3 rounded-xl hover:opacity-90">
              <span>ابدأ الآن</span><ArrowLeft className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
