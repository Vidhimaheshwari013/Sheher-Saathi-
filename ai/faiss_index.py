import faiss
import numpy as np

DIMENSION = 384  # matches MiniLM-L12-v2 output size

class ComplaintIndex:
    def __init__(self):
        self.index = faiss.IndexFlatIP(DIMENSION)  # inner product = cosine sim on normalized vectors
        self.id_map = []  # maps FAISS row position -> complaint DB id

    def add(self, complaint_id: int, embedding):
        vec = np.array([embedding], dtype="float32")
        self.index.add(vec)
        self.id_map.append(complaint_id)

    def search(self, embedding, k=5):
        if self.index.ntotal == 0:
            return []
        vec = np.array([embedding], dtype="float32")
        scores, indices = self.index.search(vec, min(k, self.index.ntotal))
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.id_map[idx], float(score)))
        return results

# Single shared in-memory index for the app's lifetime
complaint_index = ComplaintIndex()