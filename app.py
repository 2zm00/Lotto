import streamlit as st
from pages.dashboard import dashboard

st.title("메인페이지")

pg = st.navigation([
	st.Page(dashboard, title="어드민대시보드", icon="📈")
])

pg.run()