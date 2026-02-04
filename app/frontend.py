
#encoding: utf-8

from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import streamlit as st
from st_clickable_images import clickable_images
from st_click_detector import click_detector
from constants import IMAGES_INFO

ROOT_PATH = Path(__file__).resolve().parent.parent
IMG_PATH = ROOT_PATH / 'img'
EMPTY_SPACE = '‎'
LOGO_WIDTH = 200
BACK_ARROW_HEIGHT = 40
BACK_ARROW_HEIGHT_STRING = f'{BACK_ARROW_HEIGHT}px'
DATA_COLUMN_SPACING = 24
EMPTY_STATE_PANEL_LOWER_SPACING = 20
EMPTY_STATE_PANEL_UPPER_SPACING = EMPTY_STATE_PANEL_LOWER_SPACING + 15

ZONE_TO_IMAGE_NAME = {'Pulper': 'pulper', 'Depuración': 'depuracion', 'Destintado': 'destintado', 'Espesado': 'espesado', 'Blanqueo': 'blanqueo', 'Refinado': 'refinado'}

VALVE_LINKS = {'VG': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-para-pulpa', 
               'WG': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-para-pulpa-de-condiciones-severas', 
               'HG': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-para-pulpa-de-alta-presion'}

FLUID_OPTIONS_MINE = {'Molienda': ['Pulpa con agua', 'Pulpa con agua de mar', 'Pulpa con trazas de hidrocarburos'], 
                      'Hidrociclones': ['Pulpa con agua', 'Pulpa con agua de mar', 'Pulpa con trazas de hidrocarburos'], 
                      'Flotación': ['Pulpa con agua', 'Pulpa con agua de mar', 'Pulpa con trazas de hidrocarburos'], 
                      'Espesamiento': ['Concentrado de cobre', 'Pulpa con agua', 'Pulpa con agua de mar', 'Pulpa con trazas de hidrocarburos'], 
                      'Filtrado': ['Concentrado de cobre'], 
                      'Relaves': [f'Relaves, menos de 50% sólidos', f'Relaves, más de 50% sólidos'], 
                      '': [], 
                      None: []}



#Utilities

def img_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="WEBP")
    return(base64.b64encode(buffer.getvalue()).decode())

def resize_image_by_expanding_height(image, target_ratio):
    width = image.size[0]
    new_height = int(width/target_ratio)
    image = image.resize((width, new_height), Image.LANCZOS)
    return(image)

def load_images():
    images = {}

    images['logo'] = Image.open(IMG_PATH / 'Orbinox_logo.webp')
    images['logo_b64'] = img_to_base64(Image.open(IMG_PATH / 'Orbinox_logo.webp'))
    images['go_back'] = img_to_base64(Image.open(IMG_PATH / 'back_arrow.webp'))
    images['left_arrow'] = Image.open(IMG_PATH / 'left_arrow.webp')

    images['mineria_b64'] = img_to_base64(Image.open(IMG_PATH / 'mineria.webp'))
    images['mine_diagram'] = img_to_base64(Image.open(IMG_PATH / 'mine_diagram.webp'))
    images['mine_diagram_light'] = img_to_base64(Image.open(IMG_PATH / 'mine_diagram_light.webp'))

    images['pulpa_y_papel_b64'] = img_to_base64(Image.open(IMG_PATH / 'pulpa_y_papel.webp'))
    images['recycled_paper_plant_diagram'] = img_to_base64(Image.open(IMG_PATH / 'recycled_paper_plant_diagram.webp'))
    images['recycled_paper_plant_diagram_light'] = img_to_base64(Image.open(IMG_PATH / 'recycled_paper_plant_diagram_light.webp'))
    for name in ['pulper', 'depuracion', 'destintado', 'espesado', 'blanqueo', 'refinado']:
        images[name + '_dark'] = img_to_base64(Image.open(IMG_PATH / 'recycled_paper' / (name + '_dark.jpg')))
        images[name + '_light'] = img_to_base64(Image.open(IMG_PATH / 'recycled_paper' / (name + '_light.jpg')))

    images['go_back'] = img_to_base64(Image.open(IMG_PATH / 'back_arrow.webp'))
    images['left_arrow'] = Image.open(IMG_PATH / 'left_arrow.webp')
    return(images)

def init_session_state(defaults):
    for key in defaults:
        if key not in st.session_state:
            st.session_state[key] = defaults[key]

