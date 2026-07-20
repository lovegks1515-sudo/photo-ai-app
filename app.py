import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

# API 설정
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 API_KEY 설정이 없습니다.")
    st.stop()

st.title("📸 AI 사진 평가기")

# 파일 업로더
uploaded_file = st.file_uploader("사진을 선택하세요", type=None)

# 파일이 바뀌면 자동으로 이전 결과 지우기
if uploaded_file is not None:
    # 이미지 처리
    try:
        file_bytes = uploaded_file.read()
        img = Image.open(io.BytesIO(file_bytes))
        
        # 표준 규격으로 변환하여 오류 원천 차단
        buffer = io.BytesIO()
        img.convert("RGB").save(buffer, format="JPEG", quality=90)
        buffer.seek(0)
        final_img = Image.open(buffer)
        
        st.image(final_img, use_column_width=True)
        
        # 분석 버튼
        if st.button("AI 전문 사진 분석 시작"):
            with st.spinner("전문 사진가의 시선으로 분석 중..."):
                try:
                    model = genai.GenerativeModel(model_name='gemini-3.5-flash')
                    
                    # 전문성을 살린 프롬프트
                    prompt = """
                    이 사진을 전문 사진가 관점에서 상세하고 밀도 있게 평가해줘.
                    형식은 아래 구조를 반드시 지켜줘:

                    **[종합 점수]** : 0~100점 사이의 점수
                    
                    **[작품 개요]**
                    사진의 주제와 분위기, 의도를 심도 있게 분석해줘.

                    **[사진가적 장점]**
                    구도, 조명, 색감, 피사체 포착 능력 등을 상세히 2가지로 기술해줘.

                    **[기술적 제언]**
                    노이즈, 화이트 밸런스, 셔터 스피드 등 기술적으로 보완할 점을 상세히 2가지로 기술해줘.

                    **[최종 총평]**
                    작가의 성장을 위한 따뜻하고 전문적인 격려의 메시지로 마무리해줘.
                    """
                    
                    response = model.generate_content([prompt, final_img])
                    
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"분석 중 오류 발생: {e}")
                    
    except Exception:
        st.error("파일을 처리할 수 없습니다. 다른 사진으로 시도해 주세요.")
