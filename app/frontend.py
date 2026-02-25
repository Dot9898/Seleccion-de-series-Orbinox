
#encoding: utf-8

from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import streamlit as st
from st_clickable_images import clickable_images
from st_click_detector import click_detector
import constants_images
import constants_valves


ROOT_PATH = Path(__file__).resolve().parent.parent
IMG_PATH = ROOT_PATH / 'img'

EMPTY_SPACE = '‎'
LOGO_WIDTH = 200
BACK_ARROW_HEIGHT = 40
BACK_ARROW_HEIGHT_STRING = f'{BACK_ARROW_HEIGHT}px'
SELECTBOX_SPACING = 24
LABEL_SPACING = 28
EMPTY_STATE_PANEL_LOWER_SPACING = 20
EMPTY_STATE_PANEL_UPPER_SPACING = EMPTY_STATE_PANEL_LOWER_SPACING + 15

SOLIDS_CONCENTRATION_TO_INT = {'Menos de 5%': 5, f'5% - 12%': 12, 'Más de 12%': 999, 'No considerar': 0, None: None}
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

    images['mineria_b64'] = img_to_base64(Image.open(IMG_PATH / 'segments' / 'mineria.webp'))
    images['pulpa_y_papel_b64'] = img_to_base64(Image.open(IMG_PATH / 'segments' / 'pulpa_y_papel.webp'))

    images['mine_diagram'] = img_to_base64(Image.open(IMG_PATH / 'segments' / 'mine_diagram.webp'))
    images['mine_diagram_light'] = img_to_base64(Image.open(IMG_PATH / 'segments' / 'mine_diagram_light.webp'))

    images['recycled_paper_diagram'] = img_to_base64(Image.open(IMG_PATH / 'segments' / 'recycled_paper_diagram.webp'))
    #images['recycled_paper_diagram_light'] = img_to_base64(Image.open(IMG_PATH / 'segments' / 'recycled_paper_diagram_light.webp'))
    for name in ['pulper', 'depuracion', 'destintado', 'espesado', 'blanqueo', 'refinado']:
        images[name + '_dark'] = img_to_base64(Image.open(IMG_PATH / 'recycled_paper' / (name + '_dark.webp')))
        images[name + '_light'] = img_to_base64(Image.open(IMG_PATH / 'recycled_paper' / (name + '_light.webp')))
    
    images['virgin_paper_diagram'] = img_to_base64(Image.open(IMG_PATH / 'segments' / 'virgin_paper_diagram.webp'))
    #images['virgin_paper_diagram_light'] = img_to_base64(Image.open(IMG_PATH / 'segments' / 'virgin_paper_diagram_light.webp'))
    for name in ['coccion', 'cribado', 'deslignificacion', 'recuperacion']:
        images[name + '_dark'] = img_to_base64(Image.open(IMG_PATH / 'virgin_paper' / (name + '_dark.webp')))
        images[name + '_light'] = img_to_base64(Image.open(IMG_PATH / 'virgin_paper' / (name + '_light.webp')))

    return(images)

def init_session_state(defaults):
    for key in defaults:
        if key not in st.session_state:
            st.session_state[key] = defaults[key]

def select_diagram_key(selected_segment, selected_zone):

    diagram_key = None

    if selected_segment == 'mine':
        if selected_zone is None:
            diagram_key = 'mine_diagram'
        else:
            diagram_key = 'mine_diagram_light'

    elif selected_segment == 'paper':

        if selected_zone in [None, 'Papel-virgen']:
            diagram_key = 'virgin_paper_diagram'

        elif selected_zone == 'Papel-reciclado':
            diagram_key = 'recycled_paper_diagram'
        
        elif selected_zone in (constants_images.IMAGES_INFO['recycled_paper']['zones'] + 
                               constants_images.IMAGES_INFO['virgin_paper']['zones']):
            diagram_name = constants_images.ZONE_TO_IMAGE_NAME[selected_zone]
            diagram_key = f'{diagram_name}_dark'
        
        else:
            super_zone = '-'.join(selected_zone.split('-')[:-1])
            super_zone_name = constants_images.ZONE_TO_IMAGE_NAME[super_zone]
            diagram_name = super_zone_name
            diagram_key = f'{diagram_name}_light'
    
    return(diagram_key)

