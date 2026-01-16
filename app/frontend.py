
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
EMPTY_SPACE = '‎'
LOGO_WIDTH = 200
BACK_ARROW_HEIGHT = 40
BACK_ARROW_HEIGHT_STRING = f'{BACK_ARROW_HEIGHT}px'
DATA_COLUMN_SPACING = 24
EMPTY_STATE_PANEL_UPPER_SPACING = 20 + 15
EMPTY_STATE_PANEL_LOWER_SPACING = 20
VALVE_LINKS = {'VG': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-para-pulpa', 
               'WG': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-para-pulpa-de-condiciones-severas', 
               'HG': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-para-pulpa-de-alta-presion'}

#diagram_x = 5388
#diagram_y = 3404
ZONES_POINTS_MINE = {'Molienda': [(3798, 3124), (3678, 3186), (3607, 3157), (3523, 3055), (3516, 3002), (3556, 2904), (3614, 2875), (3651, 2526), (3707, 2517), (3745, 2548), (3725, 2762), (3707, 2837), (3756, 2837), (3865, 2937), (3876, 3008)], 
                     'Hidrociclones': [(4493, 1575), (4358, 1570), (4242, 1515), (4218, 1472), (4251, 1259), (4298, 1212), (4318, 1157), (4433, 1134), (4549, 1161), (4593, 1203), (4589, 1281), (4613, 1321), (4582, 1523)], 
                     'Flotación': [(4711, 1239), (4400, 699), (4418, 581), (4396, 565), (4420, 428), (4544, 423), (4587, 450), (4580, 494), (4618, 508), (4636, 430), (4751, 423), (4802, 452), (4800, 494), (4862, 523), (4858, 583), (4940, 623), (4929, 670), (5004, 703), (5000, 761), (5086, 801), (5084, 861), (5175, 912), (5142, 1070), (5122, 1088), (5080, 1259), (4960, 1257), (4855, 1077), (4820, 1241)], 
                     'Espesamiento': [(3443, 1330), (3197, 1321), (3073, 1279), (3013, 1191), (3016, 1134), (3070, 1083), (3206, 1047), (3409, 1061), (3556, 1126), (3579, 1199), (3556, 1264)], 
                     'Filtrado': [(2154, 1400), (2106, 1349), (2103, 1233), (2080, 1236), (2061, 1143), (2095, 1143), (2086, 1075), (2654, 976), (2734, 1061), (2728, 1293), (2666, 1304), (2663, 1276), (2219, 1363), (2213, 1395)], 
                     'Relaves': [(3455, 531), (3425, 618), (3231, 687), (3003, 680), (2843, 610), (2828, 568), (2714, 560), (2560, 620), (2323, 625), (2181, 580), (2137, 506), (2005, 503), (1673, 633), (1275, 673), (959, 650), (797, 577), (752, 494), (780, 391), (1028, 245), (1402, 145), (1854, 145), (2051, 204), (2124, 249), (2155, 335), (2124, 401), (2214, 411), (2331, 380), (2504, 366), (2684, 401), (2749, 463), (2860, 473), (3025, 426), (3195, 426), (3359, 459)]}
ZONES_WRAPPER_POINTS_MINE = {'Molienda': [(2995, 2322), (3821, 1964), (4285, 2404), (4326, 3388), (3003, 3400)], 
                             'Hidrociclones': [(4362, 1863), (3874, 1602), (3923, 1009), (4509, 980), (4782, 1423), (4822, 1708)], 
                             'Flotación': [(5355, 49), (5347, 1733), (4892, 1728), (4818, 1415), (4537, 968), (4192, 659), (4208, 41), (4253, 33)], 
                             'Espesamiento': [(3740, 1716), (2885, 1737), (2857, 830), (3829, 830)], 
                             'Filtrado': [(2853, 1737), (2824, 826), (1648, 769), (1713, 1822)], 
                             'Relaves': [(4073, 779), (4073, 5), (422, 5), (459, 809)]}
ZONE_POINTS_RECYCLED_PAPER = {'Pulper': [(289, 527), (287, 480), (286, 402), (293, 387), (320, 368), (344, 364), (366, 364), (391, 374), (405, 387), (408, 404), (408, 420), (413, 419), (425, 405), (446, 405), (459, 414), (460, 452), (448, 463), (437, 465), (437, 471), (477, 485), (473, 494), (421, 476), (406, 474), (408, 483), (410, 529), (384, 547), (365, 535), (363, 524), (329, 523), (329, 534), (309, 544)], 
                              'Depuración': [(517, 538), (517, 511), (496, 509), (496, 493), (514, 493), (516, 403), (509, 402), (509, 372), (519, 371), (521, 352), (718, 357), (775, 362), (940, 363), (947, 392), (942, 456), (934, 498), (944, 500), (944, 511), (740, 509), (738, 516), (717, 515), (715, 543)], 
                              'Destintado': [(960, 355), (1010, 362), (1030, 346), (1031, 330), (1055, 338), (1051, 377), (1059, 378), (1064, 332), (1032, 322), (1025, 304), (1029, 299), (1052, 296), (1067, 282), (1068, 267), (1091, 274), (1088, 315), (1094, 316), (1101, 268), (1069, 258), (1061, 245), (1060, 236), (1052, 238), (1039, 233), (1022, 233), (1015, 224), (1011, 233), (996, 240), (987, 249), (987, 273), (994, 286), (994, 293), (985, 292), (977, 283), (974, 293), (959, 299), (951, 308), (948, 336)], 
                              'Espesado': [(907, 321), (933, 272), (921, 253), (937, 225), (920, 221), (923, 196), (904, 189), (900, 200), (793, 168), (783, 183), (759, 176), (755, 182), (747, 179), (740, 190), (740, 197), (745, 199), (729, 226), (751, 233), (726, 271)], 
                              'Blanqueo': [(628, 255), (628, 245), (620, 239), (621, 211), (628, 196), (644, 191), (658, 198), (665, 197), (669, 175), (660, 173), (658, 155), (671, 143), (671, 123), (680, 111), (693, 109), (702, 118), (702, 129), (693, 145), (691, 190), (707, 184), (722, 190), (723, 210), (715, 216), (715, 225), (696, 227), (689, 240), (682, 241), (680, 258)], 
                              'Refinado': [(591, 210), (598, 210), (599, 202), (593, 201), (599, 186), (585, 178), (563, 176), (561, 183), (566, 185), (557, 192), (557, 203), (566, 215), (581, 219)]}
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
        images[name] = (Image.open(IMG_PATH / (name + '.webp')))

    images['go_back'] = img_to_base64(Image.open(IMG_PATH / 'back_arrow.webp'))
    images['left_arrow'] = Image.open(IMG_PATH / 'left_arrow.webp')
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

@st.cache_data
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

@st.cache_data
def interactive_image_html(diagram, type): #agregar parámetros de cuadriláteros y dimensiones

    if type == 'mine':
        zones_points = ZONES_POINTS_MINE
        zones_wrapper_points = ZONES_WRAPPER_POINTS_MINE
        diagram_x = 5388
        diagram_y = 3404
        stroke_width = 5
    
    if type == 'recycled_paper':
        zones_points = ZONE_POINTS_RECYCLED_PAPER
        zones_wrapper_points = ZONE_POINTS_RECYCLED_PAPER
        diagram_x = 1120
        diagram_y = 644
        stroke_width = 1

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
                        fill: rgba(0,120,255,0.3);
                        stroke: rgba(0,120,255,0.45);
                        stroke-width: {stroke_width};
                    }}
                </style>

            </svg>
        </div>
        """

    return(html)

@st.cache_data
def add_selected_zone_to_html(selected_zone, type):
    if selected_zone is None:
        return('')

    zone_id = selected_zone.replace(" ", "_")

    if type == 'mine':   #agregar todo esto a un global, y lo de interactive image html tb
        stroke_width = 5
    if type == 'recycled_paper':
        stroke_width = 1
    # rgba(255,80,0,0.95) orange
    extra_html = f"""
                <style>
                #{zone_id}.zone-group .zone-visual {{
                    fill: rgba(0,120,255,0.45);
                    stroke: rgba(0,120,255,0.6);
                    stroke-width: {stroke_width};
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

