from sentence_transformers import SentenceTransformer

# Multilingual model — handles English, Hindi, and Hinglish reasonably well
_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def get_embedding(text: str):
    return _model.encode(text, normalize_embeddings=True)