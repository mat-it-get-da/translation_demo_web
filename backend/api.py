"""
FastAPI 번역 서버

OpenAI, Google Translate, DeepL을 지원하는 번역 API
"""

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.models_config import (
    AVAILABLE_MODELS,
    get_model_list,
    get_language_code,
    get_language_name,
)

# 번역기 모듈 import
from backend.translators import (
    translate_with_openai,
    translate_with_google,
    translate_with_deepl,
    translate_with_post_editor,
    init_deepl_client,
)

# DeepL 클라이언트 초기화
init_deepl_client()

# FastAPI 앱 초기화
app = FastAPI(
    title="Translation API",
    description="OpenAI, Google Translate, DeepL 번역 서비스",
    version="3.0.0",
)

# CORS 설정 (프론트엔드 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:5174",
        "https://mat-it-get-da.github.io",  # GitHub Pages
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        "version": "3.0.0",
        "providers": ["OpenAI", "Google Translate", "DeepL"],
        "endpoints": {
            "models": "/api/models",
            "translate": "/api/translate",
            "health": "/health",
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
    텍스트 번역 - OpenAI, Google Translate, DeepL 지원

    모델에 따라 자동으로 적절한 번역 엔진을 선택합니다.

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
    # 모델 유효성 검사
    if request.model not in AVAILABLE_MODELS:
        raise HTTPException(
            status_code=400, detail=f"지원하지 않는 모델입니다: {request.model}"
        )

    # 모델 정보 가져오기
    model_info = AVAILABLE_MODELS[request.model]
    provider = model_info.get("provider", "openai")

    # 언어 코드 처리
    source_lang = get_language_code(request.source_lang)
    target_lang = get_language_code(request.target_lang)

    try:
        # Provider별 번역 처리
        if provider == "google":
            translated_text = await translate_with_google(
                request.text, source_lang, target_lang
            )

        elif provider == "deepl":
            translated_text = translate_with_deepl(
                request.text, source_lang, target_lang
            )

        elif provider == "post-editor":
            source_name = get_language_name(source_lang)
            target_name = get_language_name(target_lang)
            translated_text = await translate_with_post_editor(
                request.text,
                source_lang,
                target_lang,
                source_name,
                target_name,
            )

        elif provider == "openai":
            source_name = get_language_name(source_lang)
            target_name = get_language_name(target_lang)
            translated_text = translate_with_openai(
                request.text,
                source_lang,
                target_lang,
                request.model,
                source_name,
                target_name,
            )

        else:
            raise HTTPException(
                status_code=400, detail=f"알 수 없는 provider: {provider}"
            )

        return TranslateResponse(
            translated_text=translated_text,
            model=request.model,
            source_lang=source_lang,
            target_lang=target_lang,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"번역 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    print("=" * 80)
    print("FastAPI 번역 서버 시작 (OpenAI + Google + DeepL)")
    print("=" * 80)
    print()
    print("서버 주소: http://localhost:8001")
    print("API 문서: http://localhost:8001/docs")
    print()

    uvicorn.run(app, host="0.0.0.0", port=8001)
