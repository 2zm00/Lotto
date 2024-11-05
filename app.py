# app.py

import streamlit as st



import sys
import os

# 현재 파일의 경로를 기반으로 functions 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'functions')))


# 현재 작업 디렉터리를 기반으로 functions 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'functions'))


st.title("메인페이지")


