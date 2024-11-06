import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from pages.functions.get_address import get_store_data


def show_map():
    st.title("로또 당첨 판매점 지도")

    # API 키 확인
    # API 키 직접 가져오기
    kakao_key = st.secrets["KAKAO_KEY"]
    
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
        
        # 데이터프레임 출력 (모든 컬럼 표시)
        st.dataframe(display_data[['name', 'address', 'lat', 'lng']])
            
        # 지도를 표시할 HTML 템플릿
        map_html = f"""
        <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey={kakao_key}&libraries=services&autoload=false"></script>
        <div id="map" style="width:100%;height:600px;"></div>
        <script>
            kakao.maps.load(function() {{
                var container = document.getElementById('map');
                var options = {{
                    center: new kakao.maps.LatLng(36.5, 127.5),
                    level: 13
                }};

                var map = new kakao.maps.Map(container, options);
                var bounds = new kakao.maps.LatLngBounds();
                
                
                // 데이터를 직접 사용하여 마커 생성
                var positions = {display_data.to_dict('records')};
                
                positions.forEach(function(store) {{
                    if (store.lat && store.lng) {{  // 좌표가 있는 경우에만 마커 생성
                        var coords = new kakao.maps.LatLng(store.lat, store.lng);
                        bounds.extend(coords);
                        
                        var marker = new kakao.maps.Marker({{
                            map: map,
                            position: coords,
                            title: store.name,
                            }});
                        
                        var infowindow = new kakao.maps.InfoWindow({{
                            content: '<div style="padding:10px;width:220px;text-align:center;">' +
                                    '<strong style="font-size:14px;">' + store.name + '</strong><br>' +
                                    '<span style="color:' + (store.rank === 1 ? '#FF0000' : '#0000FF') + ';' +
                                    'font-weight:bold;font-size:12px;">' + 
                                    (store.rank === 1 ? '1등' : '2등') + ' 당첨점</span><br>' +
                                    '<span style="font-size:12px;color:#666;">' + store.address + '</span></div>'
                        }});
                        
                        kakao.maps.event.addListener(marker, 'click', function() {{
                            infowindow.open(map, marker);
                        }});
                    }}
                }});
                
                // 모든 마커가 보이도록 지도 범위 조정
                if (!bounds.isEmpty()) {{
                    map.setBounds(bounds);
                }}
            </script>
        """
        
        
        # 지도 표시
        st.components.v1.html(map_html, height=600)
        
    except Exception as e:
        st.error(f"에러 발생: {str(e)}")
        print(f"상세 에러: {str(e)}")

if __name__ == "__main__":
    show_map()