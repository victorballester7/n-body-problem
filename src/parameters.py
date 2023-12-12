# CONSTANTS
t0_years = 91.87  # years. t0 = sqrt((1au)^3/(G*M_earth))
t0_days = 33554.6043376  # days
SIZE_title = 22
SIZE_big = 18
SIZE_small = 16
FRAMES_TO_ANIMATE = 1000
DEFAULT_system_type = 'r'  # 'r' or 'p'
DEFAULT_num_bodies = 5
DEFAULT_overwrite = 'y'  # 'y' or 'n'
DEFAULT_save = 'n'  # 'd', 'a', 'b' or 'n'
DEFAULT_trace = 'y'  # 'y' or 'n'
DEFAULT_com = 'n'  # 'y' or 'n'
DEFAULT_video_format = 'g'  # 'm' or 'g'
DEFAULT_dim = 2  # 2 or 3

# PARAMETERS TO CHANGE
#### SOLAR SYSTEM ####
DEFAULT_years_solar_syst = 28
# number of days to simulate (real days)
DEFAULT_days_solar_syst = 365 * DEFAULT_years_solar_syst
# number of steps to simulate (the more steps, the smoother the animation)
DEFAULT_speed_up_solar_syst = 10  # speed up the animation by this factor

#### SOLAR SYSTEM ROCKY ####
DEFAULT_years_solar_syst_rock = 3
# number of days to simulate (real days)
DEFAULT_days_solar_syst_rock = 365 * DEFAULT_years_solar_syst_rock
# number of steps to simulate (the more steps, the smoother the animation)
DEFAULT_speed_up_solar_syst_rock = 1  # speed up the animation by this factor


#### DEFAULT FOR RANDOM SYSTEMS ####
# number of years to simulate (real years). 1 year = 365 days
DEFAULT_years = 280
DEFAULT_days = 365 * DEFAULT_years  # number of days to simulate (real days)
# number of steps to simulate (the more steps, the smoother the animation)
DEFAULT_speedup = 80  # speed up the animation by this factor


def param(days: int, f: float) -> tuple[int, float]:
    # number of steps to simulate (the more steps, the smoother the animation)
    num_steps = int(days * f)
    days_new_unit = days / t0_days  # number of new units of time
    step_size = days_new_unit / num_steps  # step size
    return num_steps, step_size


num_steps_max_flow = 10000  # maximum number of steps for the flow
TOL_rk78 = 1e-8  # tolerance for the Runge-Kutta 7(8) method
TOL_coll = 1e-3  # collision tolerance
EPS_field = 1e-4  # softening parameter for the gravitational field
