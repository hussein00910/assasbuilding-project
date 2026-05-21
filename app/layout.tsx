import type { Metadata } from 'next';
import './globals.css';
import { Toaster } from 'react-hot-toast';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: 'أساس بيلدينج | متاجر جاهزة وخدمات رقمية',
  description: 'منصة احترافية لبيع المتاجر الجاهزة والقوالب الرقمية وخدمات التعديل والدعم الفني',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>
        <Navbar />
        <main className="min-h-screen">{children}</main>
        <Footer />
        <Toaster position="top-center" toastOptions={{ style: { background: '#16162a', color: '#e2e8f0', border: '1px solid #2a2a4a' } }} />
      </body>
    </html>
  );
}
