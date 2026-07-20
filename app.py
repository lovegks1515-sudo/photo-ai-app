import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

# API 키 설정
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 API_KEY 설정이 없습니다.")
    st.stop()

st.title("📸 AI 사진 평가기")
uploaded_file = st.file_uploader("사진을 선택하세요", type=None)

if uploaded_file is not None:
    # 1. 파일 오픈 방식을 'rb' 모드로 명시
    try:
        image = Image.open(uploaded_file)
        # 이미지 모드 확인 (RGBA 등인 경우 RGB로 변환)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        st.image(image, use_column_width=True)
        
        if st.button("AI 평가 시작"):
            with st.spinner("분석 중..."):
                try:
                    # 'gemini-3.5-flash'는 이미지 처리 능력이 매우 뛰어납니다.
                    model = genai.GenerativeModel('gemini-3.5-flash')
                    
                    prompt = """
                    전문 사진가 관점에서 평가해줘. 다음 내용을 3문장 이내로 정리해:
                    1. [종합 점수] (0~100점)
                    2. [핵심 장점] 1~2개
                    3. [개선 제안] 1~2개
                    """
                    
                    # 2. 파일 객체를 그대로 전달 (Streamlit 파일 스트림 사용)
                    response = model.generate_content([prompt, image])
                    
                    st.markdown("---")
                    st.subheader("💡 AI 평가 결과")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"🚨 분석 오류: {e}")
                    st.info("사진 파일이 너무 크거나 형식이 깨졌을 수 있습니다. 사진을 작게 리사이즈해서 시도해 보세요.")
                    
    except Exception as e:
        st.error(f"🚨 파일을 읽어올 수 없습니다: {e}")
