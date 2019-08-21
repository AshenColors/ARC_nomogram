# -*- coding: utf-8 -*-
"""
    Mildot Master clone
    Requires pynomo, which can be a Bit to set up. Good luck!

    TODO: add bullet drop and dual mils/MOA scale.
"""

import sys

sys.path.insert(0, "..")
# sys.path[:0] = [".."]
from pynomo.nomographer import *
from math import log, cos, radians

mils_scale = {
    # mils
    'u_min': 1,
    'u_max': 10,
    'function': lambda m: log(m),
    'scale_type': 'linear smart',
    'title': 'Mils',
    'tick_levels': 2,
    'tick_text_levels': 2,
    'extra_params': [{
        'scale_type': 'manual line',
        'grid_length_1': 0.1,
        'manual_axis_data': {
            1.25: '',
            1.75: '',
            2.25: '',
            2.75: '',
            3.25: '',
            3.75: '',
            4.25: '',
            4.75: '',
            5.25: '',
            5.75: '',
            6.25: '',
            6.75: '',
            7.25: '',
            7.75: '',
            8.25: '',
            8.75: '',
            9.25: '',
            9.75: '',
        }
    }]
}

size_scale = {
    # size
    # TODO: make this display feet and inches properly. Make it a dual scale with meters?
    'u_min': 6,
    'u_max': 72,
    'function': lambda s: -log(s),
    'scale_type': 'linear smart',
    'title': 'Target size (in)',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

range_scale_1 = {
    # range
    'tag': range,
    'u_min': 50,
    'u_max': 500,
    'function': lambda r: log(r) - log(27.77),
    'scale_type': 'linear smart',
    'title': 'Range (yd)',
    'tick_levels': 4,
    'tick_text_levels': 3,
}

range_scale_2 = {
    # range
    'tag': range,
    'u_min': 50,
    'u_max': 500,
    'function': lambda r: log(r),
    'scale_type': 'linear smart',
    'tick_levels': 4,
    'tick_text_levels': 3,
}

angle_scale = {
    # angle target is at, 0 is default
    # TODO: pretty-print degrees with ° (maybe number format can help?)
    'u_min': 15,
    'u_max': 60,
    'function': lambda a: log(cos(radians(a))),
    'scale type': 'linear smart',
    'title': 'Angle',
    'tick_levels': 2,
    'tick_text_levels': 1,
}

adjusted_range_scale = {
    # range
    'u_min': 50,
    'u_max': 500,
    'function': lambda ar: -log(ar),
    'scale_type': 'linear smart',
    'title': 'Adj Range (yd)',
    'tick_levels': 4,
    'tick_text_levels': 3,
    'tick_side': 'left',
}

block_1_params = {
    'block_type': 'type_1',
    'height': 20.0,
    'width': 4.0,
    'f1_params': mils_scale,
    'f2_params': size_scale,
    'f3_params': range_scale_1,
    'isopleth_values': [[2, 12, 'x']],
}

block_2_params = {
    'block_type': 'type_1',
    'height': 30.0,
    'width': 1.0,
    'f1_params': range_scale_2,
    'f2_params': angle_scale,
    'f3_params': adjusted_range_scale,
    'isopleth_values': [[200, 30, 'x']],
}

main_params = {
    'filename': 'mildot.pdf',
    'block_params': [block_1_params, block_2_params],
    'paper_height': 22.0,
    'paper_width': 14.0,
    'transformations': [('rotate', 0.01), ('scale paper',)],
}

Nomographer(main_params)
