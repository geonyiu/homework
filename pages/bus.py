import streamlit as st
import pandas as pd
import time

st.title("전국 버스정류장 지도")

if "ID" not in st.session_state:
    st.session_state["ID"] = "noname"
    
ID = st.session_state["ID"]
with st.sidebar:
    st.caption(f'{ID}님 접속중')

# CSV 파일 불러오기
data = pd.read_csv("전국 버스정류장 위치정보.csv")

# 결측치 제거
data = data.copy().fillna(0)

# 위도와 경도의 범위 설정 (대한민국 범위)
latitude_min, latitude_max = 33.0, 38.0
longitude_min, longitude_max = 124.0, 132.0

# 대한민국 범위 내 데이터 필터링
data = data[
    (data["위도"] >= latitude_min) & (data["위도"] <= latitude_max) &
    (data["경도"] >= longitude_min) & (data["경도"] <= longitude_max)
]

# 필터링된 데이터 표시
st.map(data, latitude="위도", longitude="경도")
