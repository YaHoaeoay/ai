# 🍞 너마늘 전단지 생성기 - demo_ai

FastAPI 기반 API로, GPT-4와 DALL·E 3를 활용하여 전단지용 이미지와 홍보문구를 자동 생성합니다.

---

## 💡 주요 기능

- 사용자가 입력한 가게 설명을 바탕으로:
  - 전단지 문구 자동 생성 (GPT-4)
  - 배경 이미지 생성 (DALL·E 3)
  - 문구가 삽입된 전단지 이미지 생성 및 반환

---

## ⚙️ 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/YaHoaeoay/demo_ai.git
cd demo_ai
```

### 2. 가상환경 설정 (선택)
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
```

### 3. 의존 패키지 설치
```bash
pip install -r requirements.txt
```

> `requirements.txt`에는 다음과 같은 주요 패키지가 포함되어야 합니다:
> - `fastapi`
> - `uvicorn`
> - `openai`
> - `python-dotenv`
> - `Pillow`
> - `requests`

### 4. 환경변수 설정

`.env` 또는 `key.env` 파일에 OpenAI API 키를 설정합니다:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 5. 실행

```bash
uvicorn main:app --reload
```

---

## 📡 API 사용 방법

### [POST] `/generate-flyer/image`

- **설명**: 전단지용 문구 및 이미지 생성
- **요청 형식**: `x-www-form-urlencoded`
- **파라미터**:
  - `user_text` (str): 가게 또는 제품 설명

### 🧪 CURL 테스트 예시

```bash
curl -X POST "http://127.0.0.1:8000/generate-flyer/image" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "user_text=가게 이름은 너마늘이고 마늘빵을 팔아. 의성에서 직접 재배한 마늘로 만들어서 달콤하고 고소해. 따뜻한 마늘빵 많이 먹으러와줬으면 좋겠어."
```

- 생성된 이미지 파일은 `output/flyer_1.png`로 저장되며 브라우저로 바로 응답됩니다.

---

## 🗂 폴더 구조

```
demo_ai/
├── main.py              # FastAPI 서버 코드
├── key.env              # 환경변수 (gitignore 처리됨)
├── .gitignore           # 출력 폴더 및 비밀키 제외
├── font/                # 사용자 지정 폰트 파일 (예: Pretendard-Bold.ttf)
└── output/              # 생성된 이미지가 저장되는 폴더
```

---

## ⚠️ 주의사항

- `font/Pretendard-Bold.ttf` 폰트 파일이 반드시 존재해야 합니다.
- `key.env`, `output/`, `demo_front/` 폴더는 Git에 업로드되지 않도록 `.gitignore`에 포함되어야 합니다.
- OpenAI API 사용량에 따라 과금이 발생할 수 있습니다.

---

## 🥖 예시 이미지

<img src="output/flyer_1.png" width="400">

---

## 📜 License

MIT
