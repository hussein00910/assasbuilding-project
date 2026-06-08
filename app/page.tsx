'use client';
import { useEffect, useState } from 'react';
import ProductCard from '@/components/ProductCard';
import HeroSection from '@/components/HeroSection';
import ServicesSection from '@/components/ServicesSection';

interface Product {
  id: string; name: string; name_ar: string; description: string; description_ar: string;
  price: number; type: string; preview_url: string; thumbnail_url: string;
  features_ar: string[]; tech_stack: string[];
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetch('/api/products').then(r => r.json()).then(d => { setProducts(Array.isArray(d) ? d : []); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const filtered = filter === 'all' ? products : products.filter(p => p.type === filter);

  return (
    <div>
      <HeroSection />
      <section className="py-6 px-4 border-y border-white/5">
        <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          {[{v:'+50',l:'منتج جاهز'},{v:'+200',l:'عميل سعيد'},{v:'24سا',l:'دعم فني'},{v:'100%',l:'ضمان الجودة'}].map(s=>(
            <div key={s.l}><div className="text-3xl font-extrabold gradient-text mb-1">{s.v}</div><div className="text-slate-400 text-sm">{s.l}</div></div>
          ))}
        </div>
      </section>

      <section id="products" className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-10">
            <span className="text-cyan-400 text-sm font-semibold tracking-widest uppercase mb-2 block">منتجاتنا</span>
            <h2 className="text-4xl font-bold text-white mb-3">المتاجر والقوالب الجاهزة</h2>
            <p className="text-slate-400 max-w-xl mx-auto">ابدأ مشروعك اليوم بأحد متاجرنا المتكاملة أو قوالبنا الاحترافية</p>
          </div>
          <div className="flex justify-center gap-3 mb-8 flex-wrap">
            {[{v:'all',l:'الكل'},{v:'store',l:'متاجر'},{v:'template',l:'قوالب'},{v:'service',l:'خدمات'}].map(({v,l})=>(
              <button key={v} onClick={()=>setFilter(v)} className={`px-5 py-2 rounded-full text-sm font-semibold transition-all ${filter===v?'bg-cyan-400 text-gray-900':'bg-[#16162a] text-slate-300 border border-[#2a2a4a] hover:border-cyan-400/40'}`}>{l}</button>
            ))}
          </div>
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1,2,3].map(i=><div key={i} className="bg-[#16162a] rounded-2xl h-80 animate-pulse" />)}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filtered.map(p=><ProductCard key={p.id} product={p} />)}
              {filtered.length===0 && <div className="col-span-3 text-center text-slate-500 py-16">لا توجد منتجات في هذه الفئة</div>}
            </div>
          )}
        </div>
      </section>
      <ServicesSection />
    </div>
  );
}
