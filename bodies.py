import numpy as np
import ctypes

c_double_p = ctypes.POINTER(ctypes.c_double)


class body_system:  # particle class

  colors: np.ndarray

  def __init__(self, sys_name, dim, n, bodies_names, mass, r0):
    self.sys_name = sys_name
    self.dim = dim
    self.n = n  # number of planets
    self.bodies_names = bodies_names
    self.mass = mass
    self.r0 = r0
    self.volume()
    self.change_of_sr()

  def volume(self):
    if "solar_system" in self.sys_name:
      a = 0.5
      b = 3
      vol = np.array([109.2,  # sun
                      0.3829,  # mercury
                      0.9499,  # venus
                      1,  # earth
                      0.5320,  # mars
                      10.97,  # jupiter
                      9.14,  # saturn
                      3.981,  # uranus
                      3.865])  # neptune
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

  # def integrated_system(self, r, num_steps, dt, EPS):
  #   self.r = r

  def integrate_system(self, num_steps, dt, EPS):  # integration of the system
    # preparing income and outcome types of variables
    fun = ctypes.CDLL("./librk4.so")
    fun.rk4.argtypes = [
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        c_double_p,
        c_double_p,
        ctypes.c_double,
        ctypes.c_double]
    fun.rk4.restype = c_double_p
    fun.com.argtypes = [ctypes.c_int,
                        ctypes.c_int,
                        ctypes.c_int,
                        c_double_p,
                        c_double_p]
    fun.com.restype = c_double_p

    # conversion from np.array to ctype data
    aux_r0 = self.r0.astype(np.float64)
    aux_r0 = aux_r0.ctypes.data_as(c_double_p)
    aux_mass = self.mass.astype(np.float64)
    aux_mass = aux_mass.ctypes.data_as(c_double_p)

    # calling the functions
    r = fun.rk4(num_steps, self.dim, self.n, aux_r0, aux_mass, dt, EPS)
    com = fun.com(num_steps, self.dim, self.n, r, aux_mass)

    # conversion from ctype data to np.array
    self.r = np.ctypeslib.as_array(
        r, shape=(num_steps + 1, 2 * self.dim * self.n))
    self.com = np.ctypeslib.as_array(com, shape=(num_steps + 1, self.dim))

  def init_com(self, r):  # center of masses
    xyz = r[::2]
    M = np.sum(self.mass)
    aux_mass = np.repeat(self.mass, repeats=self.dim)
    XYZ = np.sum((xyz * aux_mass).reshape((self.n, self.dim)), axis=0) / M
    return XYZ

  def change_of_sr(self):
    com = np.tile(self.init_com(self.r0), self.n)
    self.r0[::2] -= com
