# 날씨 API 실습
# openweathermap 현재 날씨 API로 특정 도시의 날씨를 가져와 출력한다.
# 사전준비 openweathermap 회원 가입 후 API 발급
# pip install requests python-dotenv
# .env 파일을 생성하고 이곳에 openweather_api_key = API_code
# .env.example openweather_api_key = API_code
# .env.example 받아서 .env로 이름바꾸고 자기 API를 채운다.

import os
import requests
import streamlit as st
from dotenv import load_dotenv, find_dotenv

# 1. 상위 폴더에 있는 .env 파일 로드
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# 2. API 키 가져오기 (순서 변경 및 에러 처리 강화)
# 먼저 로컬의 .env 파일에서 키를 찾습니다.
api_key = os.getenv("openweather_api_key")

# .env에 키가 없다면 Streamlit Cloud 환경(st.secrets)에서 찾습니다.
if not api_key:
    try:
        api_key = st.secrets["openweather_api_key"]
    except Exception:
        # secrets.toml 파일이 없거나 키가 없어도 앱이 멈추지 않도록 패스합니다.
        pass

# 페이지 설정
st.set_page_config(page_title="실시간 날씨 앱", page_icon="🌤️", layout="centered")

st.title("🌤️ 실시간 날씨 정보 앱")
st.markdown("OpenWeatherMap API를 활용하여 전 세계 도시의 실시간 날씨를 확인해보세요!")

# 사용자로부터 도시 이름 입력 받기
city = st.text_input("도시 이름을 영어로 입력하세요 (예: Seoul, Tokyo, London, New York):", "Seoul")

# 버튼을 누르면 API를 호출하여 날씨 정보를 가져옵니다.
if st.button("날씨 확인하기"):
    if not api_key:
        st.error("API 키가 설정되지 않았습니다. .env 파일이나 Streamlit Secrets 설정을 확인해주세요.")
    elif city:
        # OpenWeatherMap API 호출 URL (단위: 섭씨(metric), 언어: 한국어(kr))
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=kr"
        
        with st.spinner('날씨 정보를 가져오는 중입니다...'):
            try:
                response = requests.get(url)
                data = response.json()
                
                # API 응답 성공 (상태 코드 200)
                if response.status_code == 200:
                    weather_desc = data['weather'][0]['description']
                    temp = data['main']['temp']
                    feels_like = data['main']['feels_like']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed']
                    
                    # 날씨 아이콘 이미지 URL
                    icon_code = data['weather'][0]['icon']
                    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                    
                    st.success(f"**{city.upper()}**의 현재 날씨입니다.")
                    
                    # 화면을 두 열로 나누어 예쁘게 배치
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.image(icon_url, width=120)
                        st.markdown(f"<h3 style='text-align: center; margin-top: -20px;'>{weather_desc}</h3>", unsafe_allow_html=True)
                        
                    with col2:
                        st.metric(label="현재 온도", value=f"{temp}°C")
                        st.write(f"🌡️ **체감 온도**: {feels_like}°C")
                        st.write(f"💧 **습도**: {humidity}%")
                        st.write(f"💨 **풍속**: {wind_speed} m/s")
                        
                else:
                    # 도시 이름을 잘못 입력했거나 오류가 났을 때
                    st.error(f"오류: {data.get('message', '도시를 찾을 수 없거나 API 요청에 문제가 있습니다.')}")
            
            except Exception as e:
                st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")