# 🎱 AI 로또 번호 추천 서비스

> "로또 번호 어디 좋은 거 없을까?" 를 해결해드립니다!

## 📌 프로젝트 소개
AI를 활용한 로또 번호 추천 및 통계 분석 서비스입니다. 사용자 데이터 기반의 맞춤형 로또 번호 추천과 함께 다양한 통계 정보를 제공합니다.

## 🛠 주요 기능
1. **AI 기반 로또 번호 예측**
   - 과거 당첨 번호 패턴 분석
   - AI 모델을 통한 다음 회차 번호 예측
   - 최대 10개 조합 추천

2. **데이터 시각화 대시보드**
   - 사용자 통계 (연령대, 성별, 지역별)
   - 로또 번호 출현 빈도 분석
   - 실시간 사용자 활동 모니터링

3. **당첨 판매점 지도**
   - 실시간 당첨 판매점 위치 정보
   - 1등, 2등 당첨 이력 조회
   - 회차별 당첨 지점 필터링

4. **사용자 관리**
   - 회원가입/로그인
   - 사용자 권한 관리
   - 개인화된 번호 추천 서비스

## 🎯 세부 기능

### 1. 대문 페이지
- 로그인 시스템 (관리자/일반 사용자)
- 자동 로그인 (세션 관리)
- 회차별 추첨 결과 표시
- 당첨 이력 조회

### 2. 관리자 대시보드
- 데이터 시각화 (pandas 활용)
- 사용자 통계 분석
  - 연령대별 분포
  - 성별 통계
  - 지역별 사용자 수
- 평균 서비스 이용 통계

### 3. 로또 번호 통계
- API 기반 실시간 데이터 수집
- 기간별 번호 출현 빈도 분석
- 연속 번호 출현 패턴 분석

### 4. AI 추첨 시스템
- 머신러닝 기반 번호 예측
- 맞춤형 번호 조합 제공

### 5. 판매점 정보
- 지도 API 연동
- 당첨 판매점 실시간 표시
- 회차별 필터링 기능

## 🔧 기술 스택
- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **AI/ML**: TensorFlow/PyTorch
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Matplotlib, Plotly

## 📁 프로젝트 구조
Lotto
└── main
├── dev # 테스트 및 디버깅용 브랜치
├── feature/dashboard # 대시보드 기능 구현
├── feature/maindisplay # 메인페이지 및 로그인 기능 구현
└── feature/lotto-draw-bot # AI 로또 번호 추첨 및 통계 기능 구현


## 👥 팀원 소개
- 이정모: 대시보드 개발
- 문관우: 인증 기능 개발, 유저 데이터화
- 오영록: AI 모델 개발, 데이터 분석

## 🔗 관련 링크
- [GitHub Repository](https://github.com/2zm00/Lotto)
- [Projext Link](https://nryotoxmeyrvjplwba3ohf.streamlit.app/)


## 📝 라이센스
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
