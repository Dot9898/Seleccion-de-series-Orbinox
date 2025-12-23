from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import plotly.graph_objects as go
import streamlit as st

ROOT_PATH = Path(__file__).resolve().parent.parent
IMG_PATH = ROOT_PATH / 'img'



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






