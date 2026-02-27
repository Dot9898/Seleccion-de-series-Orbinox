
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


GRAY_BLUE = (161, 202, 228) #'#a1cae4' primary
LIGHT_BLUE_ORIGINAL = (0, 120, 255) #'#0078FF'
LIGHT_BLUE = (31, 132, 181) #'#1F84B5' old secondary
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
                              'Dispersión-y-espesado': [(907, 321), (933, 272), (921, 253), (937, 225), (920, 221), (923, 196), (904, 189), (900, 200), (793, 168), (783, 183), (759, 176), (755, 182), (747, 179), (740, 190), (740, 197), (745, 199), (729, 226), (751, 233), (726, 271)], 
                              'Blanqueo': [(628, 255), (628, 245), (620, 239), (621, 211), (628, 196), (644, 191), (658, 198), (665, 197), (669, 175), (660, 173), (658, 155), (671, 143), (671, 123), (680, 111), (693, 109), (702, 118), (702, 129), (693, 145), (691, 190), (707, 184), (722, 190), (723, 210), (715, 216), (715, 225), (696, 227), (689, 240), (682, 241), (680, 258)], 
                              'Refinado': [(591, 210), (598, 210), (599, 202), (593, 201), (599, 186), (585, 178), (563, 176), (561, 183), (566, 185), (557, 192), (557, 203), (566, 215), (581, 219)]}
ZONE_WRAPPER_POINTS_RECYCLED_PAPER = {'Pulper': [(171, 625), (192, 335), (492, 336), (495, 625)], 
                                      'Depuración': [(499, 331), (500, 619), (1005, 616), (1005, 422), (964, 389), (953, 368), (932, 349)], 
                                      'Destintado': [(954, 367), (936, 349), (930, 331), (986, 195), (1038, 188), (1118, 243), (1118, 425), (1034, 417)], 
                                      'Dispersión-y-espesado': [(983, 163), (918, 351), (742, 340), (689, 309), (767, 103)], 
                                      'Blanqueo': [(682, 311), (774, 71), (661, 58), (570, 308)], 
                                      'Refinado': [(640, 93), (568, 289), (482, 280), (489, 133), (558, 84)]}

ZONE_POINTS_VIRGIN_PAPER = {'Cocción': [(389, 675), (389, 662), (381, 648), (378, 519), (382, 484), (382, 461), (397, 462), (421, 451), (427, 421), (427, 387), (435, 387), (436, 417), (444, 448), (446, 492), (478, 505), (490, 503), (489, 514), (496, 517), (496, 540), (504, 548), (507, 687), (486, 695)], 
                            'Cribado-y-lavado': [(620, 709), (605, 708), (580, 699), (555, 697), (555, 687), (548, 680), (547, 634), (569, 607), (589, 631), (601, 633), (613, 619), (624, 634), (703, 637), (758, 585), (773, 592), (773, 595), (764, 604), (803, 615), (803, 621), (710, 712), (674, 701)], 
                            'Deslignificación': [(847, 661), (838, 653), (843, 486), (852, 479), (865, 481), (869, 490), (886, 496), (897, 489), (908, 501), (904, 661), (907, 664), (908, 677), (884, 683)], 
                            'Blanqueo': [(1209, 645), (1181, 644), (939, 573), (944, 417), (960, 412), (978, 420), (972, 516), (986, 524), (1002, 520), (1016, 530), (1041, 531), (1048, 459), (1066, 444), (1077, 464), (1073, 554), (1087, 555), (1103, 550), (1119, 558), (1138, 562), (1142, 493), (1140, 477), (1160, 467), (1177, 482), (1168, 581), (1183, 584), (1199, 577), (1214, 588)], 
                            'Recuperación-de-licor': [(393, 372), (339, 376), (334, 338), (353, 311), (354, 281), (377, 268), (418, 273), (449, 266), (450, 184), (441, 181), (439, 163), (455, 158), (455, 143), (463, 140), (463, 157), (485, 148), (515, 162), (515, 183), (527, 191), (530, 208), (551, 217), (552, 251), (568, 254), (570, 235), (630, 208), (658, 196), (663, 239), (622, 259), (658, 267), (714, 237), (730, 245), (730, 301), (757, 338), (760, 360), (733, 399), (729, 417), (707, 416), (678, 429), (644, 407), (661, 399), (629, 390), (629, 347), (637, 340), (642, 347), (653, 347), (699, 364), (705, 348), (705, 336), (692, 326), (669, 333), (669, 308), (625, 291), (580, 283), (519, 285), (497, 285), (476, 294), (469, 290), (438, 304), (438, 331), (429, 337), (418, 331), (407, 330), (407, 352), (390, 355)]}
