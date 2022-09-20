# N-body problem
from animation import get_anim
from setup import get_bodies
# np.set_printoptions(threshold=sys.maxsize)


def n_body_problem(num_steps=1500, dt=0.001, EPS=0.00001):
  system = get_bodies()

  # integration of the system
  system.integrate_system(num_steps, dt, EPS)

  # Create animation)
  get_anim(system, dt)


n_body_problem()
