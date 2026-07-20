import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

# API 설정
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 API 키가 설정되지 않았습니다.")
    st.stop()

st.title("📸 AI 사진 평가기")
uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # [수정] 이미지 데이터를 직접 메모리에서 확실하게 읽어옵니다.
    bytes_data = uploaded_file.getvalue()
    image = Image.open(io.BytesIO(bytes_data))
    st.image(image, use_column_width=True)
    
    if st.button("AI 평가 시작"):
        with st.spinner("분석 중..."):
            try:
                # 사용 중인 최신 모델 사용
                model = genai.GenerativeModel(model_name='gemini-3.5-flash')
                
                prompt = "이 사진을 전문 사진가의 관점에서 상세히 분석해줘. 종합 점수(100점 만점), 구도, 조명, 색감, 주제 의식, 개선점을 알려줘."
                response = model.generate_content([prompt, image])
                
                st.markdown("---")
                st.subheader("💡 AI의 전문 평가 결과")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"🚨 분석 중 오류 발생: {e}")
