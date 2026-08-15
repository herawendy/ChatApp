# 用 GitHub 和 Render 部署前後端：初學者教學

這份文件使用目前的 ChatApp 專案當例子，說明如何把原本只能在自己電腦運行的網站，放到網路上讓其他人可以開啟。

## 1. 先用一句話理解整件事

你的網站分成兩個部分：

- **前端（frontend）**：使用者在瀏覽器看到、可以輸入訊息和按按鈕的畫面。
- **後端（backend）**：收到前端送來的資料後，用 Python 處理並回覆資料的程式。

它們的分工像這樣：

```text
使用者瀏覽器
    ↓ 開啟網頁
Render 前端網站
    ↓ fetch() 送出訊息
Render 後端 API（FastAPI）
    ↓ 回傳 JSON
Render 前端網站顯示回覆
```

## 2. GitHub、Render 分別做什麼？

### GitHub：存放程式碼的雲端倉庫

GitHub 就像程式碼的雲端硬碟，但它會記錄每一次的修改。

本專案的 GitHub repository：

<https://github.com/herawendy/ChatApp>

把程式碼推到 GitHub 的好處：

- 電腦壞掉時，程式碼不會只留在本機。
- 可以看到每次修改的歷史紀錄。
- Render 可以從 GitHub 讀取程式碼並自動部署。

### Render：把程式真正跑在網路上的平台

Render 會從 GitHub 下載程式碼，在它的伺服器安裝套件並啟動網站。

本專案有兩個 Render 服務：

- 後端 Web Service：<https://chatapp-1-4y1r.onrender.com/>
- 前端 Static Site：<https://chatapp-frontend-herawendy.onrender.com/>

## 3. 專案資料夾的意思

```text
ChatApp/
├── backend/                 # Python / FastAPI 後端
│   ├── main.py              # API 程式
│   └── requirements.txt     # 後端需要安裝的套件
├── frontend/                # 網頁前端
│   ├── index.html           # 網頁骨架
│   ├── style.css            # 外觀與排版
│   └── script.js            # 按鈕、fetch() 和畫面互動
└── GitHub與Render部署教學.md
```

## 4. 本機開發時為什麼能用？

在自己的電腦測試時：

- 前端通常在 `http://127.0.0.1:5500`
- 後端通常在 `http://127.0.0.1:8000`

`127.0.0.1` 又叫做 `localhost`，意思是「這一台電腦自己」。

因此本機可以用，不代表別人的電腦可以用。別人打開自己的 `127.0.0.1`，只會連到**他自己的電腦**，不是連到你的後端。這就是為什麼需要部署到 Render。

## 5. 第一步：把專案推到 GitHub

第一次把專案交給 GitHub 時，在專案最外層資料夾執行：

```bash
git init -b main
git add .
git commit -m "Initial full-stack application"
git remote add origin https://github.com/herawendy/ChatApp.git
git push -u origin main
```

### 指令的白話意思

| 指令 | 意思 |
| --- | --- |
| `git init -b main` | 讓這個資料夾開始使用 Git，主要分支叫 `main`。 |
| `git add .` | 選擇要記錄的檔案。 |
| `git commit -m "..."` | 建立一個有說明文字的存檔點。 |
| `git remote add origin ...` | 告訴 Git 這個專案要連到哪一個 GitHub repository。 |
| `git push -u origin main` | 把本機的 `main` 分支上傳到 GitHub。 |

之後每次修改程式並確認可用後，使用：

```bash
git add .
git commit -m "說明這次修改了什麼"
git push
```

> 注意：不要把密碼、API key、`.env` 檔案或本機資料庫密碼推到 GitHub。這些內容應放入 `.gitignore`，並在 Render 的 Environment Variables 設定。

## 6. 第二步：部署後端到 Render

後端不是單純的檔案，它需要一直執行 Python，因此在 Render 要建立 **Web Service**。

### 建立步驟

1. 到 Render Dashboard，選擇 **New → Web Service**。
2. 連接 GitHub，選擇 `herawendy/ChatApp`。
3. 設定以下欄位：

