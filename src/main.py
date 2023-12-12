# N-body problem
from animation import get_anim
from setup import get_bodies
import os
from parameters import *
import time

# np.set_printoptions(threshold=sys.maxsize)

# Refer to src/parameters.py for the changing default values of the parameters


def main(num_steps_max_flow: int,
         TOL_rk78: float, TOL_coll: float, EPS_field: float) -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename_inp = script_dir + "/../data/data.csv"
    lib_filename = script_dir + "/../libs/lib_n-body_field.so"

    # get the system
    system = get_bodies(filename_inp)
    # or "solar_system_2d_rocky" in system.name. It is not necessary.

    # count time
    start = time.time()
    # integration of the system
    system.integrate_system(
        lib_filename,
        num_steps_max_flow,
        TOL_rk78,
        TOL_coll,
        EPS_field)
    end = time.time()
    print("time: ", end - start)

    # Create animation)
    get_anim(system, filename_inp)


main(num_steps_max_flow, TOL_rk78, TOL_coll, EPS_field)
