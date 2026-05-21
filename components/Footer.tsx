import Link from 'next/link';
import { Zap, Mail, MessageCircle } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-dark-800 border-t border-white/5 mt-20">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-400 to-purple-600 flex items-center justify-center">
                <Zap className="w-4 h-4 text-white" />
              </div>
              <span className="font-bold text-white">أساس بيلدينج</span>
            </div>
            <p className="text-slate-400 text-sm leading-relaxed">منصة احترافية لبيع المتاجر الجاهزة والقوالب الرقمية وخدمات الدعم الفني.</p>
          </div>
          <div>
            <h3 className="text-white font-semibold mb-4">روابط سريعة</h3>
            <ul className="space-y-2 text-sm text-slate-400">
              <li><Link href="/#products" className="hover:text-brand-400 transition-colors">المتاجر والقوالب</Link></li>
              <li><Link href="/#services" className="hover:text-brand-400 transition-colors">خدمة التعديل</Link></li>
              <li><Link href="/contact" className="hover:text-brand-400 transition-colors">تواصل معنا</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-white font-semibold mb-4">تواصل</h3>
            <ul className="space-y-2 text-sm text-slate-400">
              <li className="flex items-center gap-2"><Mail className="w-4 h-4 text-brand-400" /><span>support@assasbuilding.com</span></li>
              <li className="flex items-center gap-2"><MessageCircle className="w-4 h-4 text-brand-400" /><span>واتساب: +966 5X XXX XXXX</span></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-white/5 pt-6 text-center text-slate-500 text-sm">
          <p>© {new Date().getFullYear()} أساس بيلدينج. جميع الحقوق محفوظة.</p>
        </div>
      </div>
    </footer>
  );
}
