import { useEffect, useState } from "react";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Stats from "./components/Stats";
import SearchBox from "./components/SearchBox";
import Answer from "./components/Answer";
import DocumentList from "./components/DocumentList";
import UploadModal from "./components/UploadModal";
import { checkHealth, listDocuments, queryRag } from "./api";

export default function App() {
  const [health, setHealth] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [answer, setAnswer] = useState(null);
  const [isAsking, setIsAsking] = useState(false);
  const [error, setError] = useState(null);
  const [uploadOpen, setUploadOpen] = useState(false);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [h, d] = await Promise.all([checkHealth(), listDocuments("ops")]);
      setHealth(h);
      setDocuments(d.documents || []);
    } catch (err) {
      setError("No se puede conectar con la API. Esta corriendo en http://localhost:8000?");
      console.error(err);
    }
  };

  const handleAsk = async (pregunta) => {
    setIsAsking(true);
    setError(null);
    setAnswer(null);
    try {
      const result = await queryRag(pregunta, "ops");
      setAnswer(result);
      const d = await listDocuments("ops");
      setDocuments(d.documents || []);
    } catch (err) {
      setError("Error al procesar la consulta. Revisa que la API y Ollama esten corriendo.");
      console.error(err);
    } finally {
      setIsAsking(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <div className="flex-1 flex">
        <Sidebar activeArea="ops" onUploadClick={() => setUploadOpen(true)} />
        <main className="flex-1 p-6 overflow-auto">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4 text-sm">
              {error}
            </div>
          )}

          <Stats stats={health?.stats} />
          <SearchBox onAsk={handleAsk} isLoading={isAsking} />

          {isAsking && (
            <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6 text-center text-plenergy-gray text-sm">
              <div className="animate-pulse">
                PlenMind esta consultando la documentacion...
                <div className="text-xs text-plenergy-gray mt-1">
                  (puede tardar 15-30 segundos en CPU local)
                </div>
              </div>
            </div>
          )}

          <Answer result={answer} />
          <DocumentList documents={documents} />
        </main>
      </div>
      <UploadModal isOpen={uploadOpen} onClose={() => setUploadOpen(false)} onUploadComplete={loadInitialData} />
    </div>
  );
}
