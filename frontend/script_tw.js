// API 地址
// 本機測試先用 localhost。
// 部署 Render 後，把這裡改成你的公開 Render URL。
const API_URL = "https://chatapp-1-4y1r.onrender.com";

// 獲取 DOM 元素
const calculateBtn = document.getElementById("calculateBtn");
const resetBtn = document.getElementById("resetBtn");
const braceletLengthInput = document.getElementById("braceletLength");
const knotTypeSelect = document.getElementById("knotType");
const threadTypeSelect = document.getElementById("threadType");
const isHeartSnakeCheckbox = document.getElementById("isHeartSnake");
const resultSection = document.getElementById("resultSection");
const errorMessage = document.getElementById("errorMessage");

// 綁定事件
calculateBtn.addEventListener("click", handleCalculate);
resetBtn.addEventListener("click", handleReset);

// 按 Enter 鍵也能計算
braceletLengthInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        handleCalculate();
    }
});

/**
 * 處理計算按鈕點擊
 */
async function handleCalculate() {
    // 獲取輸入值
    const braceletLength = parseFloat(braceletLengthInput.value);
    const knotType = knotTypeSelect.value;
    const threadType = threadTypeSelect.value;
    const isHeartSnake = isHeartSnakeCheckbox.checked;

    // 驗證輸入
    if (!braceletLength || braceletLength <= 0) {
        showError("請輸入有效的手圈長度（大於0）");
        return;
    }

    if (!knotType) {
        showError("請選擇編繩類型");
        return;
    }

    if (!threadType) {
        showError("請選擇線型");
        return;
    }

    // 禁用按鈕，顯示加載狀態
    calculateBtn.disabled = true;
    calculateBtn.innerText = "⏳ 計算中...";
    errorMessage.style.display = "none";

    try {
        // 呼叫後端 API
        const response = await fetch(`${API_URL}/api/calculate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                bracelet_length: braceletLength,
                knot_type: knotType,
                thread_type: threadType,
                is_heart_snake: isHeartSnake
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            // 顯示結果
            displayResult(data);
        } else {
            showError(data.message || "計算失敗，請檢查輸入");
        }
    } catch (error) {
        console.error("Error:", error);
        showError("無法連接到後端服務，請檢查網路或稍後重試");
    } finally {
        // 恢復按鈕狀態
        calculateBtn.disabled = false;
        calculateBtn.innerText = "📐 計算所需線長";
    }
}

/**
 * 顯示計算結果
 */
function displayResult(data) {
    document.getElementById("resultBracelet").innerText = data.bracelet_length;
    document.getElementById("resultKnot").innerText = data.knot_type;
    document.getElementById("resultThread").innerText = data.thread_type;
    document.getElementById("resultBase").innerText = data.base_length;
    document.getElementById("resultFinal").innerText = data.final_length;
    document.getElementById("resultPerThread").innerText = data.per_thread_length;
    document.getElementById("resultMessage").innerText = data.message;

    resultSection.style.display = "block";
    errorMessage.style.display = "none";

    // 平滑滾動到結果
    resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

/**
 * 顯示錯誤資訊
 */
function showError(message) {
    errorMessage.innerText = "❌ " + message;
    errorMessage.style.display = "block";
    resultSection.style.display = "none";
}

/**
 * 重置表單
 */
function handleReset() {
    braceletLengthInput.value = "20";
    knotTypeSelect.value = "";
    threadTypeSelect.value = "";
    isHeartSnakeCheckbox.checked = false;
    resultSection.style.display = "none";
    errorMessage.style.display = "none";
    braceletLengthInput.focus();
}