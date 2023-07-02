import sys
from bodies import body_system
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.animation as animation
import os

mpl.rcParams['animation.ffmpeg_path'] = "/usr/bin/ffmpeg"


def save_plot(system: body_system, anim: animation.FuncAnimation,
              FPS: int, interval: float, filename: str = "../data/data.csv") -> None:
  print("Do you want to save the data in the .csv file or save the animation?")
  print("Save the data: 'd'\nSave the animation: 'a'\nSave both: 'b'\nDon't save anything: 'n'")
  try:
    c = input()
  except KeyboardInterrupt:
    sys.exit(0)
  if c not in ['d', 'a', 'b', 'n']:
    print("The data entered is not correct.\nExiting.")
    sys.exit(0)

  if c == 'n':
    return  # same as return None

  print("Name the system:")
  try:
    name = input()
  except KeyboardInterrupt:
    sys.exit(0)

  # write the data
  if c == 'd' or c == 'b':
    df0 = pd.read_csv(filename, sep=' ', header=0)

    while name in np.array(df0[df0.columns[0]]):
      print(
          "Name '" +
          name +
          "' already used in the database. Would you like to overwrite it? (y/n, default: y)")
      try:
        c = input()
      except KeyboardInterrupt:
        sys.exit(0)
      if c not in ['y', 'n', '']:
        print("The data entered is not correct.\nExiting.")
        sys.exit(0)
      if c == 'y' or c == '':
        df0 = df0[df0.system_name != name]
        df0.to_csv(filename, index=False, sep=' ')
        break
      print("Name the system:")
      try:
        name = input()
      except KeyboardInterrupt:
        sys.exit(0)

    # add data to the end of the .csv file
    df = pd.DataFrame(
        columns=[
            "system_name",
            "body_name",
            "mass",
            "x",
            "y",
            "z",
            "vx",
            "vy",
            "vz"],
        index=np.arange(system.n_bodies))
    df.loc[:, "system_name"] = np.repeat(name, repeats=system.n_bodies)
    bodies_names = np.array([i.replace(" ", "_") for i in system.bodies_names])
    df.loc[:, "body_name"] = bodies_names
    df.loc[:, "mass"] = system.mass
    print(system.r0)
    print(system.mass)
    # r0 = n_bodies x (2 * dim)
    if system.dim == 3:
      df.iloc[:, 3:] = system.r0
    else:
      df.iloc[:, 3:5] = system.r0[:, 0:2]
      df.iloc[:, [5, 8]] = np.zeros((system.n_bodies, 2))
      df.iloc[:, 6:8] = system.r0[:, 2:4]
    df.to_csv(filename, mode='a', index=False, header=False, sep=' ')
  #   # create the .mp4 file
  if c == 'a' or c == 'b':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # choose save in .mp4 or .gif
    filename_out = script_dir + "/../animation/" + name
    # print("Save in .mp4 or .gif? (m/g)")
    # try:
    #   c = input()
    # except KeyboardInterrupt:
    #   sys.exit(0)
    # if c not in ['m', 'g']:
    #   print("The data entered is not correct.\nExiting.")
    #   sys.exit(0)
    # if c == 'm':
    filename_out += ".mp4"
    writervideo = animation.FFMpegWriter(
        fps=FPS, metadata={
            'artist': "Víctor Ballester"}, bitrate=-1)
    anim.save(filename_out, writer=writervideo)
    # else:
    #   filename_out += ".gif"
    #   anim.save(filename_out, writer='pillow', fps=FPS, dpi=100)