ZONE_WRAPPER_POINTS_VIRGIN_PAPER = {'Cocción': [(306, 750), (516, 776), (516, 425), (431, 384), (313, 434)], 
                                    'Cribado-y-lavado': [(529, 768), (534, 507), (800, 521), (807, 765)], 
                                    'Deslignificación': [(822, 757), (821, 442), (924, 497), (936, 637), (1047, 717), (1047, 761)], 
                                    'Blanqueo': [(920, 486), (876, 461), (908, 358), (1259, 467), (1261, 701), (1131, 686), (942, 610)], 
                                    'Recuperación-de-licor': [(283, 424), (289, 221), (386, 98), (641, 129), (815, 227), (796, 455), (528, 474), (527, 392), (429, 365)]}

ZONE_POINTS_PULPER = {'Pulper-1': [(25, 260), (120, 260), (120, 350), (25, 350)], 
                      'Pulper-2': [(325, 260), (405, 260), (405, 350), (325, 350)], 
                      'Pulper-3': [(535, 260), (605, 260), (605, 350), (535, 350)], 
                      'Pulper-4': [(195, 340), (320, 340), (320, 450), (195, 450)], 
                      'Pulper-5': [(395, 340), (515, 340), (515, 450), (395, 450)], 
                      'Pulper-6': [(600, 340), (745, 340), (745, 450), (600, 450)], 
                      'Pulper-7': [(905, 340), (1020, 340), (1020, 445), (905, 445)], 
                      'Pulper-8': [(980, 260), (1085, 260), (1085, 345), (980, 345)]}
ZONE_WRAPPER_POINTS_PULPER = ZONE_POINTS_PULPER

ZONE_POINTS_DEPURACION = {'Depuración-1': [(265, 230), (545, 230), (545, 340), (265, 340)], 
                          'Depuración-2': [(775, 290), (860, 290), (860, 360), (775, 360)], 
                          'Depuración-3': [(870, 235), (1150, 235), (1150, 340), (870, 340)]}
ZONE_WRAPPER_POINTS_DEPURACION = ZONE_POINTS_DEPURACION

ZONE_POINTS_DESTINTADO = {'Destintado-1': [(250, 385), (360, 385), (360, 470), (250, 470)], 
                          'Destintado-2': [(645, 190), (760, 190), (760, 270), (645, 270)], 
                          'Destintado-3': [(995, 75), (1100, 75), (1100, 160), (995, 160)]}
ZONE_WRAPPER_POINTS_DESTINTADO = ZONE_POINTS_DESTINTADO

ZONE_POINTS_ESPESADO = {'Dispersión-y-espesado-1': [(320, 230), (425, 230), (425, 310), (320, 310)], 
                        'Dispersión-y-espesado-2': [(455, 470), (565, 470), (565, 560), (455, 560)], 
                        'Dispersión-y-espesado-3': [(835, 175), (975, 175), (975, 250), (835, 250)]}
ZONE_WRAPPER_POINTS_ESPESADO = ZONE_POINTS_ESPESADO

ZONE_POINTS_BLANQUEO = {'Blanqueo-1': [(20, 325), (20, 430), (150, 430), (150, 325)], 
                        'Blanqueo-2': [(170, 290), (170, 225), (300, 225), (300, 290)], 
                        'Blanqueo-3': [(285, 525), (285, 440), (405, 440), (405, 525)], 
                        'Blanqueo-4': [(445, 525), (445, 440), (585, 440), (585, 525)], 
                        'Blanqueo-5': [(665, 525), (665, 440), (765, 440), (765, 525)]}
ZONE_WRAPPER_POINTS_BLANQUEO = ZONE_POINTS_BLANQUEO

