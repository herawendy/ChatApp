# Simple Full Stack Render Demo

這是一個給初學者使用的前後端教學專案。

## 專案結構

```text
simple-fullstack-render-demo/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── backend/
    ├── main.py
    └── requirements.txt
```

## 1. 啟動 Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

打開：

```text
http://127.0.0.1:8000
```

FastAPI Docs：

```text
http://127.0.0.1:8000/docs
```

## 2. 啟動 Frontend

可以使用 VS Code 的 Live Server 開啟：

```text
frontend/index.html
```

## 3. 部署 Render 後

Render Backend 會給你公開 URL，例如：

```text
https://your-service.onrender.com
```

請修改：

```text
frontend/script.js
```

把：

```javascript
const API_URL = "http://127.0.0.1:8000";
```

改成：

```javascript
const API_URL = "https://your-service.onrender.com";
```

再把 frontend 部署到 GitHub Pages。

## Render 設定

Root Directory:

```text
backend
```

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 建議上課方式

不要從零讓學生逐字輸入所有程式。

推薦：

1. 先解壓縮
2. 成功跑起來
3. 講 `index.html`
4. 講 `script.js` 的 `fetch()`
5. 講 `main.py` 的 API
6. 改一個小功能
7. 交給 Codex / Copilot 再加功能
8. 最後部署到 GitHub Pages + Render
