import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from pages.functions.get_address import get_store_data



# .env 파일 로드
load_dotenv()

def show_map():
    # 페이지 제목 설정
    st.title("카카오맵 마커 표시")
    
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
            
        # map.py의 JavaScript 데이터 변환 부분 수정
        js_data = [
            {
                'name': row['name'],      # '상호명' 대신 'name' 사용
                'address': row['address'], # '소재지' 대신 'address' 사용
                'rank': row['rank']       # 이미 추가된 rank 컬럼 사용
            }
            for idx, row in display_data.iterrows()
        ]
        
        # 지도를 표시할 HTML 템플릿
        map_html = f"""
    <div id="map" style="width:100%;height:600px;"></div>
    <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey={os.getenv('KAKAO_KEY')}&libraries=services"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var container = document.getElementById('map');
            var options = {{
                center: new kakao.maps.LatLng(36.5, 127.5),
                level: 13
            }};

            var map = new kakao.maps.Map(container, options);
            var geocoder = new kakao.maps.services.Geocoder();
            var bounds = new kakao.maps.LatLngBounds();
            
            // 마커 이미지 설정
            var imageSize = new kakao.maps.Size(24, 35);
            var redMarkerImage = new kakao.maps.MarkerImage(
                'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
                imageSize
            );
            var blueMarkerImage = new kakao.maps.MarkerImage(
            //근데 이거 없는 주소임..
                'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_blue.png',
                imageSize
            );
            
            var addresses = {js_data};
            
            addresses.forEach(function(store) {{
                if (store.address && !store.address.includes('동행복권')) {{
                    geocoder.addressSearch(store.address, function(result, status) {{
                        // 상태 체크 및 로깅
                        console.log('주소 검색:', store.address);
                        console.log('상태:', status);
                        
                        if (status === kakao.maps.services.Status.OK) {{
                            console.log('검색 결과:', result[0]);
                            
                            var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
                            bounds.extend(coords);
                            
                            var marker = new kakao.maps.Marker({{
                                map: map,
                                position: coords,
                                title: store.name,
                                image: store.rank === 1 ? redMarkerImage : blueMarkerImage
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
                            
                            map.setBounds(bounds);
                        }} else if (status === kakao.maps.services.Status.ZERO_RESULT) {{
                            console.error('검색 결과 없음:', store.address);
                        }} else if (status === kakao.maps.services.Status.ERROR) {{
                            console.error('검색 중 에러:', store.address);
                        }}
                    }});
                }}
            }});
        }});
    </script>
"""
        
        st.write(f"{prize_selection} 판매점 정보:", display_data)
        st.components.v1.html(map_html, height=600)
        
    except Exception as e:
        st.error(f"에러 발생: {str(e)}")
        print(f"상세 에러: {str(e)}")

if __name__ == "__main__":
    show_map()
        
        
