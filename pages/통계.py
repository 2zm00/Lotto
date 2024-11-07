import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import json



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
        
    def load_data(self):
        with open('data/user_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

        
    @staticmethod
    def set_korean_font():
        # 폰트 경로 설정
        font_path = os.path.join('pages', 'fonts', 'NotoSansKR-VariableFont_wght.ttf')
        
        # 폰트 등록
        font_prop = fm.FontProperties(fname=font_path)
        fm.fontManager.addfont(font_path)
        
        # matplotlib 기본 설정 업데이트
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False
        return font_prop


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
        font_prop = self.set_korean_font()
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
        ax.set_ylabel("추첨 횟수", fontsize=14, fontproperties=font_prop)

        # 막대 위에 수치 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontproperties=font_prop)
        
        #연령대 그래프 streamlit 표시
        st.pyplot(fig)
        plt.close()

        
    def 성별_그래프(self, df):
        font_prop = self.set_korean_font()
        st.subheader("성별 추첨 횟수")
        
        gender_data = df.groupby('gender')['draw_count'].sum()
        x = gender_data.index
        y = gender_data.values
        # 색 설정
        colors = plt.cm.coolwarm(np.interp(y, (y.min(), y.max()), (0, 1)))

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(x,y, color=colors)
        
        ax.set_ylabel("추첨 횟수", fontsize=14, fontproperties=font_prop)
        
        # 막대 위에 수치 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontproperties=font_prop)
        
        st.pyplot(fig)
        plt.close()
        
    def 시군구_그래프(self, df):
        font_prop = self.set_korean_font()
        st.subheader("시군구 별 추첨 횟수")
        
        district_data = df.groupby('city')['draw_count'].sum()
        x=district_data.index
        y=district_data.values
        # 색 설정
        colors = plt.cm.coolwarm(np.interp(y, (y.min(), y.max()), (0, 1)))

        fig, ax = plt.subplots(figsize=(15, 6))
        bars = ax.bar(x, y, color=colors)
        
        ax.set_ylabel("추첨 횟수", fontsize=14, fontproperties=font_prop)
        plt.xticks(rotation=45, ha='right', fontproperties=font_prop)
        
        # 막대 위에 수치 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontproperties=font_prop)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    def 행정구역_그래프(self, df):
        font_prop = self.set_korean_font()
        st.subheader("행정구역 별 추첨 횟수")
        
        df['administrative_region'] = df['region'].apply(lambda x: x.split()[0])
        city_data = df.groupby('administrative_region')['draw_count'].sum()
        x = city_data.index
        y = city_data.values
        # 색 설정
        colors = plt.cm.coolwarm(np.interp(y, (y.min(), y.max()), (0, 1)))

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(x, y, color=colors)
        
        ax.set_ylabel("추첨 횟수", fontsize=14, fontproperties=font_prop)
        plt.xticks(rotation=45, ha='right', fontproperties=font_prop)
        
        # 막대 위에 수치 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontproperties=font_prop)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    def 평균_추첨_횟수(self, df):
        st.subheader("평균 추첨 횟수")
        avg_draw = df['draw_count'].mean()
        st.metric("",""f"{avg_draw:.2f}회")



    def main(self):
        # self.인증_상태()
        # if not self.auth:
        #     return
            
        st.title("관리자 대시보드")
        user_data=self.load_data()
        df = pd.DataFrame(user_data.values())
        
        if df is not None:
            self.데이터_보여주기(df)







if __name__ == "__main__":
    dashboard = DashBoard()
    dashboard.main()