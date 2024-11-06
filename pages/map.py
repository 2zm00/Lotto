import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from pages.functions.get_address import get_store_data

def show_map():
    st.title("로또 당첨 판매점 지도")
    
    try:
        # 데이터 가져오기
        address1, address2 = get_store_data()
        
        # 1등, 2등 선택 라디오 버튼
        prize_selection = st.radio(
            "당첨 등수 선택",
            ["1등", "2등", "모두 보기"]
        )
        
        # 선택에 따른 데이터 필터링
        if prize_selection == "1등":
            display_data = address1
        elif prize_selection == "2등":
            display_data = address2
        else:
            display_data = pd.concat([address1, address2])

        # 전체 데이터 출력
        st.write(f"{prize_selection} 판매점 수: {len(display_data)}개")
        
        # 데이터프레임 출력
        st.dataframe(display_data[['name', 'address']])
        
        # 지도 생성 (한국 중심)
        m = folium.Map(location=[36.5, 127.5], zoom_start=7)
        
        # 마커 추가
        for _, row in display_data.iterrows():
            if pd.notna(row['lat']) and pd.notna(row['lng']):
                # 마커 색상 설정 (1등: 빨간색, 2등: 파란색)
                color = 'red' if row['rank'] == 1 else 'blue'
                
                # 팝업 내용 생성
                popup_html = f"""
                    <div style="width:200px;text-align:center;">
                        <strong>{row['name']}</strong><br>
                        <span style="color:{color};">
                            {row['rank']}등 당첨점
                        </span><br>
                        <span style="font-size:12px;">
                            {row['address']}
                        </span>
                    </div>
                """
                
                # 마커 생성
                folium.Marker(
                    location=[row['lat'], row['lng']],
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color=color),
                    tooltip=row['name']
                ).add_to(m)
        
        # Streamlit에 지도 표시
        st_folium(m, width=800, height=600)
        
    except Exception as e:
        st.error(f"에러 발생: {str(e)}")
        print(f"상세 에러: {str(e)}")

if __name__ == "__main__":
    show_map()