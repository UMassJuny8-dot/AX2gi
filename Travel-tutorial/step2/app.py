import streamlit as st

st.set_page_config(page_title="세계 여행 포털", page_icon="🌏")

# 사이드 바 메뉴 설정
menu = st.sidebar.radio("메뉴", ["홈", "미국", "중국", "일본"])

# 선택된 메뉴에 따라 화면 내용 변경
if menu == "홈":
    st.title("대한민국 🇰🇷")
    st.write("세계 여행 포털 홈 화면입니다. 왼쪽 사이드바에서 여행하고 싶은 나라를 선택해 보세요!")

elif menu == "미국":
    st.title("미국 🇺🇸")
    st.write("자유와 기회의 나라, 미국입니다. 광활한 대자연과 화려한 도시를 경험해 보세요.")
    # 링크 버튼 (기본적으로 새 탭에서 열립니다)
    st.link_button("미국 관광청 공식 사이트 방문", "https://www.gousa.or.kr/")

elif menu == "중국":
    st.title("중국 🇨🇳")
    st.write("유구한 역사와 거대한 대륙을 자랑하는 중국입니다. 만리장성과 다양한 식문화를 즐겨보세요.")
    st.link_button("중국 관광청 공식 사이트 방문", "http://www.visitchina.or.kr/")

elif menu == "일본":
    st.title("일본 🇯🇵")
    st.write("전통과 현대가 조화롭게 공존하는 일본입니다. 아름다운 자연경관과 온천을 경험해 보세요.")
    st.link_button("일본 정부관광국 공식 사이트 방문", "https://www.japan.travel/ko/kr/")