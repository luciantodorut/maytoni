# Maytoni Gomag Stock Sync

Aplicație FastAPI care:
- descarcă automat feed-ul Maytoni (CSV)
- compară stocurile cu Gomag
- trimite actualizări prin API

## Pornire locală

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

API-ul pornește pe `http://localhost:8000`

## Variabile de mediu

Creează un fișier `.env`:

```
GOMAG_API_TOKEN=tokenul_tău_real
```
