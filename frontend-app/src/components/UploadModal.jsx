import { useState } from "react";
import { X, Upload, FileText, Loader } from "lucide-react";
import { uploadDocument } from "../api";

export default function UploadModal({ isOpen, onClose, onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  if (!isOpen) return null;

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;
    if (!selectedFile.name.toLowerCase().endsWith(".pdf")) {
      setError("Solo se aceptan archivos PDF");
      return;
    }
    setError(null);
    setFile(selectedFile);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) return;
    setUploading(true);
    setError(null);
    try {
      await uploadDocument(file, "ops");
      setFile(null);
      onUploadComplete();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || "Error al subir el documento");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-full max-w-lg p-6 mx-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-plenergy-dark">Subir documento</h2>
          <button onClick={onClose} className="text-plenergy-gray hover:text-plenergy-dark">
            <X size={20} />
          </button>
        </div>
        <div
          onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          className={"border-2 border-dashed rounded-lg p-8 text-center transition " + (dragActive ? "border-plenergy-orange bg-plenergy-orange-soft" : "border-gray-300")}
        >
          {file ? (
            <div className="flex items-center justify-center gap-3">
              <FileText className="text-plenergy-orange" size={32} />
              <div className="text-left">
                <div className="text-sm font-semibold text-plenergy-dark">{file.name}</div>
                <div className="text-xs text-plenergy-gray">{(file.size / 1024 / 1024).toFixed(2)} MB</div>
              </div>
            </div>
          ) : (
            <div>
              <Upload className="mx-auto text-plenergy-gray mb-2" size={32} />
              <div className="text-sm text-plenergy-dark mb-2">Arrastra un PDF aqui o</div>
              <label className="inline-block px-4 py-2 bg-plenergy-blue text-white rounded text-sm font-semibold cursor-pointer hover:bg-blue-900">
                Seleccionar archivo
                <input
                  type="file"
                  accept=".pdf"
                  className="hidden"
                  onChange={(e) => handleFile(e.target.files[0])}
                />
              </label>
            </div>
          )}
        </div>
        {error && (
          <div className="mt-3 text-sm text-red-600 bg-red-50 px-3 py-2 rounded">{error}</div>
        )}
        <div className="flex justify-end gap-2 mt-4">
          <button onClick={onClose} disabled={uploading} className="px-4 py-2 text-sm text-plenergy-gray hover:text-plenergy-dark">
            Cancelar
          </button>
          <button onClick={handleSubmit} disabled={!file || uploading} className="px-4 py-2 bg-plenergy-orange text-white text-sm font-semibold rounded hover:bg-orange-600 disabled:bg-gray-300 flex items-center gap-2">
            {uploading ? (
              <>
                <Loader className="animate-spin" size={14} />
                Subiendo...
              </>
            ) : (
              "Subir"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
