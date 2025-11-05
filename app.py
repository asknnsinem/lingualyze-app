from fastapi import FastAPI
from routes import practice_routes, user_routes, wordlist_routes, history_routes

app = FastAPI(title="Lingualyze API", version="1.0")

# Register routes
app.include_router(practice_routes.router)
app.include_router(user_routes.router)
app.include_router(wordlist_routes.router)
app.include_router(history_routes.router)

@app.get("/")
def root():
    return {"message": "Lingualyze API is running!"}