```text
Branch: main
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

4. 按下 **Create Web Service**。

### 為什麼要這樣填？

- `Root Directory: backend`：告訴 Render 後端程式在 `backend` 資料夾，而不是專案最外層。
- `pip install -r requirements.txt`：安裝 FastAPI 和 Uvicorn。
- `uvicorn main:app ...`：啟動 `main.py` 中叫做 `app` 的 FastAPI 程式。
- `$PORT`：Render 自動提供的連接埠號碼。不要寫死成 `8000`。
- `0.0.0.0`：讓 Render 外部網路可以連到這個後端。

### 如何確認後端成功？

開啟：

<https://chatapp-1-4y1r.onrender.com/>

應該看見：

```json
{"message":"Backend is running!"}
```

也可以開啟 FastAPI 自動產生的 API 說明頁：

<https://chatapp-1-4y1r.onrender.com/docs>

## 7. 第三步：讓前端知道後端在哪裡

前端原本在本機找後端：

```js
const API_URL = "http://127.0.0.1:8000";
```

部署後，必須改成 Render 後端的公開網址：

```js
const API_URL = "https://chatapp-1-4y1r.onrender.com";
```

這段在 `frontend/script.js`。前端送出訊息時，實際上會執行：

```js
fetch(`${API_URL}/api/message`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: message })
});
```

所以最後會呼叫：

```text
https://chatapp-1-4y1r.onrender.com/api/message
```

改完後要重新推送到 GitHub：

```bash
git add frontend/script.js
git commit -m "Configure frontend for Render API"
git push
```

## 8. 第四步：部署前端到 Render

HTML、CSS、JavaScript 是不需要 Python 一直執行的靜態檔案，因此在 Render 要建立 **Static Site**，不是 Web Service。

### 建立步驟

1. 到 Render Dashboard，選擇 **New → Static Site**。
2. 選擇 `herawendy/ChatApp`。
3. 填寫：

```text
Branch: main
Root Directory: frontend
Build Command: echo "No build step"
Publish Directory: .
```

4. 按下 **Create Static Site**。

### 為什麼 Publish Directory 是 `.`？

因為 Root Directory 已經是 `frontend`。

`.` 的意思是「目前這個資料夾」，也就是：

```text
frontend/
```

裡面已經有網頁入口 `index.html`，所以 Render 可以直接發布它。

## 9. CORS 是什麼？為什麼前後端可以互相呼叫？

部署後，前端和後端的網址不同：

```text
前端：https://chatapp-frontend-herawendy.onrender.com
後端：https://chatapp-1-4y1r.onrender.com
```

瀏覽器會保護使用者，不會隨便讓一個網站呼叫另一個網站的 API。這個規則叫做 CORS。

在 `backend/main.py` 中，這個專案已加入：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

`allow_origins=["*"]` 的意思是暫時允許任何網站呼叫後端，適合初學練習。正式產品通常應改成只允許自己的前端網址。

## 10. 資料庫現在需要嗎？

**目前不需要。**

現在的聊天程式只會收到訊息、立刻回覆，不會保存聊天紀錄。重新整理網頁後，訊息就不見了，因為沒有資料庫。

等你想做下面功能時，才需要新增資料庫：

- 儲存聊天紀錄
- 登入帳號與密碼
- 使用者個人資料
- 文章、商品、訂單等資料

屆時可在 Render 建立 PostgreSQL，並把資料庫連線字串放到 Render 的 Environment Variables，而不是寫在程式碼裡。

## 11. 這次遇到的常見錯誤

### 錯誤一：Render 使用 `gunicorn your_application.wsgi`

這代表 Render 沒有拿到正確的 Start Command，誤以為是 Django 專案。

解法：

```text
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 錯誤二：`uvicorn: command not found`

這通常表示 Render 不在 `backend` 資料夾執行建置，沒有讀到正確的 `requirements.txt`。

解法：確認：

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
```

然後執行 **Manual Deploy → Clear build cache & deploy**。

### 錯誤三：`Root directory " frontend" does not exist`

`frontend` 前面多了一個空白字元。

解法：清空 Root Directory 欄位，重新手動輸入：

```text
frontend
```

前後都不要有空白。

### 錯誤四：Static Site 出現 Start Command

你可能選成 **Web Service** 了。

解法：前端要選 **New → Static Site**，Static Site 不需要 Start Command。

## 12. 未來修改網站的標準流程

```text
1. 在本機修改程式
2. 本機測試功能
3. git add / commit / push 到 GitHub
4. Render 偵測到 main 有新提交
5. Render 自動重新部署後端或前端
6. 開啟 Render 網址測試
```

因此，GitHub 是「程式碼的版本倉庫」，Render 是「把程式實際發布到網路的地方」。兩者一起使用，就完成了前後端部署。

## 13. 最後檢查清單

- [x] GitHub 有完整的 `backend/` 與 `frontend/` 程式碼
- [x] Render Web Service 使用 `backend` 作為 Root Directory
- [x] 後端使用 Uvicorn 啟動
- [x] `frontend/script.js` 使用 Render 後端網址
- [x] Render Static Site 使用 `frontend` 作為 Root Directory
- [x] 前端可送出訊息並收到後端回覆
- [ ] 資料庫：目前尚未需要

