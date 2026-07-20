import streamlit as st
import google.generativeai as genai
from PIL import Image
import ssl

# SSL 인증 오류 방지를 위한 설정 (PC/모바일 환경 연결 문제 해결)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# 1. 사이트 기본 설정
st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

# 2. API 설정 (Streamlit Secrets에서 가져오기)
# Streamlit Cloud의 [Manage app] -> [Settings] -> [Secrets]에 API_KEY가 설정되어 있어야 합니다.
try:
    if "API_KEY" not in st.secrets:
        st.error("🚨 오류: Streamlit Secrets에 'API_KEY'가 설정되지 않았습니다. 앱 설정을 확인해주세요.")
        st.stop()
    
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
    
    # 안정적인 최신 모델 사용
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"🚨 API 설정 중 오류 발생: {e}")
    st.stop()

# 3. 앱 화면 UI 구성
st.title("📸 AI 사진 평가기")
st.write("평가받고 싶은 사진을 아래에 올려주세요. AI가 전문적인 관점에서 분석해드립니다.")

# 파일 업로더 (jpg, jpeg, png 파일만 허용)
uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 업로드된 이미지 열기
    try:
        image = Image.open(uploaded_file)
        # 화면에 이미지 미리보기 (너비에 맞춤)
        st.image(image, caption="업로드한 사진", use_column_width=True)
    except Exception as e:
        st.error(f"이미지를 불러오는 중 오류가 발생했습니다: {e}")
        st.stop()
    
    # 평가 시작 버튼
    if st.button("AI 평가 시작"):
        with st.spinner("🤖 AI가 사진을 분석 중입니다. 잠시만 기다려주세요..."):
            try:
                # 사진 분석 요청 프롬프트
                prompt = """
                당신은 전문 사진가입니다. 이 사진을 예술적, 기술적 관점에서 상세히 분석해주세요.
                
                다음 항목을 포함하여 평가해주세요:
                1. **종합 점수**: 100점 만점 기준
                2. **구도 및 프레이밍 분석**: 사진의 구성이 어떤지
                3. **조명 및 색감 분석**: 빛의 사용과 색의 조화가 어떤지
                4. **주제 및 전달력**: 무엇을 말하려는 사진인지
                5. **개선점 및 조언**: 더 좋은 사진이 되기 위한 팁
                
                형식은 보기 좋게 제목과 내용을 구분해서 작성해주세요.
                """
                
                # Gemini 모델에 이미지와 프롬프트 전달
                response = model.generate_content([prompt, image])
                
                # 결과 출력
                st.markdown("---")
                st.subheader("💡 AI의 전문 평가 결과")
                # AI 응답 내용을 마크다운 형식으로 출력
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"🚨 AI 분석 중 오류가 발생했습니다. API 키, 모델 상태, 또는 네트워크 연결을 확인해주세요.\\n\\n오류 내용: {e}")

# 4. 푸터 정보
st.markdown("---")
st.caption("이 앱은 Google Gemini API를 사용하여 제작되었습니다.")
