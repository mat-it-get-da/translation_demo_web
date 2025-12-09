"""
FastAPI 번역 서버

OpenAI, Google Translate, DeepL을 지원하는 번역 API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

from .models_config import (
    AVAILABLE_MODELS,
    get_model_list,
    get_language_code,
)

# 번역기 모듈 import
from .translators import (
    translate_with_openai,
    translate_with_google,
    translate_with_deepl,
    translate_with_post_editor,
)

# 스키마 모델 import
from .schemas import (
    TranslationRequest,
    TranslationResponse,
    ModelProfile,
    ModelProfiles,
)

load_dotenv()

host = os.getenv("SERVER_HOST", "0.0.0.0")
port = int(os.getenv("SERVER_PORT", 8000))

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
        "http://localhost:5173",  # Vite Development Mode (default port)
        "http://localhost:4173",  # Vite Production Mode (default port)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/api/models", response_model=ModelProfiles)
async def get_models():
    """
    사용 가능한 모델 목록 반환

    Returns
    -------
    ModelProfiles
        모델 정보 리스트
    """
    models = get_model_list()
    return ModelProfiles(models=[ModelProfile(**model) for model in models])


@app.post("/api/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
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
            translated_text = await translate_with_deepl(
                request.text, source_lang, target_lang
            )

        elif provider == "post-editor":
            translated_text = await translate_with_post_editor(
                request.text,
                source_lang,
                target_lang,
            )

        elif provider == "openai":
            translated_text = await translate_with_openai(
                request.text,
                source_lang,
                target_lang,
                request.model,
            )

        else:
            raise HTTPException(
                status_code=400, detail=f"알 수 없는 provider: {provider}"
            )

        return TranslationResponse(
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
    print(f"서버 주소: http://{host}:{port}")
    print(f"API 문서: http://{host}:{port}/docs")
    print()

    uvicorn.run(app, host=host, port=port)
