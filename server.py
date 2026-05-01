"""
server.py — Flask backend for the RAG dashboard (Test Cases)
"""

import os
import json
import chromadb
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from groq import Groq

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(__file__)
CHROMA_DIR   = os.path.join(BASE_DIR, "chroma_db")
COLLECTION   = "vwo_testcases"
CHUNKS_CACHE = os.path.join(BASE_DIR, "chunks_cache.json")
EMBED_MODEL  = "nomic-ai/nomic-embed-text-v1.5"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "your_groq_api_key_here")
GROQ_MODEL   = "llama-3.1-8b-instant"   
TOP_K        = 5

app = Flask(__name__, static_folder=BASE_DIR)
CORS(app)

# ── Lazy singletons ───────────────────────────────────────────────────────────
_model      = None
_collection = None
_groq       = None

def get_model():
    global _model
    if _model is None:
        print("Loading Nomic Embed …")
        _model = SentenceTransformer(EMBED_MODEL, trust_remote_code=True)
    return _model

def get_collection():
    global _collection
    if _collection is None:
        client      = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_collection(COLLECTION)
    return _collection

def get_groq():
    global _groq
    if _groq is None:
        _groq = Groq(api_key=GROQ_API_KEY)
    return _groq

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/api/chunks", methods=["GET"])
def list_chunks():
    """Return all cached chunks with metadata."""
    if not os.path.exists(CHUNKS_CACHE):
        return jsonify({"error": "chunks_cache.json not found. Run ingest.py first."}), 404
    with open(CHUNKS_CACHE, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return jsonify({"chunks": chunks, "total": len(chunks)})

@app.route("/api/db_stats", methods=["GET"])
def db_stats():
    """Return ChromaDB collection statistics."""
    try:
        col   = get_collection()
        count = col.count()
        peek  = col.peek(limit=3)
        return jsonify({
            "collection": COLLECTION,
            "db_path":    CHROMA_DIR,
            "total_docs": count,
            "embed_model": EMBED_MODEL,
            "groq_model":  GROQ_MODEL,
            "sample_ids":  peek["ids"],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/query", methods=["POST"])
def query():
    """
    POST { "question": "..." }
    """
    data     = request.get_json(force=True)
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        model     = get_model()
        q_embed   = model.encode(
            ["search_query: " + question],
            normalize_embeddings=True
        ).tolist()

        col     = get_collection()
        results = col.query(
            query_embeddings=q_embed,
            n_results=TOP_K,
            include=["documents", "metadatas", "distances"]
        )

        docs       = results["documents"][0]
        metas      = results["metadatas"][0]
        distances  = results["distances"][0]

        retrieved = []
        for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances)):
            score = round(1 - dist, 4)   
            retrieved.append({
                "rank":    i + 1,
                "score":   score,
                "text":    doc,
                "source":  meta.get("source", ""),
                "page":    meta.get("page", "?"),
                "chunk_i": meta.get("chunk_i", "?"),
            })

        context = "\n\n---\n\n".join(
            [f"[Test Case Rank {r['rank']} | Score {r['score']}]\n{r['text']}"
             for r in retrieved]
        )
        system_prompt = (
            "You are a helpful assistant that answers questions about the VWO Login Dashboard "
            "Test Cases.\n"
            "Use ONLY the provided context to answer. If the answer is not in the context, say so.\n"
            "Be precise and concise."
        )
        user_prompt = (
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )

        groq_client = get_groq()
        chat        = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=1024,
        )
        answer = chat.choices[0].message.content.strip()

        return jsonify({
            "question":  question,
            "answer":    answer,
            "retrieved": retrieved,
            "model":     GROQ_MODEL,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀  Test Case RAG Server starting on http://localhost:5002")
    app.run(debug=False, port=5002, host="0.0.0.0")
