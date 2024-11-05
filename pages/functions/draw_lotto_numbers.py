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

def draw_lotto_numbers(최근회차, 전체기록, set_num = None) -> pd.DataFrame:
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
    
    if set_num is not None:
        remaining_count = 6 - len(set_num)  # 필요한 추가 번호의 개수
        available_numbers = results[~results['번호'].isin(set_num)]  # 고정 번호를 제외한 번호들
        # 확률 합이 1인지 확인하고 조정
        available_numbers['확률'] = available_numbers['확률'] / available_numbers['확률'].sum()

        selected_numbers = np.random.choice(
            available_numbers['번호'],
            size=remaining_count,
            replace=False,
            p=available_numbers['확률']
        )
        # 고정 번호와 추가 선택된 번호를 합치고 정렬
        final_numbers = np.sort(np.concatenate((set_num, selected_numbers)))
    else:
        # 고정 번호가 없을 때는 6개의 번호를 확률에 따라 무작위로 선택
        selected_numbers = np.random.choice(results['번호'], size=6, replace=False, p=results['확률'])
        final_numbers = np.sort(selected_numbers)
    
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