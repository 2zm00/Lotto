# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 20:37:50 2024

@author: Rogio
"""
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
<<<<<<< HEAD
import json
# from dotenv import load_dotenv
=======
import time
import json
from dotenv import load_dotenv
>>>>>>> ffad84c04d4f91866b9532efb0749617b9afe749
import os

# .env 파일에서 API 키 로드
# load_dotenv()
# API 키 설정
# def get_api_key():
#     try:
#         # Streamlit Cloud에서 실행될 때
#         return st.secrets["KAKAO_REST_KEY"]
#     except:
#         # 로컬에서 실행될 때
#         load_dotenv()
#         return os.getenv('KAKAO_REST_KEY')

KAKAO_REST_KEY = "60e0d7f939da04fcdb20bd983cb70fb2"

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

def get_coordinates(add_code):
    
    '''
    add_code = 11100039
    '''
        
    res = requests.get(f'https://dhlottery.co.kr/store.do?method=topStoreLocation&gbn=lotto&rtlrId={add_code}')
    a = res.text
    soup = BeautifulSoup(res.text, 'html.parser')
        
    # 위도와 경도를 포함하는 input 태그를 찾습니다.
    lat = soup.find('input', {'name': 'lat'})['value']
    lon = soup.find('input', {'name': 'lon'})['value']
        
    return {
            'lat': float(lat),
            'lng': float(lon)
                    }
    

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
    time.sleep(1)
    """카카오맵 API로 주소를 좌표로 변환"""
    try:
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        headers = {
            "Authorization": f"KakaoAK {st.secrets['KAKAO_REST_KEY']}"
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
<<<<<<< HEAD
    
    
    
=======
>>>>>>> ffad84c04d4f91866b9532efb0749617b9afe749
    return BeautifulSoup(response.text, 'html.parser')

def get_address(soup, 등위=1):
    """판매점 주소 데이터 추출 및 좌표 변환"""
<<<<<<< HEAD
    '''
    soup = soup
    등위 = 1
    '''
    
=======
>>>>>>> ffad84c04d4f91866b9532efb0749617b9afe749
    # 테이블 데이터 추출
    table = soup.find_all('table', {'class': 'tbl_data tbl_data_col'})[등위-1]
    headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
    
    rows = []
    for tr in table.find('tbody').find_all('tr'):
        cols = [td.get_text(strip=True) for td in tr.find_all('td')]
        
        cols[-1] = tr.find('a')['onclick'].split("'")[1]
        rows.append(cols)
    
    # 데이터프레임 생성
    df = pd.DataFrame(rows, columns=headers)
    
    # 인터넷 복권 판매점 제외
    df = df[~df['소재지'].str.contains('동행복권', na=False)]
    
    # 주소 정제
    df['소재지'] = df['소재지'].apply(clean_address)
    
<<<<<<< HEAD
    
    
    
    
=======
>>>>>>> ffad84c04d4f91866b9532efb0749617b9afe749
    # 결과를 저장할 새로운 리스트
    processed_data = []
    
    # 각 주소에 대해 처리
    for _, row in df.iterrows():
        store_data = {
<<<<<<< HEAD
            'name': row['상호명'],
            'address': row['소재지']
        }
        
        # 좌표 변환
        coords = get_coordinates(row['위치보기'])
=======
            '상호명': row['상호명'],
            '소재지': row['소재지']
        }
        
        # 좌표 변환
        coords = get_coordinates(row['소재지'])
>>>>>>> ffad84c04d4f91866b9532efb0749617b9afe749
        if coords:
            store_data.update(coords)  # lat, lng 추가
        else:
            store_data.update({'lat': None, 'lng': None})
        
        processed_data.append(store_data)
<<<<<<< HEAD
        # time.sleep(0.5)  # API 호출 제한 고려
=======
        time.sleep(0.5)  # API 호출 제한 고려
>>>>>>> ffad84c04d4f91866b9532efb0749617b9afe749
    
    # 새로운 DataFrame 생성
    result_df = pd.DataFrame(processed_data)
    
    # 컬럼명 변경
<<<<<<< HEAD
    return result_df



def get_store_data(회차=1144):
    """당첨 판매점 데이터 조회"""
    '''
    회차 = 1144
    '''
=======
    return result_df.rename(columns={
        '상호명': 'name',
        '소재지': 'address'
    })

@st.cache_data(ttl=3600) 
def get_store_data(회차=1144):
    """당첨 판매점 데이터 조회"""
>>>>>>> ffad84c04d4f91866b9532efb0749617b9afe749
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
    
<<<<<<< HEAD
    return address1, address2
=======
    return address1, address2
>>>>>>> ffad84c04d4f91866b9532efb0749617b9afe749
