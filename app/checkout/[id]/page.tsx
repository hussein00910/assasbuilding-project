'use client';
import { useEffect, useState } from 'react';
import { useParams, useSearchParams, useRouter } from 'next/navigation';
import { Product } from '@/lib/types';
import { formatPrice } from '@/lib/utils';
import { ShoppingCart, Lock, User, Mail } from 'lucide-react';
import toast from 'react-hot-toast';

export default function CheckoutPage() {
  const { id } = useParams<{ id: string }>();
  const searchParams = useSearchParams();
  const router = useRouter();
  const includeCustomization = searchParams.get('customization') === 'true';

  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({ name: '', email: '' });

  useEffect(() => {
    fetch(`/api/products/${id}`)
      .then((r) => r.json())
      .then((d) => { setProduct(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [id]);

  const totalPrice = product ? (includeCustomization ? product.price + 99 : product.price) : 0;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!product) return;
    setSubmitting(true);

    try {
      const res = await fetch('/api/purchases', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: id,
          customer_email: form.email,
          customer_name: form.name,
          includes_customization: includeCustomization,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error);

      router.push(`/success?purchase_id=${data.purchase_id}&download=${encodeURIComponent(data.download_url)}&customization=${includeCustomization}`);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'حدث خطأ';
      toast.error(message);
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-10 h-10 border-4 border-brand-400 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  if (!product) return null;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-extrabold text-white mb-8 text-center">إتمام الشراء</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Order Summary */}
        <div className="bg-dark-700 rounded-2xl p-6 border border-dark-500 h-fit">
          <h2 className="text-white font-bold text-xl mb-5">ملخص الطلب</h2>
          <div className="space-y-3 mb-5">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">{product.name_ar}</span>
              <span className="text-white font-semibold">{formatPrice(product.price)}</span>
            </div>
            {includeCustomization && (
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">خدمة التعديل والتخصيص</span>
                <span className="text-white font-semibold">{formatPrice(99)}</span>
              </div>
            )}
          </div>
          <div className="border-t border-dark-500 pt-4 flex justify-between">
            <span className="text-white font-bold">الإجمالي</span>
            <span className="text-2xl font-extrabold text-brand-400">{formatPrice(totalPrice)}</span>
          </div>

          <div className="mt-6 bg-dark-800 rounded-xl p-4 text-xs text-slate-400 space-y-1">
            <p>✅ تحميل فوري بعد التأكيد</p>
            <p>✅ نسخة إلى بريدك الإلكتروني</p>
            <p>✅ صلاحية 30 يوماً</p>
          </div>
        </div>

        {/* Checkout Form */}
        <div className="bg-dark-700 rounded-2xl p-6 border border-dark-500">
          <h2 className="text-white font-bold text-xl mb-5">بياناتك</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-slate-300 text-sm font-medium mb-2">اسمك الكامل</label>
              <div className="relative">
                <User className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input
                  type="text"
                  required
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="أحمد محمد"
                  className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-3 pr-10 focus:outline-none focus:border-brand-400 placeholder-slate-600 text-sm"
                />
              </div>
            </div>

            <div>
              <label className="block text-slate-300 text-sm font-medium mb-2">البريد الإلكتروني</label>
              <div className="relative">
                <Mail className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input
                  type="email"
                  required
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  placeholder="example@email.com"
                  className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-3 pr-10 focus:outline-none focus:border-brand-400 placeholder-slate-600 text-sm"
                />
              </div>
              <p className="text-xs text-slate-500 mt-1">سيصلك رابط التحميل على هذا البريد</p>
            </div>

            <div className="bg-dark-800 rounded-xl p-4 border border-dark-500">
              <p className="text-slate-400 text-sm text-center">دفع آمن بواسطة التحويل المصرفي أو المحفظة الرقمية</p>
              <p className="text-xs text-slate-500 text-center mt-1">سيتم تفعيل رابط التحميل بعد تأكيد استلام الدفعة</p>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-brand-500 to-brand-400 text-dark-900 font-extrabold py-4 rounded-xl hover:opacity-90 transition-opacity disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {submitting ? (
                <div className="w-5 h-5 border-2 border-dark-900 border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  <Lock className="w-5 h-5" />
                  <span>تأكيد الطلب وتحميل</span>
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
