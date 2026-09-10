import os
import requests
import streamlit as st
from dotenv import load_dotenv, find_dotenv

# 1. .env 파일 자동 탐색 및 로드
load_dotenv(find_dotenv())

# 2. API 키 가져오기 (로컬 .env -> Streamlit Secrets 순서로 확인)
# 날씨 API 키
openweather_key = os.getenv("openweather_api_key")
if not openweather_key:
    try:
        openweather_key = st.secrets["openweather_api_key"]
    except Exception:
        pass

# 환율 API 키
exchangerate_key = os.getenv("exchangerate_api_key")
if not exchangerate_key:
    try:
        exchangerate_key = st.secrets["exchangerate_api_key"]
    except Exception:
        pass

# 3. 페이지 기본 설정 (넓은 화면 모드 사용)
st.set_page_config(page_title="글로벌 비즈니스 대시보드", page_icon="🌐", layout="wide")

st.title("🌐 글로벌 비즈니스 대시보드 (날씨 & 환율)")
st.markdown("전 세계 날씨와 실시간 주요 환율 정보를 한눈에 확인하세요.")
st.markdown("---")

# 검색 및 설정 영역
col_input1, col_input2 = st.columns(2)
with col_input1:
    city = st.text_input("📍 날씨를 조회할 도시 (예: Seoul, New York, London)", "Seoul")
with col_input2:
    base_currency = st.selectbox("💵 기준 통화 선택 (환율)", ["USD", "KRW", "EUR", "JPY"])

# 실행 버튼
if st.button("조회하기", use_container_width=True):
    
    # API 키 누락 확인
    if not openweather_key or not exchangerate_key:
        st.error("API 키가 설정되지 않았습니다. .env 파일을 다시 확인해주세요.")
    else:
        # 화면을 좌우 두 칸으로 나눕니다.
        col_weather, col_exchange = st.columns(2)
        
        # ==========================================
        # 왼쪽: 날씨 정보 섹션
        # ==========================================
        with col_weather:
            st.subheader(f"🌤️ {city.upper()} 현재 날씨")
            
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_key}&units=metric&lang=kr"
            try:
                w_response = requests.get(weather_url)
                w_data = w_response.json()
                
                if w_response.status_code == 200:
                    w_desc = w_data['weather'][0]['description']
                    temp = w_data['main']['temp']
                    feels_like = w_data['main']['feels_like']
                    humidity = w_data['main']['humidity']
                    
                    icon_code = w_data['weather'][0]['icon']
                    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                    
                    # 날씨 UI 배치
                    wc1, wc2 = st.columns([1, 2])
                    with wc1:
                        st.image(icon_url, width=100)
                        st.markdown(f"<p style='text-align:center; font-weight:bold;'>{w_desc}</p>", unsafe_allow_html=True)
                    with wc2:
                        st.metric(label="현재 온도", value=f"{temp}°C")
                        st.write(f"🌡️ 체감: {feels_like}°C | 💧 습도: {humidity}%")
                else:
                    st.error(f"날씨 오류: {w_data.get('message', '알 수 없는 오류')}")
            except Exception as e:
                st.error(f"날씨 데이터를 가져오는 중 오류 발생: {e}")
                
        # ==========================================
        # 오른쪽: 환율 정보 섹션
        # ==========================================
        with col_exchange:
            st.subheader(f"💱 실시간 환율 (기준: 1 {base_currency})")
            
            # ExchangeRate-API 호출 (v6 엔드포인트)
            exchange_url = f"https://v6.exchangerate-api.com/v6/{exchangerate_key}/latest/{base_currency}"
            try:
                e_response = requests.get(exchange_url)
                e_data = e_response.json()
                
                if e_data.get("result") == "success":
                    rates = e_data["conversion_rates"]
                    last_update = e_data["time_last_update_utc"]
                    
                    # 보여줄 주요 통화 목록 지정
                    target_currencies = ["KRW", "USD", "EUR", "JPY", "CNY", "GBP"]
                    # 기준 통화는 목록에서 제외
                    if base_currency in target_currencies:
                        target_currencies.remove(base_currency)
                    
                    # 환율 정보를 2열로 나열
                    ex_cols = st.columns(2)
                    for i, target in enumerate(target_currencies):
                        with ex_cols[i % 2]:
                            # 쉼표를 포함하여 소수점 둘째자리까지 표기
                            rate_value = f"{rates[target]:,.2f}"
                            st.metric(label=f"{target}", value=rate_value)
                            
                    st.caption(f"최근 업데이트: {last_update}")
                else:
                    st.error("환율 데이터를 불러오지 못했습니다.")
            except Exception as e:
                st.error(f"환율 데이터를 가져오는 중 오류 발생: {e}")