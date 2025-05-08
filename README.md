# Maytoni Sync API

Un mic serviciu FastAPI care:
- preia feed-ul de stoc de la Maytoni
- compară cu datele actuale Gomag
- afișează diferențele
- trimite update automat prin API Gomag

## Comenzi locale

```bash
uvicorn main:app --reload
```

Accesează:
- http://localhost:8000/docs — documentație interactivă
- http://localhost:8000/api/check-stock — diferențe de stoc
