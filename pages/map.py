import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv

# !!!!!!!!!!! data/map.csv는 임시파일입니다. 수정이 필요해요.

# .env 파일 로드
load_dotenv()

def show_map():
    # 페이지 제목 설정
    st.title("카카오맵 마커 표시")
    
    try:
        # CSV 파일 읽기
        df = pd.read_csv('data/map.csv')
        
        # 지도를 표시할 HTML 템플릿
        map_html = f"""
            <div id="map" style="width:100%;height:600px;"></div>
            <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey={os.getenv('KAKAO_KEY')}"></script>
            <script>
                var container = document.getElementById('map');
                var options = {{
                    center: new kakao.maps.LatLng(37.5665, 126.9780),
                    level: 8
                }};

                var map = new kakao.maps.Map(container, options);
                
                var positions = {df[['name', 'lat', 'lng']].to_dict('records')}
                
                positions.forEach(function(position) {{
                    var marker = new kakao.maps.Marker({{
                        position: new kakao.maps.LatLng(position.lat, position.lng),
                        map: map
                    }});
                    
                    var infowindow = new kakao.maps.InfoWindow({{
                        content: '<div style="padding:5px;">' + position.name + '</div>'
                    }});
                    
                    kakao.maps.event.addListener(marker, 'click', function() {{
                        infowindow.open(map, marker);
                    }});
                }});
            </script>
        """
        
        # 디버깅을 위한 데이터 출력
        st.write("데이터 확인:", df.head())
        
        # HTML 컴포넌트 표시
        st.components.v1.html(map_html, height=600)
        
    except Exception as e:
        st.error(f"에러 발생: {str(e)}")

# Streamlit 앱 실행
if __name__ == "__main__":
    show_map()