import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def check_auth():
# """
# #인증 상태 확인
# """
#로그인 로직에서 session_state를 사용해야하고, 로그인 상태 함수를 통일시켜야함.
	if '로그인 상태' not in st.session_state or not st.session_state['로그인 상태']:
		st.error("로그인 필요합니다.")
		st.stop()

# """
# #관리자 권한 확인
# """
	if st.session_state['사용자이름'] != "admin":
		st.error("관리자 권한 필요.")
		st.stop()




# """
# #pandas를 이요해서 csv파일 불러오기
# """
@st.cache_data
def 데이터_불러오기():
    try:
        유저데이터_df = pd.read_csv('data/예시파일.csv')
        로그_df = pd.read_csv('data/로그예시파일.csv')
        return 유저데이터_df, 로그_df
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다.")
        return None, None




def main():
    # 인증 체크
    # check_auth()
    
    # 대시보드 제목
    st.title("어드민만 확인 가능한 Dashboard")

    # 데이터 로드
    유저데이터_df, 로그_df = 데이터_불러오기()
    if 유저데이터_df is None or 로그_df is None:
        return




# """
# #contents 표시
# """
#여기를 이제 대시보드 레이아웃 설정해야할듯





# """
# #csv파일에서 dataframe 불러오기
# """



# """#나이대age 별 그래프 (x: 20대 30대~~ 60대 y:누적 추첨 횟수, 누적 로그인 기록)"""


# """#성별gender 그래프 (x:남 여 y:누적 추첨 횟수, 누적 로그인 기록)"""


# """#시군구별region 그래프 (x:시군구 region[2] y:누적 추첨 횟수 drawcount, 누적 로그인 기록 len(loggedat))"""


# """#지역별별region 그래프 (x:행정구역 region[0] y:이용자 수 len(user))"""


# """#평균 이용자 추첨 횟수 mean(draw_count)(몇 회)"""


if __name__ == "__main__":
    main()