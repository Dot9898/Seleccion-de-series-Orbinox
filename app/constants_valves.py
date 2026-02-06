

VALVE_LINKS = {
    'VG': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-para-pulpa',
    'WG': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-para-pulpa-de-condiciones-severas',
    'HG': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-para-pulpa-de-alta-presion',
    'TL': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-de-tajadera-pasante',
    'TK': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-de-tajadera-pasante-altas',
    'HK': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-unidireccional-para-contrapresiones',
    'EX': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-unidireccional',
    'EK': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-unidireccional-altas-prestaciones',
    'ET': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-unidireccional-mss-sp-81',
    'DT': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-de-doble-tajadera',
    'CR': 'https://www.orbinox.cl/productos-orbinox/valvulas-de-guillotina/valvula-de-guillotina-de-boca-redonda-y-cuadrada', 
    'JT': 'https://youtu.be/P-PyAkLVSpQ?si=v7hZuDyuQDmZWPAm&t=135'}

VALVE_DIAMETERS_AND_PRESSURES = {
    'TL': {2: 10, 2.5: 10, 3: 10, 4: 10, 5: 10, 6: 8, 8: 8, 10: 8, 12: 6, 14: 6, 16: 6, 18: 5, 20: 4, 24: 4}, 
    'TL_neumatic': {28: 2, 32: 2}, 
    'TK': {2: 10, 2.5: 10, 3: 10, 4: 10, 5: 10, 6: 10, 8: 10, 10: 10, 12: 6, 14: 6, 16: 6, 18: 6, 20: 6, 24: 6}, 
    'TK_duplex': {12: 8, 14: 8, 16: 8, 18: 8, 20: 8, 24: 8}, 
    'TK_actuator': {28: 6, 32: 6, 36: 6}, 
    'TK_actuator_duplex': {28: 8, 32: 8, 36: 8}, 
    'HK': {2: 10, 2.5: 10, 3: 10, 4: 10, 5: 10, 6: 10, 8: 10, 10: 10, 12: 10}, 
    'HK_off': {6: 3.5, 8: 3.5, 10: 3, 12: 2}, 
    'EX': {2: 10, 2.5: 10, 3: 10, 4: 10, 5: 10, 6: 10, 8: 10, 10: 10, 12: 6, 14: 6, 16: 6, 18: 5, 20: 4, 24: 4, 28: 2, 30: 2, 32: 2, 36: 2, 40: 2}, 
    'EK': {2: 16, 2.5: 16, 3: 16, 4: 16, 5: 16, 6: 10, 8: 10, 10: 10, 12: 6, 14: 6, 16: 6, 18: 5, 20: 4, 24: 4, 28: 2, 30: 2, 32: 2, 36: 2, 40: 2}, 
    'EK_duplex': {18: 5, 20: 4, 24: 4}, 
    'EK_electric': {48: 2}, 
    'ET': {2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 8: 10, 10: 10, 12: 10, 14: 10, 16: 10, 18: 10, 20: 10, 24: 10}, 
    'ET_actuator': {30: 7, 36: 7}, 
    'DT': {4: 10, 5: 10, 6: 10, 8: 10, 10: 10, 12: 6, 14: 6, 16: 6, 18: 5, 20: 4, 24: 4}, 
    'CR': {4: 7, 6: 7, 8: 7, 10: 7, 12: 7, 16: 7, 20: 4, 24: 4}}

VALVE_NAME_TO_NAMES_WITH_FLAGS = {'TL': ['TL', 'TL_neumatic'],   #El orden importa. Al revisar si una válvula sirve, el programa corre de la primera a la última, parando en la primera que sirve
                                  'TK': ['TK', 'TK_duplex', 'TK_actuator', 'TK_actuator_duplex'], 
                                  'HK': ['HK'], 
                                  'HK_off': ['HK_off'], 
                                  'EX': ['EX'], 
                                  'EK': ['EK', 'EK_duplex', 'EK_electric'], 
                                  'ET': ['ET', 'ET_actuator'], 
                                  'DT': ['DT'], 
                                  'CR': ['CR']}

ZONE_TO_AVAILABLE_VALVES_STRING = {

    None: None, 
    'Papel-reciclado': None, 

    'Pulper': None, 
    'Pulper-1': 'TL/TK/HK',
    'Pulper-2': 'DT/TL/TK/ET',
    'Pulper-3': 'TL/TK',
    'Pulper-4': 'JT/CR/CR',
    'Pulper-5': 'JT/CR/CR',
    'Pulper-6': 'JT/CR/DT',
    'Pulper-7': 'TL/TK/HK',
    'Pulper-8': 'TL/TK/HK',

    'Depuración': None, 
    'Depuración-1': 'JT/TK/CR',
    'Depuración-2': 'TL/TK/HK',
    'Depuración-3': 'JT/TK/CR',

    'Destintado': None, 
    'Destintado-1': 'EK/ET/EX',
    'Destintado-2': 'EK/ET/EX',
    'Destintado-3': 'EK/ET/EX',

    'Espesado': None, 
    'Espesado-1': 'EK/ET/EX',
    'Espesado-2': 'EK/ET/EX',
    'Espesado-3': 'EK/ET/EX',

    'Blanqueo': None, 
    'Blanqueo-1': 'ET/EK',
    'Blanqueo-2': 'ET/EK',
    'Blanqueo-3': 'EX/EK',
    'Blanqueo-4': 'EX/EK',
    'Blanqueo-5': 'EX/EK',

    'Refinado': None, 
    'Refinado-1': 'EK/ET/TK',
    'Refinado-2': 'EK/ET/TK',
    'Refinado-3': 'EK/ET/TK'}

AVAILABLE_VALVES_STRING_TO_LIST = {
    None: [], 
    'TL/TK': ['TL', 'TK'],
    'TL/TK/HK': ['TL', 'TK', 'HK'],
    'EX/EK': ['EX', 'EK'],
    'ET/EK': ['ET', 'EK'],
    'EK/ET/EX': ['EK', 'ET', 'EX'],
    'EK/ET/TK': ['EK', 'ET', 'TK'],
    'DT/TL/TK/ET': ['DT', 'TL', 'TK', 'ET'],
    'JT/CR/DT': ['CR'],
    'JT/CR/CR': ['CR'],
    'JT/TK/CR': ['TK']}





