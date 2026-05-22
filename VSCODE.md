# VS Code ma run garne tarika

## 1. First time setup

1. VS Code ma project folder khola: `Sara Worldwide Chatbot`
2. Extension install: **Python** (Microsoft)
3. Terminal → **Run Task** → **First-time setup (venv + deps + DB)**

## 2. Run app (F5)

1. **Run and Debug** panel (Ctrl+Shift+D)
2. Dropdown bata chānnu: **FastAPI: Run Backend**
3. **F5** dabāunus

MySQL Docker auto start huncha (`preLaunchTask`).

4. Browser: http://localhost:8000

## 3. Aru launch options

| Name | Ke garcha |
|------|-----------|
| **FastAPI: Run Backend** | MySQL Docker + API server |
| **FastAPI: Run Backend (no Docker)** | MySQL pahile nai chaliraheko cha bhane |
| **Setup Database (seed)** | Products/images DB ma update |

## 4. `.env` check

`backend/.env` ma:

```env
DB_HOST=127.0.0.1
DB_PASSWORD=sara_root_password
DB_NAME=sara_chatbot_db
```

## 5. URLs

- Homepage: http://localhost:8000
- Products: http://localhost:8000/products.html
- API: http://localhost:8000/api/products
