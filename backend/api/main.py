"""
PlenMind API - Aplicacion principal FastAPI.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.api.routers import health, documents, query

load_dotenv()

app = FastAPI(
    title="PlenMind API",
    description="Sistema RAG local para documentacion IT de Plenergy",
    version="0.1.0",
    contact={"name": "Plenergy IT", "email": "it@plenergy.es"}
)

# CORS para el frontend (lo usaremos en la siguiente fase)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, tags=["health"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(query.router, prefix="/query", tags=["query"])


@app.get("/", tags=["health"])
def root():
    return {
        "app": "PlenMind",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs"
    }
