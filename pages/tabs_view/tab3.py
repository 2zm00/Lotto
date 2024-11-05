# my_html/tab3.py

from pages.functions import draw_lotto_numbers
import streamlit as st

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

def draw_number(최근회차, 전체기록,picked_num, n = 1 ):
    for _ in range(n):  # n을 사용하여 지정된 횟수만큼 반복
        drawed_numbers = draw_lotto_numbers.draw_lotto_numbers(최근회차, 전체기록 , picked_num)
        display_lotto_numbers(drawed_numbers.iloc[0].to_dict())
        
        
        
        
        
        
        
        
        
        
        
        
        
        