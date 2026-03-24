
from pathlib import Path
import streamlit as st
from screen_mode import get_screen_mode

ROOT_PATH = Path(__file__).resolve().parent.parent


screen_mode = get_screen_mode()
if screen_mode == 'desktop':
    frontend = st.Page(ROOT_PATH / 'app' / 'frontend_desktop.py', title = 'Desktop')
if screen_mode == 'mobile':
    frontend = st.Page(ROOT_PATH / 'app' / 'frontend_mobile.py', title = 'Mobile')

current_page = st.navigation([frontend])
current_page.run()

