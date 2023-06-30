# N-body problem
from animation import get_anim
from setup import get_bodies
import os
# np.set_printoptions(threshold=sys.maxsize)


def main(num_steps: int, step_size: float, num_steps_max_flow: int,
         TOL_rk78: float, EPS_field: float) -> None:
  script_dir = os.path.dirname(os.path.abspath(__file__))
  filename_inp = script_dir + "/../data/data.csv"
  lib_filename = script_dir + "/../libs/lib_n-body_field.so"

  # get the system
  system = get_bodies(filename_inp)

  # integration of the system
  system.integrate_system(
      lib_filename,
      num_steps,
      step_size,
      num_steps_max_flow,
      TOL_rk78,
      EPS_field)

  # Create animation)
  get_anim(system, step_size, filename_inp)


num_steps = 1500
step_size = 1e-6
num_steps_max_flow = 10000
TOL_rk78 = 1e-8
EPS_field = 1e-8
main(num_steps, step_size, num_steps_max_flow, TOL_rk78, EPS_field)
