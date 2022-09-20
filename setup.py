import numpy as np
import pandas as pd
from bodies import body_system
import sys


def get_dim():
  print("Dimension (2 or 3):")
  try:
    dim = int(input())
  except KeyboardInterrupt:
    sys.exit(0)
  if dim not in [2, 3]:
    print("The dimension is not correct.\nExiting.")
    sys.exit(0)
  return dim


def get_bodies(file_name="data.csv"):
  print("Random ('r') or predefined systems ('s') for the initial states of the bodies:")
  try:
    p = input()
  except KeyboardInterrupt:
    sys.exit(0)
  if p not in ['r', 'c', 's']:
    print("The data entered is not correct.\nExiting.")
    sys.exit(0)
  dim = get_dim()
  if p == 'r':
    print("Number of bodies:")
    try:
      n = int(input())
    except KeyboardInterrupt:
      sys.exit(0)
    if n <= 1:
      print("The number of bodies is does not make sense.\nExiting.")
      sys.exit(0)
    mass = np.random.uniform(1, 10, size=n)  # vector of masses
    r0 = np.zeros(2 * dim * n)

    # Names
    names = np.array(["Body " + str(i + 1) for i in range(n)])

    # initial conditions
    r0[::2] = np.random.uniform(-1, 1, size=n * dim)  # positions
    r0[1::2] = np.random.uniform(-0.1, 0.1, size=n * dim)  # velocities

    system = body_system("Random System", dim, n, names, mass, r0)
  else:
    df = pd.read_csv(file_name, sep=' ', header=0)

    syst = pd.value_counts(df[df.columns[0]])
    num_sys = len(syst)

    print("Which system do you want to see?")
    for i, system in enumerate(syst.index):
      print(str(i) + ") " + system)
    try:
      k = int(input())
    except KeyboardInterrupt:
      sys.exit(0)
    if k not in range(num_sys):
      print("The data entered is not correct.\nExiting.")
      sys.exit(0)
    data = df.loc[df[df.columns[0]] == syst.index[k]]
   # print(data)
    n = len(data)
    bodies_names = np.array(data["body_name"])
    mass = np.array(data["mass"])
    r0 = np.zeros(2 * dim * n)
    for j in range(2 * dim):
      r0[j::2 * dim] = data[data.columns[j + 3]]

    system = body_system(syst.index[k], dim, n, bodies_names, mass, r0)
  return system
