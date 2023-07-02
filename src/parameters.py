# CONSTANTS
# t0 = 91.87  # years. t0 = sqrt((1au)^3/(G*M_earth))
t0 = 33554.6043376  # days

# PARAMETERS TO CHANGE
#### SOLAR SYSTEM ####
days_solar_syst = 10000  # number of days to simulate (real days)
# number of steps to simulate (the more steps, the smoother the animation)
speed_up_solar_syst = 3  # speed up the animation by this factor

#### SOLAR SYSTEM ROCKY ####
days_solar_syst_rock = 1000  # number of days to simulate (real days)
# number of steps to simulate (the more steps, the smoother the animation)
speed_up_solar_syst_rock = 0.5  # speed up the animation by this factor


#### DEFAULT FOR RANDOM SYSTEMS ####
days = 100000  # number of days to simulate (real days)
# number of steps to simulate (the more steps, the smoother the animation)
speed_up = 75  # speed up the animation by this factor


def param(days: int, speed_up: float) -> tuple[int, float]:
  # number of steps to simulate (the more steps, the smoother the animation)
  num_steps = int(days * 1. / speed_up)
  days_new_unit = days / t0  # number of new units of time
  step_size = days_new_unit / num_steps  # step size
  return num_steps, step_size


num_steps_max_flow = 10000  # maximum number of steps for the flow
TOL_rk78 = 1e-8  # tolerance for the Runge-Kutta 7(8) method
EPS_field = 1e-4  # softening parameter for the gravitational field
