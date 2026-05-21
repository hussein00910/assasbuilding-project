import Link from 'next/link';
import { Zap, Mail } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-[#0e0e1a] border-t border-white/5 mt-20">
      <div className="max-w-7xl mx-auto px-4 py-10">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-400 to-purple-600 flex items-center justify-center"><Zap className="w-4 h-4 text-white" /></div>
              <span className="font-bold text-white">أساس بيلدينج</span>
            </div>
            <p className="text-slate-400 text-sm">منصة احترافية لبيع المتاجر الجاهزة والقوالب الرقمية وخدمات الدعم.</p>
          </div>
          <div>
            <h3 className="text-white font-semibold mb-3">روابط سريعة</h3>
            <ul className="space-y-2 text-sm text-slate-400">
              <li><Link href="/#products" className="hover:text-cyan-400">المتاجر والقوالب</Link></li>
              <li><Link href="/#services" className="hover:text-cyan-400">خدمة التعديل</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-white font-semibold mb-3">تواصل</h3>
            <div className="flex items-center gap-2 text-slate-400 text-sm"><Mail className="w-4 h-4 text-cyan-400" /><span>support@assasbuilding.com</span></div>
          </div>
        </div>
        <div className="border-t border-white/5 pt-6 text-center text-slate-500 text-sm">
          <p>© {new Date().getFullYear()} أساس بيلدينج. جميع الحقوق محفوظة.</p>
        </div>
      </div>
    </footer>
  );
}
