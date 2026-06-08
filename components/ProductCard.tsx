import Link from 'next/link';
import Image from 'next/image';
import { ExternalLink, ShoppingCart } from 'lucide-react';

export default function ProductCard({ product }: { product: any }) {
  const typeLabel: Record<string,string> = { store:'متجر', template:'قالب', service:'خدمة' };
  return (
    <div className="bg-[#16162a] rounded-2xl overflow-hidden border border-[#2a2a4a] card-hover flex flex-col">
      <div className="relative h-48 bg-[#0e0e1a]">
        {product.thumbnail_url
          ? <Image src={product.thumbnail_url} alt={product.name_ar||product.name} fill className="object-cover" sizes="400px" />
          : <div className="w-full h-full flex items-center justify-center text-5xl">🖼️</div>}
        <span className="absolute top-3 right-3 bg-cyan-400/90 text-gray-900 text-xs font-bold px-3 py-1 rounded-full">{typeLabel[product.type]??product.type}</span>
      </div>
      <div className="p-5 flex flex-col flex-1">
        <h3 className="text-white font-bold text-lg mb-2 line-clamp-1">{product.name_ar||product.name}</h3>
        <p className="text-slate-400 text-sm line-clamp-2 mb-4 flex-1">{product.description_ar||product.description}</p>
        {Array.isArray(product.tech_stack) && product.tech_stack.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {product.tech_stack.slice(0,3).map((t: string)=>(<span key={t} className="bg-[#0e0e1a] text-slate-300 text-xs px-2 py-0.5 rounded">{t}</span>))}
          </div>
        )}
        <div className="flex items-center justify-between mb-4">
          <span className="text-2xl font-bold text-cyan-400">${product.price}</span>
        </div>
        <div className="flex gap-2">
          <Link href={`/products/${product.id}`} className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-cyan-500 to-cyan-400 text-gray-900 font-bold py-2.5 rounded-xl hover:opacity-90 text-sm">
            <ShoppingCart className="w-4 h-4" />شراء
          </Link>
          {product.preview_url && (
            <a href={product.preview_url} target="_blank" rel="noopener noreferrer" className="px-3 py-2.5 bg-[#0e0e1a] border border-[#2a2a4a] text-slate-300 rounded-xl hover:border-cyan-400/50 hover:text-cyan-400 transition-colors">
              <ExternalLink className="w-4 h-4" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
