import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# Streamlit Cloud의 Secrets 또는 로컬의 .streamlit/secrets.toml에서 키를 가져옵니다.
# 키가 없을 경우를 대비해 빈 문자열을 기본값으로 설정합니다.
try:
    OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except (FileNotFoundError, KeyError):
    OPENWEATHER_API_KEY = ""

if 'itinerary' not in st.session_state:
    st.session_state.itinerary = []

def search_places_global(keyword):
    url = "https://nominatim.openstreetmap.org/search"
    params = {'q': keyword, 'format': 'json', 'limit': 5, 'addressdetails': 1}
    headers = {'User-Agent': 'TravelDashboardApp/1.0'}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return [{
                'id': r.get('place_id'),
                'place_name': r.get('display_name', '').split(',')[0] if r.get('display_name') else "알 수 없는 장소",
                'address_name': r.get('display_name', ''),
                'y': float(r.get('lat')),
                'x': float(r.get('lon'))
            } for r in response.json()]
    except Exception as e:
        st.error(f"검색 오류: {e}")
    return []

def get_exchange_rate():
    res = requests.get("https://open.er-api.com/v6/latest/USD")
    return res.json().get("rates", {}) if res.status_code == 200 else {}

def get_weather(lat, lon):
    if not OPENWEATHER_API_KEY:
        return None
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=kr"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None

def add_to_itinerary(place):
    if place['id'] not in [p['id'] for p in st.session_state.itinerary]:
        st.session_state.itinerary.append(place)

def clear_itinerary():
    st.session_state.itinerary = []

st.set_page_config(page_title="글로벌 여행 플래너", layout="wide")
st.title("🌍 글로벌 여행 날씨 & 일정 플래너")

with st.sidebar:
    st.header("💰 실시간 환율 (원화)")
    rates = get_exchange_rate()
    if rates:
        krw = rates.get("KRW", 0)
        jpy = rates.get("JPY", 0)
        eur = rates.get("EUR", 0)
        st.metric(label="1 USD (미국 달러)", value=f"{krw:,.2f} 원")
        if jpy > 0: st.metric(label="100 JPY (일본 엔)", value=f"{(krw / jpy) * 100:,.2f} 원")
        if eur > 0: st.metric(label="1 EUR (유로)", value=f"{(krw / eur):,.2f} 원")
            
    st.divider()
    
    st.header("📝 나의 여행 일정")
    if not st.session_state.itinerary:
        st.info("검색 후 장소를 추가해 일정을 짜보세요.")
    else:
        for idx, place in enumerate(st.session_state.itinerary):
            st.markdown(f"**{idx + 1}. {place['place_name']}**")
            st.caption(place['address_name'])
        if st.button("일정 전체 초기화", type="primary"):
            clear_itinerary()
            st.rerun()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔍 전 세계 장소 검색")
    search_keyword = st.text_input("목적지를 검색하세요", key="search_input")
    
    if search_keyword:
        results = search_places_global(search_keyword)
        if results:
            for r in results:
                with st.container(border=True):
                    st.markdown(f"**{r['place_name']}**")
                    st.caption(r['address_name'])
                    st.button("➕ 일정에 추가", key=f"add_{r['id']}", on_click=add_to_itinerary, args=(r,))
        else:
            st.warning("결과가 없습니다.")
            
    if st.session_state.itinerary:
        st.divider()
        last_place = st.session_state.itinerary[-1]
        st.subheader(f"📍 {last_place['place_name']} 현지 날씨")
        weather = get_weather(last_place['y'], last_place['x'])
        
        if weather:
            st.metric(label="현재 온도", value=f"{weather['main']['temp']:.1f} °C", 
                      delta=f"체감 {weather['main']['feels_like']:.1f} °C", delta_color="off")
            st.write(f"상태: {weather['weather'][0]['description']}")
        else:
            st.warning("날씨 API 키가 설정되지 않았거나 유효하지 않습니다.")

with col2:
    st.subheader("📍 나의 이동 동선")
    start_lat, start_lon = (float(st.session_state.itinerary[0]['y']), float(st.session_state.itinerary[0]['x'])) if st.session_state.itinerary else (37.5665, 126.9780)
    zoom = 13 if st.session_state.itinerary else 3
        
    m = folium.Map(location=[start_lat, start_lon], zoom_start=zoom)
    
    if st.session_state.itinerary:
        route_coords = []
        for idx, place in enumerate(st.session_state.itinerary):
            lat, lon = float(place['y']), float(place['x'])
            route_coords.append([lat, lon])
            folium.Marker([lat, lon], popup=f"{idx + 1}. {place['place_name']}", tooltip=place['place_name'], icon=folium.Icon(color="red", icon="info-sign")).add_to(m)
            
        if len(route_coords) > 1:
            folium.PolyLine(locations=route_coords, color="blue", weight=3, opacity=0.7).add_to(m)
            
    st_folium(m, width="100%", height=600)