# Project Wed - AI 번역 서비스

Lemonade Server 기반의 다중 언어 번역 웹 애플리케이션입니다. 여러 오픈소스 LLM 모델을 활용하여 고품질 번역을 제공합니다.

## 주요 기능

- 🌐 **다중 언어 지원**: 한국어, 영어, 일본어, 중국어, 스페인어, 프랑스어, 독일어
- 🤖 **다중 모델 선택**: Qwen3-4B, Gemma-3-4B, GPT-OSS-20B 등 여러 모델 지원
- ⚡ **실시간 번역**: 빠른 응답 속도와 사용자 친화적인 UI
- 📊 **번역 히스토리**: 번역 기록 관리 및 시간 측정

## 시스템 요구사항

- **Python**: 3.8 이상
- **Node.js**: 16 이상
- **Lemonade Server**: LLM 추론 엔진
- **패키지 매니저**: Rye (Python), pnpm (Node.js)

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd Project_Wed
```

### 2. Lemonade Server 설치 및 실행

Lemonade Server는 LLM 모델을 로컬에서 실행하기 위한 추론 엔진입니다.

```bash
# Lemonade Server 설치 (방법은 공식 문서 참조)
# https://github.com/lemonade-hq/lemonade-server

# Lemonade Server 실행 (포트 8000)
lemonade-server serve
```

### 3. 모델 다운로드

사용할 LLM 모델을 Lemonade Server에 다운로드합니다:

```bash
# Qwen3 4B 모델
lemonade-server pull Qwen3-4B-Instruct-2507-GGUF

# Gemma 3 4B 모델
lemonade-server pull Gemma-3-4b-it-GGUF

# GPT-OSS 20B 모델 (대용량)
lemonade-server pull gpt-oss-20b-mxfp4-GGUF
```

### 4. Python 백엔드 설정

```bash
# Rye가 설치되어 있지 않다면 먼저 설치
# https://rye-up.com/

# 의존성 설치
rye sync
```

### 5. 프론트엔드 설정

```bash
# my-app 디렉토리로 이동
cd my-app

# pnpm이 설치되어 있지 않다면 먼저 설치
# npm install -g pnpm

# 의존성 설치
pnpm install
```

## 실행 방법

### 1. Lemonade Server 시작

터미널 1에서:

```bash
lemonade-server serve
```

- **주소**: http://localhost:8000
- **역할**: LLM 모델 추론 엔진

### 2. 백엔드 API 서버 시작

터미널 2에서:

```bash
# 프로젝트 루트에서
rye run python -m backend.run_server
```

- **주소**: http://localhost:8001
- **API 문서**: http://localhost:8001/docs
- **역할**: 번역 API 제공

### 3. 프론트엔드 개발 서버 시작

터미널 3에서:

```bash
# my-app 디렉토리에서
cd my-app
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
Project_Wed/
├── backend/              # FastAPI 백엔드
│   ├── api.py           # API 엔드포인트
│   ├── models_config.py # 모델 설정
│   └── run_server.py    # 서버 실행 스크립트
├── my-app/              # SvelteKit 프론트엔드
│   ├── src/
│   │   ├── components/  # UI 컴포넌트
│   │   └── routes/      # 페이지 라우트
│   └── package.json
├── configs/             # 설정 파일
│   └── model/          # 모델별 설정
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
      "id": "Qwen3-4B-Instruct-2507-GGUF",
      "name": "Qwen3-4B-Instruct",
      "description": "Alibaba의 Qwen3 4B 모델 - 경량화된 고성능 모델"
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
  "model": "Qwen3-4B-Instruct-2507-GGUF"
}
```

**응답 예시:**
```json
{
  "translated_text": "안녕하세요, 세상!",
  "model": "Qwen3-4B-Instruct-2507-GGUF",
  "source_lang": "en",
  "target_lang": "ko"
}
```

## 문제 해결

### Lemonade Server 연결 실패

```
Error: Lemonade Server에 연결할 수 없습니다
```

**해결방법:**
- Lemonade Server가 실행 중인지 확인: `lemonade-server serve`
- http://localhost:8000 접속 가능 여부 확인

### 모델을 찾을 수 없음

```
Error: 모델을 찾을 수 없습니다
```

**해결방법:**
- 모델이 다운로드되었는지 확인
- `lemonade-server pull <model-name>` 명령으로 모델 다운로드

### 포트 충돌

**해결방법:**
- 포트 8000, 8001, 5173이 사용 중이지 않은지 확인
- 다른 포트를 사용하려면 코드에서 포트 번호 변경

## 개발

### 백엔드 테스트

```bash
# API 문서에서 직접 테스트
# http://localhost:8001/docs
```

### 프론트엔드 테스트

```bash
cd my-app
pnpm test
```

### 프로덕션 빌드

```bash
# 프론트엔드 빌드
cd my-app
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
