'use client';
import { useState } from 'react';
import { Mail, MessageCircle, Send } from 'lucide-react';
import toast from 'react-hot-toast';

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', message: '' });
  const [sent, setSent] = useState(false);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSent(true);
    toast.success('تم إرسال رسالتك، سنرد عليك خلال 24 ساعة!');
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-16">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-extrabold text-white mb-3">تواصل معنا</h1>
        <p className="text-slate-400">نحن هنا لمساعدتك — أرسل لنا رسالتك وسنرد في أسرع وقت</p>
      </div>

      <div className="flex justify-center gap-6 mb-10">
        <div className="flex items-center gap-2 text-slate-400 text-sm">
          <Mail className="w-4 h-4 text-brand-400" />
          <span>support@assasbuilding.com</span>
        </div>
        <div className="flex items-center gap-2 text-slate-400 text-sm">
          <MessageCircle className="w-4 h-4 text-brand-400" />
          <span>واتساب</span>
        </div>
      </div>

      {sent ? (
        <div className="bg-green-500/10 border border-green-500/20 rounded-2xl p-8 text-center">
          <p className="text-green-400 font-bold text-xl">شكراً! سنرد عليك قريباً ♥️</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="bg-dark-700 border border-dark-500 rounded-2xl p-6 space-y-4">
          <div>
            <label className="block text-slate-400 text-sm mb-1">الاسم</label>
            <input required type="text" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">البريد الإلكتروني</label>
            <input required type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">رسالتك</label>
            <textarea required rows={4} value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400 resize-none" />
          </div>
          <button type="submit" className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-brand-500 to-brand-400 text-dark-900 font-bold py-3 rounded-xl hover:opacity-90">
            <Send className="w-4 h-4" />إرسال
          </button>
        </form>
      )}
    </div>
  );
}
