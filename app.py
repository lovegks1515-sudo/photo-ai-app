import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 설정 오류")
    st.stop()

st.title("📸 AI 사진 평가기")
uploaded_file = st.file_uploader("사진 선택", type=None)

if uploaded_file is not None:
    try:
        # 파일 내용을 읽음
        file_bytes = uploaded_file.read()
        
        # PIL로 열기
        img = Image.open(io.BytesIO(file_bytes))
        
        # [핵심] 웹에서 가장 안전한 형식으로 메모리에서 새로 저장
        # 이렇게 하면 카메라 고유의 복잡한 메타데이터가 100% 삭제됩니다.
        buffer = io.BytesIO()
        img.convert("RGB").save(buffer, format="JPEG", quality=85)
        buffer.seek(0)
        final_img = Image.open(buffer)
        
        st.image(final_img, use_column_width=True)
        
        if st.button("AI 평가 시작"):
            with st.spinner("분석 중..."):
                try:
                    model = genai.GenerativeModel(model_name='gemini-3.5-flash')
                    prompt = """
                    전문 사진가 관점에서 평가해줘.
                    1. [종합 점수] (0~100점)
                    2. [핵심 장점] 1~2개
                    3. [개선 제안] 1~2개
                    3문장 이내로 간결하게 부탁해.
                    """
                    response = model.generate_content([prompt, final_img])
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"분석 오류: {e}")
    except Exception:
        st.error("사진 파일을 처리할 수 없습니다. 다른 사진으로 시도해주세요.")
