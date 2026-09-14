# folium으로 지도에 마커를 표시하는 예제코드
# import folium -> pip install folium
# 서울 시내 명소 4곳의 좌표(위도/경도)와 이름을 리스트로 받아 folium 지도를 만들고
# 각 좌표에 이름표가 붙은 마커를 찍은 다음, basic_map.html 파일로 저장하는 예제 코드입니다.
# 저장된 basic_map.html 웹 브라우저로 열어서 확인
# python 06-1.py

import folium

# 서울 시내 명소 4곳 이름, 위도, 경도 샘플 데이터
places = [
    {"name": "여의도한강공원", "lat": 37.5285, "lon": 126.9347},
    {"name": "경복궁", "lat": 37.5796, "lon": 126.9770},
    {"name": "홍대사거리", "lat": 37.5563, "lon": 126.9236},
    {"name": "명동", "lat": 37.5636, "lon": 126.9827},
]

# 서울 중심부 좌표로 지도 생성 (Stadia Alidade Smooth 타일 사용)
basic_map = folium.Map(
    location=[37.5665, 126.9780], 
    zoom_start=12,
    tiles="Stadia.AlidadeSmooth"
)

# 반복문을 통해 리스트의 장소들을 하나씩 꺼내어 마커 추가
for place in places:
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=place["name"],
        tooltip=place["name"]
    ).add_to(basic_map)

# 결과 지도를 HTML 파일로 저장
basic_map.save("basic_map.html")
print("지도가 성공적으로 저장되었습니다. 'basic_map.html' 파일을 열어보세요!")