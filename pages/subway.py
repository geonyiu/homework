import streamlit as st
import pandas as pd
import altair as alt

st.title("지하철 혼잡도 정보 찾기")
st.text("[자료 설명] 서울교통공사 1-8호선 30분 단위 평균 혼잡도로 30분간 지나는 열차들의 평균 혼잡도(정원대비 승차인원으로, 승차인과 좌석수가 일치할 경우를 혼잡도 34%로 산정) 입니다.(단위: %). 서울교통공사 혼잡도 데이터는 요일구분(평일, 토요일, 일요일), 호선, 역번호, 역명, 상하선구분, 30분단위 별 혼잡도 데이터로 구성되어 있습니다.")

# Load the dataset
data = pd.read_csv("지하철혼잡도정보_20240930.csv")

# Define time columns (시간대 열 필터링)
time_columns = [col for col in data.columns if "시" in col]

if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]

# Sidebar with user ID
with st.sidebar:
    st.caption(f'{ID}님 접속중')

# Form for user input
with st.form("input"):
    day_type = st.multiselect("요일구분", data['요일구분'].unique())
    line = st.multiselect("호선", data['호선'].unique())
    departure_station = st.multiselect("출발역", data['출발역'].unique())
    submitted = st.form_submit_button("조회")

    if submitted:
        # Initialize result storage
        chart_data = {"시간대": time_columns}  # Use a dictionary for chart data
        name_list = []

        for dt in day_type:
            for ln in line:
                for ds in departure_station:
                    name = f"{dt}_{ln}_{ds}"  # Create unique name for combination
                    name_list.append(name)

                    # Filter data for the current combination
                    selected_df = data[
                        (data['요일구분'] == dt) &
                        (data['호선'] == ln) &
                        (data['출발역'] == ds)
                    ]

                    if not selected_df.empty:
                        # Calculate average congestion for each time column
                        avg_congestion = selected_df[time_columns].mean().tolist()
                        chart_data[name] = avg_congestion  # Add to chart data

        # Prepare data for Altair chart
        if name_list:
            df = pd.DataFrame(chart_data)  # Convert chart_data to DataFrame
            df = df.melt(id_vars=["시간대"], var_name="조건", value_name="혼잡도")  # Reshape for Altair

            # 필터링: 시간대가 5시 30분 이후만 포함
            df = df[df["시간대"] >= "05:30"]

            # Create an Altair chart
            chart = alt.Chart(df).mark_line().encode(
                x=alt.X("시간대:O", sort=time_columns, title="시간대"),  # X축 시간대 설정
                y=alt.Y("혼잡도:Q", title="혼잡도 (%)"),  # Y축에 단위 추가
                color="조건:N"
            ).properties(
                width=800,
                height=400,
                title="지하철 혼잡도 그래프"
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
