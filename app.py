import streamlit as st
import google.generativeai as genai
from PIL import Image
import ssl

# SSL 인증 오류 방지
try:
    _create_unverified_https_context = ssl._create_unverified_context
    ssl._create_default_https_context = _create_unverified_https_context
except:
    pass

st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

# API 키 설정
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("API 키가 설정되지 않았습니다.")
    st.stop()

st.title("📸 AI 사진 평가기")
uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    if st.button("AI 평가 시작"):
        with st.spinner("분석 중..."):
            try:
                # 모델 이름을 'gemini-1.5-flash'로 다시 시도하되, genai에서 가장 보편적인 방식으로 호출
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                response = model.generate_content(["이 사진을 전문 사진가의 관점에서 평가해줘.", image])
                st.markdown(response.text)
            except Exception as e:
                # 어떤 모델을 사용할 수 있는지 오류 메시지에 출력하게 함
                st.error(f"오류 발생: {e}")
