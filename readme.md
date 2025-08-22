uvicorn app:app --reload --port 8000

http://127.0.0.1:8000/docs

curl -X POST "http://127.0.0.1:8000/search" ^
     -H "Content-Type: application/json" ^
     -d "{\"query\":\"Mức phạt khi vượt đèn đỏ\"}"