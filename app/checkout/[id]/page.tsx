'use client';
import { useEffect, useState } from 'react';
import { useParams, useSearchParams, useRouter } from 'next/navigation';
import { Lock, User, Mail } from 'lucide-react';
import toast from 'react-hot-toast';
import { Suspense } from 'react';

function CheckoutForm() {
  const { id } = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const withCustom = searchParams.get('customization') === 'true';
  const [product, setProduct] = useState<any>(null);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({ name: '', email: '' });

  useEffect(() => {
    fetch(`/api/products/${id}`).then(r => r.json()).then(setProduct);
  }, [id]);

  const total = product ? (withCustom ? Number(product.price) + 99 : Number(product.price)) : 0;

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await fetch('/api/purchases', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: id, customer_email: form.email, customer_name: form.name, includes_customization: withCustom }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      router.push(`/success?purchase_id=${data.purchase_id}&download=${encodeURIComponent(data.download_url)}&customization=${withCustom}`);
    } catch (err: any) {
      toast.error(err.message || 'حدث خطأ');
    } finally { setSubmitting(false); }
  }

  if (!product) return <div className="flex justify-center py-20"><div className="w-10 h-10 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin" /></div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-extrabold text-white mb-8 text-center">إتمام الشراء</h1>
      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-[#16162a] rounded-2xl p-6 border border-[#2a2a4a] h-fit">
          <h2 className="text-white font-bold text-xl mb-4">ملخص الطلب</h2>
          <div className="space-y-3 text-sm mb-4">
            <div className="flex justify-between"><span className="text-slate-400">{product.name_ar || product.name}</span><span className="text-white">${product.price}</span></div>
            {withCustom && <div className="flex justify-between"><span className="text-slate-400">خدمة التعديل</span><span className="text-white">$99</span></div>}
          </div>
          <div className="border-t border-[#2a2a4a] pt-3 flex justify-between">
            <span className="text-white font-bold">الإجمالي</span>
            <span className="text-2xl font-extrabold text-cyan-400">${total}</span>
          </div>
          <div className="mt-4 bg-[#0e0e1a] rounded-xl p-3 text-xs text-slate-400 space-y-1">
            <p>✅ تحميل فوري بعد التأكيد</p><p>✅ نسخة لبريدك الإلكتروني</p><p>✅ صلاحية 30 يوماً</p>
          </div>
        </div>
        <div className="bg-[#16162a] rounded-2xl p-6 border border-[#2a2a4a]">
          <h2 className="text-white font-bold text-xl mb-4">بياناتك</h2>
          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="block text-slate-400 text-sm mb-1">اسمك الكامل</label>
              <div className="relative"><User className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input required type="text" value={form.name} onChange={e => setForm({...form, name: e.target.value})}
                  className="w-full bg-[#0e0e1a] border border-[#2a2a4a] text-white rounded-xl px-4 py-3 pr-10 focus:outline-none focus:border-cyan-400 text-sm" /></div>
            </div>
            <div>
              <label className="block text-slate-400 text-sm mb-1">البريد الإلكتروني</label>
              <div className="relative"><Mail className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input required type="email" value={form.email} onChange={e => setForm({...form, email: e.target.value})}
                  className="w-full bg-[#0e0e1a] border border-[#2a2a4a] text-white rounded-xl px-4 py-3 pr-10 focus:outline-none focus:border-cyan-400 text-sm" /></div>
              <p className="text-xs text-slate-500 mt-1">سيصلك رابط التحميل على هذا البريد</p>
            </div>
            <div className="bg-[#0e0e1a] rounded-xl p-3 text-center text-slate-400 text-sm">الدفع عبر التحويل البنكي أو المحفظة الرقمية</div>
            <button type="submit" disabled={submitting}
              className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-cyan-500 to-cyan-400 text-gray-900 font-extrabold py-4 rounded-xl hover:opacity-90 disabled:opacity-60">
              {submitting ? <div className="w-5 h-5 border-2 border-gray-900 border-t-transparent rounded-full animate-spin" /> : <><Lock className="w-5 h-5" />تأكيد الطلب وتحميل</>}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default function CheckoutPage() {
  return <Suspense fallback={<div className="flex justify-center py-20"><div className="w-10 h-10 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin" /></div>}><CheckoutForm /></Suspense>;
}
