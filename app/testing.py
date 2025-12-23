
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import streamlit as st
from st_clickable_images import clickable_images
from st_click_detector import click_detector

ROOT_PATH = Path(__file__).resolve().parent.parent
IMG_PATH = ROOT_PATH / 'img'


ZONES_POINTS_MINE = {'Molienda': [(3517, 3035), (3734, 2825), (3882, 3008), (3700, 3179)], 
                     'Hidrociclones': [(4224, 1508), (4320, 1177), (4612, 1226), (4555, 1519)], 
                     'Flotación': [(4399, 693), (4711, 1226), (5076, 1260), (5175, 937), (4795, 438), (4430, 438)], 
                     'Espesamiento': [(3240, 1317), (3012, 1142), (3323, 1043), (3567, 1218)], 
                     'Filtrado': [(2118, 1367), (2719, 1279), (2723, 1043), (2662, 971), (2088, 1093)], 
                     'Transporte de relaves': [(3734, 754), (1928, 594), (2034, 274), (3840, 453)]}

ZONES_WRAPPER_POINTS_MINE = {'Molienda': [(2995, 2322), (4285, 2404), (4326, 3388), (3003, 3400), (3821, 1964)], 
                             'Hidrociclones': [(4362, 1863), (3874, 1602), (3923, 1009), (4509, 980), (4782, 1423), (4822, 1708)], 
                             'Flotación': [(5355, 49), (5347, 1733), (4892, 1728), (4818, 1415), (4537, 968), (4192, 659), (4208, 41), (4253, 33)], 
                             'Espesamiento': [(3740, 1716), (2885, 1737), (2857, 830), (3829, 830)], 
                             'Filtrado': [(2853, 1737), (2824, 826), (1648, 769), (1713, 1822)], 
                             'Transporte de relaves': [(1481, 716), (1461, 16), (4074, 20), (4074, 785)]}

def img_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return(base64.b64encode(buffer.getvalue()).decode())

def get_zones_svg_string(zones_points, zones_wrapper_points):
    fragments = []

    for zone, points in zones_points.items():
        points_str = (' ').join(f'{x},{y}' for x, y in points)
        wrapper_points = zones_wrapper_points[zone]
        wrapper_points_str = (' ').join(f'{x},{y}' for x, y in wrapper_points)

        zone_id = zone.replace(' ', '_')
        fragments.append(f"""
        <g class="zone-group" id="{zone_id}" data-name="{zone}">
            <a href="#" id="{zone_id}">
                <polygon
                    class="zone-interaction"
                    points="{wrapper_points_str}"
                />
            </a>
            <polygon
                class="zone-visual"
                points="{points_str}"
            >
                <title>{zone}</title>
            </polygon>
        </g>
        """)

    return(('\n').join(fragments))


@st.cache_data
def make_interactive_image(diagram, type: str): #agregar parámetros de cuadriláteros y dimensiones

    if type == 'mine':
        zones_points = ZONES_POINTS_MINE
        zones_wrapper_points = ZONES_WRAPPER_POINTS_MINE
        diagram_x = 5388
        diagram_y = 3404

    zones_svg = get_zones_svg_string(zones_points, zones_wrapper_points)

    html = f"""
        <div style="
            width: 100%;
            aspect-ratio: {diagram_x} / {diagram_y};
            position: relative;
        ">
            <svg
                viewBox="0 0 {diagram_x} {diagram_y}"
                preserveAspectRatio="xMidYMid meet"
                style="
                    position: absolute;
                    inset: 0;
                    width: 100%;
                    height: 100%;
                    display: block;
                "
            >

                <image
                    href="data:image/png;base64,{diagram}"
                    x="0"
                    y="0"
                    width = {diagram_x}
                    height = {diagram_y}
                />

                {zones_svg}

                <style>
                    .zone-interaction {{
                        fill: transparent;
                        stroke: transparent;
                        pointer-events: all;
                        cursor: pointer;
                    }}

                    .zone-visual {{
                        fill: transparent;
                        stroke: transparent;
                        pointer-events: none;
                    }}

                    .zone-group:hover .zone-visual {{
                        fill: rgba(0,120,255,0.35);
                        stroke: rgba(0,120,255,0.9);
                        stroke-width: 4;
                    }}
                </style>

            </svg>
        </div>
        """

    return(html)

if 'images' not in st.session_state:
    st.session_state['images'] = {}
    st.session_state['images']['mine_diagram'] = img_to_base64(Image.open(IMG_PATH / 'mine_diagram.png'))

mine_diagram = st.session_state['images']['mine_diagram']
html = make_interactive_image(mine_diagram, 'mine')
zone = click_detector(html)
zone = zone.replace('_', ' ')
zone