def make_interactive_image(diagram, type: str):
    html = interactive_image_html(diagram, type)
    html = html + add_selected_zone_to_html(st.session_state['selected_zone'], type)
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

def generate_empty_state_panel(text):

    st.markdown(f"<div style='height: {EMPTY_STATE_PANEL_UPPER_SPACING}px;'></div>", unsafe_allow_html = True)
    
    arrow_column = st.columns([7.6, 2.8, 7.6])[1]
    with arrow_column:
        st.image(st.session_state['images']['left_arrow'], 
                    width = 'stretch')
    
    st.markdown(f"<div style='height: {EMPTY_STATE_PANEL_LOWER_SPACING}px;'></div>", unsafe_allow_html = True)

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

def insert_paper_zone_image():
    zone = st.session_state['selected_zone']
    if zone is None:
        return()
    
    zone_to_image_name = {'Pulper': 'pulper', 'Depuración': 'depuracion', 'Destintado': 'destintado', 'Espesado': 'espesado', 'Blanqueo': 'blanqueo', 'Refinado': 'refinado'}
    image_name = zone_to_image_name[zone]
    image = st.session_state['images'][image_name]
    image = resize_image_by_expanding_height(image, 1120/644 * 4/3 * 18/20 * 0.99) 
    st.image(image)

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
    st.session_state['selected_segment'] = None
    st.session_state['selected_zone'] = None
    st.session_state['go_back'] = False



