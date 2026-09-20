"""
Retrieval Module: Implements Chroma vector database indexing and semantic search
over CloudServe documentation corpus.
"""

import os
import json
from typing import List, Dict, Any, Optional
from src.schema import PassageSource


class DocumentationRetriever:
    def __init__(self, doc_path: str = "Capstone_Pack/05_Datasets/documentation.json", chroma_dir: str = "./storage/chroma"):
        self.doc_path = doc_path
        self.chroma_dir = chroma_dir
        self.documents: List[Dict[str, Any]] = []
        self.store = None
        self._load_documents()
        self._init_vector_store()

    def _load_documents(self):
        """Loads knowledge base articles from json file."""
        if os.path.exists(self.doc_path):
            with open(self.doc_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)

    def _init_vector_store(self):
        """Initializes Chroma vector store or memory fallback."""
        try:
            try:
                from langchain_text_splitters import RecursiveCharacterTextSplitter
            except ImportError:
                from langchain.text_splitter import RecursiveCharacterTextSplitter

            try:
                from langchain_community.vectorstores import Chroma
                from langchain_community.embeddings import HuggingFaceEmbeddings
            except ImportError:
                from langchain.vectorstores import Chroma
                from langchain.embeddings import HuggingFaceEmbeddings

            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

            if os.path.exists(self.chroma_dir) and os.listdir(self.chroma_dir):
                self.store = Chroma(persist_directory=self.chroma_dir, embedding_function=embeddings)
            elif self.documents:
                splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
                texts, metadatas = [], []
                for doc in self.documents:
                    content = doc.get("content") or doc.get("body") or ""
                    chunks = splitter.split_text(content)
                    for i, chunk in enumerate(chunks):
                        doc_id = doc.get("doc_id") or doc.get("id") or "DOC-UNKNOWN"
                        texts.append(chunk)
                        metadatas.append({
                            "doc_id": doc_id,
                            "title": doc.get("title", ""),
                            "chunk_id": f"{doc_id}-c{i}"
                        })

                os.makedirs(self.chroma_dir, exist_ok=True)
                self.store = Chroma.from_texts(
                    texts=texts,
                    metadatas=metadatas,
                    embedding=embeddings,
                    persist_directory=self.chroma_dir
                )
                self.store.persist()
        except Exception as e:
            # Fallback keyword-based search engine if Chroma / HuggingFace embedding initialization encounters issues
            self.store = None

    def search(self, query: str, top_k: int = 5, score_threshold: float = 0.35) -> List[PassageSource]:
        """
        Searches documentation for passages matching query.
        Returns ranked list of PassageSource items.
        Applies score thresholding: returns empty list if no passage is relevant.
        """
        if not query or not query.strip():
            return []

        results: List[PassageSource] = []

        if self.store is not None:
            try:
                # Perform similarity search with score
                docs_and_scores = self.store.similarity_search_with_score(query, k=top_k)
                for doc, dist in docs_and_scores:
                    # Chroma distance to similarity score conversion
                    similarity_score = max(0.0, 1.0 - (dist / 2.0))
                    if similarity_score >= score_threshold:
                        meta = doc.metadata or {}
                        results.append(PassageSource(
                            doc_id=meta.get("doc_id", "DOC-UNKNOWN"),
                            title=meta.get("title", "Documentation"),
                            content=doc.page_content,
                            score=round(similarity_score, 4),
                            chunk_id=meta.get("chunk_id")
                        ))
                return results
            except Exception:
                pass

        # Fallback keyword matching over loaded documentation
        query_terms = set(query.lower().split())
        scored_docs = []

        for doc in self.documents:
            title = doc.get("title", "")
            content = doc.get("content", "")
            full_text = f"{title} {content}".lower()

            matches = sum(1 for term in query_terms if term in full_text and len(term) > 3)
            if matches > 0:
                score = round(matches / max(1, len(query_terms)), 4)
                if score >= 0.15:
                    scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)

        for score, doc in scored_docs[:top_k]:
            doc_id = doc.get("doc_id") or doc.get("id") or "DOC-UNKNOWN"
            results.append(PassageSource(
                doc_id=doc_id,
                title=doc.get("title", "Documentation"),
                content=doc.get("content", "")[:600],
                score=score,
                chunk_id=f"{doc_id}-c0"
            ))

        return results


# Lazy singleton instance
_retriever_instance: Optional[DocumentationRetriever] = None


def get_retriever() -> DocumentationRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = DocumentationRetriever()
    return _retriever_instance
