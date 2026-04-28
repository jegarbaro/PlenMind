import { Bell } from "lucide-react";

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <div className="text-2xl font-bold">
          <span className="text-plenergy-blue">Plen</span>
          <span className="text-plenergy-orange">Mind</span>
        </div>
        <span className="bg-plenergy-orange-soft text-plenergy-orange text-xs font-bold px-2 py-1 rounded">
          OPS
        </span>
        <nav className="ml-8 flex gap-6 text-sm">
          <a className="text-plenergy-orange font-semibold border-b-2 border-plenergy-orange pb-1">Buscar</a>
          <a className="text-plenergy-dark hover:text-plenergy-orange cursor-pointer">Documentos</a>
          <a className="text-plenergy-dark hover:text-plenergy-orange cursor-pointer">Areas</a>
          <a className="text-plenergy-dark hover:text-plenergy-orange cursor-pointer">Historial</a>
        </nav>
      </div>
      <div className="flex items-center gap-4">
        <button className="text-plenergy-gray hover:text-plenergy-dark">
          <Bell size={18} />
        </button>
        <div className="w-9 h-9 rounded-full bg-plenergy-blue text-white flex items-center justify-center text-sm font-bold">
          AD
        </div>
      </div>
    </header>
  );
}
