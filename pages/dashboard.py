import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
#영록님께서 로컬 폰트 사용하셔서, 저는 다른 방식으로 폰트 사용해보는 방식으로 pyfont로 진행했습니다.


class DashBoard():
    def __init__(self):
        self.data = None
        self.auth = False
        self.set_korean_font()

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
        
    @staticmethod
    def set_korean_font():
        # 나눔고딕 폰트 설정
        plt.rcParams['font.family'] = 'NanumGothic'
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지



    def 데이터_보여주기(self, df):
        # 연령대별 그래프
        self.연령대_그래프(df)
        
        # 성별 그래프
        self.성별_그래프(df)

        # 행정구역별 그래프
        self.행정구역_그래프(df)

        # 시군구별 그래프
        self.시군구_그래프(df)
        
        
        # 평균 추첨 횟수
        self.평균_추첨_횟수(df)

    def 연령대_그래프(self, df):
        # 나이대별 그래프 제목 설정
        st.subheader("연령대 별 추첨 횟수")

        # X축 Y축 설정
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        labels = ['10대', '20대', '30대', '40대', '50대', '60대', '70대', '80대', '90대', '100대']
        df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
        x = df['age_group']
        y = df['draw_count']

        # 색 설정
        colors = plt.cm.coolwarm(np.interp(y, (y.min(), y.max()), (0, 1)))

        #연령대 그래프 그리기
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(x, y, color=colors)


        #연령대 그래프 레이블 제목설정
        ax.set_title("연령대 별 추첨 횟수", fontsize=16)
        ax.set_xlabel("연령대", fontsize=14)
        ax.set_ylabel("추첨 횟수", fontsize=14)

        # 막대 위에 수치 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        #연령대 그래프 streamlit 표시
        st.pyplot(fig)
        plt.close()

        
    def 성별_그래프(self, df):
        st.subheader("성별 추첨 횟수")
        
        gender_data = df.groupby('gender')['draw_count'].sum()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(gender_data.index, gender_data.values, color=['blue', 'pink'])
        
        ax.set_title("성별 추첨 횟수", fontsize=16)
        ax.set_xlabel("성별", fontsize=14)
        ax.set_ylabel("추첨 횟수", fontsize=14)
        
        # 막대 위에 수치 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        st.pyplot(fig)
        plt.close()
        
    def 시군구_그래프(self, df):
        st.subheader("시군구별 추첨 횟수")
        
        df['district'] = df['region'].apply(
            lambda x: x.split()[2] if len(x.split()) > 2 else x
        )
        district_data = df.groupby('district')['draw_count'].sum()
        
        fig, ax = plt.subplots(figsize=(15, 6))
        bars = ax.bar(district_data.index, district_data.values)
        
        ax.set_title("시군구별 추첨 횟수", fontsize=16)
        ax.set_xlabel("시군구", fontsize=14)
        ax.set_ylabel("추첨 횟수", fontsize=14)
        plt.xticks(rotation=45, ha='right')
        
        # 막대 위에 수치 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    def 행정구역_그래프(self, df):
        st.subheader("행정구역별 추첨 횟수")
        
        df['city'] = df['region'].apply(lambda x: x.split()[0])
        city_data = df.groupby('city')['draw_count'].sum()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(city_data.index, city_data.values)
        
        ax.set_title("행정구역별 추첨 횟수", fontsize=16)
        ax.set_xlabel("행정구역", fontsize=14)
        ax.set_ylabel("추첨 횟수", fontsize=14)
        plt.xticks(rotation=45, ha='right')
        
        # 막대 위에 수치 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    def 평균_추첨_횟수(self, df):
        st.subheader("평균 추첨 횟수")
        avg_draw = df['draw_count'].mean()
        st.metric("", f"{avg_draw:.2f}회")



    def main(self):
        # self.인증_상태()
        # if not self.auth:
        #     return
            
        st.title("관리자 대시보드")

        df = self.데이터_불러오기()
        if df is not None:
            self.데이터_보여주기(df)







if __name__ == "__main__":
    dashboard = DashBoard()
    dashboard.main()