# 2d N-body problem

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from bodies import body_system
from save_plot import save_plot

t0 = 91.8387490005065  # years. t0 = sqrt((1au)^3/(G*M_earth))


def anim2d(system: body_system, dt, t, c):
  fig = plt.figure(figsize=(10, 10))
#  fig.title(str(system.n) + "-body system", fontsize=14)

  time_template = 'time = %.2f years'
  lim = 3
  ax = fig.add_subplot()
  ax.axis('equal')
  ax.set(xlim=(-lim, lim), ylim=(-lim, lim))
  ax.set(xlabel='x', ylabel='y')
  balls = [
      ax.plot([], [], 'o', lw=2, ms=system.vol[i], color=system.colors[i], label=system.bodies_names[i] + ": " + str(round(system.mass[i], 2)) + " M_earth")[0] for i in range(system.n)]
  traces = [
      ax.plot([], [], '-', lw=0.5, color=system.colors[i])[0] for i in range(system.n)]
  com = ax.plot([], [], 'x', label="Center of masses", color='red')[0]
  time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes)
  # lw = linewidth
  # ms = markersize
  ax.legend(
      loc="center left",
      bbox_to_anchor=(
          1,
          0.5),
      ncol=1)

  fig.subplots_adjust(right=0.75)
  fig.tight_layout()

  FRAMES = len(system.r)
  interval = dt * 1000

  def animate(frame):
    x_data, y_data = system.r[:(frame + 1), ::2 *
                              system.dim], system.r[:(frame + 1), 2::2 * system.dim]
    com_data = system.com[:(frame + 1)]

    for j in range(system.n):
      balls[j].set_data(x_data[frame, j], y_data[frame, j])
      if t == 'y':
        traces[j].set_data(x_data[:, j], y_data[:, j])
    if c == 'y':
      com.set_data(com_data[:, 0], com_data[:, 1])

    time_text.set_text(time_template % (frame * dt * t0))
    return balls + traces + [com, time_text]

  anim = animation.FuncAnimation(
      fig, animate, frames=FRAMES, interval=interval, blit=True)

  return anim


def anim3d(system: body_system, dt, t, c):
  fig = plt.figure(figsize=(10, 10))
#  fig.title(str(system.n) + "-body system", fontsize=14)

  time_template = 'time = %.2f years'
  lim = 2
  ax = fig.add_subplot(projection='3d')
  ax.set(xlim=(-lim, lim), ylim=(-lim, lim), zlim=(-lim, lim))
  ax.set(xlabel=r'$x$', ylabel=r'$y$', zlabel=r'$z$')
  balls = [ax.plot([], [], [], 'o', lw=2, ms=system.vol[i], color=system.colors[i], label=system.bodies_names[i])[0]
           for i in range(system.n)]
  traces = [ax.plot([], [], [], '-', lw=0.5, color=system.colors[i])[0]
            for i in range(system.n)]
  com = ax.plot([], [], [], 'x', label="Center of masses", color='red')[0]
  time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)

  # ax.legend(
  #     bbox_to_anchor=(
  #         0,
  #         1,
  #         1,
  #         0),
  #     loc="lower left",
  #     mode="expand",
  #     ncol=system.n + 1)

  FRAMES = len(system.r)
  interval = dt * 1000

  def animate(frame):
    x_data, y_data, z_data = system.r[:(frame + 1), ::2 * system.dim], system.r[:(
        frame + 1), 2::2 * system.dim], system.r[:(frame + 1), 4::2 * system.dim]
    com_data = system.com[:(frame + 1)]

    ax.view_init(elev=30, azim=-60 + frame / 10)
    # ax.pause(.001)
    for j in range(system.n):
      balls[j].set_data_3d(
          x_data[frame, j], y_data[frame, j], z_data[frame, j])
      if t == 'y':
        traces[j].set_data_3d(x_data[:, j], y_data[:, j], z_data[:, j])
    if c == 'y':
      com.set_data_3d(com_data[:, 0], com_data[:, 1], com_data[:, 2])

    time_text.set_text(time_template % (frame * dt * t0))
    return balls + traces + [com, time_text, ax]

  anim = animation.FuncAnimation(
      fig, animate, frames=FRAMES, interval=interval, blit=True)

  return anim


def get_anim(system: body_system, dt):

  print("Print traces of the bodies (y/n):")
  try:
    t = input()
  except KeyboardInterrupt:
    sys.exit(0)
  if t not in ['y', 'n']:
    print("The data entered is not correct.\nExiting.")
    sys.exit(0)

  print("Print the center of masses (y/n):")
  try:
    c = input()
  except KeyboardInterrupt:
    sys.exit(0)
  if c not in ['y', 'n']:
    print("The data entered is not correct.\nExiting.")
    sys.exit(0)

  system.colors = np.random.uniform(0.25, 1, size=(system.n, 3))

  # Set-up
  # mpl.rcParams['text.usetex'] = True
  plt.style.use('dark_background')

  if system.dim == 2:
    anim = anim2d(system, dt, t, c)
  else:
    anim = anim3d(system, dt, t, c)

  plt.show()
  # anim.save("prov.mp4")
  save_plot(system, anim, 60, 1)
