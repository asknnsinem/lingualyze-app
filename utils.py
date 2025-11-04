from sentence_transformers import SentenceTransformer, util
from nltk.translate.bleu_score import sentence_bleu

# Cache model
def load_model():
    return SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

def compute_score(model, ref, user):
    # Embedding tabanlı
    emb_user = model.encode(user, convert_to_tensor=True)
    emb_ref = model.encode(ref, convert_to_tensor=True)
    sim = util.cos_sim(emb_user, emb_ref).item()

    # BLEU ve kelime örtüşme
    ref_words = ref.split()
    usr_words = user.split()
    bleu = sentence_bleu([ref_words], usr_words)

    overlap = len(set(ref_words) & set(usr_words)) / max(1, len(set(ref_words)))

    # Nihai skor (anlam + yapı karışımı)
    return round((sim * 0.5) + (bleu * 0.3) + (overlap * 0.2), 2)
