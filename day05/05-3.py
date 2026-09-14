# 대화 기록을 기억하는 멀티턴 챗봇(스트리밍 응답) 
# st.session_state 에 대화 기록을 저장해서, 이전 대화 맥락을 기억하는 챗봇 
# st.chat_message / st.chat_input 같은 Streamlit의 채팅 전용 위젯을 사용합니다.
# stream=True 옵션으로 답변이 실시간으로 타이핑되듯 출력됩니다.
# streamlit run 05-3.py

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="멀티턴 챗봇", page_icon="💬")

st.title("예제2) 기억력이 있는 스트리밍 챗봇")
st.caption("대화 맥락을 기억하며, 답변이 실시간으로 생성됩니다.")

# ---------------- 사이드바: 설정 및 초기화 ------------------
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("OpenAI API Key", type="password", help="sk-로 시작하는 OpenAI API key를 입력하세요.")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o"], index=0)
    
    st.divider() # 구분선
    
    # 시스템 메시지 사용자 설정
    st.subheader("챗봇 페르소나 설정")
    system_prompt = st.text_area(
        "시스템 프롬프트", 
        value="당신은 친절하고 도움이 되는 AI 어시스턴트입니다.",
        help="챗봇의 역할이나 성격을 지정할 수 있습니다."
    )
    
    # 대화 기록 초기화 버튼
    if st.button("대화 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun() # 화면 새로고침

# ---------------- 세션 상태(session_state) 초기화 ------------------
# 처음 앱을 실행했을 때 대화 기록을 저장할 빈 리스트를 만듭니다.
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- 이전 대화 기록 화면에 출력 ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- 사용자 입력 및 AI 응답 처리 ------------------
# st.chat_input은 화면 맨 아래에 입력창을 고정시킵니다.
if prompt := st.chat_input("메시지를 입력하세요..."):
    
    if not api_key:
        st.error("좌측 사이드바에서 OpenAI API Key를 먼저 입력해주세요.")
        st.stop() # 키가 없으면 더 이상 코드를 진행하지 않음

    # 1. 사용자의 질문을 대화 기록에 추가하고 화면에 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI의 답변을 스트리밍으로 받아오기
    client = OpenAI(api_key=api_key)
    
    with st.chat_message("assistant"):
        # API에 보낼 메시지 리스트 구성 (사용자가 설정한 시스템 프롬프트 + 이전 대화 기록 전체)
        api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
        
        # stream=True 옵션으로 설정
        stream = client.chat.completions.create(
            model=model,
            messages=api_messages,
            stream=True
        )
        
        # st.write_stream을 사용하면 실시간 타이핑 효과가 적용되며, 완성된 전체 텍스트를 반환합니다.
        full_response = st.write_stream(stream)

    # 3. 완성된 AI의 답변을 대화 기록에 추가
    st.session_state.messages.append({"role": "assistant", "content": full_response})