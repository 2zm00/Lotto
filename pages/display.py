import streamlit as st
import pandas as pd
from datetime import datetime

class Display:
    def __init__(self):
        self.columns = ['id', 'password', 'age', 'gender', 'region', 'city', 'draw_count', 'last_login_at', 'created_at']
        
        
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

        draw_count = st.number_input("추첨 횟수를 입력하세요:", min_value=0, value=0)
        last_login_at =datetime.now().date()
        created_at = datetime.now()
        

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
                    'city' : city,
                    'draw_count': draw_count,
                    'last_login_at': last_login_at,
                    'created_at': created_at,
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

