from fastapi import APIRouter, Form
from database import add_word, get_wordbook

router = APIRouter(prefix="/wordlist", tags=["WordList"])

@router.post("/add")
def add_word_item(user_id: int = Form(...), word: str = Form(...), note: str = Form("")):
    add_word(user_id, word, note)
    return {"success": True}

@router.get("/list")
def list_words(user_id: int):
    words = get_wordbook(user_id)
    return {"words": words}
