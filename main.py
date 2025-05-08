from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import json
import os

app = FastAPI()

CSV_FEED_URL = "https://download.maytoni.com/stock/ecom/stock-retail-direct.csv"
GOMAG_API_URL = "https://api.gomag.ro/v1/products/update"
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
        df_stock = pd.read_csv(CSV_FEED_URL, delimiter=';')
        df_stock = df_stock.rename(columns={"ArticleNo": "SKU", "AvailInventory": "Stock"})

        gomag_data = [
            {"code": "MOD229TL-L3B3K1", "stock": 20},
            {"code": "MOD229TL-L3B3K2", "stock": 0},
            {"code": "MOD229TL-L3G3K1", "stock": 10},
            {"code": "MD-TRA034-W", "stock": 50},
        ]
        df_gomag = pd.DataFrame(gomag_data)
        df_gomag = df_gomag.rename(columns={"code": "SKU", "stock": "GomagStock"})

        df_compare = pd.merge(df_stock[["SKU", "Stock"]], df_gomag, on="SKU", how="inner")
        df_diff = df_compare[df_compare["Stock"] != df_compare["GomagStock"]]

        updates = [
            {"code": row["SKU"], "stock": int(row["Stock"])}
            for _, row in df_diff.iterrows()
        ]

        return {"products": updates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/update-stock")
def update_stock(payload: dict):
    try:
        headers = {
            "Authorization": f"Bearer {GOMAG_API_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.put(GOMAG_API_URL, headers=headers, data=json.dumps(payload))
        return {"status": response.status_code, "response": response.json()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
