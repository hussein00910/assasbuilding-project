'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Package, ShoppingBag, Wrench, TrendingUp, ArrowLeft } from 'lucide-react';

const ADMIN_KEY = process.env.NEXT_PUBLIC_ADMIN_KEY ?? 'admin123';

interface Stats {
  totalProducts: number;
  totalPurchases: number;
  pendingRequests: number;
  totalRevenue: number;
}

export default function AdminDashboard() {
  const router = useRouter();
  const [authed, setAuthed] = useState(false);
  const [key, setKey] = useState('');
  const [stats, setStats] = useState<Stats | null>(null);
  const [purchases, setPurchases] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  function login() {
    if (key === ADMIN_KEY) {
      sessionStorage.setItem('admin_key', key);
      setAuthed(true);
    } else {
      alert('مفتاح خاطئ');
    }
  }

  useEffect(() => {
    const saved = sessionStorage.getItem('admin_key');
    if (saved) setAuthed(true);
  }, []);

  useEffect(() => {
    if (!authed) return;
    const adminKey = sessionStorage.getItem('admin_key') ?? '';
    setLoading(true);

    Promise.all([
      fetch('/api/products').then((r) => r.json()),
      fetch('/api/purchases', { headers: { 'x-admin-key': adminKey } }).then((r) => r.json()),
      fetch('/api/customization-requests', { headers: { 'x-admin-key': adminKey } }).then((r) => r.json()),
    ]).then(([products, purchasesData, requests]) => {
      const totalRevenue = purchasesData.reduce((sum: number, p: any) => sum + Number(p.amount), 0);
      setStats({
        totalProducts: products.length,
        totalPurchases: purchasesData.length,
        pendingRequests: requests.filter((r: any) => r.status === 'pending').length,
        totalRevenue,
      });
      setPurchases(purchasesData.slice(0, 5));
    }).finally(() => setLoading(false));
  }, [authed]);

  if (!authed) {
    return (
      <div className="flex items-center justify-center min-h-screen px-4">
        <div className="bg-dark-700 border border-dark-500 rounded-2xl p-8 w-full max-w-sm">
          <h1 className="text-2xl font-bold text-white text-center mb-6">لوحة التحكم</h1>
          <input
            type="password"
            placeholder="مفتاح المدير"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && login()}
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-3 mb-4 focus:outline-none focus:border-brand-400"
          />
          <button onClick={login} className="w-full bg-gradient-to-r from-brand-500 to-brand-400 text-dark-900 font-bold py-3 rounded-xl hover:opacity-90">
            دخول
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-extrabold text-white">لوحة التحكم</h1>
        <button onClick={() => { sessionStorage.removeItem('admin_key'); setAuthed(false); }}
          className="text-slate-400 hover:text-red-400 text-sm">تسجيل خروج</button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { icon: Package, label: 'المنتجات', value: stats?.totalProducts ?? 0, color: 'text-brand-400' },
          { icon: ShoppingBag, label: 'المبيعات', value: stats?.totalPurchases ?? 0, color: 'text-green-400' },
          { icon: Wrench, label: 'طلبات معلقة', value: stats?.pendingRequests ?? 0, color: 'text-yellow-400' },
          { icon: TrendingUp, label: 'الإيرادات ($)', value: stats?.totalRevenue.toFixed(0) ?? 0, color: 'text-purple-400' },
        ].map(({ icon: Icon, label, value, color }) => (
          <div key={label} className="bg-dark-700 border border-dark-500 rounded-2xl p-5">
            <Icon className={`w-6 h-6 ${color} mb-3`} />
            <p className="text-2xl font-bold text-white">{value}</p>
            <p className="text-slate-400 text-sm mt-1">{label}</p>
          </div>
        ))}
      </div>

      {/* Quick Links */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <Link href="/admin/products" className="flex items-center justify-between bg-dark-700 border border-dark-500 rounded-2xl p-5 hover:border-brand-400/40 transition-colors">
          <div>
            <p className="text-white font-bold mb-1">إدارة المنتجات</p>
            <p className="text-slate-400 text-sm">إضافة وتعديل وحذف المنتجات</p>
          </div>
          <ArrowLeft className="w-5 h-5 text-brand-400" />
        </Link>
        <Link href="/admin/requests" className="flex items-center justify-between bg-dark-700 border border-dark-500 rounded-2xl p-5 hover:border-brand-400/40 transition-colors">
          <div>
            <p className="text-white font-bold mb-1">طلبات التعديل</p>
            <p className="text-slate-400 text-sm">متابعة وتنفيذ طلبات العملاء</p>
          </div>
          <ArrowLeft className="w-5 h-5 text-brand-400" />
        </Link>
      </div>

      {/* Recent Purchases */}
      <div className="bg-dark-700 border border-dark-500 rounded-2xl p-6">
        <h2 className="text-white font-bold text-xl mb-4">آخر المبيعات</h2>
        {loading ? (
          <div className="text-slate-400 text-center py-6">جاري التحميل...</div>
        ) : purchases.length === 0 ? (
          <div className="text-slate-500 text-center py-6">لا توجد مبيعات بعد</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-slate-500 border-b border-dark-500">
                  <th className="text-right pb-3 font-medium">العميل</th>
                  <th className="text-right pb-3 font-medium">البريد</th>
                  <th className="text-right pb-3 font-medium">المبلغ</th>
                  <th className="text-right pb-3 font-medium">التاريخ</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-600">
                {purchases.map((p: any) => (
                  <tr key={p.id}>
                    <td className="py-3 text-white">{p.customer_name}</td>
                    <td className="py-3 text-slate-400">{p.customer_email}</td>
                    <td className="py-3 text-brand-400 font-bold">${p.amount}</td>
                    <td className="py-3 text-slate-500">{new Date(p.created_at).toLocaleDateString('ar-SA')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
