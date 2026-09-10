# dldldldldl

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="수출 데이터 분석", layout="wide")

st.title("반도체류(HS 85) 수출 실적 분석 (미국 / 베트남)")

current_dir = os.path.dirname(__file__)

# 1. 원본 데이터 로드 (수정된 부분 ✨)
csv_path = os.path.join(current_dir, "raw_trade_data.csv") 
df = pd.read_csv(csv_path)

# 2. 다중 조건 필터링
# - HS코드가 '85'로 시작
# - 국가명이 '미국' 또는 '베트남'
# - 수출금액이 0 초과 (실제 실적 보유)
cond_hs = df["hs_code"].astype(str).str.startswith("85")
cond_country = df["국가명"].isin(["미국", "베트남"])
cond_amount = df["수출금액"] > 0

filtered_df = df[cond_hs & cond_country & cond_amount]

# 3. 수출금액 기준 내림차순 정렬 후 상위 10건 추출
top10_df = filtered_df.sort_values(by="수출금액", ascending=False).head(10).reset_index(drop=True)

# 4. report.csv 파일로 자동 저장 (한글 깨짐 방지 utf-8-sig)
top10_df.to_csv("report.csv", index=False, encoding="utf-8-sig")

# 5. Streamlit 화면 출력
st.subheader("📋 수출금액 상위 10건 내역")
st.dataframe(
    top10_df.style.format({
        "수출금액": "{:,.0f} USD",
        "중량": "{:,.2f} kg"
    }),
    use_container_width=True
)

st.success("✅ 상위 10건 데이터가 'report.csv'로 저장되었습니다.")

# 브라우저 직접 다운로드 버튼
st.download_button(
    label="📥 report.csv 다운로드",
    data=top10_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
    file_name="report.csv",
    mime="text/csv"
)