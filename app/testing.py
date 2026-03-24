
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import streamlit as st
from st_clickable_images import clickable_images
from st_click_detector import click_detector
import st_screen_stats

ROOT_PATH = Path(__file__).resolve().parent.parent
IMG_PATH = ROOT_PATH / 'img'



st.set_page_config(layout = 'centered')

screen_data_object = st_screen_stats.ScreenData(setTimeout = 1000) #timeout = 5


screen_data = screen_data_object.st_screen_data(on_change = None, 
                                                default = None, 
                                                key = 'screen_data_object', 
                                                interval = 0.1)

#screen_height = screen_data['screen']['height']
screen_width = screen_data['screen']['width']
if screen_width > 767.5:
    pass #desktop
else:
    pass #mobile










