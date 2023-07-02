# N-body problem
from animation import get_anim
from setup import get_bodies
import os
from parameters import *
import time

# np.set_printoptions(threshold=sys.maxsize)


def main(num_steps_max_flow: int,
         TOL_rk78: float, TOL_coll: float, EPS_field: float) -> None:
  script_dir = os.path.dirname(os.path.abspath(__file__))
  filename_inp = script_dir + "/../data/data.csv"
  lib_filename = script_dir + "/../libs/lib_n-body_field.so"

  # get the system
  system = get_bodies(filename_inp)
  if "solar_system_2d_rocky" in system.name:
    num_steps, step_size = param(days_solar_syst_rock, 2)
    speed_up = int(
        num_steps *
        1. /
        FRAMES_TO_ANIMATE *
        speed_up_solar_syst_rock)
  elif "solar_system_2d" in system.name:
    num_steps, step_size = param(days_solar_syst, 2)
    speed_up = int(num_steps * 1. / FRAMES_TO_ANIMATE * speed_up_solar_syst)
  else:
    num_steps, step_size = param(days, 0.5)
    speed_up = int(num_steps * 1. / FRAMES_TO_ANIMATE * speed_up_default)

  # count time
  start = time.time()
  # integration of the system
  system.integrate_system(
      lib_filename,
      num_steps,
      step_size,
      num_steps_max_flow,
      TOL_rk78,
      TOL_coll,
      EPS_field)
  end = time.time()
  print("time: ", end - start)

  # Create animation)
  get_anim(system, step_size, speed_up, filename_inp)


main(num_steps_max_flow, TOL_rk78, TOL_coll, EPS_field)
