# Project Wed - AI 번역 서비스

OpenAI API 기반의 다중 언어 번역 웹 애플리케이션입니다. GPT-3.5, GPT-4o Mini, GPT-4o 모델을 활용하여 고품질 번역을 제공합니다.

## 주요 기능

- 🌐 **다중 언어 지원**: 한국어, 영어, 일본어, 중국어, 스페인어, 프랑스어, 독일어
- 🤖 **OpenAI 모델 선택**: GPT-3.5 Turbo, GPT-4o Mini, GPT-4o
- ⚡ **실시간 번역**: 빠른 API 응답과 사용자 친화적인 UI
- 📊 **번역 히스토리**: 번역 기록 관리 및 시간 측정

## 시스템 요구사항

- **Python**: 3.8 이상
- **Node.js**: 16 이상
- **OpenAI API 키**: https://platform.openai.com/api-keys
- **패키지 매니저**: Rye (Python), pnpm (Node.js)

## 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/mat-it-get-da/translation_demo_web.git
cd translation_demo_web
```

### 2. 환경 변수 설정

OpenAI API 키를 설정합니다:

```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# .env 파일을 열고 실제 API 키 입력
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

**API 키 발급**: https://platform.openai.com/api-keys

⚠️ **주의**: `.env` 파일은 절대로 Git에 커밋하지 마세요! (`.gitignore`에 이미 추가되어 있습니다)

### 3. Python 백엔드 설정

```bash
# Rye가 설치되어 있지 않다면 먼저 설치
# https://rye-up.com/

# 의존성 설치
rye sync
```

### 4. 프론트엔드 설정

```bash
# frontend 디렉토리로 이동
cd frontend

# pnpm이 설치되어 있지 않다면 먼저 설치
# npm install -g pnpm

# 의존성 설치
pnpm install
```

## 실행 방법

### 1. 백엔드 API 서버 시작

터미널 1에서:

```bash
# 프로젝트 루트에서
rye run python -m backend.run_server
```

- **주소**: http://localhost:8001
- **API 문서**: http://localhost:8001/docs
- **역할**: OpenAI API를 사용한 번역 서비스

### 2. 프론트엔드 개발 서버 시작

터미널 2에서:

```bash
# frontend 디렉토리에서
cd frontend
pnpm dev
```

- **주소**: http://localhost:5173
- **역할**: 웹 UI 제공

## 사용 방법

1. 웹 브라우저에서 http://localhost:5173 접속
2. 원본 언어(Source Language) 선택
3. 목표 언어(Target Language) 선택
4. 사용할 AI 모델 선택
5. 번역할 텍스트 입력
6. "Translate" 버튼 클릭
7. 번역 결과 확인

## 프로젝트 구조

```
translation_demo_web/
├── backend/              # FastAPI 백엔드
│   ├── api.py           # API 엔드포인트
│   ├── models_config.py # 모델 설정
│   ├── schemas/         # API 스키마 모델
│   ├── translators/     # 번역기 모듈
│   └── run_server.py    # 서버 실행 스크립트
├── frontend/            # SvelteKit 프론트엔드
│   ├── src/
│   │   ├── components/  # UI 컴포넌트
│   │   └── routes/      # 페이지 라우트
│   └── package.json
├── .env                 # 환경 변수 (API 키, Git에 미포함)
├── .env.example         # 환경 변수 템플릿
├── .gitignore           # Git 제외 파일 목록
├── pyproject.toml       # Python 프로젝트 설정
└── README.md
```

## API 엔드포인트

### GET /api/models

사용 가능한 모델 목록 조회

**응답 예시:**
```json
{
  "models": [
    {
      "id": "gpt-3.5-turbo",
      "name": "GPT-3.5 Turbo",
      "description": "OpenAI의 가성비 좋은 모델 - 빠른 응답 속도"
    },
    {
      "id": "gpt-4o-mini",
      "name": "GPT-4o Mini",
      "description": "OpenAI의 빠르고 저렴한 최신 모델 - 번역에 최적화"
    }
  ]
}
```

### POST /api/translate

텍스트 번역

**요청 예시:**
```json
{
  "text": "Hello, world!",
  "source_lang": "en",
  "target_lang": "ko",
  "model": "gpt-4o-mini"
}
```

**응답 예시:**
```json
{
  "translated_text": "안녕하세요, 세상!",
  "model": "gpt-4o-mini",
  "source_lang": "en",
  "target_lang": "ko"
}
```

## 문제 해결

### OpenAI API 키 오류

```
Error: OpenAI 클라이언트가 초기화되지 않았습니다
```

**해결방법:**
- `.env` 파일이 프로젝트 루트에 있는지 확인
- `OPENAI_API_KEY`가 올바르게 설정되었는지 확인
- API 키 형식: `sk-...`로 시작
- API 키 재발급: https://platform.openai.com/api-keys

### API 사용량 초과

```
Error: You exceeded your current quota
```

**해결방법:**
- OpenAI 대시보드에서 사용량 확인: https://platform.openai.com/usage
- 결제 방법 추가 또는 크레딧 충전
- 사용량 제한 설정: https://platform.openai.com/account/limits

### 포트 충돌

**해결방법:**
- 포트 8001, 5173이 사용 중이지 않은지 확인
- 다른 포트를 사용하려면 코드에서 포트 번호 변경

## 개발

### 백엔드 테스트

```bash
# API 문서에서 직접 테스트
# http://localhost:8001/docs
```

### 프론트엔드 테스트

```bash
cd frontend
pnpm test
```

### 프로덕션 빌드

```bash
# 프론트엔드 빌드
cd frontend
pnpm build

# 빌드 결과 미리보기
pnpm preview
```

## 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 라이선스

이 프로젝트의 라이선스 정보를 여기에 추가하세요.

## 문의

프로젝트 관련 문의사항이 있으시면 이슈를 등록해주세요.
