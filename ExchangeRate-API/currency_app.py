import streamlit as st
import requests

# 1. 화면 제목
st.title("간편 환율 계산기 💱")
st.write("실시간 환율을 반영하여 계산합니다.")

# 2. UI 구성 (가로로 2칸 나누기)
col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox("어떤 통화에서?", ["USD", "EUR", "JPY", "KRW"])
with col2:
    to_currency = st.selectbox("어떤 통화로?", ["KRW", "USD", "EUR", "JPY"])

# 3. 금액 입력창
amount = st.number_input("금액을 입력하세요", min_value=0.0, value=1.0)

# 4. 계산 버튼 및 API 연동
if st.button("계산하기"):
    if from_currency == to_currency:
        st.warning("서로 다른 통화를 선택해주세요.")
    else:
        # Frankfurter API에 데이터 요청
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            # 결과값 추출 및 화면 출력
            result = data['rates'][to_currency]
            st.success(f"**{amount:,.2f} {from_currency} = {result:,.2f} {to_currency}**")
            
        except Exception as e:
            st.error("데이터를 가져오는 중 문제가 발생했습니다.")