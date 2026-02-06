
from functools import lru_cache


@lru_cache
def rgba(color, opacity):
    rgba_string = f'rgba({color[0]},{color[1]},{color[2]},{opacity})'
    return(rgba_string)

def make_image_info_dict(zone_points, zone_wrapper_points, diagram_x, diagram_y, border_width, color):
    image_info = {'zones': list(zone_points.keys()), 
                  'zone_points': zone_points, 
                  'zone_wrapper_points': zone_wrapper_points, 
                  'diagram_x': diagram_x, 
                  'diagram_y': diagram_y, 
                  'border_width': border_width, 
                  'highlight_color': rgba(color, 0.3), 
                  'highlight_border_color': rgba(color, 0.45), 
                  'on_select_color': rgba(color, 0.45), 
                  'on_select_border_color': rgba(color, 0.6)}
    return(image_info)



LIGHT_BLUE = (0, 120, 255)
ALICE_BLUE = (174, 198, 247)
ORANGE = (255, 80, 0)


ZONE_POINTS_MINE = {'Molienda': [(3798, 3124), (3678, 3186), (3607, 3157), (3523, 3055), (3516, 3002), (3556, 2904), (3614, 2875), (3651, 2526), (3707, 2517), (3745, 2548), (3725, 2762), (3707, 2837), (3756, 2837), (3865, 2937), (3876, 3008)], 
                    'Hidrociclones': [(4493, 1575), (4358, 1570), (4242, 1515), (4218, 1472), (4251, 1259), (4298, 1212), (4318, 1157), (4433, 1134), (4549, 1161), (4593, 1203), (4589, 1281), (4613, 1321), (4582, 1523)], 
                    'Flotación': [(4711, 1239), (4400, 699), (4418, 581), (4396, 565), (4420, 428), (4544, 423), (4587, 450), (4580, 494), (4618, 508), (4636, 430), (4751, 423), (4802, 452), (4800, 494), (4862, 523), (4858, 583), (4940, 623), (4929, 670), (5004, 703), (5000, 761), (5086, 801), (5084, 861), (5175, 912), (5142, 1070), (5122, 1088), (5080, 1259), (4960, 1257), (4855, 1077), (4820, 1241)], 
                    'Espesamiento': [(3443, 1330), (3197, 1321), (3073, 1279), (3013, 1191), (3016, 1134), (3070, 1083), (3206, 1047), (3409, 1061), (3556, 1126), (3579, 1199), (3556, 1264)], 
                    'Filtrado': [(2154, 1400), (2106, 1349), (2103, 1233), (2080, 1236), (2061, 1143), (2095, 1143), (2086, 1075), (2654, 976), (2734, 1061), (2728, 1293), (2666, 1304), (2663, 1276), (2219, 1363), (2213, 1395)], 
                    'Relaves': [(3455, 531), (3425, 618), (3231, 687), (3003, 680), (2843, 610), (2828, 568), (2714, 560), (2560, 620), (2323, 625), (2181, 580), (2137, 506), (2005, 503), (1673, 633), (1275, 673), (959, 650), (797, 577), (752, 494), (780, 391), (1028, 245), (1402, 145), (1854, 145), (2051, 204), (2124, 249), (2155, 335), (2124, 401), (2214, 411), (2331, 380), (2504, 366), (2684, 401), (2749, 463), (2860, 473), (3025, 426), (3195, 426), (3359, 459)]}
