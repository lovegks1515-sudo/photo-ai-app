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
        
        if st.button("분석 시작"):
            with st.spinner("분석 중..."):
                try:
                    model = genai.GenerativeModel(model_name='gemini-3.5-flash')
                    
                    # 교육생-선생님 관계의 담백한 프롬프트
                    prompt = """
                    나는 사진 교육생이고, 너는 사진 선생님이야. 
                    내가 찍은 사진을 보고 기술적인 관점에서 냉정하고 객관적으로 피드백해줘.
                    칭찬이나 격려는 생략하고, 무엇이 문제인지, 어떻게 고쳐야 할지만 명확히 짚어줘.
                    
                    형식은 아래 구조를 지켜줘:
                    
                    **[평가 점수]** : 0~100점
                    
                    **[분석]**
                    현재 사진의 구도, 조명, 노출, 초점 상태에 대한 팩트 위주의 기술적 분석.
                    
                    **[개선 사항]**
                    다음 촬영 시 반드시 수정해야 할 기술적 보완점 2가지.
                    
                    **[총평]**
                    교육생의 현 실력에 대한 간결한 평가와 다음 과제.
                    """
                    
                    response = model.generate_content([prompt, final_img])
                    
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"분석 오류: {e}")
                    
    except Exception:
        st.error("파일을 처리할 수 없습니다.")
