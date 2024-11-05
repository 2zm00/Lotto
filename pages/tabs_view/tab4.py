# tab4
# -*- coding: utf-8 -*-

import streamlit as st
import folium
from streamlit_folium import folium_static
# asdas
# 지도 생성
map_center = [37.5665, 126.978]  # 예: 서울
my_map = folium.Map(location=map_center, zoom_start=12)

# 마커 추가
folium.Marker(location=map_center, popup='서울').add_to(my_map)

# Streamlit에 지도 표시
folium_static(my_map)


