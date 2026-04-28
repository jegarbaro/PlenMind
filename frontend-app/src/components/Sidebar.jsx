import { Plus, Settings } from "lucide-react";

export default function Sidebar({ activeArea = "ops", onUploadClick }) {
  const areas = [
    { slug: "ops", name: "PlenMind OPS", color: "bg-plenergy-orange", active: true },
    { slug: "infra", name: "PlenMind Infra", color: "bg-plenergy-blue", active: false },
  ];

  return (
    <aside className="w-64 bg-white border-r border-gray-200 px-4 py-6 flex-shrink-0">
      <div className="text-xs font-bold text-plenergy-gray uppercase mb-3">Mis areas</div>
      <div className="space-y-1">
        {areas.map((area) => (
          <button
            key={area.slug}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded text-sm transition ${
              area.slug === activeArea
                ? "bg-plenergy-orange-soft text-plenergy-orange font-semibold"
                : "text-plenergy-dark hover:bg-plenergy-light-gray"
            } ${!area.active && "opacity-60"}`}
            disabled={!area.active}
          >
            <span className={`w-3 h-3 rounded-full ${area.color}`}></span>
            <span>{area.name}</span>
            {!area.active && <span className="text-xs ml-auto text-plenergy-gray">Prox.</span>}
          </button>
        ))}
      </div>

      <div className="text-xs font-bold text-plenergy-gray uppercase mt-8 mb-3">Acciones</div>
      <div className="space-y-1">
        <button onClick={onUploadClick} className="w-full flex items-center gap-2 px-3 py-2 rounded text-sm text-plenergy-dark hover:bg-plenergy-light-gray">
          <Plus size={16} />
          <span>Subir documento</span>
        </button>
        <button className="w-full flex items-center gap-2 px-3 py-2 rounded text-sm text-plenergy-dark hover:bg-plenergy-light-gray">
          <Settings size={16} />
          <span>Configuracion</span>
        </button>
      </div>
    </aside>
  );
}
