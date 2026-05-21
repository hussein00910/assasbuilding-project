'use client';
import Link from 'next/link';
import { useState } from 'react';
import { Menu, X, ShoppingBag, Zap } from 'lucide-react';

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="glass sticky top-0 z-50 border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-400 to-purple-600 flex items-center justify-center">
            <Zap className="w-4 h-4 text-white" />
          </div>
          <span className="font-bold text-lg text-white">أساس بيلدينج</span>
        </Link>

        <div className="hidden md:flex items-center gap-6">
          <Link href="/#products" className="text-slate-300 hover:text-brand-400 transition-colors text-sm font-medium">المنتجات</Link>
          <Link href="/#services" className="text-slate-300 hover:text-brand-400 transition-colors text-sm font-medium">الخدمات</Link>
          <Link href="/contact" className="text-slate-300 hover:text-brand-400 transition-colors text-sm font-medium">تواصل</Link>
          <Link href="/admin" className="bg-gradient-to-r from-brand-500 to-purple-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:opacity-90 transition-opacity">لوحة التحكم</Link>
        </div>

        <button className="md:hidden text-white" onClick={() => setOpen(!open)}>
          {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {open && (
        <div className="md:hidden bg-dark-800 border-t border-white/5 px-4 py-4 flex flex-col gap-4">
          <Link href="/#products" className="text-slate-300 hover:text-brand-400" onClick={() => setOpen(false)}>المنتجات</Link>
          <Link href="/#services" className="text-slate-300 hover:text-brand-400" onClick={() => setOpen(false)}>الخدمات</Link>
          <Link href="/contact" className="text-slate-300 hover:text-brand-400" onClick={() => setOpen(false)}>تواصل</Link>
          <Link href="/admin" className="bg-gradient-to-r from-brand-500 to-purple-600 text-white px-4 py-2 rounded-lg text-sm font-semibold text-center" onClick={() => setOpen(false)}>لوحة التحكم</Link>
        </div>
      )}
    </nav>
  );
}
