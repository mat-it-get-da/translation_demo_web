FROM node:20-slim AS builder

WORKDIR /app

# pnpm 설치
RUN npm install -g pnpm@10.18.1

# 빌드 인자 (API URL 및 백엔드 포트)
# 빈 문자열이면 상대 경로 사용 (Caddy 프록시 활용)
ARG VITE_API_BASE_URL=
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# 백엔드 포트 정보 (런타임에 사용)
ARG VITE_BACKEND_PORT=8000
ENV VITE_BACKEND_PORT=${VITE_BACKEND_PORT}

# Docker 환경에서는 base 경로를 빈 문자열로 설정 (루트 경로로 서빙)
ENV NODE_ENV=production
ENV SVELTE_BASE_PATH=

# 의존성 파일 복사
COPY frontend/package.json frontend/pnpm-lock.yaml ./

# 의존성 설치
RUN pnpm install --frozen-lockfile

# 소스 코드 복사
COPY frontend/ ./

# 빌드
RUN pnpm build

# Production stage
# 새로운 베이스 이미지로 전환 (이전 스테이지의 파일은 기본적으로 제거됨)
FROM caddy:2-alpine

# 이전 스테이지(builder)의 빌드 결과물을 복사
# COPY --from을 사용하면 이전 스테이지의 파일을 가져올 수 있음
COPY --from=builder /app/build /usr/share/caddy

# 빌드 결과물 확인 (디버깅용)
RUN ls -la /usr/share/caddy || echo "Warning: Build output directory is empty"

# Caddyfile 생성 스크립트 복사
COPY frontend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 포트 노출 (HTTP 80, HTTPS 443)
EXPOSE 80
EXPOSE 443

# Entrypoint 스크립트 실행 (환경 변수 기반 Caddyfile 생성)
ENTRYPOINT ["/entrypoint.sh"]
