# 2d N-body problem
from save_plot import save_plot
from bodies import body_system
from parameters import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import sys
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Use the 'TkAgg' backend


def anim2d(system: body_system, step_size: float,
           trace_bool: bool, com_bool: bool, FRAMES: int, interval: float, speed_up: int) -> animation.FuncAnimation:
  fig = plt.figure(figsize=(15, 10))

  time_template = 'time = %.2f years'
  lim = 3
  if "solar_system" in system.name and system.n_bodies >= 9:
    lim = 50
  ax = fig.add_subplot()
  ax.set_xlim(-lim, lim)
  ax.set_ylim(-lim, lim)
  ax.axis('equal')
  # changes the size of the ticks
  ax.tick_params(axis='both', which='major', labelsize=10)

  ax.set_xlabel('x (AU)', fontsize=SIZE_small)
  ax.set_ylabel('y (AU)', fontsize=SIZE_small)

  if "solar_system" in system.name:
    ax.set_title(
        "Solar system",
        fontsize=SIZE_title,
        fontweight='bold')
  else:
    ax.set_title(
        str(
            system.n_bodies) +
        "-body system",
        fontsize=SIZE_title,
        fontweight='bold')

  planets = [
      ax.plot([], [], 'o', lw=2, ms=system.vol[i], color=system.colors[i], label=system.bodies_names[i] + ": " + str(round(system.mass[i], 2)) + " M_earth")[0] for i in range(system.n_bodies)]
  traces = [
      ax.plot([], [], '-', lw=0.5, color=system.colors[i])[0] for i in range(system.n_bodies)]
  if com_bool:
    com = ax.plot([], [], 'x', label="Center of masses", color='red')[0]
  time_text = ax.text(
      0.05,
      0.95,
      '',
      transform=ax.transAxes,
      fontsize=SIZE_big)
  # lw = linewidth
  # ms = markersize
  ax.legend(
      loc="center left",
      bbox_to_anchor=(
          1,
          0.5),
      ncol=1,
      fontsize=SIZE_small)

  # fig.subplots_adjust(right=0.75)
  fig.tight_layout()

  def animate(frame):
    real_frame = frame * speed_up
    x_data = system.r[: (real_frame + 1), :, 0]
    y_data = system.r[: (real_frame + 1), :, 1]
    com_data = system.com[:(real_frame + 1)]

    time_text.set_text(time_template % (real_frame * step_size * t0_years))

    for j in range(system.n_bodies):
      planets[j].set_data(x_data[real_frame, j], y_data[real_frame, j])
      if trace_bool:
        traces[j].set_data(x_data[:, j], y_data[:, j])
    if com_bool:
      com.set_data(com_data[:, 0], com_data[:, 1])
      return planets + traces + [com, time_text]

    return planets + traces + [time_text]

  anim = animation.FuncAnimation(
      fig, animate, frames=FRAMES // speed_up, interval=interval, blit=True)

  return anim


def anim3d(system: body_system, step_size: float,
           trace_bool: bool, com_bool: bool, FRAMES: int, interval: float, speed_up: int) -> animation.FuncAnimation:
  fig = plt.figure(figsize=(15, 10))

  time_template = 'time = %.2f years'
  lim = 2
  if "solar_system" in system.name and system.n_bodies >= 9:
    lim = 50
  ax = fig.add_subplot(projection='3d')
  # ax.set(xlim=(-lim, lim), ylim=(-lim, lim), zlim=(-lim, lim))
  ax.axis('equal')
  ax.set_xlim(-lim, lim)
  ax.set_ylim(-lim, lim)
  ax.set_zlim(-lim, lim)
  # changes the size of the ticks
  ax.tick_params(axis='both', which='major', labelsize=10)
  ax.set_xlabel('x', fontsize=SIZE_small)
  ax.set_ylabel('y', fontsize=SIZE_small)
  ax.set_zlabel('z', fontsize=SIZE_small)

  # Remove the grid
  ax.grid(False)

  # change background color surface axis
  ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.05))
  ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.05))
  ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.05))

  fig.tight_layout()

  if "solar_system" in system.name:
    ax.set_title(
        "Solar system",
        fontsize=SIZE_title,
        fontweight='bold')
  else:
    ax.set_title(
        str(
            system.n_bodies) +
        "-body system",
        fontsize=SIZE_title,
        fontweight='bold')

  planets = [
      ax.plot(
          [],
          [],
          [],
          'o',
          lw=2,
          ms=system.vol[i],
          color=system.colors[i],
          label=system.bodies_names[i] +
          ": " +
          str(round(system.mass[i], 2)) + " M_earth")[0]
      for i in range(system.n_bodies)]
  traces = [
      ax.plot(
          [],
          [],
          [],
          '-',
          lw=0.5,
          color=system.colors[i])[0]
      for i in range(system.n_bodies)]  # alpha = transparency
  if com_bool:
    com = ax.plot([], [], [], 'x', label="Center of masses", color='red')[0]
  time_text = ax.text2D(
      0.05,
      0.95,
      '',
      transform=ax.transAxes,
      fontsize=SIZE_big)

  # add a legend
  # ax_legend = fig.add_subplot(111)
  # ax_legend.legend(*ax.get_legend_handles_labels(), loc='center')
  # fig.tight_layout()

  def animate(frame):
    real_frame = frame * speed_up
    x_data = system.r[: (real_frame + 1), :, 0]
    y_data = system.r[: (real_frame + 1), :, 1]
    z_data = system.r[: (real_frame + 1), :, 2]
    com_data = system.com[:(real_frame + 1)]

    ax.view_init(elev=30, azim=-60 + frame / 10)
    time_text.set_text(time_template % (real_frame * step_size * t0_years))
    for j in range(system.n_bodies):
      planets[j].set_data(x_data[real_frame, j], y_data[real_frame, j])
      planets[j].set_3d_properties(z_data[real_frame, j])
      if trace_bool:
        traces[j].set_data(x_data[:, j], y_data[:, j])
        traces[j].set_3d_properties(z_data[:, j])
    if com_bool:
      com.set_data(com_data[:, 0], com_data[:, 1])
      com.set_3d_properties(com_data[:, 2])
      return planets + traces + [com] + [time_text] + [ax]
    return planets + traces + [time_text] + [ax]

  anim = animation.FuncAnimation(
      fig, animate, frames=FRAMES // speed_up, interval=interval, blit=True)

  return anim


def get_anim(system: body_system, step_size: float,
             speed_up: int, filename: str) -> None:
  print("Print traces of the bodies: (y/n, default: y) ")
  try:
    trace = input()
  except KeyboardInterrupt:
    sys.exit(0)
  if trace not in ['y', 'n', '']:
    print("The data entered is not correct.\nExiting.")
    sys.exit(0)
  elif trace == 'y' or trace == '':
    trace = True
  else:
    trace = False

  print("Print the center of masses: (y/n, default: n) ")
  try:
    com = input()
  except KeyboardInterrupt:
    sys.exit(0)
  if com not in ['y', 'n', '']:
    print("The data entered is not correct.\nExiting.")
    sys.exit(0)
  elif com == 'y':
    com = True
  else:
    com = False

  # Set-up
  # mpl.rcParams['text.usetex'] = True
  plt.style.use('dark_background')

  FRAMES = len(system.r)
  if system.dim == 2:
    interval = 10
  else:
    interval = 10

  if system.dim == 2:
    anim = anim2d(system, step_size, trace, com, FRAMES, interval, speed_up)
  else:
    anim = anim3d(system, step_size, trace, com, FRAMES, interval, speed_up)

  plt.show()
  FPS = 60
  save_plot(system, anim, FPS, interval, filename)