def separate_valve_name_and_flags(valve_name_with_flags): #Inputs the name of a valve 'TK_actuator_duplex', outputs a the raw name 'TK' and a list of its flags ['actuator', 'duplex']
    if valve_name_with_flags is None:
        return((None, []))
    if valve_name_with_flags == 'No_valve_available':
        return(('No_valve_available', []))
    split = valve_name_with_flags.split('_')
    name = split[0]
    flags = split[1:]
    return((name, flags))

def get_flags_messages(flags):
    messages = {'duplex': '*Presión máxima seleccionada solo disponible con tajadera en dúplex', 
                'actuator': '*Diámetro solo disponible con uso de actuador', 
                'neumatic': '*Diámetro solo disponible con uso de actuador neumático', 
                'electric': '*Diámetro solo disponible con uso de actuador eléctrico'}
    to_print = []
    for flag in messages: #Keeps order and doesn't print flags not explicited here
        if flag in flags:
            to_print.append(messages[flag])
    
    return('  \n'.join(to_print))

def get_available_pressures(selected_zone):
    available_valves_string = constants_valves.ZONE_TO_AVAILABLE_VALVES_STRING[selected_zone]
    available_pressures = []
    valves = constants_valves.AVAILABLE_VALVES_STRING_TO_LIST[available_valves_string]
    for valve in valves:
        for valve_name_with_flags in constants_valves.VALVE_NAME_TO_NAMES_WITH_FLAGS[valve]:
            for max_pressure in constants_valves.VALVE_DIAMETERS_AND_PRESSURES[valve_name_with_flags].values():
                available_pressures.append(max_pressure)
    
    available_pressures = sorted(list(set(available_pressures)))
    return(available_pressures)

def get_available_diameters(selected_zone, pressure):
    if pressure is None:
        return([])
    
    available_valves_string = constants_valves.ZONE_TO_AVAILABLE_VALVES_STRING[selected_zone]
    available_diameters = []
    valves = constants_valves.AVAILABLE_VALVES_STRING_TO_LIST[available_valves_string]
    for valve in valves:
        for valve_name_with_flags in constants_valves.VALVE_NAME_TO_NAMES_WITH_FLAGS[valve]:
            for diameter, max_pressure in constants_valves.VALVE_DIAMETERS_AND_PRESSURES[valve_name_with_flags].items():
                if pressure <= max_pressure:
                    available_diameters.append(diameter)

    available_diameters = sorted(list(set(available_diameters)))
    return(available_diameters)

def is_valve_acceptable(valve_name_with_flags, pressure, diameter):
    valve_diameter_to_max_pressure = constants_valves.VALVE_DIAMETERS_AND_PRESSURES[valve_name_with_flags]
    if diameter not in valve_diameter_to_max_pressure.keys():
        return(False)
    if pressure <= valve_diameter_to_max_pressure[diameter]:
        return(True)
    return(False)

def get_acceptable_valve(valve, pressure, diameter):
    for valve_name_with_flags in constants_valves.VALVE_NAME_TO_NAMES_WITH_FLAGS[valve]:
        if is_valve_acceptable(valve_name_with_flags, pressure, diameter):
            return(valve_name_with_flags)
    return(None)