ZONE_POINTS_REFINADO = {'Refinado-1': [(250, 592), (250, 500), (385, 500), (385, 595)], 
                        'Refinado-2': [(510, 375), (510, 285), (710, 285), (710, 375)], 
                        'Refinado-3': [(820, 240), (820, 145), (930, 145), (930, 240)]}
ZONE_WRAPPER_POINTS_REFINADO = ZONE_POINTS_REFINADO

ZONE_POINTS_COCCION = {'Cocción-1': [(425, 545), (530, 545), (530, 625), (425, 625)],
                       'Cocción-2': [(700, 470), (785, 470), (785, 560), (700, 560)]}
ZONE_WRAPPER_POINTS_COCCION = ZONE_POINTS_COCCION

ZONE_POINTS_CRIBADO = {'Cribado-y-lavado-1': [(180, 300), (270, 300), (270, 410), (180, 410)],
                       'Cribado-y-lavado-2': [(355, 305), (450, 305), (450, 410), (355, 410)],
                       'Cribado-y-lavado-3': [(380, 435), (520, 435), (520, 520), (380, 520)],
                       'Cribado-y-lavado-4': [(560, 470), (770, 470), (770, 640), (560, 640)],
                       'Cribado-y-lavado-5': [(1085, 40), (1220, 40), (1220, 110), (1085, 110)]}
ZONE_WRAPPER_POINTS_CRIBADO = ZONE_POINTS_CRIBADO

ZONE_POINTS_DESLIGNIFICACION = {'Deslignificación-1': [(25, 215), (870, 215), (870, 340), (25, 340)],
                                'Deslignificación-2': [(885, 185), (975, 185), (975, 230), (885, 230)],
                                'Deslignificación-3': [(1050, 65), (1125, 65), (1125, 100), (1050, 100)]}
ZONE_WRAPPER_POINTS_DESLIGNIFICACION = ZONE_POINTS_DESLIGNIFICACION

ZONE_POINTS_MEZCLA = {'Mezcla-y-preparación-de-pasta-1': [(345, 295), (435, 295), (435, 370), (345, 370)],
                      'Mezcla-y-preparación-de-pasta-2': [(675, 140), (775, 140), (775, 210), (675, 210)],
                      'Mezcla-y-preparación-de-pasta-3': [(570, 295), (625, 295), (625, 370), (570, 370)],
                      'Mezcla-y-preparación-de-pasta-4': [(635, 295), (685, 295), (685, 370), (635, 370)],
                      'Mezcla-y-preparación-de-pasta-5': [(755, 295), (810, 295), (810, 370), (755, 370)],
                      'Mezcla-y-preparación-de-pasta-6': [(820, 295), (880, 295), (880, 370), (820, 370)]}
ZONE_WRAPPER_POINTS_MEZCLA = ZONE_POINTS_MEZCLA

ZONE_POINTS_RECUPERACION = {'Recuperación-de-licor-1': [(65, 95), (205, 95), (205, 170), (65, 170)],
                            'Recuperación-de-licor-2': [(285, 195), (500, 195), (500, 300), (285, 300)],
                            'Recuperación-de-licor-3': [(850, 245), (940, 245), (940, 350), (850, 350)],
                            'Recuperación-de-licor-4': [(1255, 320), (1390, 320), (1390, 405), (1255, 405)],
                            'Recuperación-de-licor-5': [(835, 505), (925, 505), (925, 620), (835, 620)],
                            'Recuperación-de-licor-6': [(430, 505), (685, 505), (685, 620), (430, 620)]}
ZONE_WRAPPER_POINTS_RECUPERACION = ZONE_POINTS_RECUPERACION


MINE_INFO = make_image_info_dict(ZONE_POINTS_MINE, ZONE_WRAPPER_POINTS_MINE, 5388, 3404, 5, LIGHT_BLUE)

