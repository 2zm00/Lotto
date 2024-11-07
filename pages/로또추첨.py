# 로또추첨.py

import streamlit as st
import pandas as pd


from pages.functions.get_data import Lotto_class
from pages.tabs_view.tab1 import display_current_numbers 
from pages.tabs_view.tab2 import display_past_records    
from pages.tabs_view.tab3 import draw_number    

from pages.functions import get_address

import folium
from streamlit_folium import folium_static

#%%
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


#%%




# Selectbox로 메뉴 선택
selected_option = st.selectbox("메뉴 선택", ["AI 로또 추첨기", "최근 당첨 통계", "과거 당첨 기록", "당첨 주소"])

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
    fixed_number_input = st.text_input("", key="fixed_number_input")

    st.markdown(
        """
        <style>
        div.stTextInput > label { margin-top: -10px; }
        div.stTextInput > label { margin-bottom: -10px; }
        </style>
        
        <div style="line-height:1.2;">
            제외 번호를 선택하시겠습니까?<br>
            <span style="font-size: 0.9em; color: gray;">(예: 공백 또는 3, 5, 12)</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 제외 번호 입력 (숫자만 허용)
    excluded_numbers_input = st.text_input("", key="excluded_numbers_input")

    # 사용자가 몇 개의 번호를 추첨할지 입력할 수 있는 텍스트 입력 필드 추가
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)  # 여기에 마진을 추가
    num_draws = st.number_input('몇 개의 추가 번호를 뽑으시겠습니까?', min_value=1, max_value=10, value=3)


    # 생성 버튼 추가
    if st.button('번호 생성'):
        st.write("생성된 번호 :")

        # 입력한 숫자 리스트로 변환
        if fixed_number_input:
            # 쉼표를 기준으로 나누고, 숫자로 변환 후 리스트 생성
            fixed_number = [int(num.strip()) for num in fixed_number_input.split(',') if num.strip().isdigit()]
        else:
            fixed_number = None  # 입력이 없으면 빈 리스트
            
        if excluded_numbers_input:
            # 쉼표를 기준으로 나누고, 숫자로 변환 후 리스트 생성
            excluded_numbers = [int(num.strip()) for num in excluded_numbers_input.split(',') if num.strip().isdigit()]
        else:
            excluded_numbers = None  # 입력이 없으면 빈 리스트
        

        draw_number(최근회차, 전체기록,fixed_number,excluded_numbers, num_draws )

elif selected_option == "당첨 주소":
                
    
        
    st.title("당첨 지점")
    
    
    # 데이터 가져오기 (get_address는 외부 함수로 가정)
    soup = get_address.reqeusts_address(최근회차)
    address1 = get_address.get_address(soup, 등위=1)
    address2 = get_address.get_address(soup, 등위=2)
    
    # 1등, 2등 구분을 위한 rank 컬럼 추가
    address1['rank'] = 1
    address2['rank'] = 2
    
    # 좌표 없는 데이터 제외
    address1 = address1.dropna(subset=['lat', 'lng'])
    address2 = address2.dropna(subset=['lat', 'lng'])
    
    # 첫 번째 마커의 좌표를 중심으로 지도 생성
    latitude1 = address1['lat'].iloc[0]
    longitude1 = address1['lng'].iloc[0]
    map_center = [latitude1, longitude1]  # 첫 번째 마커 위치로 지도 중심 설정
    my_map = folium.Map(location=map_center, zoom_start=12)
        
        
    # 1등, 2등 선택 라디오 버튼
    prize_selection = st.radio(
        "당첨 등수 선택",
        ["1등", "2등", "모두 보기"]
    )
    

    # 선택에 따른 데이터 필터링
    if prize_selection == "1등":
        
        # 1등 마커 추가
        for i in range(len(address1)):
            latitude1 = address1['lat'].iloc[i]
            longitude1 = address1['lng'].iloc[i]
            이름1 = address1['name'].iloc[i]
            주소1 = address1['address'].iloc[i]
            
            # 팝업을 HTML로 작성하여 가로로 표시되게 스타일을 적용
            popup_content = f'<div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">1등 당첨지역 : {이름1}<br>주소 : {주소1}</div>'
            folium.Marker([latitude1, longitude1], popup=folium.Popup(popup_content, max_width=200)).add_to(my_map)
            
    elif prize_selection == "2등":
        
        # 2등 마커 추가
        for i in range(len(address2)):
            latitude2 = address2['lat'].iloc[i]
            longitude2 = address2['lng'].iloc[i]
            이름2 = address2['name'].iloc[i]
            주소2 = address2['address'].iloc[i]
            
            # 팝업을 HTML로 작성하여 가로로 표시되게 스타일을 적용
            popup_content = f'<div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">2등 당첨지역 : {이름2}<br>주소 : {주소2}</div>'
            folium.Marker([latitude2, longitude2], popup=folium.Popup(popup_content, max_width=200)).add_to(my_map)
    else:
    
        # 1등 마커 추가
        for i in range(len(address1)):
            latitude1 = address1['lat'].iloc[i]
            longitude1 = address1['lng'].iloc[i]
            이름1 = address1['name'].iloc[i]
            주소1 = address1['address'].iloc[i]
            
            # 팝업을 HTML로 작성하여 가로로 표시되게 스타일을 적용
            popup_content = f'<div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">1등 당첨지역 : {이름1}<br>주소 : {주소1}</div>'
            folium.Marker([latitude1, longitude1], popup=folium.Popup(popup_content, max_width=200)).add_to(my_map)
            
        
        # 2등 마커 추가
        for i in range(len(address2)):
            latitude2 = address2['lat'].iloc[i]
            longitude2 = address2['lng'].iloc[i]
            이름2 = address2['name'].iloc[i]
            주소2 = address2['address'].iloc[i]
            
            # 팝업을 HTML로 작성하여 가로로 표시되게 스타일을 적용
            popup_content = f'<div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">2등 당첨지역 : {이름2}<br>주소 : {주소2}</div>'
            folium.Marker([latitude2, longitude2], popup=folium.Popup(popup_content, max_width=200)).add_to(my_map)

    
    # Streamlit에 지도 표시
    folium_static(my_map)
    
        