def valve_selection_paper(zone, pressure, diameter, solids_concentration = 0, off_seating_pressure = 0): #Returns valve name with flags
    
    available_valves_string = constants_valves.ZONE_TO_AVAILABLE_VALVES_STRING[zone]
    if available_valves_string is None or pressure is None or diameter is None:
        return(None)
    
    if available_valves_string in ['TL/TK/HK', 'EK/TK', 'EK/ET/TK', 'DT/TL/TK/ET', 'JT/CR/DT']:
        solids_concentration = SOLIDS_CONCENTRATION_TO_INT[st.session_state['solids_concentration']]
        if solids_concentration is None:
            return(None)
    
    if available_valves_string == 'TL/TK/HK':
        off_seating_pressure = st.session_state['off_seat_pressure']
        if off_seating_pressure == 'No considerar':
            off_seating_pressure = 0
        if off_seating_pressure is None:
            return(None)

    if available_valves_string == 'TL/TK':
        for valve in ['TL', 'TK']:
            valve_name_with_flags = get_acceptable_valve(valve, pressure, diameter)
            if valve_name_with_flags is not None:
                return(valve_name_with_flags)
    
    if available_valves_string == 'TH/TL':
        for valve in ['TL', 'TH']:
            valve_name_with_flags = get_acceptable_valve(valve, pressure, diameter)
            if valve_name_with_flags is not None:
                return(valve_name_with_flags)

    if available_valves_string == 'TL/TK/HK':
        if off_seating_pressure > 1:
            if solids_concentration > 5:
                return('No_valve_available')
            if is_valve_acceptable('HK_off', off_seating_pressure, diameter) and is_valve_acceptable('HK', pressure, diameter):
                return('HK')
            return('No_valve_available')
        for valve in ['TL', 'TK', 'HK']:
            valve_name_with_flags = get_acceptable_valve(valve, pressure, diameter)
            if valve_name_with_flags is not None:
                return(valve_name_with_flags)

    if available_valves_string == 'EX':
        if is_valve_acceptable('EX', pressure, diameter):
            return('EX')
            
    if available_valves_string == 'EX/EK':
        for valve in ['EX', 'EK']:
            valve_name_with_flags = get_acceptable_valve(valve, pressure, diameter)
            if valve_name_with_flags is not None:
                return(valve_name_with_flags)
            
    if available_valves_string == 'ET/EK':
        for valve in ['EK', 'ET']:
            valve_name_with_flags = get_acceptable_valve(valve, pressure, diameter)
            if valve_name_with_flags is not None:
                return(valve_name_with_flags)
    
    if available_valves_string == 'EK/ET/EX':
        for valve in ['EX', 'EK', 'ET']:
            valve_name_with_flags = get_acceptable_valve(valve, pressure, diameter)
            if valve_name_with_flags is not None:
                return(valve_name_with_flags)
    
    if available_valves_string == 'EK/TK':
        if solids_concentration > 5:
            valve_name_with_flags = get_acceptable_valve('TK', pressure, diameter)
            if valve_name_with_flags is not None:
                return(valve_name_with_flags)
        else:
            for valve in ['EK', 'TK']:
                valve_name_with_flags = get_acceptable_valve(valve, pressure, diameter)
                if valve_name_with_flags is not None:
                    return(valve_name_with_flags)

    if available_valves_string == 'EK/ET/TK':
        if solids_concentration > 5:
            valve_name_with_flags = get_acceptable_valve('TK', pressure, diameter)
            if valve_name_with_flags is not None:
                return(valve_name_with_flags)
        else:
            for valve in ['EK', 'ET', 'TK']:
                valve_name_with_flags = get_acceptable_valve(valve, pressure, diameter)
                if valve_name_with_flags is not None:
                    return(valve_name_with_flags)

    if available_valves_string == 'DT/TL/TK/ET':
        if solids_concentration > 12:
            valve_name_with_flags = get_acceptable_valve('DT', pressure, diameter)
            if valve_name_with_flags is not None:
                return(valve_name_with_flags)
        elif solids_concentration > 5:
            for valve in ['TL', 'TK']:
                valve_name_with_flags = get_acceptable_valve(valve, pressure, diameter)
                if valve_name_with_flags is not None:
                    return(valve_name_with_flags)
        else:
            for valve in ['ET', 'TL', 'TK']:
                valve_name_with_flags = get_acceptable_valve(valve, pressure, diameter)
                if valve_name_with_flags is not None:
                    return(valve_name_with_flags)

    if available_valves_string == 'JT/CR/DT':
        if is_valve_acceptable('CR', pressure, diameter):
            if solids_concentration > 12:
                return('CR_JT_DT')
            else:
                return('CR_JT_CR')

    if available_valves_string == 'JT/CR/CR':
        if is_valve_acceptable('CR', pressure, diameter):
            return('CR_JT_CR')

    if available_valves_string == 'JT/TK/CR':
        valve_name_with_flags = get_acceptable_valve('TK', pressure, diameter)
        if valve_name_with_flags is not None:
            return(f'{valve_name_with_flags}_JT_CR')

    return('No_valve_available')