RECYCLED_PAPER_INFO = make_image_info_dict(ZONE_POINTS_RECYCLED_PAPER, ZONE_WRAPPER_POINTS_RECYCLED_PAPER, 1120, 644, 1, LIGHT_BLUE)
PULPER_INFO = make_image_info_dict(ZONE_POINTS_PULPER, ZONE_WRAPPER_POINTS_PULPER, 1280, 520, 1, GRAY_BLUE)
DEPURACION_INFO = make_image_info_dict(ZONE_POINTS_DEPURACION, ZONE_WRAPPER_POINTS_DEPURACION, 1280, 524, 1, GRAY_BLUE)
DESTINTADO_INFO = make_image_info_dict(ZONE_POINTS_DESTINTADO, ZONE_WRAPPER_POINTS_DESTINTADO, 1280, 534, 1, GRAY_BLUE)
ESPESADO_INFO = make_image_info_dict(ZONE_POINTS_ESPESADO, ZONE_WRAPPER_POINTS_ESPESADO, 1280, 656, 1, GRAY_BLUE)
BLANQUEO_INFO = make_image_info_dict(ZONE_POINTS_BLANQUEO, ZONE_WRAPPER_POINTS_BLANQUEO, 863, 592, 1, GRAY_BLUE)
REFINADO_INFO = make_image_info_dict(ZONE_POINTS_REFINADO, ZONE_WRAPPER_POINTS_REFINADO, 1280, 664, 1, GRAY_BLUE)

VIRGIN_PAPER_INFO = make_image_info_dict(ZONE_POINTS_VIRGIN_PAPER, ZONE_WRAPPER_POINTS_VIRGIN_PAPER, 1276, 775, 1, LIGHT_BLUE)
COCCION_INFO = make_image_info_dict(ZONE_POINTS_COCCION, ZONE_WRAPPER_POINTS_COCCION, 825, 627, 1, GRAY_BLUE)
CRIBADO_INFO = make_image_info_dict(ZONE_POINTS_CRIBADO, ZONE_WRAPPER_POINTS_CRIBADO, 1228, 710, 1, GRAY_BLUE)
DESLIGNIFICACION_INFO = make_image_info_dict(ZONE_POINTS_DESLIGNIFICACION, ZONE_WRAPPER_POINTS_DESLIGNIFICACION, 1130, 443, 1, GRAY_BLUE)
RECUPERACION_INFO = make_image_info_dict(ZONE_POINTS_RECUPERACION, ZONE_WRAPPER_POINTS_RECUPERACION, 1408, 694, 1, GRAY_BLUE)


ZONE_TO_IMAGE_NAME = {'Pulper': 'pulper', 
                      'Depuración': 'depuracion', 
                      'Destintado': 'destintado', 
                      'Dispersión-y-espesado': 'espesado', 
                      'Blanqueo': 'blanqueo', 
                      'Refinado': 'refinado', 

                      'Cocción': 'coccion', 
                      'Cribado-y-lavado': 'cribado', 
                      'Deslignificación': 'deslignificacion', 
                      'Recuperación-de-licor': 'recuperacion'}

IMAGES_INFO = {'mine': MINE_INFO, 
               'recycled_paper': RECYCLED_PAPER_INFO, 
               'virgin_paper': VIRGIN_PAPER_INFO, 

               'pulper': PULPER_INFO, 
               'depuracion': DEPURACION_INFO, 
               'destintado': DESTINTADO_INFO, 
               'espesado': ESPESADO_INFO, 
               'blanqueo': BLANQUEO_INFO, 
               'refinado': REFINADO_INFO, 

               'coccion': COCCION_INFO, 
               'cribado': CRIBADO_INFO, 
               'deslignificacion': DESLIGNIFICACION_INFO, 
               'recuperacion': RECUPERACION_INFO}

DIAGRAM_KEYS_TO_NAMES = {'mine_diagram': 'mine', 
                         'mine_diagram_light': 'mine', 
                         'recycled_paper_diagram': 'recycled_paper', 
                         'recycled_paper_diagram_light': 'recycled_paper', 
                         'virgin_paper_diagram': 'virgin_paper', 
                         'virgin_paper_diagram_light': 'virgin_paper', 

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
                         'refinado_light': 'refinado', 
                        
                         'coccion_dark': 'coccion',
                         'coccion_light': 'coccion',
                         'cribado_dark': 'cribado',
                         'cribado_light': 'cribado',
                         'deslignificacion_dark': 'deslignificacion',
                         'deslignificacion_light': 'deslignificacion',
                         'recuperacion_dark': 'recuperacion',
                         'recuperacion_light': 'recuperacion'}















