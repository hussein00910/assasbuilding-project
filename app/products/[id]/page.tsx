'use client';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import { ExternalLink, ShoppingCart, Check, Zap, Download, Shield, Code2 } from 'lucide-react';
import { Product } from '@/lib/types';
import { formatPrice } from '@/lib/utils';

export default function ProductPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [includeCustomization, setIncludeCustomization] = useState(false);

  useEffect(() => {
    fetch(`/api/products/${id}`)
      .then((r) => r.json())
      .then((d) => { setProduct(d); setLoading(false); })
      .catch(() => { setLoading(false); });
  }, [id]);

  if (loading) return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-12 h-12 border-4 border-brand-400 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  if (!product) return (
    <div className="flex items-center justify-center min-h-screen text-slate-400">
      <p>المنتج غير موجود</p>
    </div>
  );

  const totalPrice = includeCustomization ? product.price + 99 : product.price;

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Left - Image & Preview */}
        <div>
          <div className="relative rounded-2xl overflow-hidden bg-dark-700 border border-dark-500 h-80 mb-4">
            {product.thumbnail_url ? (
              <Image src={product.thumbnail_url} alt={product.name_ar} fill className="object-cover" sizes="600px" />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-slate-600">
                <Code2 className="w-16 h-16" />
              </div>
            )}
          </div>

          {product.preview_url && (
            <a
              href={product.preview_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 w-full bg-dark-700 border border-dark-500 text-slate-200 font-semibold py-3 rounded-xl hover:border-brand-400/50 hover:text-brand-400 transition-all"
            >
              <ExternalLink className="w-5 h-5" />
              <span>معاينة حية - Live Demo</span>
            </a>
          )}
        </div>

        {/* Right - Details */}
        <div>
          <span className="inline-block bg-brand-400/10 text-brand-400 text-xs font-bold px-3 py-1 rounded-full mb-3">
            {{ store: 'متجر جاهز', template: 'قالب', service: 'خدمة' }[product.type] ?? product.type}
          </span>
          <h1 className="text-3xl font-extrabold text-white mb-3">{product.name_ar || product.name}</h1>
          <p className="text-slate-400 leading-relaxed mb-6">{product.description_ar || product.description}</p>

          {/* Features */}
          {product.features_ar?.length > 0 && (
            <div className="mb-6">
              <h3 className="text-white font-bold mb-3">المميزات الرئيسية</h3>
              <ul className="grid grid-cols-1 gap-2">
                {product.features_ar.map((f, i) => (
                  <li key={i} className="flex items-center gap-2 text-slate-300 text-sm">
                    <Check className="w-4 h-4 text-brand-400 shrink-0" />
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Tech Stack */}
          {product.tech_stack?.length > 0 && (
            <div className="mb-6">
              <h3 className="text-white font-bold mb-2">التقنيات المستخدمة</h3>
              <div className="flex flex-wrap gap-2">
                {product.tech_stack.map((t) => (
                  <span key={t} className="bg-dark-600 border border-dark-500 text-slate-300 text-xs px-3 py-1 rounded-lg">{t}</span>
                ))}
              </div>
            </div>
          )}

          {/* Customization Add-on */}
          <div
            onClick={() => setIncludeCustomization(!includeCustomization)}
            className={`cursor-pointer rounded-xl border-2 p-4 mb-6 transition-all ${
              includeCustomization
                ? 'border-brand-400 bg-brand-400/10'
                : 'border-dark-500 bg-dark-700 hover:border-dark-400'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className={`w-5 h-5 rounded border-2 flex items-center justify-center shrink-0 mt-0.5 transition-all ${
                includeCustomization ? 'border-brand-400 bg-brand-400' : 'border-slate-500'
              }`}>
                {includeCustomization && <Check className="w-3 h-3 text-dark-900" />}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-brand-400" />
                  <span className="text-white font-bold text-sm">إضافة خدمة التعديل والتخصيص</span>
                  <span className="text-brand-400 font-bold text-sm">+99$</span>
                </div>
                <p className="text-slate-400 text-xs mt-1">تعديل الألوان، إضافة أقسام، ربط بوابة الدفع، تهيئة الدومين — يُنفَّذ بواسطة كلاود</p>
              </div>
            </div>
          </div>

          {/* Pricing & Buy */}
          <div className="bg-dark-700 rounded-xl p-5 border border-dark-500 mb-4">
            <div className="flex items-center justify-between mb-4">
              <span className="text-slate-400">سعر المنتج</span>
              <span className="text-white font-bold">{formatPrice(product.price)}</span>
            </div>
            {includeCustomization && (
              <div className="flex items-center justify-between mb-4">
                <span className="text-slate-400">خدمة التعديل</span>
                <span className="text-white font-bold">{formatPrice(99)}</span>
              </div>
            )}
            <div className="border-t border-dark-500 pt-3 flex items-center justify-between">
              <span className="text-white font-bold">الإجمالي</span>
              <span className="text-2xl font-extrabold text-brand-400">{formatPrice(totalPrice)}</span>
            </div>
          </div>

          <button
            onClick={() => router.push(`/checkout/${id}?customization=${includeCustomization}`)}
            className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-brand-500 to-brand-400 text-dark-900 font-extrabold py-4 rounded-xl hover:opacity-90 transition-opacity text-lg"
          >
            <ShoppingCart className="w-5 h-5" />
            <span>شراء القالب الآن</span>
          </button>

          <div className="flex items-center justify-center gap-6 mt-4 text-xs text-slate-500">
            <span className="flex items-center gap-1"><Download className="w-3 h-3" /> تحميل فوري</span>
            <span className="flex items-center gap-1"><Shield className="w-3 h-3" /> كود مصدري كامل</span>
          </div>
        </div>
      </div>
    </div>
  );
}
