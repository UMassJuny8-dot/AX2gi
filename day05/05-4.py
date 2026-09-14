# 파일 업로드 문서 요약 앱
# 사이드바: 요약 길이, 요약 스타일 설정
# 메인화면: 파일 업로드, 파일 미리보기, 요약 실행 및 결과 출력
# 지원 형식: .txt, .pdf
# streamlit run 05-4.py

import streamlit as st
from openai import OpenAI
import PyPDF2  # PDF 파일을 읽기 위한 라이브러리

st.set_page_config(page_title="문서 요약 앱", page_icon="📄", layout="wide")

st.title("예제3) 📄 파일 업로드 문서 요약 앱")
st.caption("텍스트나 PDF 파일을 업로드하면 원하는 스타일과 길이로 요약해 드립니다.")

# ---------------- 사이드바: 설정 ------------------
with st.sidebar:
    st.header("API 설정")
    api_key = st.text_input("OpenAI API Key", type="password", help="sk-로 시작하는 OpenAI API key를 입력하세요.")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o"], index=0)
    
    st.divider() # 구분선
    
    st.header("요약 옵션 설정")
    # 1. 요약 길이 선택
    summary_length = st.selectbox(
        "요약 길이 선택", 
        ["핵심만 짧게 (1~2문단)", "보통 길이 (3~4문단)", "상세하게 길게 (5문단 이상)"]
    )
    
    # 2. 요약 스타일(수준) 선택
    summary_style = st.selectbox(
        "요약 스타일 및 수준 선택", 
        [
            "초보자/일반인 수준 (쉽고 친절하게)", 
            "전문가 수준 (전문 용어 사용, 논리적으로)", 
            "개조식 (글머리 기호 사용, 명료하게)"
        ]
    )

# ---------------- 메인 화면: 파일 업로드 ------------------
# 파일 업로더 위젯
uploaded_file = st.file_uploader("요약할 파일을 업로드하세요 (지원 형식: .txt, .pdf)", type=['txt', 'pdf'])

# 파일이 업로드 되었을 때만 아래 로직 실행
if uploaded_file is not None:
    file_text = ""
    
    # 1. 파일 확장자에 따라 텍스트 추출 방식 다르게 처리
    if uploaded_file.name.endswith('.txt'):
        # 텍스트 파일인 경우
        file_text = uploaded_file.read().decode('utf-8')
        
    elif uploaded_file.name.endswith('.pdf'):
        # PDF 파일인 경우 PyPDF2 사용
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                file_text += extracted + "\n"

    # 2. 파일 미리보기 제공 (접었다 펼칠 수 있는 expander 사용)
    st.subheader("🔎 첨부파일 미리보기")
    with st.expander("파일 내용 확인하기 (클릭하여 펼치기)"):
        # 내용이 너무 길면 화면이 버벅일 수 있으므로 앞부분 2000자만 보여주기
        preview_text = file_text[:2000] + ("\n\n... (이하 생략)" if len(file_text) > 2000 else "")
        st.text_area("문서 원본", value=preview_text, height=250, disabled=True)

    st.divider()

    # 3. 요약하기 버튼
    # 버튼을 눈에 띄게 만들기 위해 type="primary" 사용
    if st.button("✨ 설정한 옵션으로 문서 요약하기", type="primary", use_container_width=True):
        if not api_key:
            st.error("좌측 사이드바에서 OpenAI API Key를 입력해주세요.")
        elif not file_text.strip():
            st.error("파일에서 텍스트를 읽을 수 없거나 빈 문서입니다.")
        else:
            client = OpenAI(api_key=api_key)
            
            # AI에게 전달할 프롬프트 조합
            prompt = f"""
            아래 제공되는 문서 내용을 바탕으로 요약을 작성해주세요.
            
            [요약 조건]
            - 길이: {summary_length}
            - 스타일 및 수준: {summary_style}
            
            [문서 내용]
            {file_text}
            """
            
            # 스피너 표시 및 API 호출
            with st.spinner("AI가 문서를 열심히 읽고 요약하는 중입니다..."):
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "당신은 주어진 문서를 정확하고 목적에 맞게 요약하는 전문 비서입니다."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    # 4. 요약 결과 출력
                    summary_result = response.choices[0].message.content
                    
                    st.success("요약이 완료되었습니다!")
                    st.subheader("📝 문서 요약 결과")
                    
                    # 결과를 보기 좋은 컨테이너 박스 안에 출력
                    with st.container(border=True):
                        st.markdown(summary_result)
                        
                except Exception as e:
                    st.error(f"API 호출 중 오류가 발생했습니다: {str(e)}")