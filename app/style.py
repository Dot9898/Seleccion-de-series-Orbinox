
import streamlit as st

@st.cache_data
def style_css():
    with open('style.css') as css:
        style = css.read()
        return(style)

def set_style():
    st.markdown(f'<style>{style_css()}</style>', unsafe_allow_html = True)
