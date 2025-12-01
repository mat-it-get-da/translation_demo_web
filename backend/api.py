"""
FastAPI 번역 서버

Lemonade Server를 사용한 번역 API 서버
"""

import os
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.models_config import (
    get_model_list,
    get_full_model_name,
    get_language_code,
    get_language_name,
)

# FastAPI 앱 초기화
app = FastAPI(
    title="Translation API",
    description="Lemonade Server 기반 번역 API",
    version="1.0.0",
)

# CORS 설정 (프론트엔드 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:5174",
        "https://mat-it-get-da.github.io",  # GitHub Pages
    ],  # Vite 기본 포트 + GitHub Pages
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lemonade Server 클라이언트 초기화
try:
    lemonade_client = OpenAI(
        base_url="http://localhost:8000/api/v1",
        api_key="lemonade"  # required but unused
    )
    print("[OK] Lemonade Server 클라이언트 초기화 성공")
    print("[INFO] Lemonade Server: http://localhost:8000")
except Exception as e:
    print(f"[ERROR] Lemonade Server 클라이언트 초기화 실패: {e}")
    lemonade_client = None


# Request/Response 모델
class TranslateRequest(BaseModel):
    """번역 요청 모델"""
    text: str = Field(..., description="번역할 텍스트", min_length=1)
    source_lang: str = Field(..., description="원본 언어 (예: 'en', 'ko')")
    target_lang: str = Field(..., description="목표 언어 (예: 'en', 'ko')")
    model: str = Field(..., description="사용할 모델 ID")


class TranslateResponse(BaseModel):
    """번역 응답 모델"""
    translated_text: str = Field(..., description="번역된 텍스트")
    model: str = Field(..., description="사용된 모델 ID")
    source_lang: str = Field(..., description="원본 언어")
    target_lang: str = Field(..., description="목표 언어")


class ModelInfo(BaseModel):
    """모델 정보 모델"""
    id: str
    name: str
    description: str


class ModelsResponse(BaseModel):
    """모델 목록 응답 모델"""
    models: list[ModelInfo]


# API 엔드포인트
@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Translation API",
        "version": "1.0.0",
        "endpoints": {
            "models": "/api/models",
            "translate": "/api/translate",
        },
    }


@app.get("/api/models", response_model=ModelsResponse)
async def get_models():
    """
    사용 가능한 모델 목록 반환
    
    Returns
    -------
    ModelsResponse
        모델 정보 리스트
    """
    models = get_model_list()
    return ModelsResponse(models=[ModelInfo(**model) for model in models])


@app.post("/api/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """
    텍스트 번역
    
    Parameters
    ----------
    request : TranslateRequest
        번역 요청 데이터
    
    Returns
    -------
    TranslateResponse
        번역 결과
    
    Raises
    ------
    HTTPException
        번역 실패 시
    """
    # Lemonade 클라이언트 확인
    if lemonade_client is None:
        raise HTTPException(
            status_code=500,
            detail="Lemonade Server 클라이언트가 초기화되지 않았습니다. 서버를 확인하세요.",
        )
    
    # 모델명 확인 및 검증
    try:
        model_name = get_full_model_name(request.model)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # 언어 코드 처리 (전체 이름이 들어올 경우 변환)
    source_lang = get_language_code(request.source_lang)
    target_lang = get_language_code(request.target_lang)
    
    # 언어 전체 이름 가져오기
    source_name = get_language_name(source_lang)
    target_name = get_language_name(target_lang)
    
    # 번역 프롬프트 생성
    system_prompt = f"""You are a professional translator. Translate the given text from {source_name} to {target_name}.
Provide ONLY the translated text without any explanations or additional comments."""

    user_message = f"Translate this text to {target_name}:\n\n{request.text}"
    
    # API 호출
    try:
        response = lemonade_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,  # 번역은 창의성이 덜 필요하므로 낮게
            max_tokens=512,  # 번역에는 충분한 길이
        )
        
        translated_text = response.choices[0].message.content.strip()
        
        return TranslateResponse(
            translated_text=translated_text,
            model=request.model,
            source_lang=source_lang,
            target_lang=target_lang,
        )
    
    except Exception as e:
        error_msg = str(e)
        
        # 에러 메시지 파싱
        if "NOT_FOUND" in error_msg or "not found" in error_msg.lower():
            raise HTTPException(
                status_code=404,
                detail=f"모델을 찾을 수 없습니다: {model_name}. Lemonade Server에서 모델을 다운로드했는지 확인하세요.",
            )
        elif "Connection" in error_msg or "connect" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Lemonade Server에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요 (http://localhost:8000)",
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"번역 중 오류 발생: {error_msg}",
            )


@app.get("/health")
async def health_check():
    """
    헬스 체크 엔드포인트
    
    Returns
    -------
    dict
        서버 상태 정보
    """
    return {
        "status": "healthy",
        "lemonade_client": "initialized" if lemonade_client else "not initialized",
        "lemonade_server": "http://localhost:8000",
    }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 80)
    print("FastAPI 번역 서버 시작 (Lemonade Server 기반)")
    print("=" * 80)
    print()
    print("서버 주소: http://localhost:8001")
    print("API 문서: http://localhost:8001/docs")
    print()
    print("[INFO] Lemonade Server (http://localhost:8000)가 실행 중이어야 합니다.")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8001)