#Frontend

st.set_page_config(layout = 'wide')

if st.session_state['show_disclaimer']:
    generate_disclaimer()

generate_title_and_logo()


if st.session_state['selected_segment'] is None:
    generate_segment_buttons()


if st.session_state['selected_segment'] == 'mine':
    diagram_column, data_column = st.columns([1, 1])

    with diagram_column:
        if st.session_state['selected_zone'] is None:
            mine_diagram = st.session_state['images']['mine_diagram']
        else:
            mine_diagram = st.session_state['images']['mine_diagram_light']
        make_interactive_image(mine_diagram, 'mine')

    with data_column:
        st.markdown(f"<div style='height: {DATA_COLUMN_SPACING}px;'></div>", unsafe_allow_html = True)

        dropdowns_column, go_back_column = st.columns([18, 2])

        with dropdowns_column:
            generate_dropdowns()
            if not print_selected_series():
                generate_empty_state_panel('Elegir sector de la planta, fluido, y presión de trabajo')
        
        with go_back_column:
            generate_go_back_button()


if st.session_state['selected_segment'] == 'paper':

    if st.session_state['selected_zone'] is None:
        diagram_column, data_column = st.columns([1, 1])

        with diagram_column:
            paper_diagram = st.session_state['images']['recycled_paper_plant_diagram']
            make_interactive_image(paper_diagram, 'recycled_paper')

        with data_column:
            st.markdown(f"<div style='height: {DATA_COLUMN_SPACING}px;'></div>", unsafe_allow_html = True)
            stuff_column, go_back_column = st.columns([18, 2])
            with go_back_column:
                generate_go_back_button()
            generate_empty_state_panel('Elegir sector de la planta')
    
    else:
        diagram_column, data_column = st.columns([3, 4])

        with diagram_column:
            paper_diagram = st.session_state['images']['recycled_paper_plant_diagram_light']
            make_interactive_image(paper_diagram, 'recycled_paper')

        with data_column:
            st.markdown(f"<div style='height: {DATA_COLUMN_SPACING}px;'></div>", unsafe_allow_html = True)
            stuff_column, go_back_column = st.columns([18, 2])
            with stuff_column:
                insert_paper_zone_image()
            with go_back_column:
                generate_go_back_button()


if st.session_state['rerun']: #Reruns on some selections, to avoid input lag
    st.session_state['rerun'] = False
    st.rerun()























