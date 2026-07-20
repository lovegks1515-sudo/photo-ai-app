import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import piexif # 메타데이터 처리를 위한 라이브러리 추가

st.set_page_config(page_title="📸 AI 사진 평가기", layout="centered")

# API 설정
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("🚨 API 키가 설정되지 않았습니다.")
    st.stop()

st.title("📸 AI 사진 평가기")
st.write("모든 형식의 사진 업로드를 시도합니다. (HEIC, 스크린샷 등 포함)")

# ----------------------------------------------------------------
# [핵심 변경] 모든 확장자를 허용하도록 변경
uploaded_file = st.file_uploader("사진 업로드", type=None) 
# type=None으로 설정하면 모든 파일 형식이 업로드 가능해집니다.
# ----------------------------------------------------------------

if uploaded_file is not None:
    with st.spinner("이미지 처리 중..."):
        try:
            # 파일 데이터를 바이트로 읽음
            bytes_data = uploaded_file.getvalue()
            
            # ----------------------------------------------------------------
            # [핵심 변경] 메타데이터(Exif)를 제거하고 안전하게 변환
            try:
                # PIL로 이미지 오픈
                image = Image.open(io.BytesIO(bytes_data))
                
                # 이미지를 RGB 모드로 변환 (알파 채널 제거 등)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # 이미지를 메모리상에 JPEG로 다시 저장하여 메타데이터를 완전히 제거
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG', exif=b"") # exif=b""로 메타데이터 제거
                img_byte_arr.seek(0)
                
                # 메타데이터가 제거된 새로운 이미지 객체 생성
                clean_image = Image.open(img_byte_arr)
                
            except Exception as e:
                st.error(f"🚨 이미지 포맷을 분석할 수 없습니다. 지원하지 않는 형식일 수 있습니다: {e}")
                st.stop()
            # ----------------------------------------------------------------

            # 화면에 업로드된 이미지 표시
            st.image(clean_image, caption="업로드한 사진 (최적화됨)", use_column_width=True)
            
            if st.button("AI 평가 시작"):
                with st.spinner("분석 중..."):
                    try:
                        # 사용자님이 보유한 최신 모델 사용
                        model = genai.GenerativeModel(model_name='gemini-3.5-flash')
                        
                        prompt = "이 사진을 전문 사진가의 관점에서 상세히 분석해줘. 종합 점수(100점 만점), 구도, 조명, 색감, 주제 의식, 개선점 및 조언을 상세히 알려줘."
                        # 깨끗하게 처리된 이미지 객체를 전달
                        response = model.generate_content([prompt, clean_image])
                        
                        st.markdown("---")
                        st.subheader("💡 AI의 전문 평가 결과")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"🚨 AI 분석 중 오류 발생: {e}")
                        
        except Exception as e:
            st.error(f"🚨 이미지를 불러오는 중 오류 발생: {e}")
