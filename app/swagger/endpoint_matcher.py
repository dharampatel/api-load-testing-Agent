# endpoint_matcher.py
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EndpointMatcher:
    def __init__(self, endpoints: List[Dict[str, Any]]):
        """
        endpoints: list from swagger_loader.extract_endpoints()
        """
        self.endpoints = endpoints
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = self._compute_embeddings()

    def _compute_embeddings(self) -> np.ndarray:
        """
        Create embeddings for all endpoints using summary+description+path
        """
        texts = []
        for ep in self.endpoints:
            text = f"{ep['method']} {ep['path']} {ep.get('summary', '')} {ep.get('description', '')}"
            texts.append(text.strip())
        return self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    def match(self, query: str, top_k: int = 3) -> List[Tuple[float, Dict[str, Any]]]:
        """
        Return top_k endpoints similar to user query
        """
        query_emb = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        sims = cosine_similarity(query_emb, self.embeddings)[0]
        top_idx = np.argsort(sims)[::-1][:top_k]
        return [(float(sims[i]), self.endpoints[i]) for i in top_idx]
