import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime

# ==========================================
# 1. 초기 설정 및 API 키
# ==========================================
st.set_page_config(page_title="트래블 마스터 대시보드", layout="wide", initial_sidebar_state="expanded")

try:
    OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except (FileNotFoundError, KeyError):
    OPENWEATHER_API_KEY = ""

if 'itinerary' not in st.session_state:
    st.session_state.itinerary = []

# 커스텀 CSS (UI 고급화)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0 0; gap: 1px; padding-top: 10px; padding-bottom: 10px; font-weight: 600; font-size: 1.1rem; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 데이터 처리 함수
# ==========================================
@st.cache_data(ttl=3600)
def get_exchange_rate():
    res = requests.get("https://open.er-api.com/v6/latest/USD")
    return res.json().get("rates", {}) if res.status_code == 200 else {}

def search_places_global(keyword):
    url = "https://nominatim.openstreetmap.org/search"
    params = {'q': keyword, 'format': 'json', 'limit': 8, 'addressdetails': 1}
    headers = {'User-Agent': 'TravelMasterApp/1.0'}
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return [{
                'id': r.get('place_id'),
                'place_name': r.get('display_name', '').split(',')[0],
                'address': r.get('display_name', ''),
                'lat': float(r.get('lat')),
                'lon': float(r.get('lon')),
                'type': r.get('type', 'Unknown')
            } for r in response.json()]
    except:
        pass
    return []

def get_weather(lat, lon):
    if not OPENWEATHER_API_KEY: return None
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=kr"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None

def add_to_itinerary(place):
    if place['id'] not in [p['id'] for p in st.session_state.itinerary]:
        place['added_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.itinerary.append(place)

# ==========================================
# 3. 메인 화면 UI 구성
# ==========================================
# 히어로 배너 이미지
st.image("https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=2000&q=80", use_container_width=True)
st.title("✈️ 황준영의 글로벌 트래블 마스터")
st.markdown("전 세계 장소 검색부터 날씨, 환율, 동선 데이터 분석까지 한 번에 관리하는 통합 대시보드입니다.")

# 탭 구조 생성
tab1, tab2, tab3 = st.tabs(["🌍 장소 검색 및 지도", "📋 내 일정 데이터 분석", "💰 실시간 글로벌 환율"])

# ----------------- 탭 1: 검색 및 지도 -----------------
with tab1:
    col_search, col_map = st.columns([1.2, 2])
    
    with col_search:
        st.subheader("🔍 목적지 검색")
        keyword = st.text_input("도시, 명소, 식당 등을 자유롭게 입력하세요", placeholder="예: 파리 루브르 박물관, 런던 타워브릿지")
        
        if keyword:
            with st.spinner('전 세계 데이터를 검색 중입니다...'):
                results = search_places_global(keyword)
            if results:
                for r in results:
                    with st.container(border=True):
                        st.markdown(f"**{r['place_name']}** <span style='color:gray; font-size:0.8em'>({r['type']})</span>", unsafe_allow_html=True)
                        st.caption(r['address'])
                        col_btn, col_blank = st.columns([1, 2])
                        with col_btn:
                            st.button("➕ 일정 추가", key=f"btn_{r['id']}", on_click=add_to_itinerary, args=(r,), use_container_width=True)
            else:
                st.warning("결과가 없습니다. 영어나 현지어로 검색해 보세요.")

        if st.session_state.itinerary:
            st.divider()
            last = st.session_state.itinerary[-1]
            st.subheader(f"🌤️ {last['place_name']} 현지 날씨")
            w_data = get_weather(last['lat'], last['lon'])
            if w_data:
                wc1, wc2, wc3 = st.columns(3)
                wc1.metric("현재 온도", f"{w_data['main']['temp']:.1f}°C", f"{w_data['main']['temp'] - 20:.1f}°C (어제대비)")
                wc2.metric("체감 온도", f"{w_data['main']['feels_like']:.1f}°C")
                wc3.metric("습도/상태", f"{w_data['main']['humidity']}%", w_data['weather'][0]['description'], delta_color="off")
            else:
                st.info("날씨 데이터를 불러오려면 정확한 API 키가 필요합니다.")

    with col_map:
        st.subheader("📍 인터랙티브 이동 동선")
        start_lat, start_lon = (st.session_state.itinerary[0]['lat'], st.session_state.itinerary[0]['lon']) if st.session_state.itinerary else (37.5665, 126.9780)
        m = folium.Map(location=[start_lat, start_lon], zoom_start=12 if st.session_state.itinerary else 2, tiles='CartoDB positron')
        
        if st.session_state.itinerary:
            coords = []
            for idx, p in enumerate(st.session_state.itinerary):
                coords.append([p['lat'], p['lon']])
                folium.Marker(
                    [p['lat'], p['lon']], 
                    popup=folium.Popup(f"<b>{idx+1}. {p['place_name']}</b><br>{p['address']}", max_width=300),
                    tooltip=p['place_name'],
                    icon=folium.Icon(color="darkblue", icon="info-sign")
                ).add_to(m)
            if len(coords) > 1:
                folium.PolyLine(coords, color="#2563eb", weight=4, opacity=0.8, dash_array='10').add_to(m)
                
        st_folium(m, width="100%", height=700)

# ----------------- 탭 2: 일정 데이터 분석 -----------------
with tab2:
    st.subheader("📊 일정 데이터 테이블")
    if not st.session_state.itinerary:
        st.info("선택된 일정이 없습니다. 검색 탭에서 장소를 추가해 주세요.")
    else:
        # Pandas DataFrame을 활용한 데이터 시각화
        df = pd.DataFrame(st.session_state.itinerary)
        df.index = df.index + 1
        display_df = df[['place_name', 'address', 'type', 'lat', 'lon', 'added_time']]
        display_df.columns = ['장소명', '상세주소', '장소유형', '위도', '경도', '추가된 시간']
        
        st.dataframe(display_df, use_container_width=True)
        
        col_clear, _ = st.columns([1, 5])
        with col_clear:
            if st.button("🗑️ 전체 일정 초기화", type="primary", use_container_width=True):
                st.session_state.itinerary = []
                st.rerun()

# ----------------- 탭 3: 환율 대시보드 -----------------
with tab3:
    st.subheader("💹 주요 국가 실시간 환율 (원화 환산)")
    rates = get_exchange_rate()
    if rates:
        krw = rates.get("KRW", 0)
        
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("🇺🇸 미국 (1 USD)", f"{krw:,.2f} 원")
        r2.metric("🇯🇵 일본 (100 JPY)", f"{(krw / rates.get('JPY', 1)) * 100:,.2f} 원" if rates.get('JPY') else "N/A")
        r3.metric("🇪🇺 유럽 (1 EUR)", f"{(krw / rates.get('EUR', 1)):,.2f} 원" if rates.get('EUR') else "N/A")
        r4.metric("🇬🇧 영국 (1 GBP)", f"{(krw / rates.get('GBP', 1)):,.2f} 원" if rates.get('GBP') else "N/A")
        
        st.caption(f"데이터 업데이트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    else:
        st.error("환율 API 서버에 연결할 수 없습니다.")