ZONE_WRAPPER_POINTS_MINE = {'Molienda': [(2995, 2322), (3821, 1964), (4285, 2404), (4326, 3388), (3003, 3400)], 
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
ZONE_WRAPPER_POINTS_RECYCLED_PAPER = {'Pulper': [(171, 625), (192, 335), (492, 336), (495, 625)], 
                                      'Depuración': [(499, 331), (500, 619), (1005, 616), (1005, 422), (964, 389), (953, 368), (932, 349)], 
                                      'Destintado': [(954, 367), (936, 349), (930, 331), (986, 195), (1038, 188), (1118, 243), (1118, 425), (1034, 417)], 
                                      'Espesado': [(983, 163), (918, 351), (742, 340), (689, 309), (767, 103)], 
                                      'Blanqueo': [(682, 311), (774, 71), (661, 58), (570, 308)], 
                                      'Refinado': [(640, 93), (568, 289), (482, 280), (489, 133), (558, 84)]}


ZONE_POINTS_PULPER = {'Papel-reciclado': [(5, 4), (5, 132), (228, 132), (228, 4)], 
                      'Pulper-1': [(25, 260), (120, 260), (120, 350), (25, 350)], 
                      'Pulper-2': [(325, 260), (405, 260), (405, 350), (325, 350)], 
                      'Pulper-3': [(535, 260), (605, 260), (605, 350), (535, 350)], 
                      'Pulper-4': [(195, 340), (320, 340), (320, 450), (195, 450)], 
                      'Pulper-5': [(395, 340), (515, 340), (515, 450), (395, 450)], 
                      'Pulper-6': [(600, 340), (745, 340), (745, 450), (600, 450)], 
                      'Pulper-7': [(905, 340), (1020, 340), (1020, 445), (905, 445)], 
                      'Pulper-8': [(980, 260), (1085, 260), (1085, 345), (980, 345)]}
ZONE_WRAPPER_POINTS_PULPER = ZONE_POINTS_PULPER

ZONE_POINTS_DEPURACION = {'Papel-reciclado': [(15, 27), (15, 124), (182, 122), (181, 27)], 
                          'Depuración-1': [(265, 230), (545, 230), (545, 340), (265, 340)], 
                          'Depuración-2': [(775, 290), (860, 290), (860, 360), (775, 360)], 
                          'Depuración-3': [(870, 235), (1150, 235), (1150, 340), (870, 340)]}
ZONE_WRAPPER_POINTS_DEPURACION = ZONE_POINTS_DEPURACION

ZONE_POINTS_DESTINTADO = {'Papel-reciclado': [(25, 15), (25, 144), (250, 144), (250, 15)], 
                          'Destintado-1': [(250, 385), (360, 385), (360, 470), (250, 470)], 
                          'Destintado-2': [(645, 190), (760, 190), (760, 270), (645, 270)], 
                          'Destintado-3': [(995, 75), (1100, 75), (1100, 160), (995, 160)]}
ZONE_WRAPPER_POINTS_DESTINTADO = ZONE_POINTS_DESTINTADO

ZONE_POINTS_ESPESADO = {'Papel-reciclado': [(12, 511), (233, 511), (234, 640), (11, 640)], 
                        'Espesado-1': [(320, 230), (425, 230), (425, 310), (320, 310)], 
                        'Espesado-2': [(455, 470), (565, 470), (565, 560), (455, 560)], 
                        'Espesado-3': [(835, 175), (975, 175), (975, 250), (835, 250)]}
ZONE_WRAPPER_POINTS_ESPESADO = ZONE_POINTS_ESPESADO

ZONE_POINTS_BLANQUEO = {'Papel-reciclado': [(21, 20), (187, 20), (187, 115), (21, 115)], 
                        'Blanqueo-1': [(20, 325), (20, 430), (150, 430), (150, 325)], 
                        'Blanqueo-2': [(170, 290), (170, 225), (300, 225), (300, 290)], 
                        'Blanqueo-3': [(285, 525), (285, 440), (405, 440), (405, 525)], 
                        'Blanqueo-4': [(445, 525), (445, 440), (585, 440), (585, 525)], 
                        'Blanqueo-5': [(665, 525), (665, 440), (765, 440), (765, 525)]}
ZONE_WRAPPER_POINTS_BLANQUEO = ZONE_POINTS_BLANQUEO

ZONE_POINTS_REFINADO = {'Papel-reciclado': [(4, 135), (4, 8), (227, 8), (227, 135)], 
                        'Refinado-1': [(250, 592), (250, 500), (385, 500), (385, 595)], 
                        'Refinado-2': [(510, 375), (510, 285), (710, 285), (710, 375)], 
                        'Refinado-3': [(820, 240), (820, 145), (930, 145), (930, 240)]}
ZONE_WRAPPER_POINTS_REFINADO = ZONE_POINTS_REFINADO


MINE_INFO = make_image_info_dict(ZONE_POINTS_MINE, ZONE_WRAPPER_POINTS_MINE, 5388, 3404, 5, LIGHT_BLUE)
RECYCLED_PAPER_INFO = make_image_info_dict(ZONE_POINTS_RECYCLED_PAPER, ZONE_WRAPPER_POINTS_RECYCLED_PAPER, 1120, 644, 1, LIGHT_BLUE)
PULPER_INFO = make_image_info_dict(ZONE_POINTS_PULPER, ZONE_WRAPPER_POINTS_PULPER, 1280, 520, 1, ALICE_BLUE)
DEPURACION_INFO = make_image_info_dict(ZONE_POINTS_DEPURACION, ZONE_WRAPPER_POINTS_DEPURACION, 1280, 524, 1, ALICE_BLUE)
DESTINTADO_INFO = make_image_info_dict(ZONE_POINTS_DESTINTADO, ZONE_WRAPPER_POINTS_DESTINTADO, 1280, 534, 1, ALICE_BLUE)
ESPESADO_INFO = make_image_info_dict(ZONE_POINTS_ESPESADO, ZONE_WRAPPER_POINTS_ESPESADO, 1280, 656, 1, ALICE_BLUE)
BLANQUEO_INFO = make_image_info_dict(ZONE_POINTS_BLANQUEO, ZONE_WRAPPER_POINTS_BLANQUEO, 863, 592, 1, ALICE_BLUE)
REFINADO_INFO = make_image_info_dict(ZONE_POINTS_REFINADO, ZONE_WRAPPER_POINTS_REFINADO, 1280, 664, 1, ALICE_BLUE)

IMAGES_INFO = {'mine': MINE_INFO, 
               'recycled_paper': RECYCLED_PAPER_INFO, 
               'pulper': PULPER_INFO, 
               'depuracion': DEPURACION_INFO, 
               'destintado': DESTINTADO_INFO, 
               'espesado': ESPESADO_INFO, 
               'blanqueo': BLANQUEO_INFO, 
               'refinado': REFINADO_INFO}

DIAGRAM_KEYS_TO_NAMES = {'mine_diagram': 'mine', 
                         'mine_diagram_light': 'mine', 
                         'recycled_paper_plant_diagram': 'recycled_paper', 
                         'recycled_paper_plant_diagram_light': 'recycled_paper', 
                         'pulper_dark': 'pulper', 
                         'pulper_light': 'pulper', 
                         'depuracion_dark': 'depuracion', 
                         'depuracion_light': 'depuracion', 
                         'destintado_dark': 'destintado', 
                         'destintado_light': 'destintado', 
                         'espesado_dark': 'espesado', 
                         'espesado_light': 'espesado', 
                         'blanqueo_dark': 'blanqueo', 
                         'blanqueo_light': 'blanqueo', 
                         'refinado_dark': 'refinado', 
                         'refinado_light': 'refinado'}


















