from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import json
import os

app = FastAPI()

CSV_FEED_URL = "https://download.maytoni.com/stock/ecom/stock-retail-direct.csv"
GOMAG_API_URL = "https://api.gomag.ro/api/v1/product/read/json"
GOMAG_UPDATE_URL = "https://api.gomag.ro/v1/products/update"
GOMAG_API_TOKEN = os.getenv("GOMAG_API_TOKEN", "TOKENUL_TAU_AICI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/check-stock")
def check_stock():
    try:
        # Load Maytoni feed
        df_stock = pd.read_csv(CSV_FEED_URL, delimiter=';')
        df_stock = df_stock.rename(columns={"ArticleNo": "SKU", "AvailInventory": "Stock"})

        # Get Gomag product list
        headers = {
            "Authorization": GOMAG_API_TOKEN,
            "Content-Type": "application/json"
        }
        response = requests.get(GOMAG_API_URL, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Gomag API error: {response.status_code} - {response.text}"
            )

        try:
            gomag_data = response.json()
        except Exception:
            raise HTTPException(status_code=500, detail="Răspuns invalid de la Gomag: nu este JSON")

        # Temporar: returnăm structura completă a răspunsului pentru analiză
        return {"raw_response": gomag_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/update-stock")
def update_stock(payload: dict):
    try:
        headers = {
            "Authorization": f"Bearer {GOMAG_API_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.put(GOMAG_UPDATE_URL, headers=headers, data=json.dumps(payload))
        return {"status": response.status_code, "response": response.json()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

