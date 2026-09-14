import os
import streamlit as st
import requests
from dotenv import load_dotenv
import streamlit.components.v1 as components

# .env 파일 로드
load_dotenv()
KAKAO_APP_KEY = os.getenv("KAKAO_APP_KEY")

st.set_page_config(page_title="✈️ 글로벌 여행 앱", layout="wide")

st.title("✈️ 스마트 여행 가이드 (카카오맵 장소 검색)")

countries_data = {
    "대한민국 (서울)": {"lat": 37.5665, "lon": 126.9780, "currency": "KRW", "name": "서울", "unit": 1},
    "일본 (도쿄)": {"lat": 35.6762, "lon": 139.6503, "currency": "JPY", "name": "도쿄", "unit": 100},
    "중국 (베이징)": {"lat": 39.9042, "lon": 116.4074, "currency": "CNY", "name": "베이징", "unit": 1},
    "미국 (뉴욕)": {"lat": 40.7128, "lon": -74.0060, "currency": "USD", "name": "뉴욕", "unit": 1}
}

selected_country = st.sidebar.selectbox("🌍 여행 국가 선택", list(countries_data.keys()))
target_info = countries_data[selected_country]

col1, col2 = st.columns([1, 1.5])

with col1:
    # **💱 실시간 환율 정보**
    try:
        res = requests.get("https://open.er-api.com/v6/latest/USD")
        rates = res.json()["rates"]
        krw_per_usd = rates["KRW"]
        curr_code = target_info["currency"]
        
        if curr_code == "KRW":
            st.info("대한민국 원화(KRW) 기준입니다.")
        else:
            target_per_usd = rates[curr_code]
            krw_per_target = krw_per_usd / target_per_usd
            unit = target_info["unit"]
            st.info(f"- {unit} {curr_code} = **{krw_per_target * unit:,.2f} 원**")
            
            amount_krw = st.number_input(f"환산할 금액 (KRW)", min_value=0, value=100000, step=10000)
            st.success(f"🧮 약 **{amount_krw / krw_per_target:,.2f} {curr_code}**")
    except Exception:
        st.warning("환율 정보를 불러올 수 없습니다.")
        
    st.write("---")
    
    # **🌤️ 날씨 정보**
    try:
        w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={target_info['lat']}&longitude={target_info['lon']}&current_weather=true")
        current = w_res.json()["current_weather"]
        st.metric(label=f"{target_info['name']} 기온", value=f"{current['temperature']} °C", delta=f"풍속: {current['windspeed']} km/h")
    except Exception:
        st.warning("날씨 정보를 불러올 수 없습니다.")

with col2:
    # **🗺️ 카카오맵 검색**
    if not KAKAO_APP_KEY:
        st.error("`.env` 파일에 `KAKAO_APP_KEY`를 설정해주세요.")
    else:
        # libraries=services 파라미터를 추가하여 장소 검색 기능 활성화
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                #searchWrap {{
                    position: absolute; top: 10px; left: 10px; z-index: 10;
                    background: rgba(255, 255, 255, 0.9); padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                }}
            </style>
        </head>
        <body style="margin:0;">
            <div id="map" style="width:100%;height:550px;"></div>
            <div id="searchWrap">
                <input type="text" id="keyword" value="{target_info['name']} 맛집" onkeypress="if(event.keyCode==13) searchPlaces();" style="padding:5px;">
                <button onclick="searchPlaces()" style="padding:5px 10px; cursor:pointer;">검색</button>
            </div>

            <script src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_APP_KEY}&libraries=services"></script>
            <script>
                if (typeof kakao === 'undefined') {{
                    document.body.innerHTML = "<div style='padding:20px; color:red;'><b>오류: 카카오맵이 차단되었습니다.</b><br>브라우저 주소창 왼쪽의 자물쇠나 눈 모양 아이콘을 눌러 '추적 방지'를 끄고 새로고침 하세요.</div>";
                }} else {{
                    var mapContainer = document.getElementById('map'),
                        mapOption = {{ center: new kakao.maps.LatLng({target_info['lat']}, {target_info['lon']}), level: 4 }};
                    var map = new kakao.maps.Map(mapContainer, mapOption);
                    var ps = new kakao.maps.services.Places();
                    var markers = [];
                    var infowindow = new kakao.maps.InfoWindow({{zIndex:1}});

                    function searchPlaces() {{
                        var keyword = document.getElementById('keyword').value;
                        if (!keyword.trim()) return alert('키워드를 입력해주세요!');
                        ps.keywordSearch(keyword, placesSearchCB);
                    }}

                    function placesSearchCB(data, status) {{
                        if (status === kakao.maps.services.Status.OK) {{
                            var bounds = new kakao.maps.LatLngBounds();
                            for (var i=0; i<markers.length; i++) markers[i].setMap(null);
                            markers = [];

                            for (var i=0; i<data.length; i++) {{
                                displayMarker(data[i]);
                                bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
                            }}
                            map.setBounds(bounds);
                        }} else {{
                            alert('검색 결과가 없습니다.');
                        }}
                    }}

                    function displayMarker(place) {{
                        var marker = new kakao.maps.Marker({{ map: map, position: new kakao.maps.LatLng(place.y, place.x) }});
                        markers.push(marker);
                        kakao.maps.event.addListener(marker, 'click', function() {{
                            infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
                            infowindow.open(map, marker);
                        }});
                    }}
                    
                    searchPlaces(); // 초기 로딩 시 기본값 자동 검색
                }}
            </script>
        </body>
        </html>
        """
        components.html(html_code, height=570)