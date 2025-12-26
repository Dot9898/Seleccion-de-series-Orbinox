
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
ZONES_POINTS_MINE = {'Molienda': [(3517, 3035), (3734, 2825), (3882, 3008), (3700, 3179)], 
                     'Hidrociclones': [(4224, 1508), (4320, 1177), (4612, 1226), (4555, 1519)], 
                     'Flotación': [(4399, 693), (4711, 1226), (5076, 1260), (5175, 937), (4795, 438), (4430, 438)], 
                     'Espesamiento': [(3240, 1317), (3012, 1142), (3323, 1043), (3567, 1218)], 
                     'Filtrado': [(2118, 1367), (2719, 1279), (2723, 1043), (2662, 971), (2088, 1093)], 
                     'Relaves': [(3734, 754), (1928, 594), (2034, 274), (3840, 453)]}
ZONES_WRAPPER_POINTS_MINE = {'Molienda': [(2995, 2322), (3821, 1964), (4285, 2404), (4326, 3388), (3003, 3400)], 
                             'Hidrociclones': [(4362, 1863), (3874, 1602), (3923, 1009), (4509, 980), (4782, 1423), (4822, 1708)], 
                             'Flotación': [(5355, 49), (5347, 1733), (4892, 1728), (4818, 1415), (4537, 968), (4192, 659), (4208, 41), (4253, 33)], 
                             'Espesamiento': [(3740, 1716), (2885, 1737), (2857, 830), (3829, 830)], 
                             'Filtrado': [(2853, 1737), (2824, 826), (1648, 769), (1713, 1822)], 
                             'Relaves': [(1481, 716), (1461, 16), (4074, 20), (4074, 785)]}
FLUID_OPTIONS_MINE = {'Molienda': ['Pulpa con agua', 'Pulpa con agua de mar', 'Pulpa con trazas de hidrocarburos'], 
                      'Hidrociclones': ['Pulpa con agua', 'Pulpa con agua de mar', 'Pulpa con trazas de hidrocarburos'], 
                      'Flotación': ['Pulpa con agua', 'Pulpa con agua de mar', 'Pulpa con trazas de hidrocarburos'], 
                      'Espesamiento': ['Concentrado de cobre', 'Pulpa con agua', 'Pulpa con agua de mar', 'Pulpa con trazas de hidrocarburos'], 
                      'Filtrado': ['Concentrado de cobre'], 
                      'Relaves': [f'Relaves <50% sólidos', f'Relaves >50% sólidos'], 
                      '': [], 
                      None: []}


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

    if zone is None or pressure is None or fluid is None:
        return(None)

    if pressure == 50:
        return('HG 50')
    
    if pressure == 20:
        return('HG 20')
    
    if pressure == 16:
        if fluid == f'Relaves >50% sólidos':
            return('WG 16')
        if fluid == f'Relaves <50% sólidos':
            return('VG 16')
        if zone in ['Molienda', 'Espesamiento', 'Filtrado', 'Relaves']:
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
        if zone in ['Hidrociclones', 'Flotación', 'Relaves']:
            return('VG')
    
    return(None)

def tajadera_selection(pressure, fluid):
    if fluid is None or pressure is None:
        return(None)
    
    if fluid == 'Pulpa con agua de mar':
        return('Súperduplex')
    
    if fluid in ['Concentrado de cobre', 'Pulpa con agua', 'Pulpa con trazas de hidrocarburos', f'Relaves <50% sólidos', f'Relaves >50% sólidos']:
        if pressure == 10:
            return('Acero inoxidable 316')
        if pressure == 16:
            return('Dúplex')
        if pressure == 20:
            return('Acero inoxidable 316 cromado')
        if pressure == 50:
            return('Dúplex cromado')
    
    return(None)

def mangon_selection(fluid):
    if fluid is None:
        return(None)
    
    if fluid == 'Pulpa con trazas de hidrocarburos':
        return('Nitrilo')
    if fluid in ['Concentrado de cobre', 'Pulpa con agua', 'Pulpa con agua de mar', 'Pulpa con trazas de hidrocarburos', f'Relaves <50% sólidos', f'Relaves >50% sólidos']:
        return('Caucho natural')
    
    return(None)

def get_zones_svg_string(zones_points, zones_wrapper_points):
    fragments = []

    for zone, points in zones_points.items():
        points_str = (' ').join(f'{x},{y}' for x, y in points)
        wrapper_points = zones_wrapper_points[zone]
        wrapper_points_str = (' ').join(f'{x},{y}' for x, y in wrapper_points)

        zone_id = zone.replace(' ', '_')
        fragments.append(f"""
        <g class="zone-group" id="{zone_id}" data-name="{zone}">
            <title>{zone}</title>
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
                     FLUID_OPTIONS_MINE[st.session_state['selected_zone']], 
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
        html = make_interactive_image(mine_diagram, 'mine')
        zone = click_detector(html)
        zone = zone.replace('_', ' ')
        if zone == '':
            zone = None
        st.session_state['selected_zone'] = zone

    with data_column:
        st.markdown(f"<div style='height: {DATA_COLUMN_SPACING}px;'></div>", unsafe_allow_html = True)

        dropdowns_column, go_back_column = st.columns([18, 2])

        with dropdowns_column:
            generate_dropdowns()
        
        with go_back_column:
            generate_go_back_button()
        
        zone = st.session_state['selected_zone']
        pressure = st.session_state['pressure']
        fluid = st.session_state['fluid']
        valve = valve_selection(zone, pressure, fluid)
        tajadera = tajadera_selection(pressure, fluid)
        mangon = mangon_selection(fluid)
        if None not in [zone, valve, tajadera, mangon]:
            st.subheader(zone)
            st.write('Serie recomendada:', valve)
            st.write('Material de mangón:', mangon)
            st.write('Material de tajadera:', tajadera)

if st.session_state['selected_segment'] == 'paper':
    diagram_column, data_column = st.columns([1, 1])

    with diagram_column:
        pass

    with data_column:
        generate_go_back_button()

if st.session_state['first_run']: #Preload the cache
    mine_image = st.session_state['images']['mine_diagram']
    html = make_interactive_image(mine_image, 'mine')
    st.session_state['first_run'] = False

if st.session_state['rerun']: #Reruns on some selections, to avoid input lag
    st.session_state['rerun'] = False
    st.rerun()
























