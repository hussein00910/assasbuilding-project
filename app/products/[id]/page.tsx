'use client';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import { ExternalLink, ShoppingCart, Check, Download, Shield, Zap } from 'lucide-react';

export default function ProductPage() {
  const { id } = useParams();
  const router = useRouter();
  const [product, setProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [withCustom, setWithCustom] = useState(false);

  useEffect(() => {
    fetch(`/api/products/${id}`).then(r => r.json()).then(d => { setProduct(d); setLoading(false); }).catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="flex items-center justify-center min-h-screen"><div className="w-10 h-10 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin" /></div>;
  if (!product || product.error) return <div className="text-center py-20 text-slate-400">المنتج غير موجود</div>;

  const total = withCustom ? Number(product.price) + 99 : Number(product.price);
  const typeMap: Record<string,string> = { store: 'متجر جاهز', template: 'قالب', service: 'خدمة' };

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <div>
          <div className="relative rounded-2xl overflow-hidden bg-[#16162a] border border-[#2a2a4a] h-72 mb-4">
            {product.thumbnail_url
              ? <Image src={product.thumbnail_url} alt={product.name_ar || product.name} fill className="object-cover" sizes="600px" />
              : <div className="w-full h-full flex items-center justify-center text-slate-600 text-6xl">🖼️</div>}
          </div>
          {product.preview_url && (
            <a href={product.preview_url} target="_blank" rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 w-full bg-[#16162a] border border-[#2a2a4a] text-slate-200 font-semibold py-3 rounded-xl hover:border-cyan-400/50 hover:text-cyan-400 transition-all">
              <ExternalLink className="w-5 h-5" /><span>معاينة حية — Live Demo</span>
            </a>
          )}
        </div>

        <div>
          <span className="inline-block bg-cyan-400/10 text-cyan-400 text-xs font-bold px-3 py-1 rounded-full mb-3">{typeMap[product.type] ?? product.type}</span>
          <h1 className="text-3xl font-extrabold text-white mb-3">{product.name_ar || product.name}</h1>
          <p className="text-slate-400 leading-relaxed mb-6">{product.description_ar || product.description}</p>

          {Array.isArray(product.features_ar) && product.features_ar.length > 0 && (
            <ul className="mb-6 space-y-2">
              {product.features_ar.map((f: string, i: number) => (
                <li key={i} className="flex items-center gap-2 text-slate-300 text-sm"><Check className="w-4 h-4 text-cyan-400 shrink-0" />{f}</li>
              ))}
            </ul>
          )}

          <div onClick={() => setWithCustom(!withCustom)}
            className={`cursor-pointer rounded-xl border-2 p-4 mb-5 transition-all ${withCustom ? 'border-cyan-400 bg-cyan-400/10' : 'border-[#2a2a4a] bg-[#16162a] hover:border-[#3a3a5a]'}`}>
            <div className="flex items-center gap-3">
              <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${withCustom ? 'border-cyan-400 bg-cyan-400' : 'border-slate-500'}`}>
                {withCustom && <Check className="w-3 h-3 text-gray-900" />}
              </div>
              <Zap className="w-4 h-4 text-cyan-400" />
              <span className="text-white font-bold text-sm">إضافة خدمة التعديل والتخصيص</span>
              <span className="text-cyan-400 font-bold text-sm mr-auto">+99$</span>
            </div>
            <p className="text-slate-400 text-xs mt-2 mr-8">تعديل الألوان، إضافة أقسام، ربط بوابة دفع، تهيئة الدومين</p>
          </div>

          <div className="bg-[#16162a] rounded-xl p-5 border border-[#2a2a4a] mb-4">
            <div className="flex justify-between mb-3"><span className="text-slate-400">سعر المنتج</span><span className="text-white font-bold">${product.price}</span></div>
            {withCustom && <div className="flex justify-between mb-3"><span className="text-slate-400">خدمة التعديل</span><span className="text-white font-bold">$99</span></div>}
            <div className="border-t border-[#2a2a4a] pt-3 flex justify-between">
              <span className="text-white font-bold">الإجمالي</span>
              <span className="text-2xl font-extrabold text-cyan-400">${total}</span>
            </div>
          </div>

          <button onClick={() => router.push(`/checkout/${id}?customization=${withCustom}`)}
            className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-cyan-500 to-cyan-400 text-gray-900 font-extrabold py-4 rounded-xl hover:opacity-90 transition-opacity text-lg mb-3">
            <ShoppingCart className="w-5 h-5" />شراء القالب الآن
          </button>
          <div className="flex justify-center gap-6 text-xs text-slate-500">
            <span className="flex items-center gap-1"><Download className="w-3 h-3" />تحميل فوري</span>
            <span className="flex items-center gap-1"><Shield className="w-3 h-3" />كود مصدري كامل</span>
          </div>
        </div>
      </div>
    </div>
  );
}
