const stats = [
  { value: '+50', label: 'متجر وقالب جاهز' },
  { value: '+200', label: 'عميل سعيد' },
  { value: '24سا', label: 'دعم فني' },
  { value: '100%', label: 'ضمان الجودة' },
];

export default function StatsSection() {
  return (
    <section className="py-12 px-4 border-y border-white/5">
      <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6">
        {stats.map((s) => (
          <div key={s.label} className="text-center">
            <div className="text-3xl font-extrabold gradient-text mb-1">{s.value}</div>
            <div className="text-slate-400 text-sm">{s.label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
