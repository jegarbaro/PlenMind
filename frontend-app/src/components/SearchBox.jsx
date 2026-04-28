import { Search, Loader2 } from "lucide-react";
import { useState } from "react";

export default function SearchBox({ onAsk, isLoading }) {
  const [pregunta, setPregunta] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (pregunta.trim() && !isLoading) {
      onAsk(pregunta.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg border border-gray-200 px-4 py-3 flex items-center gap-3 mb-6">
      <div className="w-9 h-9 rounded-full bg-plenergy-orange-soft flex items-center justify-center flex-shrink-0">
        <Search className="text-plenergy-orange" size={16} />
      </div>
      <input
        type="text"
        value={pregunta}
        onChange={(e) => setPregunta(e.target.value)}
        placeholder="Pregunta a PlenMind sobre cualquier procedimiento, manual o proceso..."
        className="flex-1 outline-none text-sm text-plenergy-dark placeholder-plenergy-gray"
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={isLoading || !pregunta.trim()}
        className="bg-plenergy-orange text-white px-5 py-2 rounded text-sm font-semibold hover:bg-orange-600 disabled:opacity-50 flex items-center gap-2"
      >
        {isLoading && <Loader2 size={14} className="animate-spin" />}
        {isLoading ? "Pensando..." : "Preguntar"}
      </button>
    </form>
  );
}
