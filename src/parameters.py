# CONSTANTS
# t0 = 91.87  # years. t0 = sqrt((1au)^3/(G*M_earth))
t0 = 33554.6043376  # days

# PARAMETERS TO CHANGE
#### SOLAR SYSTEM ####
# days = 1000  # number of days to simulate (real days)
# # number of steps to simulate (the more steps, the smoother the animation)
# speed_up = 3  # speed up the animation by this factor

#### SOLAR SYSTEM ROCKY ####
# days = 1000  # number of days to simulate (real days)
# # number of steps to simulate (the more steps, the smoother the animation)
# speed_up = 0.5  # speed up the animation by this factor


#### DEFAULT FOR RANDOM SYSTEMS ####
days = 100000  # number of days to simulate (real days)
# number of steps to simulate (the more steps, the smoother the animation)
speed_up = 40  # speed up the animation by this factor

# number of steps to simulate (the more steps, the smoother the animation)
num_steps = int(days / speed_up)
days_new_unit = days / t0  # number of new units of time
step_size = days_new_unit * 1. / num_steps  # step size
num_steps_max_flow = 10000  # maximum number of steps for the flow
TOL_rk78 = 1e-8  # tolerance for the Runge-Kutta 7(8) method
EPS_field = 1e-8  # softening parameter for the gravitational field