def select_diagram_and_image_name(selected_segment, selected_zone):

    diagram = None
    image_name = None

    if selected_segment == 'mine':
        if selected_zone is None:
            diagram = st.session_state['images']['mine_diagram']
        else:
            diagram = st.session_state['images']['mine_diagram_light']
        image_name = 'mine'

    elif selected_segment == 'paper':

        if selected_zone in [None, 'Papel-reciclado']:
            image_name = 'recycled_paper'
            diagram = st.session_state['images']['recycled_paper_plant_diagram']

        elif selected_zone in IMAGES_INFO['recycled_paper']['zones']:
            image_name = ZONE_TO_IMAGE_NAME[selected_zone]
            diagram = st.session_state['images'][f'{image_name}_dark']
        
        else:
            for paper_zone in IMAGES_INFO['recycled_paper']['zones']:
                paper_zone_name = ZONE_TO_IMAGE_NAME[paper_zone]
                if selected_zone in IMAGES_INFO[paper_zone_name]['zones']:   #En este listado está incluido papel reciclado, por lo tanto es importante el orden, y que este else vaya al final
                    image_name = paper_zone_name
                    diagram = st.session_state['images'][f'{image_name}_light']
    
    return((diagram, image_name))

def valve_selection(zone, pressure, fluid):

    if zone is None or pressure is None or fluid is None:
        return(None)

    if pressure == 50:
        return('HG 50')
    
    if pressure == 20:
        return('HG 20')
    
    if pressure == 16:
        if fluid == f'Relaves, más de 50% sólidos':
            return('WG 16')
        if fluid == f'Relaves, menos de 50% sólidos':
            return('VG 16')
        if zone in ['Molienda', 'Espesamiento', 'Filtrado', 'Relaves']:
            return('WG 16')
        if zone in ['Hidrociclones', 'Flotación']:
            return('VG 16')
        
    if pressure == 10:
        if fluid == f'Relaves, más de 50% sólidos':
            return('WG')
        if fluid == f'Relaves, menos de 50% sólidos':
            return('VG')
        if zone in ['Molienda', 'Espesamiento', 'Filtrado']:
            return('WG')
        if zone in ['Hidrociclones', 'Flotación', 'Relaves']:
            return('VG')
    
    return(None)

def available_diameters_as_string(valve):
    if valve is None:
        return(None)
    
    valve_name = valve[:2]

    if valve_name == 'VG':
        return('2" a 36" in. / 50 a 900 mm')
    if valve_name in ['WG', 'HG']:
        return('3" a 36" in. / 75 a 900 mm')
    
    return(None)

def tajadera_selection(pressure, fluid):
    if fluid is None or pressure is None:
        return(None)
    
    if fluid == 'Pulpa con agua de mar':
        return('Superdúplex')
    
    if fluid in ['Concentrado de cobre', 'Pulpa con agua', 'Pulpa con trazas de hidrocarburos', f'Relaves, menos de 50% sólidos', f'Relaves, más de 50% sólidos']:
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
    if fluid in ['Concentrado de cobre', 'Pulpa con agua', 'Pulpa con agua de mar', 'Pulpa con trazas de hidrocarburos', f'Relaves, menos de 50% sólidos', f'Relaves, más de 50% sólidos']:
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
            <a href="javascript:void(0)" id="{zone_id}">
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

