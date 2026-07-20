import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI 사진 평가기")

# API 설정
genai.configure(api_key=st.secrets["API_KEY"])

# 모델 이름 직접 지정하지 않고 라이브러리가 자동으로 찾게 함
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📸 AI 사진 평가기")
uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    if st.button("AI 평가 시작"):
        with st.spinner("분석 중..."):
            try:
                # generate_content 호출 시 명시적으로 모델 이름을 넣지 않거나, 
                # 위에서 정의한 model 객체를 바로 사용
                response = model.generate_content(["이 사진을 전문 사진가의 관점에서 평가해줘.", image])
                st.markdown(response.text)
            except Exception as e:
                # 오류 발생 시 어떤 모델이 리스트에 있는지 확인 가능하게
                st.error(f"오류: {e}")
