from .conductivities import conductivity, conductivity2
from .freq_collisions import collision_frequencies, ion_neutral
from .core import (
    cond_from_file, 
    cond_from_models, 
    test_data, 
    compute_parameters, 
    load_calculate
    )


import settings as s

s.config_labels()