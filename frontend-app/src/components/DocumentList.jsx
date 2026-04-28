import { FileText } from "lucide-react";
import { downloadDocument } from "../api";

export default function DocumentList({ documents }) {
  if (!documents || documents.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 text-center text-plenergy-gray text-sm">
        No hay documentos cargados todavia
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100">
        <div className="text-sm font-bold text-plenergy-dark">
          Documentos cargados ({documents.length})
        </div>
      </div>
      <div className="divide-y divide-gray-100">
        {documents.map((doc) => (
          <a
            key={doc.id}
            href={downloadDocument(doc.id)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-3 px-4 py-3 hover:bg-plenergy-light-gray transition"
          >
            <div className="w-9 h-7 rounded bg-plenergy-blue-soft text-plenergy-blue text-xs font-bold flex items-center justify-center flex-shrink-0">
              PDF
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-semibold text-plenergy-dark truncate">{doc.titulo}</div>
              <div className="text-xs text-plenergy-gray mt-0.5">{doc.page_count} pags - {doc.autor}</div>
            </div>
            <FileText className="text-plenergy-gray flex-shrink-0" size={16} />
          </a>
        ))}
      </div>
    </div>
  );
}
