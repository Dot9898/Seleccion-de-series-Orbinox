
#encoding: utf-8

from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import plotly.graph_objects as go
import streamlit as st
from streamlit.components.v1 import html
from st_click_detector import click_detector

ROOT_PATH = Path(__file__).resolve().parent.parent
IMG_PATH = ROOT_PATH / 'img'
LOGO_WIDTH = 200

def img_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return(base64.b64encode(buffer.getvalue()).decode())

def load_images():
    images = {}
    #images['logo'] = Image.open(IMG_PATH / 'Orbinox_logo.png')
    images['mine'] = img_to_base64(Image.open(IMG_PATH / 'mine_diagram.png'))
    return(images)

if 'images' not in st.session_state:
    st.session_state['images'] = load_images()

images = st.session_state['images']
mine_image = images['mine']

html = f"""
    <svg
        viewBox="0 0 5388 3404"
        preserveAspectRatio="xMidYMid meet"
        style="width: 100%; height: 100%; border: 1px solid black;">

        <image
            href="data:image/png;base64,{mine_image}"
            x="0"
            y="0"
            width="5388"
            height="3404"
        />

        <a href="#" id="Pila de mineral">
            <polygon
                points = '1500, 2500 2050, 2800 2650, 2350 2030, 1780'
                data-name = 'Pila de mineral'
                class = 'zone'>
                <title> Pila de mineral </title>
            </polygon>
        </a>

        <style>
            .zone {{
            fill: transparent;
            stroke: transparent;
            cursor: pointer
            }}

            .zone:hover {{
            fill: rgba(0, 120, 255, 0.35);
            stroke: rgba(0, 120, 255, 0.9);
            stroke-width: 4;
            }}
        </style>

    </svg>
    """


clicked_id = click_detector(html)

if clicked_id:
    st.write("Clicked region:", clicked_id)

print(clicked_id, type(clicked_id))


























