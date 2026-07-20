import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API 키 설정 (Streamlit의 안전한 보관소에서 불러옴)
# 나중에 Streamlit Cloud 설정에서 [API_KEY] 라는 이름으로 키를 저장하세요!
try:
    genai.configure(api_key=st.secrets["API_KEY"])
except:
    st.error("API 키가 설정되지 않았습니다! Streamlit Secrets 설정을 확인하세요.")

# 2. 모델 설정
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📸 AI 사진 평가기")

uploaded_file = st.file_uploader("평가받을 사진을 올려주세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드 완료', use_container_width=True)
    
    if st.button("AI 평가 시작"):
        with st.spinner('AI가 사진을 정밀 분석 중입니다...'):
            try:
                # 이미지 리사이징 (속도 향상)
                image_resized = image.resize((1024, 1024))
                
                # 프롬프트 설정
                prompt = """
                당신은 전문 사진 작가입니다. 다음 양식으로만 간결하게 평가해주세요.
                
                **[Score]** (점수)/100.00
                
                <개요>
                (분위기와 의도 요약)
                
                <장점>
                1. (장점 1)
                2. (장점 2)
                
                <단점>
                1. (단점 1)
                2. (단점 2)
                
                <총평>
                (개선점을 포함한 최종 총평)
                """
                
                # 응답 속도 최적화
                response = model.generate_content(
                    [prompt, image_resized], 
                    generation_config={"max_output_tokens": 400}
                )
                
                st.write("### 💡 AI 평가 결과")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")