'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';

const STATUS_LABEL: Record<string,string> = { pending:'قيد الانتظار', in_progress:'قيد التنفيذ', review:'مراجعة', completed:'مكتمل', cancelled:'ملغي' };
const STATUS_COLOR: Record<string,string> = { pending:'bg-yellow-500/20 text-yellow-400', in_progress:'bg-blue-500/20 text-blue-400', completed:'bg-green-500/20 text-green-400', cancelled:'bg-red-500/20 text-red-400' };

export default function AdminRequests() {
  const router = useRouter();
  const [requests, setRequests] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<any>(null);
  const [filter, setFilter] = useState('all');

  function load() {
    const ak = sessionStorage.getItem('ak') ?? '';
    if (!ak) { router.push('/admin'); return; }
    const url = filter === 'all' ? '/api/customization-requests' : `/api/customization-requests?status=${filter}`;
    setLoading(true);
    fetch(url, { headers: { 'x-admin-key': ak } }).then(r => r.json()).then(d => { setRequests(Array.isArray(d) ? d : []); setLoading(false); });
  }

  useEffect(() => { load(); }, [filter]);

  async function updateStatus(id: string, status: string) {
    const ak = sessionStorage.getItem('ak') ?? '';
    const res = await fetch(`/api/customization-requests/${id}`, { method:'PATCH', headers:{'Content-Type':'application/json','x-admin-key':ak}, body: JSON.stringify({ status }) });
    if (res.ok) { toast.success('تم التحديث'); setSelected(null); load(); } else toast.error('حدث خطأ');
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-white mb-6">طلبات التعديل والتخصيص</h1>
      <div className="flex gap-2 mb-6 flex-wrap">
        {['all','pending','in_progress','completed'].map(s=>(
          <button key={s} onClick={()=>setFilter(s)} className={`px-4 py-1.5 rounded-full text-sm font-semibold transition-all ${filter===s?'bg-cyan-400 text-gray-900':'bg-[#16162a] text-slate-300 border border-[#2a2a4a]'}`}>
            {s==='all'?'الكل':STATUS_LABEL[s]}
          </button>
        ))}
      </div>
      {loading ? <div className="text-center text-slate-400 py-12">جاري التحميل...</div> : requests.length===0 ? <div className="text-center text-slate-500 py-12">لا توجد طلبات</div> : (
        <div className="space-y-4">
          {requests.map(r=>(
            <div key={r.id} className="bg-[#16162a] border border-[#2a2a4a] rounded-2xl p-5">
              <div className="flex justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${STATUS_COLOR[r.status]??'bg-slate-500/20 text-slate-400'}`}>{STATUS_LABEL[r.status]??r.status}</span>
                    <span className="text-slate-500 text-xs">{new Date(r.created_at).toLocaleDateString('ar-SA')}</span>
                  </div>
                  <p className="text-white font-semibold">{r.customer_name} — <span className="text-slate-400 font-normal text-sm">{r.customer_email}</span></p>
                  <p className="text-slate-300 text-sm mt-2 line-clamp-2">{r.request_details}</p>
                </div>
                <button onClick={()=>setSelected(r)} className="bg-[#1e1e36] border border-[#2a2a4a] text-slate-300 text-sm px-3 py-1.5 rounded-lg hover:border-cyan-400/50 hover:text-cyan-400 shrink-0">إدارة</button>
              </div>
            </div>
          ))}
        </div>
      )}
      {selected && (
        <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center px-4" onClick={()=>setSelected(null)}>
          <div className="bg-[#16162a] border border-[#2a2a4a] rounded-2xl p-6 w-full max-w-lg" onClick={e=>e.stopPropagation()}>
            <h2 className="text-xl font-bold text-white mb-4">تفاصيل الطلب</h2>
            <div className="space-y-2 text-sm mb-5">
              {[['العميل',selected.customer_name],['البريد',selected.customer_email],['التفاصيل',selected.request_details],['الألوان',selected.color_changes],['بوابة الدفع',selected.payment_gateway],['الدومين',selected.domain_config],['أقسام جديدة',selected.new_sections]].filter(([,v])=>v).map(([k,v])=>(
                <p key={k}><span className="text-slate-500">{k}: </span><span className="text-white">{v}</span></p>
              ))}
            </div>
            <div className="grid grid-cols-2 gap-2">
              {selected.status !== 'in_progress' && <button onClick={()=>updateStatus(selected.id,'in_progress')} className="bg-blue-500/20 text-blue-400 border border-blue-500/30 py-2 rounded-xl text-sm font-semibold">بدء التنفيذ</button>}
              {selected.status !== 'completed' && <button onClick={()=>updateStatus(selected.id,'completed')} className="bg-green-500/20 text-green-400 border border-green-500/30 py-2 rounded-xl text-sm font-semibold">تم التسليم</button>}
            </div>
            <button onClick={()=>setSelected(null)} className="w-full mt-3 text-slate-500 text-sm">إغلاق</button>
          </div>
        </div>
      )}
    </div>
  );
}
