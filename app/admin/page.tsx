'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Package, ShoppingBag, Wrench, TrendingUp, ArrowLeft } from 'lucide-react';

export default function AdminDashboard() {
  const [authed, setAuthed] = useState(false);
  const [key, setKey] = useState('');
  const [stats, setStats] = useState({ products: 0, purchases: 0, pending: 0, revenue: 0 });
  const [recentPurchases, setRecentPurchases] = useState<any[]>([]);

  useEffect(() => { if (sessionStorage.getItem('ak')) setAuthed(true); }, []);

  function login() {
    if (!key) return;
    sessionStorage.setItem('ak', key);
    setAuthed(true);
  }

  useEffect(() => {
    if (!authed) return;
    const ak = sessionStorage.getItem('ak') ?? '';
    Promise.all([
      fetch('/api/products').then(r => r.json()),
      fetch('/api/purchases', { headers: { 'x-admin-key': ak } }).then(r => r.json()),
      fetch('/api/customization-requests', { headers: { 'x-admin-key': ak } }).then(r => r.json()),
    ]).then(([prods, purch, reqs]) => {
      const purchases = Array.isArray(purch) ? purch : [];
      const requests = Array.isArray(reqs) ? reqs : [];
      setStats({ products: Array.isArray(prods) ? prods.length : 0, purchases: purchases.length, pending: requests.filter((r: any) => r.status === 'pending').length, revenue: purchases.reduce((s: number, p: any) => s + Number(p.amount), 0) });
      setRecentPurchases(purchases.slice(0, 5));
    });
  }, [authed]);

  if (!authed) return (
    <div className="flex items-center justify-center min-h-screen px-4">
      <div className="bg-[#16162a] border border-[#2a2a4a] rounded-2xl p-8 w-full max-w-sm">
        <h1 className="text-2xl font-bold text-white text-center mb-6">لوحة التحكم</h1>
        <input type="password" placeholder="مفتاح المدير" value={key} onChange={e => setKey(e.target.value)} onKeyDown={e => e.key === 'Enter' && login()}
          className="w-full bg-[#0e0e1a] border border-[#2a2a4a] text-white rounded-xl px-4 py-3 mb-4 focus:outline-none focus:border-cyan-400" />
        <button onClick={login} className="w-full bg-gradient-to-r from-cyan-500 to-cyan-400 text-gray-900 font-bold py-3 rounded-xl">دخول</button>
      </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-extrabold text-white">لوحة التحكم</h1>
        <button onClick={() => { sessionStorage.removeItem('ak'); setAuthed(false); }} className="text-slate-400 hover:text-red-400 text-sm">خروج</button>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[{icon:Package,label:'المنتجات',val:stats.products,col:'text-cyan-400'},{icon:ShoppingBag,label:'المبيعات',val:stats.purchases,col:'text-green-400'},{icon:Wrench,label:'طلبات معلقة',val:stats.pending,col:'text-yellow-400'},{icon:TrendingUp,label:'الإيرادات $',val:stats.revenue.toFixed(0),col:'text-purple-400'}].map(({icon:Icon,label,val,col})=>(
          <div key={label} className="bg-[#16162a] border border-[#2a2a4a] rounded-2xl p-5">
            <Icon className={`w-6 h-6 ${col} mb-3`} />
            <p className="text-2xl font-bold text-white">{val}</p>
            <p className="text-slate-400 text-sm mt-1">{label}</p>
          </div>
        ))}
      </div>
      <div className="grid md:grid-cols-2 gap-4 mb-8">
        {[{href:'/admin/products',title:'إدارة المنتجات',desc:'إضافة وتعديل وحذف المنتجات'},{href:'/admin/requests',title:'طلبات التعديل',desc:'متابعة وتنفيذ طلبات العملاء'}].map(({href,title,desc})=>(
          <Link key={href} href={href} className="flex justify-between items-center bg-[#16162a] border border-[#2a2a4a] rounded-2xl p-5 hover:border-cyan-400/40 transition-colors">
            <div><p className="text-white font-bold mb-1">{title}</p><p className="text-slate-400 text-sm">{desc}</p></div>
            <ArrowLeft className="w-5 h-5 text-cyan-400" />
          </Link>
        ))}
      </div>
      {recentPurchases.length > 0 && (
        <div className="bg-[#16162a] border border-[#2a2a4a] rounded-2xl p-6">
          <h2 className="text-white font-bold text-xl mb-4">آخر المبيعات</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead><tr className="text-slate-500 border-b border-[#2a2a4a]">
                <th className="text-right pb-3">العميل</th><th className="text-right pb-3">البريد</th><th className="text-right pb-3">المبلغ</th><th className="text-right pb-3">التاريخ</th>
              </tr></thead>
              <tbody className="divide-y divide-[#16162a]">
                {recentPurchases.map((p: any) => (
                  <tr key={p.id}>
                    <td className="py-3 text-white">{p.customer_name}</td>
                    <td className="py-3 text-slate-400">{p.customer_email}</td>
                    <td className="py-3 text-cyan-400 font-bold">${p.amount}</td>
                    <td className="py-3 text-slate-500">{new Date(p.created_at).toLocaleDateString('ar-SA')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
