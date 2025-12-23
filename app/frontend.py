
#encoding: utf-8

from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import streamlit as st
from st_clickable_images import clickable_images
from st_click_detector import click_detector

ROOT_PATH = Path(__file__).resolve().parent.parent
IMG_PATH = ROOT_PATH / 'img'
LOGO_WIDTH = 200
BACK_ARROW_HEIGHT = 40
BACK_ARROW_HEIGHT_STRING = f'{BACK_ARROW_HEIGHT}px'
DATA_COLUMN_SPACING = 23


#Utilities

def img_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return(base64.b64encode(buffer.getvalue()).decode())

def load_images():
    images = {}
    images['logo'] = img_to_base64(Image.open(IMG_PATH / 'Orbinox_logo.png'))
    images['mine_diagram'] = img_to_base64(Image.open(IMG_PATH / 'mine_diagram.png'))
    images['mineria'] = Image.open(IMG_PATH / 'mineria.jpg')
    images['pulpa_y_papel'] = Image.open(IMG_PATH / 'pulpa_y_papel.jpg')
    images['go_back'] = img_to_base64(Image.open(IMG_PATH / 'back_arrow.png'))
    return(images)

def init_session_state(defaults):
    for key in defaults:
        if key not in st.session_state:
            st.session_state[key] = defaults[key]

def valve_selection(zone, pressure, fluid):

    if pressure is None:
        pressure = 10

    if pressure == 50:
        return('HG 50')
    
    if pressure == 20:
        return('HG 20')
    
    if pressure == 16:
        if fluid == f'Relaves >50% sólidos':
            return('WG 16')
        if fluid == f'Relaves <50% sólidos':
            return('VG 16')
        if zone in ['Molienda', 'Espesamiento', 'Filtrado', 'Transporte de relaves']:
            return('WG 16')
        if zone in ['Hidrociclones', 'Flotación']:
            return('VG 16')
        
    if pressure == 10:
        if fluid == f'Relaves >50% sólidos':
            return('WG')
        if fluid == f'Relaves <50% sólidos':
            return('VG')
        if zone in ['Molienda', 'Espesamiento', 'Filtrado']:
            return('WG')
        if zone in ['Hidrociclones', 'Flotación', 'Transporte de relaves']:
            return('VG')
    
    return(None)

def format_points_into_html_containers():
    all_x = [3517, 3734, 3882, 3700, 4224, 4320, 4612, 4555, 4399, 4711, 5076, 5175, 4795, 4430, 3240, 3012, 3323, 3567, 2118, 2719, 2723, 2662, 2088, 3734, 1928, 2034, 3840]
    all_y = [3035, 2825, 3008, 3179, 1508, 1177, 1226, 1519, 693, 1226, 1260, 937, 438, 438, 1317, 1142, 1043, 1218, 1367, 1279, 1043, 971, 1093, 754, 594, 274, 453]
    points = {}
    zones = ['Molienda', 'Hidrociclones', 'Flotación', 'Espesamiento', 'Filtrado', 'Transporte de relaves']
    for zone in zones:
        points[zone] = []

    zone_index = 0
    for index in range(4+4+6+4+5+4):
        if index in [4, 8, 14, 18, 23]:
            zone_index = zone_index + 1
        zone = zones[zone_index]

        point = (all_x[index], all_y[index])
        points[zone].append(point)

    all_zones_html_string = ''
    for zone in zones:
        all_points_string = ''
        for point in points[zone]:
            x, y = point[0], point[1]
            current_point_string = f'{x}, {y} '
            all_points_string = all_points_string + current_point_string
        all_points_string = all_points_string[:-1]
        zone_id = zone.replace(' ', '_')

        full_zone_html_string = f"""<a href='#' id='{zone_id}'>
                                    <polygon
                                        points = '{all_points_string}'
                                        data-name = '{zone}'
                                        class = 'zone'>
                                        <title> {zone} </title>
                                    </polygon>
                                </a>
                                
                                """
        
        all_zones_html_string = all_zones_html_string + full_zone_html_string

    return(all_zones_html_string)


#Callbacks

def set_selected_segment(segment):
    st.session_state['selected_segment'] = segment



#Frontend

def generate_title_and_logo():
    title_column, logo_column = st.columns([3, 1])

    with title_column:
        st.markdown("""
                    <div style="display: flex; flex-direction: column; justify-content: flex-end; height: 150px;">
                        <h4 style="margin: 0; font-size: 3rem; font-weight: 450;">
                            Selección de series
                        </h4>
                    </div>
                    """,
                    unsafe_allow_html=True)

    with logo_column:
        logo = st.session_state['images']['logo']
        st.markdown(f"""
                    <div style="
                        display: flex;
                        justify-content: flex-end;
                        align-items: flex-end;
                        height: 122px;
                    ">
                        <img src="data:image/png;base64,{logo}" width="{LOGO_WIDTH}">
                    </div>
                    """,
                    unsafe_allow_html=True)

