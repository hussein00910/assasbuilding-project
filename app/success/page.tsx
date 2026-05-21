'use client';
import { useSearchParams } from 'next/navigation';
import { useState, Suspense } from 'react';
import { Download, CheckCircle, Zap } from 'lucide-react';
import CustomizationForm from '@/components/CustomizationForm';
import Link from 'next/link';

function SuccessContent() {
  const searchParams = useSearchParams();
  const purchaseId = searchParams.get('purchase_id') ?? '';
  const downloadUrl = searchParams.get('download') ?? '';
  const includeCustomization = searchParams.get('customization') === 'true';
  const [showForm, setShowForm] = useState(false);

  return (
    <div className="max-w-2xl mx-auto px-4 py-16 text-center">
      <div className="w-20 h-20 rounded-full bg-green-500/20 flex items-center justify-center mx-auto mb-6">
        <CheckCircle className="w-10 h-10 text-green-400" />
      </div>

      <h1 className="text-3xl font-extrabold text-white mb-3">شكراً لشرائك! رابط التحميل جاهز ♥️</h1>
      <p className="text-slate-400 mb-8">تم إرسال رابط التحميل أيضاً إلى بريدك الإلكتروني. صلاحية 30 يوماً.</p>

      {downloadUrl && (
        <a
          href={downloadUrl}
          className="inline-flex items-center gap-2 bg-gradient-to-r from-brand-500 to-brand-400 text-dark-900 font-extrabold px-8 py-4 rounded-xl hover:opacity-90 transition-opacity text-lg mb-6"
        >
          <Download className="w-5 h-5" />
          <span>تحميل الملف الآن</span>
        </a>
      )}

      {includeCustomization && !showForm && (
        <div className="mt-8 bg-brand-400/10 border border-brand-400/20 rounded-2xl p-6">
          <Zap className="w-8 h-8 text-brand-400 mx-auto mb-3" />
          <h2 className="text-xl font-bold text-white mb-2">خدمة التعديل مفعّلة!</h2>
          <p className="text-slate-400 mb-4">أخبرنا بتفاصيل التعديلات المطلوبة وسنبدأ العمل فوراً</p>
          <button
            onClick={() => setShowForm(true)}
            className="bg-brand-400 text-dark-900 font-bold px-6 py-2.5 rounded-xl hover:opacity-90 transition-opacity"
          >
            ملء نموذج التعديل
          </button>
        </div>
      )}

      {showForm && <CustomizationForm purchaseId={purchaseId} />}

      <div className="mt-10">
        <Link href="/" className="text-brand-400 hover:underline text-sm">← العودة إلى الرئيسية</Link>
      </div>
    </div>
  );
}

export default function SuccessPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><div className="w-10 h-10 border-4 border-brand-400 border-t-transparent rounded-full animate-spin" /></div>}>
      <SuccessContent />
    </Suspense>
  );
}
