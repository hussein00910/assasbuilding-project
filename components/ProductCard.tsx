import Link from 'next/link';
import Image from 'next/image';
import { ExternalLink, ShoppingCart, Tag } from 'lucide-react';
import { Product } from '@/lib/types';
import { formatPrice } from '@/lib/utils';

export default function ProductCard({ product }: { product: Product }) {
  const typeLabel: Record<string, string> = {
    store: 'متجر',
    template: 'قالب',
    service: 'خدمة',
  };

  return (
    <div className="bg-dark-700 rounded-2xl overflow-hidden border border-dark-500 card-hover flex flex-col">
      <div className="relative h-48 bg-dark-800 overflow-hidden">
        {product.thumbnail_url ? (
          <Image
            src={product.thumbnail_url}
            alt={product.name_ar}
            fill
            className="object-cover"
            sizes="(max-width: 768px) 100vw, 33vw"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-slate-600">
            <Tag className="w-12 h-12" />
          </div>
        )}
        <span className="absolute top-3 right-3 bg-brand-400/90 text-dark-900 text-xs font-bold px-3 py-1 rounded-full">
          {typeLabel[product.type] ?? product.type}
        </span>
      </div>

      <div className="p-5 flex flex-col flex-1">
        <h3 className="text-white font-bold text-lg mb-2 line-clamp-1">{product.name_ar || product.name}</h3>
        <p className="text-slate-400 text-sm line-clamp-2 mb-4 flex-1">{product.description_ar || product.description}</p>

        {product.tech_stack?.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {product.tech_stack.slice(0, 3).map((t) => (
              <span key={t} className="bg-dark-600 text-slate-300 text-xs px-2 py-0.5 rounded">{t}</span>
            ))}
          </div>
        )}

        <div className="flex items-center justify-between mb-4">
          <span className="text-2xl font-bold text-brand-400">{formatPrice(product.price)}</span>
        </div>

        <div className="flex gap-2">
          <Link
            href={`/products/${product.id}`}
            className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-brand-500 to-brand-400 text-dark-900 font-bold py-2.5 rounded-xl hover:opacity-90 transition-opacity text-sm"
          >
            <ShoppingCart className="w-4 h-4" />
            <span>شراء</span>
          </Link>
          {product.preview_url && (
            <a
              href={product.preview_url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2.5 bg-dark-600 border border-dark-500 text-slate-300 rounded-xl hover:bg-dark-500 transition-colors"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
