from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 編繩類型和倍數（基於72號玉線）
KNOT_MULTIPLIERS = {
    "二股辮": 2,
    "四股辮": 2,
    "六股辮": 2,
    "八股辮": 2,
    "十股辮": 2,
    "雙鎖結": 2,
    "蛇結": 9,
    "金剛結": 10,
    "單向平結": 10,
    "雙向平結": 10,
    "玉米結": 10
}

# 線型調整係數（相對於72號玉線）
THREAD_ADJUSTMENTS = {
    "72號玉線": 1.0,
    "A線": 1.1,      # 比72號粗，需要增加10%
    "B線": 1.05,     # 比72號略粗，需要增加5%
    "0.8mm": 0.9,    # 比72號細，需要減少10%
    "1mm": 1.0,      # 相當於72號
    "1.2mm": 1.15    # 比72號粗，需要增加15%
}

# 握持余量（厘米）
GRIP_LENGTH = 17  # 15-20厘米的中值

class CalculatorRequest(BaseModel):
    bracelet_length: float  # 手圈長度（公分）
    knot_type: str          # 編繩類型
    thread_type: str        # 線型
    is_heart_snake: bool = False  # 是否為包心蛇結

class CalculatorResponse(BaseModel):
    success: bool
    bracelet_length: float
    knot_type: str
    thread_type: str
    base_length: float      # 基礎線長（不含握持餘量）
    final_length: float     # 最終線長（含握持餘量）
    per_thread_length: float  # 每條線的長度
    message: str

@app.get("/")
def home():
    return {
        "message": "編繩長度計算器已就緒！"
    }

@app.post("/api/calculate")
def calculate_rope_length(data: CalculatorRequest):
    """
    計算編繩所需的線長
    
    計算邏輯：
    1. 基礎線長 = 手圈長度 × 編繩類型倍數 × 線型調整係數
    2. 最終線長 = 基礎線長 + 握持餘量
    3. 每條線長 = 最終線長（大多數編繩由2條線組成）
    """
    
    try:
        # 验证漢子
        if data.bracelet_length <= 0:
            return {
                "success": False,
                "message": "手圈長度必須大於0"
            }
        
        if data.knot_type not in KNOT_MULTIPLIERS:
            return {
                "success": False,
                "message": f"不支持的編繩類型: {data.knot_type}"
            }
        
        if data.thread_type not in THREAD_ADJUSTMENTS:
            return {
                "success": False,
                "message": f"不支持的線型: {data.thread_type}"
            }
        
        # 獲取倍數和調整係數
        multiplier = KNOT_MULTIPLIERS[data.knot_type]
        adjustment = THREAD_ADJUSTMENTS[data.thread_type]
        
        # 計算基礎線長
        base_length = data.bracelet_length * multiplier * adjustment
        
        # 如果是包心蛇結，額外增加20%
        if data.is_heart_snake and data.knot_type == "蛇結": 
            base_length *= 1.2
        
        # 加上握持餘量
        final_length = base_length + GRIP_LENGTH
        
        # 每條線的長度（大多數編繩由2條線組成）
        per_thread_length = final_length / 2
        
        # 生成說明資訊
        message = f"需要剪2條各{per_thread_length:.1f}cm的{data.thread_type}，共{final_length:.1f}cm"
        if data.is_heart_snake and data.knot_type == "蛇結": 
            message += "（已加上包心蛇結的增加量）"
        
        return CalculatorResponse(
            success=True,
            bracelet_length=data.bracelet_length,
            knot_type=data.knot_type,
            thread_type=data.thread_type,
            base_length=round(base_length, 1),
            final_length=round(final_length, 1),
            per_thread_length=round(per_thread_length, 1),
            message=message
        ).dict()
        
    except Exception as e:
        return {
            "success": False,
            "message": f"計算出錯: {str(e)}"
        }

@app.get("/api/knot-types")
def get_knot_types():
    """獲取所有支持的編繩類型"""
    return {
        "knot_types": list(KNOT_MULTIPLIERS.keys())
    }

@app.get("/api/thread-types")
def get_thread_types():
    """獲取所有支持的線型"""
    return {
        "thread_types": list(THREAD_ADJUSTMENTS.keys())
    }
