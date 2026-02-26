from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Translator Backend Running"}

@app.post("/translate")
def translate_text(data: dict):
    text = data.get("text")
    source = data.get("source")
    target = data.get("target")

    if not text or not source or not target:
        return {"error": "Missing required fields"}

    url = "https://translate.googleapis.com/translate_a/single"

    params = {
        "client": "gtx",
        "sl": source,
        "tl": target,
        "dt": "t",
        "q": text
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return {"error": "Translation API failed", "details": response.text}

        try:
            result = response.json()
        except Exception:
            return {"error": "Invalid response from translation API"}

        translated_text = result[0][0][0]

        return {"translatedText": translated_text}

    except Exception as e:
        return {"error": str(e)}