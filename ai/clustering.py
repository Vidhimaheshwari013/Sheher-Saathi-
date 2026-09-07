import numpy as np
from sklearn.cluster import DBSCAN

def cluster_complaints(complaint_ids: list, embeddings: list, eps: float = 0.35, min_samples: int = 2):
    """
    complaint_ids: list of DB ids, same order as embeddings
    embeddings: list of vectors (normalized)
    Returns: dict mapping complaint_id -> cluster_label (-1 = noise/no cluster)
    """
    if len(embeddings) < min_samples:
        return {cid: -1 for cid in complaint_ids}

    X = np.array(embeddings, dtype="float32")
    # Since embeddings are normalized, cosine distance = 1 - cosine similarity
    db = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine")
    labels = db.fit_predict(X)

    return {cid: int(label) for cid, label in zip(complaint_ids, labels)}