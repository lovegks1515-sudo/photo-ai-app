import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="📸 사진 분석", layout="centered")

if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 API_KEY 설정이 필요합니다.")
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
            with st.spinner("분석 중입니다..."):
                try:
                    model = genai.GenerativeModel(model_name='gemini-3.5-flash')
                    
                    # 담백한 어조로 수정된 프롬프트
                    prompt = """
                    사진 초보 교육생의 사진을 분석해줘.
                    기술적인 부분 위주로 명확하고 담백하게 피드백해주면 돼.
                    나는 '라이트룸 모바일(Lightroom Mobile)' 앱으로 보정해.
                    
                    형식은 아래 구조를 지켜줘:
                    
                    **[평가 점수]** : 0~100점
                    
                    **[사진 분석]**
                    구도, 빛, 초점 상태를 사실 위주로 설명해줘.
                    
                    **[장점]**
                    잘된 점 1~2가지.
                    
                    **[단점]**
                    기술적으로 아쉬운 점 1~2가지.
                    
                    **[라이트룸 모바일 보정 팁]**
                    라이트룸 모바일 '편집' 메뉴의 슬라이더를 기준으로, 조절하면 좋을 항목 2가지를 알려줘.
                    (예: 노출, 대비, 밝은 영역, 어두운 영역, 흰색 계열, 검정 계열, 생동감, 채도 등)
                    
                    **[총평]**
                    다음 촬영 때 참고할 점을 담백하게 요약.
                    """
                    
                    response = model.generate_content([prompt, final_img])
                    
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"분석 오류: {e}")
                    
    except Exception:
        st.error("파일을 처리할 수 없습니다.")
