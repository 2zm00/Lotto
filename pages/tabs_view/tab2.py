# tab2
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

def display_past_records(lotto_instance, 최근회차):
    st.header("과거 당첨 기록")
    주차선택 = st.selectbox("주차를 선택하세요:", 
                             ["1주 전", "2주 전", "3주 전", "4주 전", 
                              "2달 전", "3달 전"])

    # 선택된 주차에 따른 데이터 출력
    if 주차선택 == "1주 전":
        과거기록 = lotto_instance.download_records(최근회차, 최근회차)
    elif 주차선택 == "2주 전":
        과거기록 = lotto_instance.download_records(최근회차-1, 최근회차)
    elif 주차선택 == "3주 전":
        과거기록 = lotto_instance.download_records(최근회차-2, 최근회차)
    elif 주차선택 == "4주 전":
        과거기록 = lotto_instance.download_records(최근회차-3, 최근회차)
    elif 주차선택 == "2달 전":
        과거기록 = lotto_instance.download_records(최근회차-7, 최근회차)
    elif 주차선택 == "3달 전":
        과거기록 = lotto_instance.download_records(최근회차-11, 최근회차)

    # 과거 기록 출력
    if 과거기록:
        for 회차, 번호 in 과거기록.items():
            st.subheader(f"{회차}회차")
            display_lotto_numbers(번호)
    else:
        st.write("해당 기록이 없습니다.")
