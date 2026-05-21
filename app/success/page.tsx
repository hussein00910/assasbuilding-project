'use client';
import { useSearchParams } from 'next/navigation';
import { useState, Suspense } from 'react';
import { Download, CheckCircle, Zap } from 'lucide-react';
import Link from 'next/link';
import toast from 'react-hot-toast';

function SuccessContent() {
  const sp = useSearchParams();
  const purchaseId = sp.get('purchase_id') ?? '';
  const downloadUrl = sp.get('download') ?? '';
  const withCustom = sp.get('customization') === 'true';
  const [showForm, setShowForm] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ customer_name:'', customer_email:'', request_details:'', color_changes:'', payment_gateway:'', domain_config:'', new_sections:'' });

  async function submitRequest(e: React.FormEvent) {
    e.preventDefault(); setLoading(true);
    try {
      const res = await fetch('/api/customization-requests', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ ...form, purchase_id: purchaseId }) });
      if (!res.ok) throw new Error();
      setSubmitted(true); toast.success('تم إرسال طلبك!');
    } catch { toast.error('حدث خطأ'); } finally { setLoading(false); }
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-16 text-center">
      <div className="w-20 h-20 rounded-full bg-green-500/20 flex items-center justify-center mx-auto mb-6">
        <CheckCircle className="w-10 h-10 text-green-400" />
      </div>
      <h1 className="text-3xl font-extrabold text-white mb-3">شكراً لشرائك! ❤️</h1>
      <p className="text-slate-400 mb-8">تم إرسال رابط التحميل إلى بريدك الإلكتروني. صلاحيته 30 يوماً.</p>
      {downloadUrl && (
        <a href={downloadUrl} className="inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-cyan-400 text-gray-900 font-extrabold px-8 py-4 rounded-xl hover:opacity-90 text-lg mb-8">
          <Download className="w-5 h-5" />تحميل الملف الآن
        </a>
      )}
      {withCustom && !showForm && (
        <div className="mt-6 bg-cyan-400/10 border border-cyan-400/20 rounded-2xl p-6">
          <Zap className="w-8 h-8 text-cyan-400 mx-auto mb-2" />
          <h2 className="text-xl font-bold text-white mb-2">خدمة التعديل مفعّلة!</h2>
          <p className="text-slate-400 mb-4">أخبرنا بتفاصيل التعديلات المطلوبة</p>
          <button onClick={() => setShowForm(true)} className="bg-cyan-400 text-gray-900 font-bold px-6 py-2.5 rounded-xl hover:opacity-90">ملء نموذج التعديل</button>
        </div>
      )}
      {showForm && !submitted && (
        <form onSubmit={submitRequest} className="mt-6 bg-[#16162a] border border-[#2a2a4a] rounded-2xl p-6 text-right space-y-4">
          <h3 className="text-xl font-bold text-white">نموذج طلب التعديل</h3>
          {[{f:'customer_name',l:'اسمك',t:'text'},{f:'customer_email',l:'بريدك',t:'email'}].map(({f,l,t})=>(
            <div key={f}><label className="block text-slate-400 text-sm mb-1">{l} *</label>
            <input required type={t} value={(form as any)[f]} onChange={e=>setForm({...form,[f]:e.target.value})} className="w-full bg-[#0e0e1a] border border-[#2a2a4a] text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-cyan-400" /></div>
          ))}
          <div><label className="block text-slate-400 text-sm mb-1">وصف شامل للتعديلات *</label>
            <textarea required rows={3} value={form.request_details} onChange={e=>setForm({...form,request_details:e.target.value})} className="w-full bg-[#0e0e1a] border border-[#2a2a4a] text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-cyan-400 resize-none" /></div>
          {[{f:'color_changes',l:'تغيير الألوان'},{f:'payment_gateway',l:'بوابة الدفع'},{f:'domain_config',l:'الدومين'},{f:'new_sections',l:'أقسام جديدة'}].map(({f,l})=>(
            <div key={f}><label className="block text-slate-400 text-sm mb-1">{l}</label>
            <input type="text" value={(form as any)[f]} onChange={e=>setForm({...form,[f]:e.target.value})} className="w-full bg-[#0e0e1a] border border-[#2a2a4a] text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-cyan-400" /></div>
          ))}
          <button type="submit" disabled={loading} className="w-full bg-gradient-to-r from-cyan-500 to-cyan-400 text-gray-900 font-bold py-3 rounded-xl hover:opacity-90 disabled:opacity-60">
            {loading ? '...جاري الإرسال' : 'إرسال الطلب'}
          </button>
        </form>
      )}
      {submitted && <div className="mt-6 bg-green-500/10 border border-green-500/20 rounded-2xl p-6"><p className="text-green-400 font-bold text-lg">تم استلام طلبك! سنتواصل خلال 24 ساعة ❤️</p></div>}
      <div className="mt-10"><Link href="/" className="text-cyan-400 hover:underline text-sm">← العودة للرئيسية</Link></div>
    </div>
  );
}

export default function SuccessPage() {
  return <Suspense fallback={<div className="flex justify-center py-20"><div className="w-10 h-10 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin" /></div>}><SuccessContent /></Suspense>;
}
