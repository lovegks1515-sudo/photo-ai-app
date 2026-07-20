import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

# API 설정
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 설정 오류: API_KEY가 없습니다.")
    st.stop()

st.title("📸 AI 사진 평가기")
uploaded_file = st.file_uploader("사진을 업로드하세요", type=None)

if uploaded_file is not None:
    try:
        # 1. 파일 전체를 메모리에 로드
        bytes_data = uploaded_file.getvalue()
        
        # 2. 메타데이터(Exif)를 아예 무시하고 이미지 데이터만 읽어옴
        image = Image.open(io.BytesIO(bytes_data))
        
        # 3. 모든 데이터를 RGB로 단순화하여 메타데이터 완벽 차단
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        st.image(image, use_column_width=True)
        
        if st.button("AI 평가 시작"):
            with st.spinner("분석 중..."):
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
                    st.error(f"🚨 분석 오류: {e}")
    except Exception as e:
        st.error(f"🚨 파일을 읽을 수 없습니다. 다시 시도해주세요.")