def interactive_image_html(diagram, diagram_name): #agregar parámetros de cuadriláteros y dimensiones

    image_info = IMAGES_INFO[diagram_name]
    zones_points = image_info['zone_points']
    zones_wrapper_points = image_info['zone_wrapper_points']
    diagram_x = image_info['diagram_x']
    diagram_y = image_info['diagram_y']
    border_width = image_info['border_width']
    highlight_color = image_info['highlight_color']
    highlight_border_color = image_info['highlight_border_color']

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
                    href="data:image/webp;base64,{diagram}"
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
                        fill: {highlight_color};
                        stroke: {highlight_border_color};
                        stroke-width: {border_width};
                    }}
                </style>

            </svg>
        </div>
        """

    return(html)

def add_selected_zone_to_html(selected_zone, diagram_name):
    if selected_zone is None:
        return('')

    zone_id = selected_zone.replace(" ", "_")

    image_info = IMAGES_INFO[diagram_name]
    border_width = image_info['border_width']
    on_select_color = image_info['on_select_color']
    on_select_border_color = image_info['on_select_border_color']

    extra_html = f"""
                <style>
                #{zone_id}.zone-group .zone-visual {{
                    fill: {on_select_color};
                    stroke: {on_select_border_color};
                    stroke-width: {border_width};
                }}
                </style>
                """
    #rgba(31,132,181,0.35) rgba(0,120,255,0.35)
    return(extra_html)



#Callbacks

def disable_disclaimer():
    st.session_state['show_disclaimer'] = False

def set_selected_segment(segment):
    st.session_state['selected_segment'] = segment

def go_back():
    st.session_state['selected_segment'] = None
    st.session_state['selected_zone'] = None
    st.session_state['go_back'] = False
    st.session_state['rerun'] = True


#Frontend

@st.dialog(EMPTY_SPACE, width = 'medium', on_dismiss = disable_disclaimer)
def generate_disclaimer():
    logo_column = st.columns([1, 1, 1,])[1]
    with logo_column:
        st.image(st.session_state['images']['logo'], width = 'stretch')
    st.write('')
    st.write('La selección de Series Orbinox se ofrece exclusivamente como recomendación. '\
             'Orbinox no garantiza precisión, conveniencia, ni durabilidad de las selecciones aquí descritas. '\
             'Para más información, contactar con nuestro equipo de ingenieros.')

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
        logo = st.session_state['images']['logo_b64']
        st.markdown(f"""
                    <div style="
                        display: flex;
                        justify-content: flex-end;
                        align-items: flex-end;
                        height: 122px;
                    ">
                        <img src="data:image/webp;base64,{logo}" width="{LOGO_WIDTH}">
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

        mine_image_URL = [f"data:image/webp;base64,{st.session_state['images']['mineria_b64']}"]
        mine_image_index = clickable_images([mine_image_URL], 
                                            div_style = {"display": "flex", "justify-content": "center"}, 
                                            img_style = {"cursor": "pointer", "width": "100%", "border-radius": "8px"})
                        
        if mine_image_index == 0:
            set_selected_segment('mine')
            st.session_state['rerun'] = True

    with paper_column:
        st.button('Pulpa y papel', 
                key = 'paper_button', 
                width = 'stretch', 
                on_click = set_selected_segment, 
                args = ['paper'])

        paper_image_URL = [f"data:image/webp;base64,{st.session_state['images']['pulpa_y_papel_b64']}"]
        paper_image_index = clickable_images([paper_image_URL], 
                                            div_style = {"display": "flex", "justify-content": "center"}, 
                                            img_style = {"cursor": "pointer", "width": "100%", "border-radius": "8px"})
        if paper_image_index == 0:
            set_selected_segment('paper')
            st.session_state['rerun'] = True

def make_interactive_image(diagram, diagram_name: str):

    if diagram is None or image_name is None:
        return(None)

    html = interactive_image_html(diagram, diagram_name)
    html = html + add_selected_zone_to_html(st.session_state['selected_zone'], diagram_name)
    zone = click_detector(html)
    zone = zone.replace('_', ' ')
    if zone == '':
        zone = None
    if zone is not None:
        st.session_state['selected_zone'] = zone
        st.session_state['rerun'] = True

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
    back_arrow_img = f'data:image/webp;base64,{back_arrow_img_b64}'
    clicked_image_index = clickable_images([back_arrow_img], 
                                            titles = ['Volver'], 
                                            div_style = {'display': 'flex', 'justify-content': 'flex-end'}, 
                                            img_style = {'cursor': 'pointer', 'height': BACK_ARROW_HEIGHT_STRING}, 
                                            key = 'back_click')
    if clicked_image_index == 0:
        st.session_state['go_back'] = True
        st.session_state['selected_zone'] = None
        st.session_state['rerun'] = True
    else:
        st.session_state['go_back'] = False

def add_vertical_spacing(pixels):
    st.markdown(f"<div style='height: {pixels}px;'></div>", unsafe_allow_html = True)

def generate_empty_state_panel(text):

    add_vertical_spacing(EMPTY_STATE_PANEL_UPPER_SPACING)
    
    arrow_column = st.columns([7.6, 2.8, 7.6])[1]
    with arrow_column:
        st.image(st.session_state['images']['left_arrow'], 
                    width = 'stretch')
    
    add_vertical_spacing(EMPTY_STATE_PANEL_LOWER_SPACING)

    st.markdown("<div style='text-align: center; color: gray; font-size: 1.25rem; font-weight: 600;'>"
                f"{text}"
                "</div>",
                unsafe_allow_html = True,)

