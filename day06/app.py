import os
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()
KAKAO_APP_KEY = os.getenv("KAKAO_APP_KEY")

st.title("📍 Streamlit Kakao Map 연동 예제")

if not KAKAO_APP_KEY:
    st.error(".env 파일에 KAKAO_APP_KEY가 설정되어 있지 않습니다.")
else:
    # 서울 시내 명소 샘플 데이터
    places = [
        {"name": "여의도한강공원", "lat": 37.5285, "lon": 126.9347},
        {"name": "경복궁", "lat": 37.5796, "lon": 126.9770},
        {"name": "홍대사거리", "lat": 37.5563, "lon": 126.9236},
        {"name": "명동", "lat": 37.5636, "lon": 126.9827},
    ]

    # 1. 기본 Folium 지도 객체 생성 (중심 좌표: 서울 시청)
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

    # 2. 리스트의 장소들을 반복문으로 돌며 마커 추가
    for place in places:
        folium.Marker(
            location=[place["lat"], place["lon"]],
            popup=place["name"],
            tooltip=place["name"]
        ).add_to(m)

    # 3. Streamlit 화면에 지도 출력
    st.write("아래는 스트림릿에 렌더링된 지도입니다:")
    st_folium(m, width=700, height=500)