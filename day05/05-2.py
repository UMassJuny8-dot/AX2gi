# OpenAI + streamlit 앱
# 질문 하나 입력하면 OpenAI chat completions API 한번 호출
# 답변을 받아오는 가장 단순한 방법
# 대화 기록을 기억하지 않는 단발성 질문-답변
# streamlit run 05-2.py

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="나의 첫번째 챗봇", page_icon="🤖")

st.title("예제1) 나의 첫번째 챗봇")
st.caption("질문 하나 입력하면 OpenAI chat Completions API 한번 호출")

# ----------------사이드바 API 모델------------------

with st.sidebar:
    st.header("설정")
    api_key = st.text_input("OpenAI API Key", type="password", help="sk-로 시작하는 OpenAI API key를 입력하세요.")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"], index=0)
    st.markdown("[api 발급 받기](https://platform.openai.com/api-keys)")

# ---------------메인 화면--------------------
question = st.text_input("질문을 입력하세요", placeholder="예) 오늘 날씨가 어떤가요?")

if st.button("질문하기", type="tertiary"):
    if not api_key:
        st.error("OpenAI API Key를 입력하세요.")
    elif not question:
        st.error("질문을 입력하세요.")
    else:
        try:
            # OpenAI 클라이언트 초기화
            client = OpenAI(api_key=api_key)
            
            # 스피너(로딩) 표시
            with st.spinner("답변을 생각하는 중 ..."):
                
                # API 호출 (단발성 질문)
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "당신은 항상 '주인님'이라는 호칭으로 시작하며 매우 친절하게 대답하는 어시스턴트입니다."},
                        {"role": "user", "content": question}
                    ]
                )
            
            # 답변 출력
            answer = response.choices[0].message.content
            st.info(answer) # st.success()나 st.write()를 써도 좋습니다.
            
            # 사용한 토큰 수 표시 (비용 감각 익히기)
            usage = response.usage
            st.caption(f"💡 **사용한 토큰 수:** 입력 {usage.prompt_tokens} + 출력 {usage.completion_tokens} = 총 **{usage.total_tokens}** 토큰")
            
        except Exception as e:
            # 에러 발생 시 메시지 출력
            st.error(f"API 호출 중 오류가 발생했습니다: {str(e)}")