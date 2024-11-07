#  pate3/draw_lotto_numbers.py

# pages/functions/draw_lotto_numbers.py


import pandas as pd
import numpy as np
from tensorflow import keras
from keras.layers import LeakyReLU
import joblib
import streamlit as st


# from functions.get_data import Lotto_class

# 모델과 스케일러를 불러오는 함수
@st.cache_resource
def load_model_and_scaler():
    model = keras.models.load_model('pages/model/ann_model.h5', custom_objects={'LeakyReLU': LeakyReLU})
    scaler = joblib.load('pages/model/scaler.save')
    return model, scaler

# 모델과 스케일러 불러오기
try:
    model, scaler = load_model_and_scaler()
except Exception as e:
    st.error(f"모델 로드 중 에러 발생: {e}")

def analyze_number(df, draw_number, number) -> dict:
    '''
    df = 전체기록
    draw_number = 1144
    number = 1
    '''
    
    # 분석할 회차
    current_draw_index = draw_number
    
    # 0. 출현 여부
    appearance = 1 if number in df.loc[draw_number].values else 0
    
    # 1. 연속 출현 횟수
    consecutive_count = 0
    for i in range(current_draw_index, 0, -1):  # 0보다 클 때까지
        if number in df.loc[i].values:
            consecutive_count += 1
        else:
            break

    # 2. 연속 미출현 횟수
    consecutive_non_appearance = 0
    for i in range(current_draw_index , 0, -1):  # 0보다 클 때까지
        if number not in df.loc[i].values:
            # print(df.loc[i].values)
            consecutive_non_appearance += 1
        else:
            break

    # 3. 최근 100회차 출현 횟수
    start_index = draw_number 
    end_index = draw_number - 99
    recent_100_count = df.loc[start_index : end_index].isin([number]).sum().sum()
    
    # 4. 최근 4회차 출현 횟수
    start_index = draw_number 
    end_index = draw_number - 3
    recent_4_count = df.loc[start_index : end_index].isin([number]).sum().sum()
    
    return {
        '번호' : number,
        '회차' : draw_number,
        "출현 여부" : appearance,
        "연속 출현 횟수": consecutive_count,
        "연속 미출현 횟수": consecutive_non_appearance,
        "최근 100회차 출현 횟수": recent_100_count,
        "최근 4회차 출현 횟수": recent_4_count,
    }


def draw_lotto_numbers(최근회차, 전체기록,fixed_numbers = None, excluded_numbers = None) -> pd.DataFrame:
    results = []
    for number in range(1, 46):
        record = pd.DataFrame([analyze_number(전체기록, 최근회차, number)])
        record['연속 미출현 횟수'] = record['연속 미출현 횟수'] * 2
        
        features = pd.DataFrame(record[['연속 출현 횟수', '연속 미출현 횟수', '최근 100회차 출현 횟수', '최근 4회차 출현 횟수']]).reset_index(drop=True)
        
        features_scaled = scaler.transform(features)
        
        predictions = model.predict(features_scaled, verbose=0)
    
        formatted_predictions = [f"{pred[0]:.4f}" for pred in predictions]
    
        result = pd.DataFrame([{
                                    '번호': number,
                                    '확률': float(formatted_predictions[0])
                                }])
                            
        results.append(result)    
    
    results = pd.concat(results)
    
    results['확률'] = results['확률'] / results['확률'].sum()
    
    if fixed_numbers is None:
        fixed_numbers = []
    if excluded_numbers is None:
        excluded_numbers = []
    
    # 고정 번호를 제외한 번호들 필터링
    available_numbers = results[~results['번호'].isin(fixed_numbers)]  # 고정 번호를 제외
    
    # 제외 번호도 제외
    available_numbers = available_numbers[~available_numbers['번호'].isin(excluded_numbers)]
    
    # 확률 합이 1인지 확인하고 조정
    available_numbers['확률'] = available_numbers['확률'] / available_numbers['확률'].sum()
    
    # 필요한 추가 번호 개수
    remaining_count = 6 - len(fixed_numbers)  # 고정 번호가 이미 선택되었으므로 나머지 번호 개수
    
    # 고정 번호와 제외 번호를 제외한 번호들에서 랜덤으로 선택
    if len(available_numbers) > 0:
        selected_numbers = np.random.choice(
            available_numbers['번호'],
            size=remaining_count,
            replace=False,
            p=available_numbers['확률']
        )
        # 고정 번호와 선택된 번호들을 합침
        final_numbers = np.sort(np.concatenate((fixed_numbers, selected_numbers)))
    else:
        # 고정 번호와 제외 번호를 제외한 번호가 없을 경우 오류 처리 또는 기본 처리 추가
        final_numbers = np.array(fixed_numbers)  # 예시로 고정 번호만 반환 (필요에 따라 조정)

    # 결과를 데이터프레임으로 정리
    df_numbers = pd.DataFrame([final_numbers], columns=[1, 2, 3, 4, 5, 6])
    
    return df_numbers


# analyze_number(전체기록, 최근회차, 1)

if __name__ == '__main__':
    
    test = []
    
    for i in range(0,100):
        test.append(draw_lotto_numbers(최근회차,전체기록))

    test = pd.concat(test)
        
        
    # 각 번호의 출현 횟수 계산
    total_counts = test.values.flatten()  # 데이터프레임을 1차원 배열로 변환
    number_counts = pd.Series(total_counts).value_counts().sort_index()  # 각 번호의 출현 횟수 계산
    
    # 출현 횟수를 데이터프레임으로 변환
    number_counts_df = number_counts.reset_index()
    number_counts_df.columns = ['번호', '출현 횟수']  # 컬럼 이름 설정
    
    # 결과 출력
    print(number_counts_df)