def generate_segment_buttons():
    mine_column, paper_column = st.columns([1, 1])
    
    with mine_column:
        st.button('Minería', 
                key = 'mine_button', 
                width = 'stretch', 
                on_click = set_selected_segment, 
                args = ['mine'])
        st.image(st.session_state['images']['mineria'], 
                 width = 'stretch')
    
    with paper_column:
        st.button('Pulpa y papel', 
                key = 'paper_button', 
                width = 'stretch', 
                on_click = set_selected_segment, 
                args = ['paper'])
        st.image(st.session_state['images']['pulpa_y_papel'], 
                 width = 'stretch')

@st.cache_data
def make_interactive_image(mine_image): #agregar parámetros de cuadriláteros y dimensiones

    zones_svg = format_points_into_html_containers()

    html = f"""
        <div style="
            width: 100%;
            aspect-ratio: 5388 / 3404;
            position: relative;
        ">
            <svg
                viewBox="0 0 5388 3404"
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
                    href="data:image/png;base64,{mine_image}"
                    x="0"
                    y="0"
                    width="5388"
                    height="3404"
                />

                {zones_svg}

                <style>
                    .zone {{
                        fill: transparent;
                        stroke: transparent;
                        cursor: pointer;
                    }}
                    .zone:hover {{
                        fill: rgba(0, 120, 255, 0.35);
                        stroke: rgba(0, 120, 255, 0.9);
                        stroke-width: 4;
                    }}
                </style>

            </svg>
        </div>
        """

    return(html)

def generate_dropdowns():
    fluid_column, pressure_column = st.columns([1, 1])
    with pressure_column:
        st.selectbox('Presión en la válvula (bar)', 
                    [10, 16, 20, 50], 
                    index = None, 
                    label_visibility = 'collapsed', 
                    accept_new_options = False, 
                    placeholder = 'Presión en la válvula (bar)', 
                    key = 'pressure')
    
    with fluid_column:
        st.selectbox('Fluido', 
                    ['Agua con sólidos', 'Agua de mar', 'Concentrado de cobre', f'Relaves <50% sólidos', f'Relaves >50% sólidos', 'Trazas de hidrocarburos'], 
                    index = None, 
                    label_visibility = 'collapsed', 
                    accept_new_options = False, 
                    placeholder = 'Fluido', 
                    key = 'fluid')

def generate_go_back_button():
    back_arrow_img_b64 = st.session_state['images']['go_back']
    back_arrow_img = f'data:image/png;base64,{back_arrow_img_b64}'
    clicked_image_index = clickable_images([back_arrow_img], 
                                            titles = ['Volver'], 
                                            div_style = {'display': 'flex', 'justify-content': 'flex-end'}, 
                                            img_style = {'cursor': 'pointer', 'height': BACK_ARROW_HEIGHT_STRING}, 
                                            key = 'back_click')
    if clicked_image_index == 0:
        st.session_state['go_back'] = True
        st.session_state['rerun'] = True
    else:
        st.session_state['go_back'] = False


#--------------------------------------------------------------------------------------------------------


#Key initialization

if 'images' not in st.session_state:
    st.session_state['images'] = load_images()

defaults = {}
defaults['selected_segment'] = None
defaults['go_back'] = False
defaults['rerun'] = False
defaults['selected_zone'] = None
defaults['first_run'] = True
init_session_state(defaults)

if st.session_state['go_back']:
    st.session_state['selected_segment'] = None
    st.session_state['go_back'] = False



#Frontend

st.set_page_config(layout = 'wide')

generate_title_and_logo()

if st.session_state['selected_segment'] is None:
    generate_segment_buttons()

if st.session_state['selected_segment'] == 'mine':
    diagram_column, data_column = st.columns([1, 1])

    with diagram_column:
        mine_diagram = st.session_state['images']['mine_diagram']
        html = click_detector(make_interactive_image(mine_diagram))
        zone = click_detector(html)
        zone = zone.replace('_', ' ')
        if zone == '':
            zone = None
        st.session_state['selected_zone'] = zone
    
    with data_column:
        st.markdown(f"<div style='height: {DATA_COLUMN_SPACING}px;'></div>", unsafe_allow_html=  True)

        dropdowns_column, go_back_column = st.columns([18, 2])

        with dropdowns_column:
            generate_dropdowns()
        
        with go_back_column:
            generate_go_back_button()
        
        zone = st.session_state['selected_zone']
        pressure = st.session_state['pressure']
        fluid = st.session_state['fluid']
        valve = valve_selection(zone, pressure, fluid)
        if zone is not None and valve is not None:
            st.subheader(zone)
            st.subheader(valve)

if st.session_state['selected_segment'] == 'paper':
    diagram_column, data_column = st.columns([1, 1])

    with diagram_column:
        pass

    with data_column:
        generate_go_back_button()

if st.session_state['first_run']: #Preload the cache
    mine_image = st.session_state['images']['mine_diagram']
    html = make_interactive_image(mine_image)
    st.session_state['first_run'] = False

if st.session_state['rerun']: #Reruns on some selections, to avoid input lag
    st.session_state['rerun'] = False
    st.rerun()
























