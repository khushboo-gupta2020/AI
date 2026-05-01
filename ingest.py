"""
ingest.py — Ingests Test_case.xlsx into ChromaDB using Nomic Embed Text v1.5
Run once: python ingest.py
"""

import os
import json
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

# ── Config ────────────────────────────────────────────────────────────────────
DATA_DIR       = os.path.join(os.path.dirname(__file__), "data")
CHROMA_DIR     = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION     = "vwo_testcases"
EMBED_MODEL    = "nomic-ai/nomic-embed-text-v1.5"
CHUNKS_CACHE   = os.path.join(os.path.dirname(__file__), "chunks_cache.json")
EXCEL_FILE     = "Test_case.xlsx"

# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_chunks_from_excel(excel_path: str) -> list[dict]:
    """Read Excel and treat each test case row as a chunk."""
    df = pd.read_excel(excel_path)
    
    all_chunks = []
    for i, row in df.iterrows():
        # Convert row to a readable string format
        text_lines = []
        for col in df.columns:
            text_lines.append(f"{col}: {row[col]}")
        
        chunk_text = "\n".join(text_lines)
        
        all_chunks.append({
            "id":      f"testcase_{row['TID']}_{i}",
            "text":    chunk_text,
            "source":  "Test_case.xlsx",
            "page":    1, # Dummy page for UI consistency
            "chunk_i": i,
        })
    return all_chunks


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("🔵  Loading Nomic Embed model …")
    model = SentenceTransformer(EMBED_MODEL, trust_remote_code=True)

    print("🔵  Connecting to local ChromaDB …")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    
    try:
        client.delete_collection(COLLECTION)
        print(f"   ♻️  Deleted existing collection '{COLLECTION}'")
    except Exception:
        pass
        
    collection = client.create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )

    excel_path = os.path.join(DATA_DIR, EXCEL_FILE)
    if not os.path.exists(excel_path):
        print(f"❌  Could not find {EXCEL_FILE} in {DATA_DIR}")
        return

    print(f"\n📄  Processing: {EXCEL_FILE}")
    all_chunks = extract_chunks_from_excel(excel_path)
    print(f"   ✔  Extracted {len(all_chunks)} test case chunks")

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
