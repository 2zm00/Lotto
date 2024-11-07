# app.py




import sys
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import json
from pages.functions.draw_lotto_numbers import draw_lotto_numbers
from pages.functions.get_data import Lotto_class
from collections import OrderedDict


# 현재 파일의 경로를 기반으로 functions 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'functions')))


# 현재 작업 디렉터리를 기반으로 functions 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'functions'))


class Display:
    def __init__(self):
        self.columns = ['id', 'password', 'age', 'gender', 'region', 'city', 'draw_count', 'last_login_date', 'created_at', 'login_at']
        if 'users' not in st.session_state:
            st.session_state.users = pd.DataFrame(columns=self.columns)
        # if 'login_user' not in st.session_state:
        #     st.session_state.login_user = None
        self.regions = {
            "서울특별시": ["강남구", "강동구", "강북구", "관악구", "광진구", "구로구", "금천구", "노원구", "동대문구", "동작구", "마포구",
                          "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "은평구", "중구", "중랑구", "용산구"],
            "부산광역시": ["강서구", "금정구", "남구", "동구", "동래구", "부산진구", "사하구",
                          "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
            "대구광역시": ["달서구", "달성군", "동구", "남구", "북구", "서구", "수성구", "중구"],
            "대전광역시": ["대덕구", "동구", "서구", "중구", "유성구"],
            "광주광역시": ["동구", "남구", "북구", "서구", "광산구"],
            "인천광역시": ["계양구", "동구", "미추홀구", "남동구", "부평구", "서구", "옹진군", "연수구", "중구"],
            "울산광역시": ["중구", "남구", "동구", "북구", "울주군"],
            "세종특별자치시": ["세종시"],
            "경기도": ["고양시", "구리시", "김포시", "남양주시", "부천시", "수원시", "성남시", "시흥시", "안산시", "안양시", "여주시", 
                      "양주","용인시", "의정부시", "이천시", "파주시", "화성시", "광명시", "하남시", "양평군", "철원군", "동두천시"],
            "경상남도": ["거제시", "김해시", "밀양시", "사천시", "창녕군", "창원시", "통영시", "양산시", "의령군", "함안군", "하동군", "산청군", "진주시", "거창군", "합천군"],
            "경상북도": ["경주시", "구미시", "김천시", "문경시", "안동시", "영천시", "포항시", "봉화군", "울진군", "영양군", "청송군", "성주군", "칠곡군", "상주시", "예천군"],
            "강원도": ["강릉시", "고성군", "동해시", "물론", "산청군", "삼척시", "속초시", "태백시", "춘천시", "횡성군", "원주시", "영월군", "정선군", "철원군", "양양군"],
            "전라남도": ["곡성군", "구례군", "나주시", "담양군", "목포시", "순천시", "신안군", "여수시", "영광군", "완도군", "해남군", "진도군", "함평군", "장성군"],
            "전라북도": ["군산시", "김제시", "남원시", "무주군", "부안군", "순창군", "완주군", "익산시", "정읍시", "전주시", "장수군", "임실군"],
            "충청남도": ["공주시", "논산시", "보령시", "아산시", "서산시", "천안시", "계룡시", "당진시", "홍성군", "예산군", "청양군", "부여군", "서천군", "태안군"],
            "충청북도": ["괴산군", "단양군", "보은군", "옥천군", "영동군", "증평군", "진천군", "청주시", "충주시", "제천시"],
            "제주특별자치도": ["제주시", "서귀포시"]
        }
    
    def load_data(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return {}  # 파일이 없으면 빈 딕셔너리 리턴
  
    def save_to_json(self):
        
        data = st.session_state.users
        with open('data/user_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def navigate_to(self,current_page):
        st.session_state.page = current_page
    

    def get_session_state(self):

        return st.session_state.login_user
    

    def display_signup(self):
        col1, col2 = st.columns([5,1])
        with col1:
            st.write("")
        
        with col2:
            if st.button("HOME"):
                self.navigate_to('home')

            

        st.title("회원가입")
        id = st.text_input("아이디를 입력하세요:")
        password = st.text_input("비밀번호를 입력하세요:")
        age = st.number_input("나이를 입력하세요:", min_value=1, max_value=100,value=None)
        gender = st.selectbox("성별을 선택하세요:", ["남성", "여성", "기타"])
        col1, col2 = st.columns(2)

        with col1:
            region = st.selectbox("거주 지역(도)을 선택하세요:", list(self.regions.keys()))
        
        with col2:
            city = st.selectbox("거주 도시를 선택하세요:", self.regions[region])
        
        if st.button("회원가입"):
            if id in st.session_state.users:
                st.error("이미 사용 중인 아이디입니다. 다른 아이디를 선택해주세요.")
            elif len(password)<7 or len(password)>15:
                st.error("비밀번호의 길이는 7이상 15이하 입니다")
            elif age==None:
                st.error("나이를 입력하세요")
            

            else:
                
                login_at=[]
                current_datetime = datetime.now()
                last_login_date=current_datetime.strftime("%Y-%m-%d")

                created_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                
                new_user = {
                    'id': id,
                    'password': password,
                    'age': age,
                    'gender': gender,
                    'region': region,
                    'city' : city,
                    'draw_count': 0,
                    'last_login_date': last_login_date,
                    'created_at': created_at,
                    'login_at' : login_at
                }
                
                st.session_state.users[id] = new_user
                self.save_to_json()
                
                st.success("회원가입이 완료되었습니다!")
                self.navigate_to('login')
    
    def display_login(self):
        col1, col2 = st.columns([5,1])
        with col1:
            st.write("")
        
        with col2:
            if st.button("HOME"):
                self.navigate_to('home')
        st.title("로그인")

        login_id = st.text_input("아이디를 입력하세요:")
        login_password = st.text_input("비밀번호를 입력하세요:", type='password')

        if st.button("로그인"):
            # 입력된 아이디가 users 딕셔너리에 있는지 확인
            if login_id in st.session_state.users:
                # 비밀번호 일치 여부 확인
                
                if login_password == st.session_state.users[login_id]['password']:
                    # 로그인 성공
                    st.session_state.login_user = login_id  # 로그인한 사용자 정보 저장
                    current_datetime = datetime.now()
                    login_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

                    st.session_state.users[login_id]['login_at'].append(login_at)
                    
                    self.save_to_json()
                    self.navigate_to("home")  # 홈 페이지로 이동
                    st.success("로그인 성공!")
                else:
                    st.error("로그인 실패: 비밀번호가 잘못되었습니다.")
            else:
                st.error("로그인 실패: 사용자 이름이 존재하지 않습니다.")
        # 회원가입 페이지로 이동하는 버튼 추가
        if st.button("회원가입 페이지로 이동"):
            self.navigate_to('signup')
    
    st.markdown("""
        <style>
            .lotto-ball {
                display: inline-block;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                color: white;
                text-align: center;
                line-height: 50px;  /* 수직 정렬 */
                font-size: 20px;
                margin: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            }
            .lotto-container {
                display: flex;
                justify-content: center; /* 가운데 정렬 */
                margin-bottom: 20px;
            }
        </style>
        """, unsafe_allow_html=True)

    # 색상 지정 함수
    def get_color(self,number):
        if number==0:
            return "#000000" #검은색
        elif number==1:
            return "#ffd700" #황금색
        elif 1 < number <= 10:
            return "#ff7f00"  # 주황색
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

    def display_lotto_numbers(self,numbers):
        lotto_balls_html = '<div class="lotto-container">'
        if len(numbers)<7:

            for value in numbers:
                color = self.get_color(value)
                lotto_balls_html += f'<div class="lotto-ball" style="background-color: {color};">{value}</div>'
            lotto_balls_html += '</div>'
            st.markdown(lotto_balls_html, unsafe_allow_html=True)
        else:
            
            for i in range(6):
                color = self.get_color(numbers[i+6])
                lotto_balls_html += f'<div class="lotto-ball" style="background-color: {color};">{numbers[i]}</div>'
            lotto_balls_html += '</div>'
            st.markdown(lotto_balls_html, unsafe_allow_html=True)

    def display_home(self):
        lotto_dict =self.load_data('data/lotto_dict.json') 

        # '''
        # 메인화면 우측 맨위 로그인버튼과 회원가입버튼
        # - 로그인버튼클릭
        # --로그인화면으로 이동
        #    아이디와 비밀번호를 입력받고 자동로그인 체크박스
        #    체크하면 세션을사용해서 아이디비번저장하고
        #    로그인버튼누르면 다시 대쉬보드로이동
        # -회원가입버튼클릭
        # --회원가입화면으로 이동
        #    DB 구축(성별, 나이, 시도(목록( 시/도 )), 고객이 추첨 횟수 누적, 로그인 기록(YYYY-MM-DD-HH) 입력받아
        #    데이터프레임생성하고
        #    csv파일생성streamlit run pages\dashboard.py
        #    이때
        #    id password입력받고
        #    성별과 시도은 셀렉트박스로 선택하게 함
        #    고객의 추첨횟수는 기본값 0으로설정
        #    나이는 최솟값과 최댓값 설정 1~100
        #    로그인기록은 데이트타임으로 받기
        #                     streamlit run pages\display.py
        
        # 로그인이 되어 있다면 매 회차 10회 추첨 결과를 화면에출력

        # 오른쪽 위에 버튼을 배치하기 위한 열 설정
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])  # 각 열의 비율 설정

        with col1:
            if 'login_user' in st.session_state:
                st.page_link("pages/로또추첨.py", label="로또추첨", icon="🎱")
            else:
                # 빈 공간을 만들어 오른쪽 열에 버튼을 배치
                st.write("")  # 빈 공간을 사용
        with col2:
            if 'login_user' in st.session_state:
                if st.session_state.login_user=="admin":
                 st.page_link("pages/dashboard.py", label="통계", icon="📊")
                else:
                  # 빈 공간을 만들어 오른쪽 열에 버튼을 배치
                   st.write("")  # 빈 공간을 사용

        with col1:
            # 빈 공간을 만들어 오른쪽 열에 버튼을 배치
            st.write("")  # 빈 공간을 사용
            
            


        with col4:
            if 'login_user' in st.session_state:
                st.write(f"id: {st.session_state.login_user}")
                
            # 내일 로그인중이면 디스에이블하기위한것
            #누르면 로그인페이지로 이동
            elif st.button("로그인"):
                self.navigate_to('login')
            
        with col5:
            if 'login_user' in st.session_state:
                if st.button("로그 아웃"):
                    del st.session_state.login_user
                    
            #누르면회원가입페이지로이동
            elif st.button("회원 가입"):
                self.navigate_to('signup')
                           
        st.title("로또 번호 추첨 페이지")
        reversed_data = OrderedDict(reversed(list(lotto_dict.items())))
        reversed_data={key:reversed_data[key] for key in list(reversed_data.keys())[:5]}
        for round,nums in reversed_data.items():
            
            st.write(f"{round} 예측번호")
            
            for num in list(nums.values()):
                
                self.display_lotto_numbers(num)               
            
if __name__ == "__main__":
    lotto_instance = Lotto_class()
    display = Display()
    # 전체 기록을 캐시하는 함수
    @st.cache_data
    def load_all_records():
        최근회차 = lotto_instance.최근회차()
        전체기록 = pd.DataFrame(lotto_instance.download_records(1, 최근회차)).transpose()
        전체기록.index = 전체기록.index.str.replace('회차', '').astype(int)
        return 전체기록
    
    최근회차 = lotto_instance.최근회차()
    lotto_dict=display.load_data('data/lotto_dict.json')

    if f'{최근회차+1}'==list(lotto_dict.keys())[-1][0:4]:
        pass
    else:

        전체기록 = load_all_records()
        회차기록=전체기록.values.tolist()

        new_exam={}
        
        for i in range(10):
            lotto_nums=list(list(lotto_dict.values())[-1].values())[i]
            result = [1 if item in 회차기록[0][:6] else 0 for item in lotto_nums]
            lotto_nums=lotto_nums+result
            new_exam[f'ex{i+1}']=lotto_nums
        
        lotto_dict[f"{최근회차}회차"]=new_exam

        new_exam={}
        for i in range(1,11):
            drawed_numbers=draw_lotto_numbers(최근회차,전체기록)
            drawed_list = drawed_numbers.values.tolist()
            new_exam[f'ex{i}']=drawed_list[0]
    
        lotto_dict[f"{최근회차+1}회차"]=new_exam

        with open('data/lotto_dict.json', 'w', encoding='utf-8') as f:
            json.dump(lotto_dict, f, ensure_ascii=False)

    if 'page' not in st.session_state:
        st.session_state.page = "home"  # 기본 페이지는 회원가입
    
    st.session_state.users=display.load_data('data/user_data.json')

    if st.session_state.page == "signup":
        display.display_signup()
    elif st.session_state.page == "login":
        display.display_login()
    elif st.session_state.page == "home":
        display.display_home()
