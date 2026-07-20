import streamlit as st
import google.generativeai as genai
from PIL import Image
import ssl

# SSL 인증 오류 방지를 위한 설정
ssl._create_default_https_context = ssl._create_unverified_context

# 1. 사이트 설정
st.set_page_config(page_title="AI 사진 평가 앱", layout="centered")

# 2. API 설정 (Streamlit Secrets에서 가져오기)
try:
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API 키 설정에 문제가 있습니다. Secrets를 확인해주세요.")

# 3. 화면 UI 구성
st.title("📸 AI 사진 평가기")
uploaded_file = st.file_uploader("평가받을 사진을 올려주세요!", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 사진", use_column_width=True)
    
    if st.button("AI 평가 시작"):
        with st.spinner("AI가 사진을 분석 중입니다..."):
            try:
                # 사진 분석 프롬프트
                prompt = "이 사진을 전문 사진가의 관점에서 평가해줘. 구도, 조명, 색감 등을 분석하고 100점 만점에 몇 점인지 점수와 함께 자세한 총평을 적어줘."
                response = model.generate_content([prompt, image])
                
                st.subheader("💡 AI 평가 결과")
                st.write(response.text)
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")
