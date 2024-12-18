# 🎱 AI 로또 번호 추천 서비스

> "로또 번호 어디 좋은 거 없을까?" 를 해결해드립니다!

## 📌 프로젝트 소개
머신러닝 기술을 활용한 로또 번호 추천 및 통계 분석 서비스입니다. 과거 당첨 데이터를 분석하여 패턴을 찾고, 사용자 맞춤형 번호를 추천해드립니다.

## 🛠 주요 기능
1. **AI 기반 로또 번호 예측**
- 매주 5개 번호 조합 자동 추첨
- 고정 번호 포함 추첨
- 제외 번호 설정 기능
- 학습된 AI 모델 기반 예측

2. **통계 분석 대시보드**
- 최근 100회 당첨 통계
- 최근 4회차 분석
- 연속 출현 번호 분석
- 미출현 번호 통계
- 3개월 이내 추첨 이력 조회

3. **당첨 판매점 지도**
- 실시간 당첨 판매점 위치 정보
- 1등, 2등 당첨 이력 조회
- 회차별 당첨 지점 필터링

4. **관리자 기능**
- 사용자 데이터 분석
- 이용 패턴 통계
- 지역별/연령별/성별 분석
- 서비스 사용 현황 모니터링

## 🎯 세부 기능

### 1. 대문 페이지
- 로그인 시스템 (관리자/일반 사용자)
- 회차별 추첨 결과 표시
- 당첨 이력 조회

### 2. 관리자 대시보드
- 데이터 시각화 (matplotlib 활용)
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
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Matplotlib
- **AI/ML**: TensorFlow/PyTorch
- **Map**: Folium
- **Database**: JSON

## 📁 프로젝트 브랜치 구조
```
Lotto/
└── main
├── dev # 테스트 및 디버깅용 브랜치
├── feature/dashboard # 대시보드 기능 구현
├── feature/maindisplay # 메인페이지 및 로그인 기능 구현
└── feature/lotto-draw-bot # AI 로또 번호 추첨 및 통계 기능 구현
```

## 👥 팀원 소개
- 이정모: 대시보드 개발, 지도 개발, 데이터 통계
- 문관우: 인증 기능 개발, 유저 데이터화, 데이터 관리
- 오영록: AI 모델 개발, 로또 데이터 분석, 지도 개발

## 🔗 관련 링크
- [GitHub Repository](https://github.com/2zm00/Lotto)
- [Project Link](https://lottoai.streamlit.app/)


## 📝 라이센스
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
