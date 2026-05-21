'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { CustomizationRequest } from '@/lib/types';
import { getStatusLabel, getStatusColor } from '@/lib/utils';
import toast from 'react-hot-toast';

export default function AdminRequests() {
  const router = useRouter();
  const [requests, setRequests] = useState<CustomizationRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<CustomizationRequest | null>(null);
  const [statusFilter, setStatusFilter] = useState('all');

  const adminKey = typeof window !== 'undefined' ? sessionStorage.getItem('admin_key') ?? '' : '';

  useEffect(() => {
    if (!sessionStorage.getItem('admin_key')) { router.push('/admin'); return; }
    loadRequests();
  }, [statusFilter]);

  function loadRequests() {
    setLoading(true);
    const url = statusFilter === 'all' ? '/api/customization-requests' : `/api/customization-requests?status=${statusFilter}`;
    fetch(url, { headers: { 'x-admin-key': adminKey } })
      .then((r) => r.json())
      .then((d) => { setRequests(d); setLoading(false); })
      .catch(() => setLoading(false));
  }

  async function updateStatus(id: string, status: string, notes?: string) {
    const res = await fetch(`/api/customization-requests/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', 'x-admin-key': adminKey },
      body: JSON.stringify({ status, admin_notes: notes }),
    });
    if (res.ok) {
      toast.success('تم تحديث الحالة');
      loadRequests();
      setSelected(null);
    } else {
      toast.error('حدث خطأ');
    }
  }

  const statuses = ['all', 'pending', 'in_progress', 'review', 'completed'];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-white mb-6">طلبات التعديل والتخصيص</h1>

      {/* Filter */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {statuses.map((s) => (
          <button key={s} onClick={() => setStatusFilter(s)}
            className={`px-4 py-1.5 rounded-full text-sm font-semibold transition-all ${
              statusFilter === s ? 'bg-brand-400 text-dark-900' : 'bg-dark-700 text-slate-300 border border-dark-500'
            }`}>
            {s === 'all' ? 'الكل' : getStatusLabel(s)}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-center text-slate-400 py-12">جاري التحميل...</div>
      ) : requests.length === 0 ? (
        <div className="text-center text-slate-500 py-12">لا توجد طلبات</div>
      ) : (
        <div className="space-y-4">
          {requests.map((req) => (
            <div key={req.id} className="bg-dark-700 border border-dark-500 rounded-2xl p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${getStatusColor(req.status)}`}>
                      {getStatusLabel(req.status)}
                    </span>
                    <span className="text-slate-500 text-xs">{new Date(req.created_at).toLocaleString('ar-SA')}</span>
                  </div>
                  <p className="text-white font-semibold">{req.customer_name} — <span className="text-slate-400 font-normal text-sm">{req.customer_email}</span></p>
                  <p className="text-slate-300 text-sm mt-2 line-clamp-2">{req.request_details}</p>
                  {req.color_changes && <p className="text-slate-500 text-xs mt-1">ألوان: {req.color_changes}</p>}
                  {req.payment_gateway && <p className="text-slate-500 text-xs">بوابة دفع: {req.payment_gateway}</p>}
                </div>
                <button onClick={() => setSelected(req)}
                  className="bg-dark-600 border border-dark-400 text-slate-300 text-sm px-3 py-1.5 rounded-lg hover:border-brand-400/50 hover:text-brand-400 transition-colors shrink-0">
                  إدارة
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {selected && (
        <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center px-4" onClick={() => setSelected(null)}>
          <div className="bg-dark-700 border border-dark-500 rounded-2xl p-6 w-full max-w-lg max-h-screen overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-bold text-white mb-4">تفاصيل الطلب</h2>
            <div className="space-y-3 text-sm mb-6">
              <p><span className="text-slate-500">العميل:</span> <span className="text-white">{selected.customer_name}</span></p>
              <p><span className="text-slate-500">البريد:</span> <span className="text-white">{selected.customer_email}</span></p>
              <p><span className="text-slate-500">التفاصيل:</span> <span className="text-white">{selected.request_details}</span></p>
              {selected.color_changes && <p><span className="text-slate-500">ألوان:</span> <span className="text-white">{selected.color_changes}</span></p>}
              {selected.new_sections && <p><span className="text-slate-500">أقسام جديدة:</span> <span className="text-white">{selected.new_sections}</span></p>}
              {selected.payment_gateway && <p><span className="text-slate-500">بوابة الدفع:</span> <span className="text-white">{selected.payment_gateway}</span></p>}
              {selected.domain_config && <p><span className="text-slate-500">الدومين:</span> <span className="text-white">{selected.domain_config}</span></p>}
              {selected.other_changes && <p><span className="text-slate-500">أخرى:</span> <span className="text-white">{selected.other_changes}</span></p>}
            </div>
            <div className="grid grid-cols-2 gap-2">
              {selected.status !== 'in_progress' && (
                <button onClick={() => updateStatus(selected.id, 'in_progress')}
                  className="bg-blue-500/20 text-blue-400 border border-blue-500/30 py-2 rounded-xl text-sm font-semibold hover:bg-blue-500/30">
                  بدء التنفيذ
                </button>
              )}
              {selected.status !== 'completed' && (
                <button onClick={() => updateStatus(selected.id, 'completed')}
                  className="bg-green-500/20 text-green-400 border border-green-500/30 py-2 rounded-xl text-sm font-semibold hover:bg-green-500/30">
                  تم التسليم
                </button>
              )}
            </div>
            <button onClick={() => setSelected(null)} className="w-full mt-3 text-slate-500 text-sm hover:text-slate-300">إغلاق</button>
          </div>
        </div>
      )}
    </div>
  );
}
