from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
import openai
import os
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import textwrap

# 환경변수 로드
load_dotenv("key.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

def generate_background_image(prompt: str, index: int) -> str:
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="url"
        )
        image_url = response.data[0].url
        os.makedirs("output", exist_ok=True)
        bg_path = f"output/flyer_{index}_bg.png"
        with open(bg_path, "wb") as f:
            f.write(requests.get(image_url).content)
        return bg_path
    except Exception as e:
        print(f"[{index}] 이미지 생성 실패: {e}")
        return ""

def add_text_to_image(image_path: str, title: str, body: str, index: int) -> str:
    try:
        img = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        font_path = "./font/Pretendard-Bold.ttf"
        if not os.path.exists(font_path):
            raise FileNotFoundError("폰트 파일이 없습니다.")

        font_title = ImageFont.truetype(font_path, 64)
        font_body = ImageFont.truetype(font_path, 36)

        width, height = img.size
        margin = 40
        spacing = 20

        wrapped_body = textwrap.fill(body, width=28)
        title_size = draw.textbbox((0, 0), title, font=font_title)
        body_size = draw.multiline_textbbox((0, 0), wrapped_body, font=font_body, spacing=spacing)

        box_height = (title_size[3] - title_size[1]) + (body_size[3] - body_size[1]) + 3 * spacing
        box_top = height - box_height - margin
        box_bottom = height - margin

        draw.rectangle([(margin, box_top), (width - margin, box_bottom)], fill=(255, 255, 255, 230))

        draw.text((margin + 10, box_top + spacing), title, font=font_title, fill=(0, 0, 0))
        draw.multiline_text(
            (margin + 10, box_top + spacing + (title_size[3] - title_size[1]) + spacing),
            wrapped_body,
            font=font_body,
            fill=(0, 0, 0),
            spacing=spacing
        )

        out_path = f"output/flyer_{index}.png"
        img.save(out_path)
        return out_path
    except Exception as e:
        print(f"[{index}] 텍스트 삽입 실패: {e}")
        return ""

@app.post("/generate-flyer/image")
async def generate_flyer_image(user_text: str = Form(...)):
    prompt = (
        f"{user_text} 라는 설명을 바탕으로 전단지 문구 딱 1세트만 만들어줘.\n"
        f"아래 형식을 꼭 지켜줘:\n\n"
        f"[제목]\n(짧고 인상적인 제목)\n\n[홍보문구]\n(1~2문장)\n\n[배경프롬프트]\n(이미지 생성용 설명문)\n\n"
        f"설명이나 옵션, 번호, 구분선(---) 없이 항목만 출력해줘."
    )

    try:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        flyer_text = completion.choices[0].message.content.strip()
        print("GPT 응답:\n", flyer_text)
    except Exception as e:
        return JSONResponse(content={"error": f"GPT 생성 실패: {e}"}, status_code=500)

    try:
        title = flyer_text.split("[제목]")[1].split("[홍보문구]")[0].strip()
        body = flyer_text.split("[홍보문구]")[1].split("[배경프롬프트]")[0].strip()
        bg_prompt = flyer_text.split("[배경프롬프트]")[1].strip()
    except Exception as e:
        return JSONResponse(content={"error": f"파싱 실패: {e}"}, status_code=400)

    image_path = generate_background_image(bg_prompt, 1)
    result_path = add_text_to_image(image_path, title, body, 1)

    if not os.path.exists(result_path):
        return JSONResponse(content={"error": "이미지 파일 생성 실패"}, status_code=500)

    return FileResponse(result_path, media_type="image/png")





"""
C:\Python\python.exe -m uvicorn main:app --reload

curl -X POST "http://127.0.0.1:8000/generate-flyer/image" -H "Content-Type: application/x-www-form-urlencoded" -d "user_text=가게 이름은 너마늘이고 마늘빵을 팔아. 의성에서 직접 재배한 마늘로 만들어서 달콤하고 고소해. 따뜻한 마늘빵 많이 먹으러와줬으면 좋겠어."

"""
