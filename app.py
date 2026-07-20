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

st.set_page_config(page_title="📸 AI 사진 평가기")

# API 키 설정
if "API_KEY" in st.secrets:
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("🚨 오류: Streamlit Secrets에 'API_KEY'가 설정되지 않았습니다.")
    st.stop()

# 화면 UI
st.title("📸 AI 사진 평가기")
uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    if st.button("AI 평가 시작"):
        with st.spinner("분석 중..."):
            try:
                # ----------------------------------------------------------------
                # [핵심 변경] 특정 모델을 지정하지 않고, 라이브러리가 기본으로 설정하게 함
                # 이렇게 하면 사용자의 키에서 허용하는 기본 모델을 찾을 확률이 높음
                model = genai.GenerativeModel('gemini-pro') # 또는 'gemini-1.5-flash'로 시도
                # ----------------------------------------------------------------
                
                response = model.generate_content(["이 사진을 전문 사진가의 관점에서 평가해줘.", image])
                st.markdown(response.text)
                
            except Exception as e:
                # ----------------------------------------------------------------
                # [핵심 변경] 오류 발생 시, 어떤 모델을 사용할 수 있는지 리스트를 보여주도록 수정
                st.error(f"🚨 오류 발생: {e}")
                st.info("이 오류가 계속 발생한다면, 아래 내용이 포함된 화면을 캡처해서 보여주세요.")
                
                st.write("---")
                st.write("### 🔍 디버깅 정보 (사용 가능한 모델 확인)")
                try:
                    models = list(genai.list_models())
                    st.write("사용자님의 API 키로 접근 가능한 모델 목록:")
                    for m in models:
                        st.code(f"- Name: {m.name}, Display Name: {m.display_name}")
                    st.info("위의 목록에 있는 이름(예: 'models/gemini-pro')을 코드의 'model_name'에 정확히 입력해야 합니다.")
                except Exception as list_e:
                    st.error(f"모델 목록을 불러오는 중에도 오류 발생: {list_e}")
                    st.warning("API 키가 아예 유효하지 않을 수 있습니다.")
                # ----------------------------------------------------------------

# 푸터
st.markdown("---")
st.caption("이 앱은 Google Gemini API를 사용하여 제작되었습니다.")
