# -*- coding: utf-8 -*-
"""
    Angular range calculator
    Mildot Master clone
    Requires pynomo, which can be a Bit to set up. Good luck!

    TODO: add bullet drop and dual mils/MOA scale. It'll probably have to be on a different nomogram altogether.
"""

import sys
from wrapt import patch_function_wrapper
from itertools import chain
from math import log, cos, radians
from pynomo import *
from pyx import text

sys.path.insert(0, "..")
# sys.path[:0] = [".."]

version = "1.0.3-prerelease"


@patch_function_wrapper(nomo_axis.Nomo_Axis, '_put_text_')
def new_put_text(wrapped, instance, args, kwargs):
    u = args[0]
    if instance.text_style == 'oldstyle':
        return r"$\oldstylenums{%3.2f}$ " % u
    else:
        # return r"$%3.2f$ " %u
        if instance.axis_appear['text_format_func'] is not None:
            return instance.axis_appear['text_format_func'](u)
        return instance.axis_appear['text_format'] % u


def format_feet(n):
    """Converts a length in inches to both feet and inches in a nicely formatted string."""
    n = int(n)
    feet = n // 12
    inches = n % 12
    if feet == 0:
        return f"${inches}''$ "
    elif n < 60:
        return f"${n}''$ "
    elif n >= 120 and inches == 0:
        return f"${feet}'$ "
    else:
        return r"${}' {}''$ ".format(feet, inches)


mils_scale = {
    # mils
    'title': 'Mils',
    'u_min': 1,
    'u_max': 10,
    'function': lambda m: log(m),
    'scale_type': 'manual line',
    'text_size_manual': text.size.scriptsize,
    'manual_axis_data':
        {**{i / 100: i / 100 for i in range(125, 300, 50)}, **{i / 100: '' for i in range(325, 1000, 50)}},
    'grid_length_1': 0.2,
    'extra_params': [{
        'u_min': 1,
        'u_max': 10,
        'scale_type': 'linear smart',
        'tick_levels': 2,
        'tick_text_levels': 2,
    }]
}

size_scale = {
    # size
    # TODO: make this a dual scale with meters
    # TODO: also make this scale a LOT prettier in regards to feet and inches
    'u_min': 4,
    'u_max': 240,
    'function': lambda s: -log(s),
    'scale_type': 'manual line',
    'manual_axis_data':
        {i: format_feet(i) for i in chain(range(4, 16), range(16, 40, 2), range(40, 60, 5),
                                          range(60, 108, 6), range(108, 241, 12))},
    'grid_length_1': 0.6,
    'text_format_func': lambda n: format_feet(n),
    'text_size_manual': text.size.scriptsize,
    'text_distance_1': 0.7,
    'title': 'Target size (in)',
    'extra_params': [{
        # This part is for the minor markings between numbered ticks.
        # 'linear smart' doesn't handle this very well, so we've gotta do it manually.
        'u_min': 4,
        'u_max': 240,
        'scale_type': 'manual line',
        'manual_axis_data':
            {i: '' for i in chain(range(16, 60), range(60, 108, 2), range(108, 240, 6))},
        'grid_length_1': 0.3,
    }]
}

range_scale_1 = {
    # range
    'tag': range,
    'u_min': 100,
    'u_max': 2000,
    'function': lambda r: log(r) - log(27.77),
    'scale_type': 'linear smart',
    'title': 'Range (yd)',
    'tick_levels': 3,
    'tick_text_levels': 3,
}

range_scale_2 = {
    # range
    'tag': range,
    'u_min': 100,
    'u_max': 2000,
    'function': lambda r: log(r),
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 3,
}

angle_scale = {
    # angle target is at, 0 is default
    'u_min': 15,
    'u_max': 60,
    'function': lambda a: log(cos(radians(a))),
    'text_format': r'$%3d^\circ$ ',
    'scale type': 'linear smart',
    'title': 'Angle',
    'tick_levels': 2,
    'tick_text_levels': 2,
    'text_size_0': text.size.tiny,
    'text_size_1': text.size.small,
    'grid_length_0': 0.25,
    'grid_length_1': 0.75,
    'text_distance_0': 0.30,
    'text_distance_1': 0.85,
}

adjusted_range_scale = {
    # range
    'u_min': 100,
    'u_max': 2000,
    'function': lambda ar: -log(ar),
    'scale_type': 'linear smart',
    'title': 'Adj Range (yd)',
    'tick_levels': 3,
    'tick_text_levels': 3,
    'tick_side': 'left',
}

block_1_params = {
    'block_type': 'type_1',
    'height': 10.0,
    'width': 6.0,
    'f1_params': mils_scale,
    'f2_params': size_scale,
    'f3_params': range_scale_1,
    'isopleth_values': [[1.5, 12, 'x']],
}

block_2_params = {
    'block_type': 'type_1',
    'height': 10.0,
    'width': 2.0,
    'f1_params': range_scale_2,
    'f2_params': angle_scale,
    'f3_params': adjusted_range_scale,
    'isopleth_values': [[223, 30, 'x']],
}

main_params = {
    'filename': 'mildot.pdf',
    'block_params': [block_1_params, block_2_params],
    'paper_height': 33.0,
    'paper_width': 14.0,
    'transformations': [('rotate', 0.01), ('scale paper',)],
    'title_str': "Angular range calculator v" + version,
    'title_y': 34.5,  # If this isn't set 1.5 higher than paper_height, the title and scale overlap badly.
}

nomographer.Nomographer(main_params)
