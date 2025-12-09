"""
FastAPI 서버 실행 스크립트

OpenAI API 기반 번역 API 서버를 실행합니다.

실행 방법:
    uv run python -m backend.run_server
    또는
    uv run python backend/run_server.py

주의사항:
    - .env 파일에 OPENAI_API_KEY가 설정되어 있어야 합니다
    - API 키 발급: https://platform.openai.com/api-keys
"""

import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("SERVER_HOST", "0.0.0.0")
port = int(os.getenv("SERVER_PORT", 8000))

if __name__ == "__main__":
    print("=" * 80)
    print("FastAPI 번역 서버 시작 (OpenAI API 기반)")
    print("=" * 80)
    print()
    print("📍 서버 정보:")
    print(f"  - 번역 API 서버: http://{host}:{port}")
    print(f"  - API 문서: http://{host}:{port}/docs")
    print(f"  - Interactive API: http://{host}:{port}/redoc")
    print()
    print("📡 사용 가능한 엔드포인트:")
    print("  - GET  /api/models    - 모델 목록 조회")
    print("  - POST /api/translate - 텍스트 번역")
    print("  - GET  /health        - 헬스 체크")
    print()
    print("⚙️  OpenAI API:")
    print("  - 사용 모델: GPT-3.5 Turbo, GPT-4o Mini, GPT-4o")
    print("  - API 키는 .env 파일에서 로드됩니다")
    print()
    print("⚠️  시작 전 확인사항:")
    print("  1. .env 파일에 OPENAI_API_KEY가 설정되어 있는지 확인")
    print("  2. API 키 발급: https://platform.openai.com/api-keys")
    print()
    print("서버를 중지하려면 Ctrl+C를 누르세요.")
    print("=" * 80)
    print()

    # 프로덕션 환경에서는 reload 비활성화
    reload = os.getenv("ENV", "production") == "development"

    uvicorn.run(
        "backend.api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
