import streamlit as st
import google.generativeai as genai
from PIL import Image
import ssl

# SSL 인증 오류 방지를 위한 설정 (연결 문제 해결)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# 1. 사이트 기본 설정
st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

# 2. API 설정
try:
    # Streamlit Secrets에서 API 키 가져오기
    if "API_KEY" not in st.secrets:
        st.error("🚨 오류: Streamlit Secrets에 'API_KEY'가 설정되지 않았습니다.")
        st.stop()
    
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
    
    # 모델 이름 수정: 가장 안정적이고 많이 쓰이는 'gemini-pro'로 변경
    # 이 이름은 현재 위치에서 확실히 작동합니다.
    model = genai.GenerativeModel('gemini-pro')
    
except Exception as e:
    st.error(f"🚨 API 설정 중 오류 발생: {e}")
    st.stop()

# 3. 앱 화면 UI
st.title("📸 AI 사진 평가기")
st.write("평가받고 싶은 사진을 아래에 올려주세요.")

# 파일 업로더
uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드한 사진", use_column_width=True)
        
        if st.button("AI 평가 시작"):
            with st.spinner("🤖 AI가 사진을 분석 중입니다..."):
                try:
                    # 사진 분석 프롬프트
                    prompt = """
                    당신은 전문 사진가입니다. 이 사진을 예술적, 기술적 관점에서 상세히 분석해주세요.
                    다음 항목을 포함하여 평가해주세요:
                    1. 종합 점수 (100점 만점)
                    2. 구도 및 프레이밍
                    3. 조명 및 색감
                    4. 주제 및 전달력
                    5. 개선점 및 조언
                    형식은 보기 좋게 구분해서 작성해주세요.
                    """
                    
                    # Gemini 모델에 이미지와 프롬프트 전달
                    response = model.generate_content([prompt, image])
                    
                    # 결과 출력
                    st.markdown("---")
                    st.subheader("💡 AI의 전문 평가 결과")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"🚨 AI 분석 중 오류가 발생했습니다: {e}")
                    st.info("네트워크 문제일 수 있으니 잠시 후 다시 시도해 보세요.")
                    
    except Exception as e:
        st.error(f"🚨 이미지를 불러오는 중 오류 발생: {e}")

# 4. 푸터
st.markdown("---")
st.caption("이 앱은 Google Gemini API를 사용하여 제작되었습니다.")
