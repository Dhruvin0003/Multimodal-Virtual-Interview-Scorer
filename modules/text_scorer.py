import nltk
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util

nltk.data.path.append("models/nltk_data")

semantic_model = SentenceTransformer("models/text_similarity/all-MiniLM-L6-v2")

def analyze_text(transcript, reference_answer=None):

    words = word_tokenize(transcript)
    word_count = len(words)

    unique_words = set(words)
    vocab_richness = round((len(unique_words) / word_count)*100, 2) if word_count else 0

    coherence_score = None
    if reference_answer:
        emb1 = semantic_model.encode(transcript, convert_to_tensor=True)
        emb2 = semantic_model.encode(reference_answer, convert_to_tensor=True)
        coherence_score = round(float(util.cos_sim(emb1, emb2))*100, 2)

    return {
        "word_count": int(word_count),
        "vocab_richness": float(vocab_richness),
        "coherence_score": "Reference Question not submitted" if coherence_score is None else float(coherence_score)
    }