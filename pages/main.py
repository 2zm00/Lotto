# main.py
import streamlit as st
import pandas as pd
from page3.get_data import Lotto_class
from my_html.tab1 import display_current_numbers 
from my_html.tab2 import display_past_records    
from my_html.tab3 import draw_number    


st.set_page_config(page_title="진연녹의 AI 로또 추첨기!!")






# Lotto_class의 인스턴스 생성
lotto_instance = Lotto_class()

# 전체 기록을 캐시하는 함수
@st.cache_data
def load_all_records():
    최근회차 = lotto_instance.최근회차()
    전체기록 = pd.DataFrame(lotto_instance.download_records(1, 최근회차)).transpose()
    전체기록.index = 전체기록.index.str.replace('회차', '').astype(int)
    return 전체기록

# 전체 기록을 한 번만 불러오기
전체기록 = load_all_records()
최근회차 = lotto_instance.최근회차()

st.title('이번주 당첨번호')
st.title(f'최근 회차 : {최근회차}')




# Selectbox로 메뉴 선택
selected_option = st.selectbox("메뉴 선택", ["당첨 번호", "과거 당첨 기록", "AI 로또 추첨기", "당첨 주소"])

if selected_option == "당첨 번호":
    display_current_numbers(lotto_instance, 최근회차, 전체기록)

elif selected_option == "과거 당첨 기록":
    display_past_records(lotto_instance, 최근회차)

elif selected_option == "AI 로또 추첨기":
    st.markdown(
        """
        <style>
        div.stTextInput > label { margin-top: -10px; }
        </style>
        
        <div style="line-height:1.2;">
            고정 번호를 선택하시겠습니까?<br>
            <span style="font-size: 0.9em; color: gray;">(예: 공백 또는 3, 5, 12)</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 고정 번호 입력 (숫자만 허용)
    input_numbers = st.text_input("")

    # 사용자가 몇 개의 번호를 추첨할지 입력할 수 있는 텍스트 입력 필드 추가
    num_draws = st.number_input('몇 개의 추가 번호를 뽑으시겠습니까?', min_value=1, max_value=10, value=3)

    # 생성 버튼 추가
    if st.button('번호 생성'):
        st.write("생성된 번호 :")

        # 입력한 숫자 리스트로 변환
        if input_numbers:
            # 쉼표를 기준으로 나누고, 숫자로 변환 후 리스트 생성
            picked_num = [int(num.strip()) for num in input_numbers.split(',') if num.strip().isdigit()]
        else:
            picked_num = None  # 입력이 없으면 빈 리스트
        
        draw_number(최근회차, 전체기록, picked_num, num_draws)  # 입력받은 숫자를 draw_number 함수에 전달

elif selected_option == "당첨 주소":
    
    
    st.title('')
    
    # Google Maps iframe 사용
    st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3168.371067633137!2d126.97865241502782!3d37.56654197979855!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x357ca2ef8e8c5d61%3A0xf1de5e8d8e6de2c1!2sSeoul!5e0!3m2!1sen!2skr!4v1633124003205!5m2!1sen!2skr" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>', unsafe_allow_html=True)
    

# # 탭 추가
# tab1, tab2, tab3 ,tab4 = st.tabs(["당첨 번호", "과거 당첨 기록", "AI 로또 추첨기", "당첨 주소"])

# with tab1:
#     display_current_numbers(lotto_instance,최근회차, 전체기록)

# with tab2:
#     display_past_records(lotto_instance, 최근회차)

# with tab3:
            
#     st.markdown(
#                  """
#                  <style>
#                  div.stTextInput > label { margin-top: -10px; }
#                  </style>
                 
#                  <div style="line-height:1.2;">
#                      고정 번호를 선택하시겠습니까?<br>
#                      <span style="font-size: 0.9em; color: gray;">(예: 공백 또는 3, 5, 12)</span>
#                  </div>
#                  """,
#                  unsafe_allow_html=True
#                 )
    
    
#     # 고정 번호 입력 (숫자만 허용)
#     input_numbers = st.text_input("")
    
#     # 사용자가 몇 개의 번호를 추첨할지 입력할 수 있는 텍스트 입력 필드 추가
#     num_draws = st.number_input('몇 개의 추가 번호를 뽑으시겠습니까?', min_value=1, max_value=10, value=3)

#     # 생성 버튼 추가
#     if st.button('번호 생성'):
#         st.write("생성된 번호 :")
        

#         # 입력한 숫자 리스트로 변환
#         if input_numbers:
#             # 쉼표를 기준으로 나누고, 숫자로 변환 후 리스트 생성
#             picked_num = [int(num.strip()) for num in input_numbers.split(',') if num.strip().isdigit()]
#         else:
#             picked_num = None  # 입력이 없으면 빈 리스트
        
#         draw_number(최근회차, 전체기록,picked_num,num_draws)  # 입력받은 숫자를 draw_number 함수에 전달
        
   
# with tab4:
                 
#     st.title('Google Maps Example')
    
#     # Google Maps iframe 사용
#     st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3168.371067633137!2d126.97865241502782!3d37.56654197979855!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x357ca2ef8e8c5d61%3A0xf1de5e8d8e6de2c1!2sSeoul!5e0!3m2!1sen!2skr!4v1633124003205!5m2!1sen!2skr" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>', unsafe_allow_html=True)      
            
            
            
        
        
        
        