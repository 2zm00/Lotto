# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 20:37:50 2024

@author: Rogio
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


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
    return pd.DataFrame(rows, columns=headers)
    

회차 = 1144
soup = reqeusts_address(회차)

address1 = get_address(soup,등위 = 1)


address2 = get_address(soup,등위 = 2)












