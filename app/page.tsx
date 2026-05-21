'use client';
import { useEffect, useState } from 'react';
import { Product } from '@/lib/types';
import ProductCard from '@/components/ProductCard';
import HeroSection from '@/components/HeroSection';
import ServicesSection from '@/components/ServicesSection';
import StatsSection from '@/components/StatsSection';

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    fetch('/api/products')
      .then((r) => r.json())
      .then((data) => { setProducts(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const filtered = filter === 'all' ? products : products.filter((p) => p.type === filter);

  return (
    <div>
      <HeroSection />
      <StatsSection />

      {/* Products Section */}
      <section id="products" className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-brand-400 text-sm font-semibold tracking-widest uppercase mb-3 block">منتجاتنا</span>
            <h2 className="text-4xl font-bold text-white mb-4">المتاجر والقوالب الجاهزة</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">ابدأ مشروعك اليوم بأحد متاجرنا المتكاملة أو قوالبنا الاحترافية — جاهزة للنشر فور الشراء</p>
          </div>

          {/* Filter Tabs */}
          <div className="flex justify-center gap-3 mb-10 flex-wrap">
            {[{v:'all',l:'الكل'},{v:'store',l:'متاجر'},{v:'template',l:'قوالب'},{v:'service',l:'خدمات'}].map(({v,l})=>(
              <button
                key={v}
                onClick={() => setFilter(v)}
                className={`px-6 py-2.5 rounded-full text-sm font-semibold transition-all ${
                  filter === v
                    ? 'bg-brand-400 text-dark-900'
                    : 'bg-dark-700 text-slate-300 hover:bg-dark-600 border border-dark-500'
                }`}
              >{l}</button>
            ))}
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1,2,3].map((i) => (
                <div key={i} className="bg-dark-700 rounded-2xl h-80 animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filtered.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
              {filtered.length === 0 && (
                <div className="col-span-3 text-center text-slate-500 py-16">
                  <p className="text-xl">لا توجد منتجات في هذه الفئة</p>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      <ServicesSection />
    </div>
  );
}
