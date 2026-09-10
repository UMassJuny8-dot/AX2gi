import streamlit as st
# streamlit run 9-3-2.py 실행하는 방법 터미널 cmd 입력

# st.title("내용") 은 페이지에서 가장 크고 굵은 제목을 만든다.(h1 느낌)
st.title("무역마스터😊부트캠프😘자기소개")
st.markdown("---")

# st.header("내용") 은 타이틀보다는 한단계 작은 큰제목(h2 느낌).
st.header('안녕하세요 !! Streamlit으로 만든 첫 페이지 입니다.')
st.markdown("---")

# st.subheader("내용") 은 header보다는 한단계 작은 큰제목(h3 느낌).
st.subheader("오늘 배운 것 : 텍스트 화면에 예쁘게 보여주는 방법 !!")
st.markdown("---")

# st.text("내용") 은 꾸밈이 전혀 없는 순수 텍스트 그대로 출력
st.text("st.text로 출력한 문장입니다아아아")

# st.caption("내용") 은 아주 작은 글씨로 보조 설명을 넣을때
st.caption("희미~~  한 캡션입니다아아아 ~~~")

# st.markdown("") 은 마크다운 문법 -> 굵게, 기울임, 링크, 목록
st.markdown("---") # ---로 긴줄 생성
st.markdown(
    """
    ### 📌마크다운으로 작성한 자기소개📌
    - **이름** : 황준영
    - **관심분야** : *데이터분석*, *무역데이터 시각화*
    - **목표** : 나만의 데시보드 만들기
    - 참고 링크 :[네이버](HTTPS://www.naver.com)
"""
)
st.markdown("---")

st.subheader("오늘 배운 한줄 코드")

st.code(
    """
    st.title("hello streamlit!")
"""
)