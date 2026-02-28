from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

class TranslateRequest(BaseModel):
    text: str
    source: str
    target: str

@app.get("/")
def home():
    return {"message": "AI Translator Backend Running"}

@app.post("/translate")
def translate_text(data: TranslateRequest):

    url = "https://translate.googleapis.com/translate_a/single"

    params = {
        "client": "gtx",
        "sl": data.source,
        "tl": data.target,
        "dt": "t",
        "q": data.text
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return {"error": "Translation API failed", "details": response.text}

        try:
            result = response.json()
        except Exception:
            return {"error": "Invalid response from translation API"}

        translated_text = "".join([item[0] for item in result[0]])

        return {"translatedText": translated_text}

    except Exception as e:
        return {"error": str(e)}