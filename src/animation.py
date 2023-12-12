# 2d N-body problem
from save_plot import save_plot
from bodies import body_system
from parameters import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import sys
from typing import cast
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3D


def anim2d(system: body_system, step_size: float,
           trace_bool: bool, com_bool: bool, FRAMES: int, FPS: int) -> animation.FuncAnimation:
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
    ax.set_aspect('equal', adjustable='box')

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
    else:
        com = ax.plot([], [])[0]  # dummy plot to avoid error
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
        real_frame = frame * system.speed_up
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
        fig, animate, frames=FRAMES // system.speed_up, interval=1000/FPS, blit=True)

    return anim


def anim3d(system: body_system, step_size: float, trace_bool: bool, com_bool: bool, FRAMES: int, FPS: int) -> animation.FuncAnimation:
    fig = plt.figure(figsize=(15, 10))

    time_template = 'time = %.2f years'
    lim = 2
    if "solar_system" in system.name and system.n_bodies >= 9:
        lim = 35
    ax = fig.add_subplot(projection='3d')
    ax = cast(Axes3D, ax)
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
    ax.set_aspect('equal', adjustable='box')

    # Remove the grid
    ax.grid(False)

    # change background color surface axis to a more
    # Get rid of the panes
    # ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.zaxis.set_pane_color((1.0, 1.0, 1.0), alpha=alpha)

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
    planets = cast(list[Line3D], planets)
    traces = [
        ax.plot(
            [],
            [],
            [],
            '-',
            lw=0.5,
            color=system.colors[i])[0]
        for i in range(system.n_bodies)]  # alpha = transparency
    traces = cast(list[Line3D], traces)

    if com_bool:
        com = ax.plot([], [], [], 'x',
                      label="Center of masses", color='red')[0]
        com = cast(Line3D, com)
    else:
        com = ax.plot([], [], [])[0]
        com = cast(Line3D, com)
    time_text = ax.text2D(
        0.05,
        0.95,
        '',
        transform=ax.transAxes,
        fontsize=SIZE_big)

    def animate(frame):
        real_frame = frame * system.speed_up
        x_data = system.r[: (real_frame + 1), :, 0]
        y_data = system.r[: (real_frame + 1), :, 1]
        z_data = system.r[: (real_frame + 1), :, 2]
        com_data = system.com[:(real_frame + 1)]

        ax.view_init(elev=30, azim=-60 + frame / 10)
        time_text.set_text(time_template % (real_frame * step_size * t0_years))
        for j in range(system.n_bodies):
            planets[j].set_data(x_data[real_frame, j],
                                y_data[real_frame, j])
            # if I use set_data_3d, I have an error
            planets[j].set_3d_properties(z_data[real_frame, j])
            if trace_bool:
                traces[j].set_data_3d(x_data[:, j], y_data[:, j], z_data[:, j])
        if com_bool:
            com.set_data_3d(com_data[:, 0], com_data[:, 1], com_data[:, 2])
            return planets + traces + [com] + [time_text] + [ax]
        return planets + traces + [time_text] + [ax]

    anim = animation.FuncAnimation(
        fig, animate, frames=FRAMES // system.speed_up, interval=1000/FPS, blit=True)

    return anim


def get_anim(system: body_system, filename: str) -> None:
    print("Print traces of the bodies: (y/n, default: " + DEFAULT_trace + ")")
    while True:
        try:
            trace = input()
        except KeyboardInterrupt:
            sys.exit(0)
        if trace == '':
            trace = DEFAULT_trace
        if trace not in ['y', 'n']:
            print("Data entered is not correct. Enter it again.")
        elif trace == 'y':
            trace = True
            break
        else:
            trace = False
            break

    print("Print the center of masses: (y/n, default: " + DEFAULT_com + ")")
    while True:
        try:
            com = input()
        except KeyboardInterrupt:
            sys.exit(0)
        if com == '':
            com = DEFAULT_com
        if com not in ['y', 'n']:
            print("Data entered is not correct. Enter it again.")
        elif com == 'y':
            com = True
            break
        else:
            com = False
            break

    def get_default_speed_up(system: body_system) -> int:
        if "solar_system_2d_rocky" in system.name:
            return DEFAULT_speed_up_solar_syst_rock
        elif "solar_system_2d" in system.name:
            return DEFAULT_speed_up_solar_syst
        else:
            return DEFAULT_speedup

    print("Factor to speed up the animation: (default: " +
          str(get_default_speed_up(system)) + ")")
    while True:
        try:
            speed_up = input()
        except KeyboardInterrupt:
            sys.exit(0)
        if speed_up == '':
            speed_up = get_default_speed_up(system)
        else:
            try:
                speed_up = int(speed_up)
            except ValueError:
                print("The factor is not correct. Enter it again.")
                continue
        if speed_up <= 0:
            print("The factor does not make sense. Enter it again.")
        else:
            break
    system.speed_up = speed_up
    # Set-up
    # mpl.rcParams['text.usetex'] = True
    plt.style.use('dark_background')

    FRAMES = len(system.r)
    FPS = 50

    if system.dim == 2:
        anim = anim2d(system, system.step_size, trace, com,
                      FRAMES, FPS)
    else:
        anim = anim3d(system, system.step_size, trace, com,
                      FRAMES, FPS)

    plt.show(block=False)
    save_plot(system, anim, FPS, filename)
