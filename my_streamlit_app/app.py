import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="국가별 정보 및 여행 서비스",
    page_icon="🌍",
    layout="wide"
)

# 세션 상태를 이용한 페이지 관리
if "page" not in st.session_state:
    st.session_state.page = "홈"

def set_page(page_name):
    st.session_state.page = page_name

# 사이드바 네비게이션
st.sidebar.title("🧭 네비게이션")
if st.sidebar.button("🏠 홈", use_container_width=True):
    set_page("홈")

st.sidebar.markdown("---")
st.sidebar.subheader("국가별 바로가기")
countries = ["대한민국", "미국", "중국", "일본"]
for country in countries:
    if st.sidebar.button(country, use_container_width=True):
        set_page(country)

# 국가별 데이터 (정보, 여행 사이트 링크, 이미지 파일명 매핑)
country_data = {
    "대한민국": {
        "desc": "역동적인 문화와 최첨단 기술, 전통이 공존하는 아름다운 나라입니다.",
        "capital": "서울",
        "language": "한국어",
        "link": "https://t2.daumcdn.net/thumb/R720x0/?fname=http://t1.daumcdn.net/brunch/service/user/7u4B/image/Q42j_bM2oT4d8a1c6E5x0g8Vz4Y.jpg", # 임시 링크이거나 assets 경로 사용
        "img": "assets/korea.jpg"
    },
    "미국": {
        "desc": "다양한 문화와 광대한 자연경관을 자랑하는 글로벌 중심 국가입니다.",
        "capital": "워싱턴 D.C.",
        "language": "영어",
        "link": "https://www.visittheusa.com/",
        "img": "assets/usa.jpg"
    },
    "중국": {
        "desc": "유구한 역사와 세계적인 유적지, 거대한 영토를 가진 나라입니다.",
        "capital": "베이징",
        "language": "중국어",
        "link": "https://www.travelchinaguide.com/",
        "img": "assets/china.jpg"
    },
    "일본": {
        "desc": "세련된 도시 감성과 독창적인 전통 문화를 동시에 느낄 수 있는 나라입니다.",
        "capital": "도쿄",
        "language": "일본어",
        "link": "https://www.jnto.go.kr/",
        "img": "assets/japan.jpg"
    }
}

# 메인 페이지 라우팅
if st.session_state.page == "홈":
    st.title("🌍 글로벌 여행 및 정보 포털")
    st.write("왼쪽 사이드바에서 원하는 국가를 선택하여 상세 정보와 공식 여행 사이트를 확인해 보세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **이용 안내**\n- 대한민국, 미국, 중국, 일본의 기본 정보를 제공합니다.\n- 각 국가별 공식 여행 사이트로 바로 이동할 수 있습니다.")
    with col2:
        st.success("📁 **폴더 구조**\n- `assets/`: 나라별 이미지 저장 완료 ✅\n- `src/`: 컴포넌트 및 데이터 모듈 저장 공간")

else:
    current_country = st.session_state.page
    info = country_data[current_country]
    
    st.title(f"📌 {current_country} 정보")
    st.write(info["desc"])
    
    # 🖼️ assets 폴더의 이미지를 화면에 출력 (오류 방지를 위해 try-except 또는 존재 여부 확인 가능)
    try:
        st.image(info["img"], caption=current_country, use_container_width=True)
    except Exception:
        st.warning(f"⚠️ `assets/` 폴더에 `{current_country}` 이미지 파일(`{info['img']}`)이 없습니다. 파일을 확인해주세요!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("수도", info["capital"])
    with col2:
        st.metric("공인 언어", info["language"])
        
    st.markdown("---")
    st.subheader(f"🔗 {current_country} 공식 여행 사이트")
    st.markdown(f"현지 여행 정보, 관광지, 숙박 정보를 확인하려면 아래 링크를 방문하세요: [바로가기]({info['link']})")