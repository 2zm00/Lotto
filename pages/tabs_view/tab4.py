# tab4
# -*- coding: utf-8 -*-

import streamlit as st

# 카카오맵 API 키
KAKAO_API_KEY = '60e0d7f939da04fcdb20bd983cb70fb2'

# Streamlit 애플리케이션 레이아웃
st.title("주소 마킹하기 - KakaoMap API")
address = st.text_input("주소를 입력하세요:", "서울특별시 중구 태평로 1가")

# 주소를 입력받고 버튼 클릭 시 마커 표시
if st.button("마커 표시"):
    # HTML과 JavaScript로 Kakao Map을 사용하여 마커 표시하기
    st.write(
        f"""
        <div id="map" style="width: 100%; height: 780px;"></div>
    
        <script type="text/javascript"
            src="//dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_API_KEY}&libraries=services"></script>
        <script>
            var mapContainer = document.getElementById('map'), 
                mapOption = {{
                    center: new daum.maps.LatLng(36.633535, 127.425882), 
                    level: 4
                }};
    
            var map = new daum.maps.Map(mapContainer, mapOption);
            var geocoder = new daum.maps.services.Geocoder();
    
            // 입력된 주소를 사용하여 마커 표시
            function myMarker(address) {{
                geocoder.addressSearch(address, function(result, status) {{
                    if (status === daum.maps.services.Status.OK) {{
                        var coords = new daum.maps.LatLng(result[0].y, result[0].x);
    
                        var content = '<div class="customoverlay">' +
                                      '<div style="font-weight:bold; color:red; font-size:2em;">' +
                                      address + '</div></div>';
    
                        var customOverlay = new daum.maps.CustomOverlay({{
                            map: map,
                            position: coords,
                            content: content,
                            yAnchor: 1
                        }});
    
                        map.setCenter(coords);
                    }} else {{
                        alert("주소 검색 결과가 없습니다.");
                    }}
                }});
            }}
    
            // 주소로 마커 표시 호출
            myMarker("{address}");
        </script>
        """,
        unsafe_allow_html=True
    )
