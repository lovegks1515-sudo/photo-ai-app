import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. 페이지 설정
st.set_page_config(page_title="📸 사진 분석", layout="centered")

# 2. API 키 확인
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 API_KEY 설정이 필요합니다.")
    st.stop()

st.title("📸 사진 분석")

# 3. 파일 업로더
uploaded_file = st.file_uploader("사진을 선택하세요", type=None)

if uploaded_file is not None:
    try:
        # 4. 파일 스트림 및 이미지 정규화 (업로드 오류 원천 차단)
        file_bytes = uploaded_file.read()
        img = Image.open(io.BytesIO(file_bytes))
        
        # JPEG 변환을 통한 데이터 단순화
        buffer = io.BytesIO()
        img.convert("RGB").save(buffer, format="JPEG", quality=90)
        buffer.seek(0)
        final_img = Image.open(buffer)
        
        st.image(final_img, use_column_width=True)
        
        # 5. 분석 버튼
        if st.button("분석 시작"):
            with st.spinner("선생님이 사진을 확인 중입니다..."):
                try:
                    model = genai.GenerativeModel(model_name='gemini-3.5-flash')
                    
                    # 6. 초보 교육생 맞춤형 담백한 프롬프트
                    prompt = """
                    너는 사진 선생님이고, 나는 사진 초보 교육생이야.
                    내가 찍은 사진을 기술적인 관점에서 냉정하고 객관적으로 피드백해줘.
                    칭찬이나 격려는 생략하고, 무엇이 문제인지 어떻게 고쳐야 할지만 명확히 짚어줘.
                    
                    형식은 아래 구조를 반드시 지켜줘:
                    
                    **[평가 점수]** : 0~100점
                    
                    **[사진 분석]**
                    현재 사진의 구도, 빛의 상태, 초점 등을 초보자도 이해하기 쉬운 용어로 사실 위주로 설명해줘.
                    
                    **[장점]**
                    잘한 점 1~2가지.
                    
                    **[단점]**
                    기술적으로 아쉬운 점 1~2가지. (전문 용어보다는 '초점이 어디에 맞지 않았다', '사진이 흔들렸다' 식으로 설명해줘)
                    
                    **[총평]**
                    현재 사진의 상태를 한 문장으로 요약하고, 다음 촬영 때 딱 한 가지만 기억할 점을 담백하게 알려줘.
                    """
                    
                    response = model.generate_content([prompt, final_img])
                    
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"분석 오류: {e}")
                    
    except Exception:
        st.error("파일을 처리할 수 없습니다. 다른 사진으로 시도해 주세요.")
