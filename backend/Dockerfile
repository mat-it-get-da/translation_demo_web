FROM ubuntu:22.04

# 쉘을 bash로 고정
SHELL ["/bin/bash", "-c"]

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    python3 \
    python3-pip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# uv가 제대로 설치되었는지 확인
RUN uv --version

# 프로젝트 파일 복사
COPY pyproject.toml requirements.lock README.md ./

# uv를 사용하여 의존성 설치 (가상 환경 생성)
RUN uv sync

# 애플리케이션 코드 복사
COPY backend/ ./backend/

# 환경 변수
ENV PYTHONPATH=/app
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=8000

# 포트 노출
EXPOSE 8000

# 헬스체크용 curl 설치 확인
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# uv를 사용하여 서버 실행 (uv run은 가상 환경을 자동으로 활성화)
CMD ["uv", "run", "python", "-m", "backend.run_server"]

