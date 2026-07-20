import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="📸 사진 분석", layout="centered")

if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 API_KEY 설정이 없습니다.")
    st.stop()

# 제목 담백하게 변경
st.title("📸 사진 분석")

uploaded_file = st.file_uploader("사진을 선택하세요", type=None)

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        img = Image.open(io.BytesIO(file_bytes))
        
        buffer = io.BytesIO()
        img.convert("RGB").save(buffer, format="JPEG", quality=90)
        buffer.seek(0)
        final_img = Image.open(buffer)
        
        st.image(final_img, use_column_width=True)
        
        # 버튼 문구 담백하게 변경
        if st.button("분석 시작"):
            with st.spinner("분석 중..."):
                try:
                    model = genai.GenerativeModel(model_name='gemini-3.5-flash')
                    
                    prompt = """
                    이 사진을 전문 사진가 관점에서 냉정하고 간결하게 분석해줘.
                    감정적인 표현이나 격려의 말은 일절 배제하고, 사실 기반의 기술적 피드백만 제공해.
                    
                    형식은 아래 구조를 반드시 지켜줘:
                    
                    **[종합 점수]** : 0~100점
                    
                    **[작품 분석]**
                    주제, 구도, 조명, 색감에 대한 사실적인 평가.
                    
                    **[기술적 피드백]**
                    노이즈, 선명도, 셔터 스피드, 조명 균형 등 보완이 필요한 기술적 요소 2가지.
                    
                    **[총평]**
                    작품의 특징과 기술적 개선 방향에 대한 담백한 요약.
                    """
                    
                    response = model.generate_content([prompt, final_img])
                    
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"분석 오류: {e}")
                    
    except Exception:
        st.error("파일을 처리할 수 없습니다.")
