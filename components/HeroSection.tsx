import Link from 'next/link';
import { ArrowLeft, Star, Download, Shield } from 'lucide-react';

export default function HeroSection() {
  return (
    <section className="relative overflow-hidden py-24 px-4">
      {/* Background glow */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-brand-400/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl" />
      </div>

      <div className="max-w-4xl mx-auto text-center relative z-10">
        <div className="inline-flex items-center gap-2 bg-brand-400/10 border border-brand-400/20 rounded-full px-4 py-1.5 mb-6">
          <Star className="w-4 h-4 text-brand-400" />
          <span className="text-brand-400 text-sm font-medium">منتجات رقمية جاهزة للتحميل الفوري</span>
        </div>

        <h1 className="text-5xl md:text-6xl font-extrabold text-white leading-tight mb-6">
          ابدأ متجرك الإلكتروني
          <br />
          <span className="gradient-text">في دقائق لا أشهر</span>
        </h1>

        <p className="text-xl text-slate-400 mb-10 leading-relaxed max-w-2xl mx-auto">
          احصل على متجر إلكتروني متكامل بكود مصدري كامل، جاهز للتخصيص والنشر فوراً
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <Link
            href="/#products"
            className="flex items-center justify-center gap-2 bg-gradient-to-r from-brand-500 to-brand-400 text-dark-900 font-bold px-8 py-4 rounded-xl hover:opacity-90 transition-opacity text-lg"
          >
            <span>استعرض المنتجات</span>
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <Link
            href="/#services"
            className="flex items-center justify-center gap-2 bg-dark-700 border border-dark-500 text-white font-bold px-8 py-4 rounded-xl hover:bg-dark-600 transition-colors text-lg"
          >
            <span>خدمة التعديل</span>
          </Link>
        </div>

        <div className="flex items-center justify-center gap-8 text-sm text-slate-400 flex-wrap">
          <div className="flex items-center gap-2"><Download className="w-4 h-4 text-brand-400" /><span>تحميل فوري بعد الشراء</span></div>
          <div className="flex items-center gap-2"><Shield className="w-4 h-4 text-brand-400" /><span>دعم فني متوفر</span></div>
          <div className="flex items-center gap-2"><Star className="w-4 h-4 text-brand-400" /><span>كود نظيف واحترافي</span></div>
        </div>
      </div>
    </section>
  );
}
