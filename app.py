import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

# 1. API 설정
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 API_KEY 설정이 필요합니다.")
    st.stop()

st.title("📸 AI 사진 평가기")

# 2. 파일 업로드 (Type 제한 없음)
uploaded_file = st.file_uploader("사진을 선택하세요 (선택 후 아래 버튼을 누르세요)", type=None)

# 3. 파일이 있으면 화면에 띄우고 버튼 활성화
if uploaded_file is not None:
    try:
        # 파일 데이터를 읽음
        bytes_data = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(bytes_data))
        
        # 이미지 최적화
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        st.image(image, caption="사진 로드 완료", use_column_width=True)
        
        # 4. 분석 버튼 (파일이 로드된 후에만 활성화됨)
        if st.button("AI 평가 시작"):
            with st.spinner("이미지 분석 중..."):
                try:
                    model = genai.GenerativeModel(model_name='gemini-3.5-flash')
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
                    st.error(f"🚨 분석 중 오류: {e}")
    except Exception as e:
        st.error(f"🚨 파일을 처리하는 중 문제가 발생했습니다: {e}")
