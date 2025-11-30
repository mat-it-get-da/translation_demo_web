"""
FastAPI 서버 실행 스크립트

Lemonade Server 기반 번역 API 서버를 실행합니다.

실행 방법:
    rye run python -m backend.run_server
    또는
    rye run python backend/run_server.py

주의사항:
    - Lemonade Server가 http://localhost:8000에서 실행 중이어야 합니다
    - 사용할 모델을 미리 다운로드해야 합니다:
      lemonade-server pull Qwen3-4B-Instruct-2507-GGUF
      lemonade-server pull Gemma-3-4b-it-GGUF
      lemonade-server pull gpt-oss-20b-mxfp4-GGUF
"""

import uvicorn

if __name__ == "__main__":
    print("=" * 80)
    print("FastAPI 번역 서버 시작 (Lemonade Server 기반)")
    print("=" * 80)
    print()
    print("📍 서버 정보:")
    print("  - 번역 API 서버: http://localhost:8001")
    print("  - API 문서: http://localhost:8001/docs")
    print("  - Interactive API: http://localhost:8001/redoc")
    print()
    print("📡 사용 가능한 엔드포인트:")
    print("  - GET  /api/models    - 모델 목록 조회")
    print("  - POST /api/translate - 텍스트 번역")
    print("  - GET  /health        - 헬스 체크")
    print()
    print("⚙️  Lemonade Server:")
    print("  - 주소: http://localhost:8000")
    print("  - 포트 8000은 Lemonade Server 전용")
    print("  - 포트 8001은 번역 API 서버 전용")
    print()
    print("⚠️  시작 전 확인사항:")
    print("  1. Lemonade Server가 실행 중인지 확인")
    print("  2. 사용할 모델이 다운로드되어 있는지 확인")
    print()
    print("서버를 중지하려면 Ctrl+C를 누르세요.")
    print("=" * 80)
    print()
    
    uvicorn.run(
        "backend.api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,  # 코드 변경 시 자동 재시작
        log_level="info",
    )

