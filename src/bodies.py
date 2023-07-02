import numpy as np
import ctypes

c_double_p = ctypes.POINTER(ctypes.c_double)


class body_system:  # particle class

  def __init__(self: 'body_system', name: str, dim: int, n_bodies: int,
               bodies_names: np.ndarray, mass: np.ndarray, r0: np.ndarray) -> None:
    self.name = name
    self.dim = dim
    self.n_bodies = n_bodies  # number of planets
    self.bodies_names = bodies_names
    self.mass = mass
    self.r0 = r0
    self.volume()
    self.color()
    # self.change_of_rf()

  def volume(self) -> None:
    if "solar_system" in self.name:
      a = 0.5
      b = 3
      vol = np.array([109.2,  # sun
                      0.3829,  # mercury
                      0.9499,  # venus
                      1,  # earth
                      # 0.107,  # moon
                      0.5320,  # mars
                      10.97,  # jupiter
                      9.14,  # saturn
                      3.981,  # uranus
                      3.865])  # neptune
      if self.n_bodies >= 9:
        vol[0] = 0.3829
      self.vol = a * vol + b
    else:
      if self.dim == 2:
        a = 2
        b = 0
        self.vol = a * np.sqrt(self.mass) + b
      else:
        a = 3
        b = 0
        self.vol = a * np.cbrt(self.mass) + b

  def color(self) -> None:
    if "solar_system" in self.name:
      self.colors = np.zeros((self.n_bodies, 3))
      for i, planet in enumerate(self.bodies_names):
        if planet == "sun":
          self.colors[i] = np.array([1, 1, 0])
        elif planet == "mercury":
          self.colors[i] = np.array([0.5, 0.5, 0.5])
        elif planet == "venus":
          self.colors[i] = np.array([0.5, 0.5, 0])
        elif planet == "earth":
          self.colors[i] = np.array([0, 0, 1])
        elif planet == "moon":
          self.colors[i] = np.array([0.8, 0.8, 0.8])
        elif planet == "mars":
          self.colors[i] = np.array([1, 0, 0])
        elif planet == "jupiter":
          self.colors[i] = np.array([1, 0.5, 0])
        elif planet == "saturn":
          self.colors[i] = np.array([0.5, 0.5, 0])
        elif planet == "uranus":
          self.colors[i] = np.array([0, 0.5, 0.5])
        elif planet == "neptune":
          self.colors[i] = np.array([0, 0, 0.5])
    else:
      self.colors = np.random.uniform(0.25, 1, size=(self.n_bodies, 3))

  # integration of the system

  def integrate_system(self: 'body_system', lib_filename: str,
                       num_steps: int, step_size: float, num_steps_max_flow: int,
                       TOL_rk78: float, EPS_field: float) -> None:
    # preparing income and outcome types of variables
    fun = ctypes.CDLL(lib_filename)

    fun.integration.argtypes = [
        ctypes.c_int,  # numSteps
        ctypes.POINTER(ctypes.c_double),  # x
        ctypes.POINTER(ctypes.c_double),  # m
        ctypes.c_double,  # h
        ctypes.c_double,  # hmin
        ctypes.c_double,  # hmax
        ctypes.c_double,  # tol
        ctypes.c_int,  # maxNumStepsFlow
        ctypes.c_int,  # n_bodies
        ctypes.c_int,  # dim
        ctypes.c_double,  # G
        ctypes.c_double,  # EPS
    ]
    fun.integration.restype = ctypes.POINTER(ctypes.c_double)  # result
    fun.com.argtypes = [ctypes.c_int,  # dim
                        ctypes.c_int,  # num_steps
                        ctypes.c_int,  # n_bodies
                        ctypes.POINTER(ctypes.c_double),  # r
                        ctypes.POINTER(ctypes.c_double)  # mass
                        ]
    fun.com.restype = ctypes.POINTER(ctypes.c_double)

    self.r = np.zeros((num_steps + 1, 2 * self.dim * self.n_bodies))
    self.com = np.zeros((num_steps + 1, self.dim))

    # conversion from np.array to ctype data
    aux_r0 = self.r0.flatten().astype(np.float64)
    aux_r0 = aux_r0.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    aux_mass = self.mass.astype(np.float64)
    aux_mass = aux_mass.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    # calling the functions
    step_size_min = step_size / 100
    step_size_max = step_size * 100
    G = 1.
    r = fun.integration(num_steps, aux_r0, aux_mass, step_size, step_size_min,
                        step_size_max, TOL_rk78, num_steps_max_flow, self.n_bodies,
                        self.dim, G, EPS_field)
    com = fun.com(self.dim, num_steps, self.n_bodies, r, aux_mass)

    # conversion from ctype data to np.array
    # reshape r in num_steps+1 blocks of n_bodies x dim
    self.r = np.ctypeslib.as_array(
        r, shape=(num_steps + 1, self.n_bodies, self.dim))
    # with open("data/positions_body1.txt", "w") as f:
    #   for i in range(num_steps + 1):
    #     f.write(str(self.r[i, 0, 0]) + " " + str(self.r[i, 0, 1]) + "\n")
    self.com = np.ctypeslib.as_array(com, shape=(num_steps + 1, self.dim))

  def init_com(self, r) -> np.ndarray:
    xyz = r[:, 0:self.dim]
    M = np.sum(self.mass)
    aux_mass = np.tile(self.mass, (self.dim, 1)).T
    XYZ = np.sum(xyz * aux_mass, axis=0) / M
    return XYZ

  def change_of_rf(self) -> None:
    # np.tile = repeat the array (first argument) n times (second argument)
    com = np.tile(self.init_com(self.r0), (self.n_bodies, 1))
    self.r0[:, 0:self.dim] -= com
