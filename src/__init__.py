from .conductivities import conductivity, conductivity2
from .freq_collisions import collision_frequencies, ion_neutral
from .core import (
    cond_from_file, 
    cond_from_models, 
    compute_parameters, 
    load_calculate
    )

from .methods import scale_gradient
# from .run_models import test_data

import settings as s

s.config_labels()