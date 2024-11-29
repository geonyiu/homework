import streamlit as st
import pandas as pd
import time

st.title("통합데이터 서비스")
st.image("image.jpg")

# CSV 파일 불러오기
try:
    data = pd.read_csv("members.csv")
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")
    st.stop()

# 로그인 상태 변수 초기화
if "ID" not in st.session_state:
    st.session_state.ID = ""
if "PW" not in st.session_state:
    st.session_state.PW = ""
if "login_success" not in st.session_state:
    st.session_state.login_success = False
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False  # 로그인 실패 상태

# 로그인 폼
with st.form("login_form",clear_on_submit=True):
    ID = st.text_input("ID", value=st.session_state.ID, placeholder="아이디를 입력하세요")
    PW = st.text_input("Password", value=st.session_state.PW, type="password", placeholder="비밀번호를 입력하세요")
    submit_button = st.form_submit_button("로그인")

if submit_button:
    if not ID or not PW:
        st.warning("ID와 비밀번호를 모두 입력해주세요")
        st.session_state.login_failed = False  # 경고 메시지 상태에서는 새로고침하지 않음
    else:
        # 데이터 정리
        data["ID"] = data["ID"].astype(str).str.strip()
        data["PW"] = data["PW"].astype(str).str.strip()
        ID = ID.strip()
        PW = PW.strip()

        # 로그인 체크
        user = data[(data["ID"] == ID) & (data["PW"] == PW)]
        if not user.empty:
            st.success(f"{ID}님 환영합니다")
            st.session_state.login_success = True
            st.session_state.login_failed = False  # 성공 시 실패 상태 초기화
            st.session_state.ID = ID  # 로그인 성공 시 ID 유지
            st.session_state.PW = ""  # 비밀번호 초기화
            st.switch_page("pages/bus.py")
        else:
            st.warning("사용자 정보가 일치하지 않습니다.")
            st.session_state.login_failed = True  # 실패 상태 설정

# 로그인 실패 시 페이지 새로고침
if st.session_state.login_failed:
    time.sleep(2)  # 2초 대기 후 새로고침
    st.session_state.login_failed = False  # 실패 상태 초기화
    st.session_state.ID = ""  # 실패 시 ID 초기화
    st.session_state.PW = ""  # 실패 시 PW 초기화

    st.rerun()  # 새로고침

