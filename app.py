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

st.set_page_config(page_title="📸 AI 사진 평가기 (Pro)", layout="centered")

# API 키 설정
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 오류: Streamlit Secrets에 'API_KEY'가 설정되지 않았습니다.")
    st.stop()

# 화면 UI
st.title("📸 AI 사진 평가기 (Advanced)")
st.write("사용자님의 특별한 API 권한으로 최신 모델을 사용합니다.")
uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    if st.button("AI 평가 시작 (Gemini 3.5 Flash)"):
        with st.spinner("분석 중..."):
            try:
                # ----------------------------------------------------------------
                # [핵심 변경] 보내주신 목록에 있는 가장 최신으로 보이는 안정적인 모델명 사용
                # 'gemini-3.5-flash'로 설정합니다. (목록 28번째)
                model = genai.GenerativeModel(model_name='gemini-3.5-flash')
                # ----------------------------------------------------------------
                
                prompt = "이 사진을 전문 사진가의 관점에서 상세히 분석해줘. 종합 점수(100점 만점)와 함께 구도, 조명, 색감, 주제 의식을 평가해주고 개선점도 알려줘."
                response = model.generate_content([prompt, image])
                
                st.markdown("---")
                st.subheader("💡 AI의 전문 평가 결과")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"🚨 오류 발생: {e}")
                st.info("모델 이름 문제일 수 있습니다. 위의 '디버깅 정보' 목록에 있는 다른 이름을 복사해서 코드에 넣어보세요.")

# 푸터
st.markdown("---")
st.caption(f"이 앱은 Google Gemini API의 최신 프리뷰 모델을 사용 중입니다.")