def valve_selection_mine(zone, pressure, fluid):
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
def interactive_image_html(diagram_key): #agregar parámetros de cuadriláteros y dimensiones

    diagram = st.session_state['images'][diagram_key]
    diagram_name = constants_images.DIAGRAM_KEYS_TO_NAMES[diagram_key]

    image_info = constants_images.IMAGES_INFO[diagram_name]
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

@st.cache_data
def add_selected_zone_to_html(selected_zone, diagram_key):
    if selected_zone is None:
        return('')

    zone_id = selected_zone.replace(' ', '_')
    diagram_name = constants_images.DIAGRAM_KEYS_TO_NAMES[diagram_key]

    image_info = constants_images.IMAGES_INFO[diagram_name]
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
    st.session_state['rerun'] = True

def set_selected_zone(zone):
    st.session_state['selected_zone'] = zone
    st.session_state['rerun'] = True

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

def generate_title_zone_name_and_logo(selected_zone, selected_segment):
    title_column, zone_name_column, logo_column = st.columns([3, 2, 1])

    with title_column:
        st.markdown("""
                    <div style="display: flex; flex-direction: column; justify-content: flex-end; height: 150px;">
                        <h4 style="margin: 0; font-size: 3rem; font-weight: 450;">
                            Selección de series
                        </h4>
                    </div>
                    """,
                    unsafe_allow_html = True)

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
                    unsafe_allow_html = True)
    
    if selected_zone in [None, 'Papel-reciclado', 'Papel-virgen']:
        return()

    with zone_name_column:
        if selected_zone in (constants_images.IMAGES_INFO['mine']['zones'] + 
                             constants_images.IMAGES_INFO['recycled_paper']['zones'] + 
                             constants_images.IMAGES_INFO['virgin_paper']['zones']):
            super_zone = selected_zone.replace('-', ' ')
        else:
            super_zone = ' '.join(selected_zone.split('-')[:-1])
        if selected_segment == 'mine':
            font_size = 1.8
            font_weight = 520
        if selected_segment == 'paper':
            font_size = 1.5
            font_weight = 500
        st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: flex-end; height: 150px;">
                    <h4 style="margin: 0; font-size: {font_size}rem; font-weight: {font_weight};">
                        {super_zone}
                    </h4>
                </div>
                """,
                unsafe_allow_html = True)

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

def generate_paper_buttons():
    virgin_column, recycled_column = st.columns([1, 1])
    
    with virgin_column:
        st.button('Papel virgen', 
                key = 'virgin_button', 
                width = 'stretch', 
                on_click = set_selected_zone, 
                args = ['Papel-virgen'])

    with recycled_column:
        st.button('Papel reciclado', 
                key = 'recycled_button', 
                width = 'stretch', 
                on_click = set_selected_zone, 
                args = ['Papel-reciclado'])

def make_interactive_image(diagram_key):

    if diagram_key is None:
        return(None)

    html = interactive_image_html(diagram_key)
    html = html + add_selected_zone_to_html(st.session_state['selected_zone'], diagram_key)
    zone = click_detector(html)
    zone = zone.replace('_', ' ')
    if zone == '':
        zone = None
    if zone is not None:
        st.session_state['selected_zone'] = zone
        st.session_state['rerun'] = True

def generate_dropdowns_mine():
    fluid_column, pressure_column = st.columns([1, 1])
    
    with pressure_column:
        st.selectbox(':gray[Presión máxima (bar)]', 
                     [10, 16, 20, 50], 
                     index = None, 
                     label_visibility = 'visible', 
                     accept_new_options = False, 
                     placeholder = '', 
                     key = 'pressure')
    
    with fluid_column:
        st.selectbox(':gray[Fluido]', 
                     FLUID_OPTIONS_MINE[st.session_state['selected_zone']], 
                     index = None, 
                     label_visibility = 'visible', 
                     accept_new_options = False, 
                     placeholder = '', 
                     key = 'fluid')

def generate_dropdowns_paper():
    double_spacing = True
    pressure_column, diameter_column = st.columns([1, 1])
    selected_zone = st.session_state['selected_zone']
    available_valves_string = constants_valves.ZONE_TO_AVAILABLE_VALVES_STRING[selected_zone]

    with pressure_column:
        st.selectbox(':gray[Presión máxima (bar)]', 
                     get_available_pressures(selected_zone), 
                     index = None, 
                     label_visibility = 'visible', 
                     accept_new_options = False, 
                     placeholder = '', 
                     key = 'pressure')
        
        if available_valves_string == 'TL/TK/HK':
            st.selectbox(':gray[Contra-presión máxima (bar)]', 
                         [1, 2, 3, 3.5, 'No considerar'], 
                         index = None, 
                         label_visibility = 'visible', 
                         accept_new_options = False, 
                         placeholder = '', 
                         key = 'off_seat_pressure')
            double_spacing = False

        if available_valves_string in ['EK/TK', 'EK/ET/TK', 'DT/TL/TK/ET', 'JT/CR/DT']:
            st.selectbox(':gray[Concentración de sólidos]', 
                         ['Menos de 5%', f'5% - 12%', 'Más de 12%', 'No considerar'], 
                         index = None, 
                         label_visibility = 'visible', 
                         accept_new_options = False, 
                         placeholder = '', 
                         key = 'solids_concentration')
            double_spacing = False

    with diameter_column:
        st.selectbox(':gray[Diámetro (in.)]', 
                     get_available_diameters(selected_zone, st.session_state['pressure']), 
                     index = None, 
                     label_visibility = 'visible', 
                     accept_new_options = False, 
                     placeholder = '', 
                     key = 'diameter')
        
        if available_valves_string == 'TL/TK/HK':
            st.selectbox(':gray[Concentración de sólidos]', 
                         ['Menos de 5%', f'5% - 12%', 'Más de 12%', 'No considerar'], 
                         index = None, 
                         label_visibility = 'visible', 
                         accept_new_options = False, 
                         placeholder = '', 
                         key = 'solids_concentration')
            double_spacing = False
    
    return(double_spacing)

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

def generate_empty_state_panel(text, double_spacing = True):

    add_vertical_spacing(EMPTY_STATE_PANEL_UPPER_SPACING)
    if double_spacing:
        add_vertical_spacing(SELECTBOX_SPACING + LABEL_SPACING)
    
    arrow_column = st.columns([7.6, 2.8, 7.6])[1]
    with arrow_column:
        st.image(st.session_state['images']['left_arrow'], 
                    width = 'stretch')
    
    add_vertical_spacing(EMPTY_STATE_PANEL_LOWER_SPACING)

    st.markdown("<div style='text-align: center; color: gray; font-size: 1.25rem; font-weight: 600;'>"
                f"{text}"
                "</div>",
                unsafe_allow_html = True,)

def print_selected_series_mine():
    zone = st.session_state['selected_zone']
    pressure = st.session_state['pressure']
    fluid = st.session_state['fluid']
    valve = valve_selection_mine(zone, pressure, fluid)
    tajadera = tajadera_selection(pressure, fluid)
    mangon = mangon_selection(fluid)
    diameters = available_diameters_as_string(valve)
    
    if None in [zone, valve, tajadera, mangon]:
        return(False)
    
    else:
        valve_name = valve[:2]
        valve_link = constants_valves.VALVE_LINKS[valve_name]
        #st.subheader(zone)
        st.markdown(f'Serie recomendada: [{valve}]({valve_link})')
        st.write('Material de mangón:', mangon + '*' if mangon == 'Nitrilo' else mangon)
        st.write('Material de tajadera:', tajadera)
        if mangon == 'Nitrilo':
            st.caption('*Caucho natural para porcentajes pequeños de hidrocarburos')
        st.write('')
        st.write('')
        st.caption('Diámetros disponibles: ' + diameters + '  \n' + '*DN superiores bajo consulta')
        return(True)

def print_selected_series_paper():
    
    zone = st.session_state['selected_zone']
    pressure = st.session_state['pressure']
    if pressure == None or zone in ['Papel-reciclado', 'Papel-virgen', None] + constants_images.IMAGES_INFO['recycled_paper']['zones'] + constants_images.IMAGES_INFO['virgin_paper']['zones']:
        return(False)
    
    diameter = st.session_state['diameter']
    paper_zone = ' '.join(zone.split('-')[:-1])
    valve_name_with_flags = valve_selection_paper(zone, pressure, diameter)
    valve, valve_flags = separate_valve_name_and_flags(valve_name_with_flags)
    
    if get_available_diameters(zone, pressure) == []:
        st.caption('La presión de trabajo es demasiado alta para las series usualmente recomendadas en esta zona.' + '  \n' + 'Para válvulas a medida consultar con nuestro equipo de ingenieros.')
        return(True)
    
    if None in [valve, diameter]:
        return(False)
    
    if valve == 'No_valve_available':
        st.caption('No hemos podido seleccionar una serie adecuada para estas condiciones de trabajo.' + '  \n' + 'Para presiones altas o fluidos muy contaminados, consultar con nuestro equipo de ingenieros.')
        return(True)

    else:
        valve_link = constants_valves.VALVE_LINKS[valve]
        #st.subheader(paper_zone)
        if 'JT' not in valve_flags:
            st.markdown(f'Serie recomendada: [{valve}]({valve_link})')
        else:
            second_valve = valve_flags[valve_flags.index('JT') + 1]
            second_valve_link = constants_valves.VALVE_LINKS[second_valve]
            junk_trap_link = constants_valves.VALVE_LINKS['JT']
            st.markdown(f'Serie recomendada: [Junk trap]({junk_trap_link}) de series [{valve}]({valve_link}) con [{second_valve}]({second_valve_link})')
        st.write('')
        st.write('')
        st.write('')
        st.caption(get_flags_messages(valve_flags)) #+ '  \n' + '*Diámetros superiores bajo consulta')
        return(True)

def insert_paper_zone_image(): #UNUSED
    zone = st.session_state['selected_zone']
    if zone is None:
        return()
    
    image_name = constants_images.ZONE_TO_IMAGE_NAME[zone]
    image = st.session_state['images'][image_name + '_dark']
    #image = resize_image_by_expanding_height(image, 1120/644 * 4/3 * 18/20 * 0.99) 
    st.image(image)

def make_goback_paper_thumbnail(): #UNUSED
    paper_diagram_URL = [f"data:image/webp;base64,{st.session_state['images']['recycled_paper_diagram']}"]
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

generate_title_zone_name_and_logo(selected_zone, selected_segment)


if selected_segment is None:
    generate_segment_buttons()


if selected_segment == 'mine':
    diagram_column, data_column = st.columns([1, 1])
    
    with diagram_column:
        diagram_key = select_diagram_key(selected_segment, selected_zone)
        make_interactive_image(diagram_key)
    
    with data_column:
        dropdowns_column, go_back_column = st.columns([18, 2])
        
        with dropdowns_column:
            generate_dropdowns_mine()
            if not print_selected_series_mine():
                generate_empty_state_panel('Elegir sector de la planta, fluido, y presión de trabajo')
        
        with go_back_column:
            add_vertical_spacing(LABEL_SPACING)
            generate_go_back_button()


if selected_segment == 'paper':

    diagram_column, data_column = st.columns([1, 1])

    with diagram_column:
        add_vertical_spacing(LABEL_SPACING)
        generate_paper_buttons()
        diagram_key = select_diagram_key(selected_segment, selected_zone)
        make_interactive_image(diagram_key)

    with data_column:
        dropdowns_column, go_back_column = st.columns([18, 2])
        
        with dropdowns_column:
            double_spacing = generate_dropdowns_paper()
            if not print_selected_series_paper():
                if selected_zone in [None, 'Papel-reciclado', 'Papel-virgen']:
                    generate_empty_state_panel('Elegir sector de la planta')
                elif selected_zone in (constants_images.IMAGES_INFO['recycled_paper']['zones'] + constants_images.IMAGES_INFO['virgin_paper']['zones']):
                    generate_empty_state_panel('Elegir zona y condiciones de trabajo', double_spacing)
                else:
                    st.caption('*Diámetros y presiones superiores bajo consulta')
                    generate_empty_state_panel('Elegir zona y condiciones de trabajo', double_spacing)

        with go_back_column:
            add_vertical_spacing(LABEL_SPACING)
            generate_go_back_button()
        


if st.session_state['rerun']: #Reruns on some selections, to avoid input lag
    st.session_state['rerun'] = False
    st.rerun()




















