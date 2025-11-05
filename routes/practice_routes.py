from fastapi import APIRouter, Form
from utils import load_model, compute_score
from database import save_translation
import pandas as pd, random

router = APIRouter(prefix="/practice", tags=["Practice"])
model = load_model()
df = pd.read_excel("data/paragraph.xlsx")

@router.get("/get_paragraph")
def get_paragraph(level: str):
    row = df[df["seviye"] == level].sample(1).iloc[0]
    return {"paragraph": row["paragraf"], "reference": row["translate"]}

@router.post("/evaluate")
def evaluate(user_id: int = Form(...), paragraph: str = Form(...), reference: str = Form(...), user_translation: str = Form(...)):
    score = compute_score(model, reference, user_translation)
    save_translation(user_id, paragraph, user_translation, reference, score)
    return {"score": score}
