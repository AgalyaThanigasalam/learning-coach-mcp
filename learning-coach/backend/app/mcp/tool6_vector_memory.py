"""
MCP Tool 6: Vector Memory (RAG Tool)
Stores and retrieves learning history using FAISS for context-aware responses.
"""
import os, json
from typing import List, Dict, Optional
from datetime import datetime

# In-memory fallback store
_memory_store: Dict[str, List[Dict]] = {}

class VectorMemory:
    def __init__(self):
        self.use_faiss = False
        self.index = None
        self.documents = []
        self._try_init_faiss()

    def _try_init_faiss(self):
        try:
            import faiss
            import numpy as np
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.dimension = 384
            self.index = faiss.IndexFlatL2(self.dimension)
            self.use_faiss = True
            print("FAISS vector store initialized")
        except Exception as e:
            print(f"FAISS not available, using in-memory store: {e}")
            self.use_faiss = False

    def store(self, user_id: str, content: str, metadata: Dict = {}):
        entry = {"content": content, "metadata": metadata, "timestamp": datetime.utcnow().isoformat(), "user_id": user_id}
        if user_id not in _memory_store:
            _memory_store[user_id] = []
        _memory_store[user_id].append(entry)
        if self.use_faiss:
            try:
                import numpy as np
                embedding = self.model.encode([content])
                self.index.add(embedding.astype("float32"))
                self.documents.append(entry)
            except Exception as e:
                print(f"FAISS store error: {e}")

    def retrieve(self, user_id: str, query: str, top_k: int = 5) -> List[Dict]:
        if self.use_faiss and self.index and self.index.ntotal > 0:
            try:
                import numpy as np
                query_vec = self.model.encode([query]).astype("float32")
                distances, indices = self.index.search(query_vec, min(top_k, self.index.ntotal))
                results = []
                for idx in indices[0]:
                    if idx < len(self.documents) and self.documents[idx]["user_id"] == user_id:
                        results.append(self.documents[idx])
                return results
            except Exception as e:
                print(f"FAISS retrieve error: {e}")
        user_history = _memory_store.get(user_id, [])
        return user_history[-top_k:]

    def store_chat(self, user_id: str, role: str, message: str, topic: Optional[str] = None):
        self.store(user_id, message, {"role": role, "topic": topic or "general", "type": "chat"})

    def store_question_result(self, user_id: str, question: str, answer: str, is_correct: bool, topic: str):
        content = f"Q: {question} | A: {answer} | Correct: {is_correct}"
        self.store(user_id, content, {"type": "question", "topic": topic, "is_correct": is_correct})

    def get_chat_history(self, user_id: str, limit: int = 20) -> List[Dict]:
        history = _memory_store.get(user_id, [])
        chat = [h for h in history if h.get("metadata", {}).get("type") == "chat"]
        return chat[-limit:]

    def get_context_summary(self, user_id: str) -> str:
        history = _memory_store.get(user_id, [])
        if not history:
            return "No previous learning history."
        recent = history[-10:]
        topics = list(set(h.get("metadata", {}).get("topic", "") for h in recent if h.get("metadata", {}).get("topic")))
        return f"Recent topics studied: {', '.join(topics) if topics else 'None'}. Total interactions: {len(history)}."

vector_memory = VectorMemory()
