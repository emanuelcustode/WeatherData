import streamlit as st
from streamlit.logger import get_logger


LOGGER = get_logger(__name__)

pg = st.navigation([
        st.Page("welcome.py"),
        st.Page("hot_days.py"),
        st.Page("forecast.py"),
        st.Page("interactive_page.py"),
     ])


pg.run()