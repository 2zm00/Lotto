import streamlit as st
import pandas as pd
from datetime import datetime

class Display:
    def __init__(self):
        self.columns = ['id', 'password', 'age', 'gender', 'region', 'draw_count', 'last_login_date', 'created_time']
        
        
        if 'users' not in st.session_state:
            st.session_state.users = pd.DataFrame(columns=self.columns)
        
        # if 'login_user' not in st.session_state:
        #     st.session_state.login_user = None
        

        self.regions = {
            '서울특별시': ['서울특별시'],
            '경기도': [
                '수원시', '성남시', '고양시', '용인시', '부천시', '안산시', '안양시',
                '화성시', '평택시', '시흥시', '파주시', '김포시', '남양주시', '구리시',
                '군포시', '광명시', '이천시', '오산시', '양주시', '여주시', '동두천시',
                '포천시', '안성시', '의왕시', '의정부시', '광주시', '하남시'
            ],
            '강원도': [
                '춘천시', '강릉시', '속초시', '원주시', '동해시', '태백시', '홍천군',
                '횡성군', '영월군', '평창군', '정선군', '철원군', '화천군', '양구군',
                '고성군'
            ],
            '충청북도': [
                '청주시', '충주시', '제천시', '단양군', '보은군', '옥천군', '영동군',
                '증평군', '괴산군', '진천군', '음성군'
            ],
            '충청남도': [
                '천안시', '공주시', '아산시', '서산시', '홍성군', '예산군', '논산시',
                '계룡시', '당진시', '금산군', '부여군', '서천군', '태안군'
            ],
            '전라북도': [
                '전주시', '군산시', '익산시', '남원시', '정읍시', '김제시', '완주군',
                '진안군', '무주군', '장수군', '임실군', '순창군', '고창군', '부안군'
            ],
            '전라남도': [
                '여수시', '순천시', '광양시', '목포시', '나주시', '담양군', '곡성군',
                '구례군', '해남군', '완도군', '장흥군', '진도군', '신안군'
            ],
            '경상북도': [
                '포항시', '경주시', '안동시', '구미시', '영주시', '영천시', '상주',
                '문경시', '칠곡군', '고령군', '성주군', '청도군', '경산시', '울진군',
                '울릉군'
            ],
            '경상남도': [
                '부산시', '창원시', '김해시', '진주시', '밀양시', '거제시', '통영시',
                '사천시', '양산시', '함안군', '창녕군', '고성군', '하동군', '남해군',
                '산청군', '함양군', '거창군'
            ],
            '제주특별자치도': [
                '제주시', '서귀포시'
            ]
        }
    def load_data(self):
        try:
            st.session_state.users = pd.read_csv('user_data.csv')
        except FileNotFoundError:
            st.session_state.users = pd.DataFrame(columns=self.columns)

    def save_to_csv(self):
        st.session_state.users.to_csv('user_data.csv', index=False)
    
    def navigate_to(self,current_page):
        st.session_state.page = current_page
    

    def display_signup(self):
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
        if region=="서울특별시":
            region=="서울특별시"
        else:
            region=region+" "+city

        draw_count = st.number_input("추첨 횟수를 입력하세요:", min_value=0, value=0)
        last_login_date =datetime.now().date()
        created_time = datetime.now()
        

        if st.button("회원가입"):
            if id in st.session_state.users['id'].values:
                st.error("이미 사용 중인 아이디입니다. 다른 아이디를 선택해주세요.")
            else:
                new_user = {
                    'id': id,
                    'password': password,
                    'age': age,
                    'gender': gender,
                    'region': region,
                    'draw_count': draw_count,
                    'last_login_date': last_login_date,
                    'created_at': created_time,
                }
                new_index = len(st.session_state.users)
                st.session_state.users.loc[new_index] = new_user
                self.save_to_csv()
                
                st.success("회원가입이 완료되었습니다!")
                self.navigate_to('login')

    def display_login(self):
        st.title("로그인")

        login_id = st.text_input("아이디를 입력하세요:")
        login_password = st.text_input("비밀번호를 입력하세요:", type='password')

        if st.button("로그인"):
            #로그인 정보에 입력 된 아이디가 세션스테이트 유저스에 id랑 같고 세션스테이트 유저스의 로그인정보에 해당하는 비밀번호와 입력 된 비밀번호만 일치 두조건만족하면 로그인성공
            if login_id in st.session_state.users['id'].values and login_password == st.session_state.users.loc[st.session_state.users['id'] == login_id, 'password'].values[0]:
                st.session_state.login_user = login_id  # 로그인한 사용자 정보 저장
                self.navigate_to("home")  # 홈 페이지로 이동
                st.success("로그인 성공!")
                

            else:
                st.error("로그인 실패: 사용자 이름이나 비밀번호가 잘못되었습니다.")

        # 회원가입 페이지로 이동하는 버튼 추가
        if st.button("회원가입 페이지로 이동"):
            self.navigate_to('signup')
    def display_home(self):
        
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
        #                     streamlit run pages\sign_up.py
        

        # 로그인이 되어 있다면 매 회차 10회 추첨 결과를 화면에출력




        # 오른쪽 위에 버튼을 배치하기 위한 열 설정
        col1, col2, col3 = st.columns([4, 1, 1])  # 각 열의 비율 설정

        with col1:
            # 빈 공간을 만들어 오른쪽 열에 버튼을 배치
            st.write("")  # 빈 공간을 사용

        with col2:
            if 'login_user' in st.session_state:
                st.write(f"id: {st.session_state.login_user}")
            # 내일 로그인중이면 디스에이블하기위한것
            #누르면 로그인페이지로 이동
            elif st.button("로그인"):
                self.navigate_to('login')
                

        with col3:
            if 'login_user' in st.session_state:
                if st.button("로그 아웃"):
                    del st.session_state.login_user
                    
            #누르면회원가입페이지로이동
            elif st.button("회원 가입"):
                self.navigate_to('signup')
                
            
                
        st.title("로또 번호 추첨 페이지")



                

    
if __name__ == "__main__":
    
    
    if 'page' not in st.session_state:
        st.session_state.page = "home"  # 기본 페이지는 회원가입
    display = Display()
    display.load_data()

    if st.session_state.page == "signup":
        display.display_signup()
    elif st.session_state.page == "login":
        display.display_login()
    elif st.session_state.page == "home":
        display.display_home()

