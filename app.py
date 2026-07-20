import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. 페이지 설정
st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

# 2. API 설정 (Secrets에서 키를 가져옴)
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 설정 오류: API_KEY가 없습니다.")
    st.stop()

# 3. 화면 UI
st.title("📸 AI 사진 평가기")
uploaded_file = st.file_uploader("사진을 업로드하세요", type=None)

if uploaded_file is not None:
    # 이미지 데이터 처리
    bytes_data = uploaded_file.getvalue()
    image = Image.open(io.BytesIO(bytes_data))
    
    # 이미지 RGB 변환 및 메타데이터 제거 (오류 방지)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    st.image(image, use_column_width=True)
    
    # 4. 분석 시작
    if st.button("AI 평가 시작"):
        with st.spinner("분석 중..."):
            try:
                # 최신 프리뷰 모델 사용
                model = genai.GenerativeModel(model_name='gemini-3.5-flash')
                
                # 간결한 프롬프트 설정
                prompt = """
                이 사진을 전문 사진가 관점에서 평가해줘.
                다음 항목을 3문장 이내로 아주 간결하게 정리해줘:
                1. [종합 점수] (0~100점)
                2. [핵심 장점] 1~2개
                3. [개선 제안] 1~2개
                """
                
                response = model.generate_content([prompt, image])
                
                st.markdown("---")
                st.subheader("💡 AI 평가 결과")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"🚨 오류 발생: {e}")
