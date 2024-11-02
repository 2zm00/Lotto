import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



class DashBoard():
    def __init__(self):
        self.data = None
        self.auth = False

    def 인증_상태(self):
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
        self.auth = True




# """
# #pandas를 이요해서 csv파일 불러오기
# """
    @st.cache_data
    def 데이터_불러오기(_self):
        try:
            df = pd.read_csv('data/user_data.csv')
            df.columns = df.columns.str.strip()
            return df
        except FileNotFoundError:
            st.error("데이터 파일을 찾을 수 없습니다.")
            return None

    def 데이터_보여주기(self, df):
            # 나이대별 그래프
        plt.figure(figsize=(10, 6))
        plt.plot(df['age'], df['draw_count'], marker='o')
        plt.title('age/drawcount')
        plt.xlabel('age')
        plt.ylabel('drawcount')
        plt.grid(True)
        st.pyplot(plt)
        plt.close()
        
        # 성별 그래프
        plt.figure(figsize=(8, 6))
        male_data = df[df['gender'] == '남성']['draw_count']
        female_data = df[df['gender'] == '여성']['draw_count']
        plt.bar(['Male', 'Female'], [male_data.sum(), female_data.sum()])
        plt.title('gender/drawcount')
        plt.ylabel('drawcount')
        st.pyplot(plt)
        plt.close()
        
        # 시군구별 그래프
        plt.figure(figsize=(12, 6))
        districts = [x.split()[2] if len(x.split()) > 2 else x for x in df['region']]
        plt.bar(districts, df['draw_count'])
        plt.title('region/drawcount')
        plt.xticks(rotation=45)
        plt.ylabel('draw_count')
        st.pyplot(plt)
        plt.close()

        
        # 행정구역별 그래프
        plt.figure(figsize=(10, 6))
        regions = [x.split()[0] for x in df['region']]
        plt.bar(regions, df['draw_count'])
        plt.title('region/draw_count')
        plt.xticks(rotation=45)
        plt.ylabel('draw_count')
        st.pyplot(plt)
        plt.close()

        
        # 평균 추첨 횟수
        avg_draw = df['draw_count'].mean()
        st.metric("평균 추첨 횟수", f"{avg_draw:.2f}회")



    def main(self):
        # self.인증_상태()
        # if not self.auth:
        #     return
            
        st.title("어드민만 확인 가능한 Dashboard")

        df = self.데이터_불러오기()
        if df is not None:
            self.데이터_보여주기(df)




# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 저 데이터 불러온거 표현이 영어로 밖에 안되서 일단 수정해야될 거 같습니다.



if __name__ == "__main__":
    dashboard = DashBoard()
    dashboard.main()