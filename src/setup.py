import numpy as np
import pandas as pd
from bodies import body_system
import sys


def get_dim() -> int:
  print("Dimension (2 or 3):")
  try:
    dim = int(input())
  except (ValueError, KeyboardInterrupt):
    print("The dimension is not correct.\nExiting.")
    sys.exit(0)
  if dim not in [2, 3]:
    print("The dimension is not correct.\nExiting.")
    sys.exit(0)
  return dim


def get_bodies(filename: str) -> body_system:
  print("Random ('r') or predefined systems ('s') for the initial states of the bodies:")
  try:
    p = input()
  except (ValueError, KeyboardInterrupt):
    print("The data entered is not correct.\nExiting.")
    sys.exit(0)
  if p not in ['r', 's']:
    print("The data entered is not correct.\nExiting.")
    sys.exit(0)
  dim = get_dim()
  if p == 'r':
    print("Number of bodies:")
    try:
      n = int(input())
    except (ValueError, KeyboardInterrupt):
      print("The number of bodies does not make sense.\nExiting.")
      sys.exit(0)
    if n <= 1:
      print("The number of bodies does not make sense.\nExiting.")
      sys.exit(0)
    mass = np.random.uniform(1, 10, size=n)  # vector of masses
    r0 = np.zeros((n, 2 * dim))

    # Names
    names = np.array(["body " + str(i + 1) for i in range(n)])

    # initial conditions
    max_pos = 1
    max_vel = 0.1 * max_pos
    r0[:, 0:dim] = np.random.uniform(-max_pos,
                                     max_pos, size=(n, dim))  # positions
    r0[:, dim:] = np.random.uniform(-max_vel,
                                    max_vel, size=(n, dim))  # velocities
    system = body_system("Random System", dim, n, names, mass, r0)
  else:
    df = pd.read_csv(filename, sep=' ', header=0)

    syst_names = pd.value_counts(df[df.columns[0]]).index
    syst_names = syst_names.sort_values()
    num_sys = len(syst_names)

    print("Which system do you want to see?")
    for i, system in enumerate(syst_names):
      print(str(i) + ") " + system)
    try:
      k = int(input())
    except (ValueError, KeyboardInterrupt):
      print("The data entered is not correct.\nExiting.")
      sys.exit(0)
    if k not in range(num_sys):
      print("The data entered is not correct.\nExiting.")
      sys.exit(0)
    data = df.loc[df["system_name"] == syst_names[k]]
    n = len(data)

    bodies_names = np.array(data["body_name"])
    mass = np.array(data["mass"])
    r0 = np.zeros((n, 2 * dim))

    if dim == 3:
      r0[:, 0:] = np.array(data[["x", "y", "z", "vx", "vy", "vz"]])
    if dim == 2:
      r0[:, 0:] = np.array(data[["x", "y", "vx", "vy"]])

    system = body_system(syst_names[k], dim, n, bodies_names, mass, r0)
  return system
