import { FileText, Download, Clock, Cpu } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { downloadDocument } from "../api";

export default function Answer({ result }) {
  if (!result) return null;
  const fuentes = result.fuentes || [];
  const metricas = result.metricas;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
      <div className="text-xs font-bold text-plenergy-gray uppercase mb-2">Pregunta</div>
      <div className="text-plenergy-dark mb-4 italic">{result.pregunta}</div>
      <div className="text-xs font-bold text-plenergy-gray uppercase mb-2">Respuesta</div>
      <div className="text-plenergy-dark mb-6 prose prose-sm max-w-none">
        <ReactMarkdown>{result.respuesta}</ReactMarkdown>
      </div>
      {fuentes.length > 0 && (
        <div>
          <div className="text-xs font-bold text-plenergy-gray uppercase mb-3">
            Fuentes ({fuentes.length})
          </div>
          <div className="space-y-2 mb-4">
            {fuentes.map((fuente, i) => (
              <a
                key={i}
                href={downloadDocument(fuente.document_id)}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 px-3 py-2 bg-plenergy-orange-soft rounded hover:bg-orange-100 transition"
              >
                <FileText className="text-plenergy-orange flex-shrink-0" size={16} />
                <div className="flex-1 text-sm">
                  <span className="font-semibold text-plenergy-orange">{fuente.document_titulo}</span>
                  <span className="text-plenergy-gray ml-2">pag. {fuente.page_number}</span>
                </div>
                <Download className="text-plenergy-orange flex-shrink-0" size={14} />
              </a>
            ))}
          </div>
        </div>
      )}
      {metricas && (
        <div className="border-t border-gray-100 pt-3 flex items-center gap-4 text-xs text-plenergy-gray">
          <span className="flex items-center gap-1">
            <Clock size={12} />
            Busqueda: {metricas.tiempo_busqueda_ms}ms
          </span>
          <span className="flex items-center gap-1">
            <Cpu size={12} />
            Generacion: {(metricas.tiempo_generacion_ms / 1000).toFixed(1)}s
          </span>
          <span>Modelo: {metricas.modelo}</span>
          <span className="ml-auto font-semibold text-green-600">Coste: 0,00 EUR</span>
        </div>
      )}
    </div>
  );
}
