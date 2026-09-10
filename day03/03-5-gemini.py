# 인코딩 자동 감지 + 한글 폰트 막대그래프
# 여러 인코딩("utf-8-sig", "cp949", "euc-kr")
# 내가 쓸 폰트 같은 경로에 있어야 함
# 객실 등급별 생존율 막대그래프 생성 후 그림으로 저장 chart.png
# 실행방법: streamlit run 03-5.py


import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import font_manager

st.title("인코딩 자동 감지 + 한글 폰트 막대 그래프 (Titanic 연습)")
st.caption("여러 인코딩 순서대로 시도해서 파일을 읽고, 객실등급별 생존율을 그래프로 그립니다..")

csv_path = os.path.join(os.path.dirname(__file__), "titanic_cleaned.csv")
font_path = os.path.join(os.path.dirname(__file__), "Distort-Medium.ttf")

def read_csv_with_auto_encoding(filepath):
    # 시도할 인코딩 목록
    encodings = ["utf-8-sig", "cp949", "euc-kr"]
    
    for enc in encodings:
        try:
            # 해당 인코딩으로 읽기 시도
            df = pd.read_csv(filepath, encoding=enc)
            st.success(f"✅ 성공: '{enc}' 인코딩으로 데이터를 불러왔습니다.")
            return df
        except UnicodeDecodeError:
            # 인코딩이 맞지 않으면 에러 무시하고 다음 인코딩 시도
            continue
        except FileNotFoundError:
            st.error(f"❌ 파일을 찾을 수 없습니다: {filepath}")
            return None
            
    # 모든 인코딩이 실패했을 경우
    st.error("❌ 지원하는 인코딩 형식(utf-8-sig, cp949, euc-kr)으로 파일을 읽을 수 없습니다.")
    return None

# 1. 데이터 불러오기 함수 실행
df = read_csv_with_auto_encoding(csv_path)

if df is not None:
    st.dataframe(df.head()) # 데이터 확인용 출력

    # 2. 한글 폰트 설정
    if os.path.exists(font_path):
        # 폰트 매니저에 폰트 추가 및 설정
        font_manager.fontManager.addfont(font_path)
        prop = font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = prop.get_name()
    else:
        st.warning(f"⚠️ 폰트 파일을 찾을 수 없습니다: {font_path} (기본 폰트를 사용합니다)")

    # 마이너스 폰트 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False 

    # 3. 데이터 가공: 객실 등급(Pclass)별 생존율(Survived) 계산
    # Survived 컬럼이 1(생존), 0(사망)이므로 평균(mean)을 구하면 생존율이 됩니다.
    if 'Pclass' in df.columns and 'Survived' in df.columns:
        survival_rate = df.groupby('Pclass')['Survived'].mean() * 100

        # 4. 막대그래프 생성
        fig, ax = plt.subplots(figsize=(7, 5))
        
        # 막대그래프 그리기 (색상 지정)
        bars = ax.bar(survival_rate.index.astype(str) + "등급", survival_rate.values, color=['#FF9999', '#66B2FF', '#99FF99'])
        
        # 그래프 디자인 추가
        ax.set_title("객실 등급별 생존율", fontsize=16, fontweight='bold', pad=15)
        ax.set_xlabel("객실 등급", fontsize=12)
        ax.set_ylabel("생존율 (%)", fontsize=12)
        ax.set_ylim(0, 100) # y축 범위를 0~100%로 고정
        
        # 막대 위에 정확한 수치(퍼센트) 텍스트 추가
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{height:.1f}%', ha='center', va='bottom')

        # 5. 그래프를 이미지 파일로 저장
        plt.savefig("chart.png", dpi=300, bbox_inches='tight')
        st.info("💾 그래프가 같은 폴더에 'chart.png' 파일로 저장되었습니다.")

        # 6. 스트림릿 화면에 그래프 출력
        st.pyplot(fig)
        
    else:
        st.error("데이터에 'Pclass' 또는 'Survived' 컬럼이 없어 그래프를 그릴 수 없습니다.")

































