"""
ingest.py — Ingests PDFs from ./data into ChromaDB using Nomic Embed Text v1.5
Run once: python ingest.py
"""

import os
import json
import fitz  # PyMuPDF
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# ── Config ────────────────────────────────────────────────────────────────────
DATA_DIR       = os.path.join(os.path.dirname(__file__), "data")
CHROMA_DIR     = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION     = "vwo_prd"
CHUNK_SIZE     = 500   # characters
CHUNK_OVERLAP  = 80    # characters
EMBED_MODEL    = "nomic-ai/nomic-embed-text-v1.5"
CHUNKS_CACHE   = os.path.join(os.path.dirname(__file__), "chunks_cache.json")

# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """Extract text page-by-page from a PDF."""
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text").strip()
        if text:
            pages.append({"page": i + 1, "text": text})
    doc.close()
    return pages


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return [c for c in chunks if len(c) > 30]  # drop tiny leftovers


def build_chunks(pages: list[dict], source_name: str) -> list[dict]:
    """Build chunk dicts with metadata from page list."""
    all_chunks = []
    chunk_idx = 0
    for page in pages:
        raw_chunks = chunk_text(page["text"])
        for ci, chunk in enumerate(raw_chunks):
            all_chunks.append({
                "id":      f"{source_name}_p{page['page']}_c{ci}",
                "text":    chunk,
                "source":  source_name,
                "page":    page["page"],
                "chunk_i": chunk_idx,
            })
            chunk_idx += 1
    return all_chunks


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("🔵  Loading Nomic Embed model …")
    model = SentenceTransformer(EMBED_MODEL, trust_remote_code=True)

    print("🔵  Connecting to local ChromaDB …")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    # Delete existing collection to allow re-ingestion
    try:
        client.delete_collection(COLLECTION)
        print(f"   ♻️  Deleted existing collection '{COLLECTION}'")
    except Exception:
        pass
    collection = client.create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )

    all_chunks = []
    pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("❌  No PDF files found in ./data — add a PDF and re-run.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(DATA_DIR, pdf_file)
        source   = os.path.splitext(pdf_file)[0]
        print(f"\n📄  Processing: {pdf_file}")
        pages  = extract_text_from_pdf(pdf_path)
        chunks = build_chunks(pages, source)
        print(f"   ✔  {len(pages)} pages → {len(chunks)} chunks")
        all_chunks.extend(chunks)

    print(f"\n🔵  Embedding {len(all_chunks)} chunks with Nomic …")
    texts = [c["text"] for c in all_chunks]
    # Nomic requires a task prefix for best performance
    prefixed = ["search_document: " + t for t in texts]
    embeddings = model.encode(prefixed, show_progress_bar=True, normalize_embeddings=True)

    print("🔵  Upserting into ChromaDB …")
    batch_size = 50
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i : i + batch_size]
        collection.add(
            ids        = [c["id"]   for c in batch],
            documents  = [c["text"] for c in batch],
            embeddings = embeddings[i : i + batch_size].tolist(),
            metadatas  = [{"source": c["source"], "page": c["page"], "chunk_i": c["chunk_i"]} for c in batch],
        )

    # Cache chunks for the UI
    with open(CHUNKS_CACHE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"\n✅  Done! {len(all_chunks)} chunks ingested into ChromaDB collection '{COLLECTION}'.")
    print(f"   DB path : {CHROMA_DIR}")
    print(f"   Cache   : {CHUNKS_CACHE}")


if __name__ == "__main__":
    main()