def print_selected_series():
    zone = st.session_state['selected_zone']
    pressure = st.session_state['pressure']
    fluid = st.session_state['fluid']
    valve = valve_selection(zone, pressure, fluid)
    tajadera = tajadera_selection(pressure, fluid)
    mangon = mangon_selection(fluid)
    diameters = available_diameters_as_string(valve)
    if None not in [zone, valve, tajadera, mangon]:
        valve_name = valve[:2]
        valve_link = VALVE_LINKS[valve_name]
        st.subheader(zone)
        st.markdown(f'Serie recomendada: [{valve}]({valve_link})')
        st.write('Material de mangón:', mangon + '*' if mangon == 'Nitrilo' else mangon)
        st.write('Material de tajadera:', tajadera)
        if mangon == 'Nitrilo':
            st.caption('*Caucho natural para porcentajes pequeños de hidrocarburos')
        st.write('')
        st.write('')
        st.caption('Diámetros disponibles: ' + diameters + '  \n' + '*DN superiores bajo consulta')
        return(True)
    else:
        return(False)

def insert_paper_zone_image(): #UNUSED
    zone = st.session_state['selected_zone']
    if zone is None:
        return()
    
    image_name = ZONE_TO_IMAGE_NAME[zone]
    image = st.session_state['images'][image_name + '_dark']
    #image = resize_image_by_expanding_height(image, 1120/644 * 4/3 * 18/20 * 0.99) 
    st.image(image)

def make_goback_paper_thumbnail(): #UNUSED
    paper_diagram_URL = [f"data:image/webp;base64,{st.session_state['images']['recycled_paper_plant_diagram_light']}"]
    paper_diagram_index = clickable_images([paper_diagram_URL], 
                                            div_style = {"display": "flex", "justify-content": "center"}, 
                                            img_style = {"cursor": "pointer", "width": "100%", "border-radius": "8px"})
    if paper_diagram_index == 0:
        st.session_state['selected_zone'] = None
        st.session_state['rerun'] = True


#--------------------------------------------------------------------------------------------------------


#Key initialization

if 'images' not in st.session_state:
    st.session_state['images'] = load_images()

defaults = {}
defaults['selected_segment'] = None
defaults['go_back'] = False
defaults['rerun'] = False
defaults['selected_zone'] = None
defaults['show_disclaimer'] = True
init_session_state(defaults)

if st.session_state['go_back']:
    go_back()

selected_segment = st.session_state['selected_segment']
selected_zone = st.session_state['selected_zone']


#Frontend

st.set_page_config(layout = 'wide')

if st.session_state['show_disclaimer']:
    generate_disclaimer()

generate_title_and_logo()


if selected_segment is None:
    generate_segment_buttons()


if selected_segment == 'mine':
    diagram_column, data_column = st.columns([1, 1])
    
    with diagram_column:
        diagram, image_name = select_diagram_and_image_name(selected_segment, selected_zone)
        make_interactive_image(diagram, image_name)
    
    with data_column:
        add_vertical_spacing(DATA_COLUMN_SPACING)
        dropdowns_column, go_back_column = st.columns([18, 2])
        
        with dropdowns_column:
            generate_dropdowns()
            if not print_selected_series():
                generate_empty_state_panel('Elegir sector de la planta, fluido, y presión de trabajo')
        
        with go_back_column:
            generate_go_back_button()


if selected_segment == 'paper':

    diagram_column, data_column = st.columns([1, 1])

    with diagram_column:
        diagram, image_name = select_diagram_and_image_name(selected_segment, selected_zone)
        make_interactive_image(diagram, image_name)

    with data_column:
        add_vertical_spacing(DATA_COLUMN_SPACING)
        dropdowns_column, go_back_column = st.columns([18, 2])
        
        with dropdowns_column:
            st.write(selected_zone)

        with go_back_column:
            generate_go_back_button()
        
        if selected_zone in [None, 'Papel-reciclado']:
            generate_empty_state_panel('Elegir sector de la planta')
        elif selected_zone in IMAGES_INFO['recycled_paper']['zones']:
            generate_empty_state_panel('Elegir zona')



if st.session_state['rerun']: #Reruns on some selections, to avoid input lag
    st.session_state['rerun'] = False
    st.rerun()























