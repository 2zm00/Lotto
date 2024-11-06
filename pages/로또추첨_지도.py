# 로또추첨.py

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import urllib.parse


from pages.functions.get_data import Lotto_class
from pages.tabs_view.tab1 import display_current_numbers 
from pages.tabs_view.tab2 import display_past_records    
from pages.tabs_view.tab3 import draw_number    





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
                
    import re
    import requests
    import json
    
    from bs4 import BeautifulSoup
    import time
    
    
    KAKAO_REST_KEY = '60e0d7f939da04fcdb20bd983cb70fb2'
    
    def clean_address(address):
        """주소 정제 함수"""
        # 괄호와 그 안의 내용 제거
        address = re.sub(r'\([^)]*\)', '', address)
        
        # 층, 호수 등 상세주소 제거
        patterns = [
            r'\d+층\s*\d*호*',  # 1층, 1층 5호 등
            r'\d+호',           # 101호 등
            r'지하\d+층',       # 지하1층 등
            r'좌측상가',
            r'우측상가',
            r'앞 가판',
        ]
        
        for pattern in patterns:
            address = re.sub(pattern, '', address)
        
        return address.strip()
    
    def get_coordinates(address):
        """카카오맵 API로 주소를 좌표로 변환"""
        try:
            url = "https://dapi.kakao.com/v2/local/search/address.json"
            headers = {
                "Authorization": f"KakaoAK {KAKAO_REST_KEY}"
            }
            params = {"query": address}
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                result = json.loads(response.text)
                if result['documents']:
                    return {
                        'lat': float(result['documents'][0]['y']),
                        'lng': float(result['documents'][0]['x'])
                    }
            return None
        except Exception as e:
            print(f"좌표 변환 실패 ({address}): {str(e)}")
            return None
    
    def reqeusts_address(회차):
        """로또 당첨판매점 데이터 요청"""
        url = 'https://dhlottery.co.kr/store.do?method=topStore&pageGubun=L645'
        
        query_params = {
            'method': 'topStore',
            'pageGubun': 'L645'
        }
        
        form_data = {
            'method': 'topStore',
            'nowPage': '1',
            'rankNo': '',
            'gameNo': '5133',
            'hdrwComb': '1',
            'drwNo': 회차,
            'schKey': 'all',
            'schVal': ''
        }
        
        response = requests.post(url, params=query_params, data=form_data)
        return BeautifulSoup(response.text, 'html.parser')
    
    def get_address(soup, 등위=1):
        """판매점 주소 데이터 추출 및 좌표 변환"""
        # 테이블 데이터 추출
        table = soup.find_all('table', {'class': 'tbl_data tbl_data_col'})[등위-1]
        headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
        
        rows = []
        for tr in table.find('tbody').find_all('tr'):
            cols = [td.get_text(strip=True) for td in tr.find_all('td')]
            rows.append(cols)
        
        # 데이터프레임 생성
        df = pd.DataFrame(rows, columns=headers)
        
        # 인터넷 복권 판매점 제외
        df = df[~df['소재지'].str.contains('동행복권', na=False)]
        
        # 주소 정제
        df['소재지'] = df['소재지'].apply(clean_address)
        
        # 결과를 저장할 새로운 리스트
        processed_data = []
        
        # 각 주소에 대해 처리
        for _, row in df.iterrows():
            store_data = {
                '상호명': row['상호명'],
                '소재지': row['소재지']
            }
            
            # 좌표 변환
            coords = get_coordinates(row['소재지'])
            if coords:
                store_data.update(coords)  # lat, lng 추가
            else:
                store_data.update({'lat': None, 'lng': None})
            
            processed_data.append(store_data)
            time.sleep(0.5)  # API 호출 제한 고려
        
        # 새로운 DataFrame 생성
        result_df = pd.DataFrame(processed_data)
        
        # 컬럼명 변경
        return result_df.rename(columns={
            '상호명': 'name',
            '소재지': 'address'
        })
    
    def get_store_data(회차=1144):
        """당첨 판매점 데이터 조회"""
        soup = reqeusts_address(회차)
        address1 = get_address(soup, 등위=1)
        address2 = get_address(soup, 등위=2)
        
        # 1등, 2등 구분을 위한 rank 컬럼 추가
        address1['rank'] = 1
        address2['rank'] = 2
        
        # 좌표 없는 데이터 제외
        address1 = address1.dropna(subset=['lat', 'lng'])
        address2 = address2.dropna(subset=['lat', 'lng'])
        
        print(f"1등 당첨점: {len(address1)}개")
        print(f"2등 당첨점: {len(address2)}개")
        
        return address1, address2
        
    
    
    
    
    
    
    
    
    
    
        
        