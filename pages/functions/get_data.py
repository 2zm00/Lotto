# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:35:23 2024

@author: Rogio

"""

# lotto.py
import requests
from bs4 import BeautifulSoup
import pandas as pd


# 로또 기록확인 클래스 생성
class Lotto_class:
    
    # return 받을 records 리스트 초기화
    def __init__(self,records = None):
        
        self.records = records if records is not None else []
        pass
        
    # 회차별 당첨번호 + 보너스 번호 프린트
    def check_num(self, 회차) -> print:
        
        '''
        테스트용
        round_id = 1
        '''
        
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={회차}"
        response= requests.get(url)
        '''
        a = response.json()['drwNoDate']
        '''        
        # result = []
        if response.status_code == 200:
            data = response.json()
            numbers = {
                '번호1' : data['drwtNo1'],
                '번호2' : data['drwtNo2'],
                '번호3' : data['drwtNo3'],
                '번호4' : data['drwtNo4'],
                '번호5' : data['drwtNo5'],
                '번호6' : data['drwtNo6'],
                '보너스' : data['bnusNo']
            }
            # result.append(numbers)
            return numbers
        else:
            print(f'호출 에러가 발생했습니다. 상태 코드: {response.status_code}\n, 메시지: {response.text}')
        
        
    # strat 회차 부터 ~ end 회차 까지의 기록을 dict 형대로 return
    def download_records(self, start, end) -> dict:
        '''
        테스트용
        start = 1000
        end = 1004
        '''
        
        payload = {
                    'method': 'allWinPrint',
                    'gubun': 'byWin',
                    'nowPage': '',
                    'drwNoStart': start,
                    'drwNoEnd': end
                }
        url = 'https://www.dhlottery.co.kr/gameResult.do?'
        
        
        res = requests.get(url, params = payload)
        # res.text
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        tbody = soup.find_all('tbody')[0]

        rows = tbody.find_all('tr')
        
        '''
        테스트용 코드
        for i in range(0,len(rows)):
            
            print('')
            print('')
            print('')
            print(rows[i].find_all('td')[1].find_all('span')[0].text)
            print(rows[i].find_all('td')[1].find_all('span')[1].text)
            print(rows[i].find_all('td')[1].find_all('span')[2].text)
            print(rows[i].find_all('td')[1].find_all('span')[3].text)
            print(rows[i].find_all('td')[1].find_all('span')[4].text)
            print(rows[i].find_all('td')[1].find_all('span')[5].text)
            print(rows[i].find_all('td')[2].find_all('span')[0].text) #<<<보너스
        '''
        
        
        # 웹상에 회차가 역순으로 있기 때문에 for문을 역순으로 제작하여 낮은 회차가 위로 가게 함
        numbers = {}
        for i in range(0,len(rows)):
            '''
            테스트용
            row = rows[1]
            '''
            # print(i)
            nums_td = rows[i].find_all('td')[1].find_all('span')
            bonus = rows[i].find_all('td')[2].text
            numbers[f'{end-i}회차'] = {
                                        '번호1' : int(nums_td[0].text),
                                        '번호2' : int(nums_td[1].text),
                                        '번호3' : int(nums_td[2].text),
                                        '번호4' : int(nums_td[3].text),
                                        '번호5' : int(nums_td[4].text),
                                        '번호6' : int(nums_td[5].text),
                                        '보너스' : int(bonus)
                                        }
            
        return numbers
    

    def 빈도추출(self, start,end):
        '''
        start = 1142
        end = 1143
        '''
        
        전체기록 = pd.DataFrame(self.download_records(start, end)).transpose()
        print(전체기록)
        all_numbers = pd.Series(전체기록[['번호1', '번호2', '번호3', '번호4', '번호5', '번호6', '보너스']].values.ravel())

        # 각 번호의 등장 횟수 계산
        number_counts = all_numbers.value_counts().sort_index(key=lambda x: x.astype(int))
        
        return number_counts
    
    
    def 최근회차(self):
        
        url = "https://dhlottery.co.kr/common.do?method=main"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        max_numb = soup.find(name="strong", attrs={"id": "lottoDrwNo"}).text
        return int(max_numb)
        

            
# 패키지 모듈을 테스트 하기 위한 코드, 실제 main()에서는 실행되지 않도록 if문 작성
if __name__ == '__main__':
    
    테스트_클래스 = Lotto_class()
    
    테스트_클래스.check_num(10)
        
    # 테스트 = 테스트_클래스.download_records(1,9999)
    
    테스트_빈도 = 테스트_클래스.빈도추출(1,100)
    




































