/**
 * Cliente HTTP para la API de PlenMind.
 */
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 60000,
  headers: { "Content-Type": "application/json" },
});

export const checkHealth = () => api.get("/health").then((r) => r.data);

export const listDocuments = (areaSlug = "ops") =>
  api.get(`/documents?area_slug=${areaSlug}`).then((r) => r.data);

export const queryRag = (pregunta, areaSlug = "ops") =>
  api.post("/query", {
    pregunta,
    area_slug: areaSlug,
    top_k: 5,
    temperatura: 0.3,
  }).then((r) => r.data);

export const downloadDocument = (documentId) =>
  `${API_BASE}/documents/${documentId}/download`;

export const uploadDocument = (file, areaSlug = "ops", titulo = null, autor = null) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("area_slug", areaSlug);
  if (titulo) formData.append("titulo", titulo);
  if (autor) formData.append("autor", autor);
  return api.post("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    timeout: 120000,
  }).then((r) => r.data);
};
