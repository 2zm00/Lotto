# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 20:37:50 2024

@author: Rogio
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import os

def reqeusts_address(회차):
    
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
    
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    return soup


def get_address(soup,등위 = 1):
    # 테이블 데이터 추출
    table = soup.find_all('table', {'class': 'tbl_data tbl_data_col'})[등위-1]
    
    # 컬럼 헤더 추출
    headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
    
    
    # 데이터 행 추출
    rows = []
    for tr in table.find('tbody').find_all('tr'):
        cols = [td.get_text(strip=True) for td in tr.find_all('td')]
        rows.append(cols)
    
    # 데이터프레임 생성
    df = pd.DataFrame(rows, columns=headers)
    
    # 인터넷 복권 판매점 제외
    df = df[~df['소재지'].str.contains('동행복권', na=False)]
    
    # 필요한 컬럼만 선택하고 이름 변경
    return df[['상호명', '소재지']].rename(columns={'상호명': 'name', '소재지': 'address'})
    

def get_store_data(회차=1144):
    soup = reqeusts_address(회차)
    address1 = get_address(soup, 등위=1)
    address2 = get_address(soup, 등위=2)
    
    # 1등, 2등 구분을 위한 rank 컬럼 추가
    address1['rank'] = 1
    address2['rank'] = 2
    
    return address1, address2
