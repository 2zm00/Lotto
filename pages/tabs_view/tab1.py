# tab1
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

from page3 import draw_lotto_numbers



# 색상 지정 함수
def get_color(number):
    number = int(number)
    if 1 <= number <= 10:
        return "#f9c74f"  # 노란색
    elif 11 <= number <= 20:
        return "#007bff"  # 파란색
    elif 21 <= number <= 30:
        return "#dc3545"  # 빨간색
    elif 31 <= number <= 40:
        return "#6c757d"  # 회색
    elif 41 <= number <= 45:
        return "#28a745"  # 녹색
    else:
        return "#000000"  # 기본 색상
    
def display_lotto_numbers(numbers):
    lotto_balls_html = '''
    <style>
        .lotto-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            margin-bottom: 20px;
        }
        .lotto-ball {
            border-radius: 50%;
            width: 50px;  /* 기본 너비 */
            height: 50px; /* 기본 높이 */
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 5px;
            color: white;
            font-weight: bold;
        }
        @media (max-width: 600px) { /* 모바일 화면 */
            .lotto-ball {
                width: 40px;  /* 모바일에서는 너비를 줄임 */
                height: 40px; /* 모바일에서는 높이를 줄임 */
            }
        }
    </style>
    <div class="lotto-container">
    '''
    
    for value in numbers.values():
        color = get_color(value)
        lotto_balls_html += f'<div class="lotto-ball" style="background-color: {color};">{value}</div>'
    lotto_balls_html += '</div>'
    
    st.markdown(lotto_balls_html, unsafe_allow_html=True)






def display_current_numbers(lotto_instance, 최근회차, 전체기록):
    st.header("당첨 번호")
    당첨번호 = lotto_instance.check_num(최근회차)
    display_lotto_numbers(당첨번호)

    통계 = []
    for i in range(1, 46):
        통계.append(draw_lotto_numbers.analyze_number(전체기록, 최근회차, i))

    통계 = pd.DataFrame(통계)

    # 사용자 지정 폰트 로드
    font_path = 'fonts/NotoSansKR-VariableFont_wght.ttf'  # 경로를 조정하세요
    font_prop = font_manager.FontProperties(fname=font_path)



    # Streamlit에서 제목 설정
    st.title("최근 100회 출현")

    # x축 및 y축 설정
    x = 통계["번호"]
    y = 통계["최근 100회차 출현 횟수"]

    # 색상 설정
    colors = plt.cm.coolwarm(np.interp(y, (y.min(), y.max()), (0, 1)))

    # 그래프를 그리기
    plt.figure(figsize=(12, 6))
    bars = plt.bar(x, y, color=colors)

    # x축의 눈금 설정 (2당 하나씩)
    plt.xticks(ticks=x[::2], labels=x[::2])

    # 그래프 레이블 및 제목 설정
    plt.title("최근 100회 동안 출현 횟수", fontproperties=font_prop, fontsize=16)
    plt.xlabel("로또 번호", fontproperties=font_prop, fontsize=14)
    plt.ylabel("횟수", fontproperties=font_prop, fontsize=14)
    
    # y축의 범위를 조정하여 적절한 눈금 표시
    plt.ylim(0, max(y) * 1.1)  # 최대값보다 약간 높은 값으로 y축 설정


    # 각 막대 위에 번호 표시
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontproperties=font_prop)

    # 그래프를 Streamlit에 표시
    st.pyplot(plt)
    plt.close()  # Streamlit에서 plt 객체를 클리어
    
    
    
    # Streamlit에서 제목 설정
    st.title("최근 4회 출현")

    # x축 및 y축 설정
    x = 통계["번호"]
    y = 통계["최근 4회차 출현 횟수"]

    # 색상 설정
    colors = plt.cm.coolwarm(np.interp(y, (y.min(), y.max()), (0, 1)))

    # 그래프를 그리기
    plt.figure(figsize=(12, 6))
    bars = plt.bar(x, y, color=colors)

    # x축의 눈금 설정 (2당 하나씩)
    plt.xticks(ticks=x[::2], labels=x[::2])

    # 그래프 레이블 및 제목 설정
    plt.title("최근 4회 동안 출현 횟수", fontproperties=font_prop, fontsize=16)
    plt.xlabel("로또 번호", fontproperties=font_prop, fontsize=14)
    plt.ylabel("횟수", fontproperties=font_prop, fontsize=14)

    # 각 막대 위에 번호 표시
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontproperties=font_prop)

    # 그래프를 Streamlit에 표시
    st.pyplot(plt)
    plt.close()  # Streamlit에서 plt 객체를 클리어




    # Streamlit에서 제목 설정
    st.title("연속 출현")

    # x축 및 y축 설정
    x = 통계["번호"]
    y = 통계["연속 출현 횟수"]

    # 색상 설정
    colors = plt.cm.coolwarm(np.interp(y, (y.min(), y.max()), (0, 1)))


    # 그래프를 그리기
    plt.figure(figsize=(12, 6))
    bars = plt.bar(x, y, color=colors)

    # x축의 눈금 설정 (2당 하나씩)
    plt.xticks(ticks=x[::2], labels=x[::2])

    # 그래프 레이블 및 제목 설정
    plt.title("최근 연속으로 나온 횟수", fontproperties=font_prop, fontsize=16)
    plt.xlabel("로또 번호", fontproperties=font_prop, fontsize=14)
    plt.ylabel("횟수", fontproperties=font_prop, fontsize=14)

    # 각 막대 위에 번호 표시
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontproperties=font_prop)

    # 그래프를 Streamlit에 표시
    st.pyplot(plt)
    plt.close()  # Streamlit에서 plt 객체를 클리어




    # Streamlit에서 제목 설정
    st.title("연속 미출현")

    # x축 및 y축 설정
    x = 통계["번호"]
    y = 통계["연속 미출현 횟수"]

    # 색상 설정
    colors = plt.cm.coolwarm(np.interp(y, (y.min(), y.max()), (0, 1)))


    # 그래프를 그리기
    plt.figure(figsize=(12, 6))
    bars = plt.bar(x, y, color=colors)

    # x축의 눈금 설정 (2당 하나씩)
    plt.xticks(ticks=x[::2], labels=x[::2])

    # 그래프 레이블 및 제목 설정
    plt.title("최근 연속으로 안나온 횟수", fontproperties=font_prop, fontsize=16)
    plt.xlabel("로또 번호", fontproperties=font_prop, fontsize=14)
    plt.ylabel("횟수", fontproperties=font_prop, fontsize=14)

    # 각 막대 위에 번호 표시
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontproperties=font_prop)

    # 그래프를 Streamlit에 표시
    st.pyplot(plt)
    plt.close()  # Streamlit에서 plt 객체를 클리어

