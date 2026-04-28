export default function Stats({ stats }) {
  if (!stats) return null;

  const items = [
    { label: "DOCUMENTOS", value: stats.documents_active ?? 0, color: "text-plenergy-blue" },
    { label: "CHUNKS", value: stats.chunks_total ?? 0, color: "text-plenergy-orange" },
    { label: "AREAS", value: stats.areas ?? 0, color: "text-plenergy-blue" },
    { label: "ESTADO", value: "Activo", color: "text-green-600" },
  ];

  return (
    <div className="grid grid-cols-4 gap-3 mb-6">
      {items.map((item) => (
        <div key={item.label} className="bg-white rounded-lg border border-gray-200 px-4 py-3">
          <div className="text-xs font-bold text-plenergy-gray">{item.label}</div>
          <div className={`text-2xl font-bold ${item.color} mt-1`}>{item.value}</div>
        </div>
      ))}
    </div>
  );
}
