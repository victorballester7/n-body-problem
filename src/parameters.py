# CONSTANTS
# t0 = 91.87  # years. t0 = sqrt((1au)^3/(G*M_earth))
t0 = 33554.6043376  # days


# PARAMETERS TO CHANGE
days = 100  # number of days to simulate (real days)
# number of steps to simulate (the more steps, the smoother the animation)
num_steps = 10000
speed_up = 100  # speed up the animation by this factor
days_new_unit = days / t0 * speed_up  # number of days to simulate (new unit)
step_size = days_new_unit * 1. / num_steps  # step size for the simulation
num_steps_max_flow = 10000  # maximum number of steps for the flow
TOL_rk78 = 1e-8  # tolerance for the Runge-Kutta 7(8) method
EPS_field = 1e-8  # softening parameter for the gravitational field
