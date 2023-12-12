import matplotlib.animation as animation
import time
import pandas as pd
import numpy as np
from bodies import body_system
from parameters import *
import sys
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['animation.ffmpeg_path'] = "/usr/bin/ffmpeg"


def save_plot(system: body_system, anim: animation.FuncAnimation,
              FPS: int, filename_data: str) -> None:
    print("Do you want to save the data in the .csv file or save the animation? (d/a/b/n, default: " + DEFAULT_save + ")")
    print("Save the data: 'd'\nSave the animation: 'a'\nSave both: 'b'\nDon't save anything: 'n'")
    while True:
        try:
            c = input()
        except KeyboardInterrupt:
            sys.exit(0)
        if c == '':
            c = DEFAULT_save
        if c not in ['d', 'a', 'b', 'n']:
            print("Data entered is not correct. Enter it again.")
        else:
            break

    if c == 'n':
        return  # same as return None

    def set_name() -> str:
        print("Name the system: (default: system_currentTime)")
        try:
            name = input()
        except KeyboardInterrupt:
            sys.exit(0)
        if name in ['']:
            name = "system_" + \
                time.strftime("%Y%m%d%H%M%S", time.localtime())
        return name

    name = set_name()
    # check if the name is already used
    script_dir = os.path.dirname(os.path.abspath(__file__))
    df0 = pd.read_csv(filename_data, sep=' ', header=0)
    while ((c == 'd' or c == 'b') and (name in np.array(df0[df0.columns[0]]))) or ((c == 'a' or c == 'b') and (os.path.isfile(script_dir + "/../animations/" + name + ".mp4") or os.path.isfile(script_dir + "/../animations/" + name + ".gif"))):
        print(
            "Name '" +
            name +
            "' already used in the database. Would you like to overwrite it? (y/n, default: " + DEFAULT_overwrite + ")")
        try:
            cc = input()
        except KeyboardInterrupt:
            sys.exit(0)
        if cc == '':
            cc = DEFAULT_overwrite
        if cc not in ['y', 'n']:
            print("Data entered is not correct. Enter it again.")
        elif cc == 'n':
            name = set_name()
        else:
            # remove the data from the .csv file
            df0 = df0[df0.system_name != name]
            df0.to_csv(filename_data, index=False, sep=' ')
            break
        set_name()

    # write the data
    if c == 'd' or c == 'b':
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
        bodies_names = np.array([i.replace(" ", "_")
                                for i in system.bodies_names])
        df.loc[:, "body_name"] = bodies_names
        df.loc[:, "mass"] = system.mass
        # r0 = n_bodies x (2 * dim)
        if system.dim == 3:
            df.iloc[:, 3:] = system.r0
        else:
            df.iloc[:, 3:5] = system.r0[:, 0:2]
            df.iloc[:, [5, 8]] = np.zeros((system.n_bodies, 2))
            df.iloc[:, 6:8] = system.r0[:, 2:4]
        df.to_csv(filename_data, mode='a', index=False, header=False, sep=' ')

        print("Data saved in " + filename_data)

    # create the .mp4 file
    if c == 'a' or c == 'b':
        filename_anim = script_dir + "/../animations/" + name
        print("Save in .mp4 or .gif? (m/g, default: " + DEFAULT_video_format + ")")
        while True:
            try:
                ccc = input()
            except KeyboardInterrupt:
                sys.exit(0)
            if ccc == '':
                ccc = DEFAULT_video_format
            if ccc not in ['m', 'g']:
                print("Data entered is not correct. Enter it again.")
            else:
                break
        print("Be patient, it may take a while.")
        plt.close()
        if ccc == 'g':
            filename_anim += ".gif"
            writervideo = animation.PillowWriter(fps=FPS)
            anim.save(filename_anim, writer=writervideo)
            print("Animation saved in " + filename_anim)
        else:
            filename_anim += ".mp4"
            writervideo = animation.FFMpegWriter(
                fps=FPS, metadata={'artist': 'Víctor Ballester'})
            anim.save(filename_anim, writer=writervideo)
            print("Animation saved in " + filename_anim)
        # else:
        #   filename_out += ".gif"
        #   anim.save(filename_out, writer='pillow', fps=FPS, dpi=100)

        # print("Quality of the video (500-5000, default: 1000):")
        # while True:
        #   try:
        #     bitrate = input()
        #   except KeyboardInterrupt:
        #     sys.exit(0)
        #   if bitrate == '':
        #     bitrate = 1000
        #   else:
        #     try:
        #       bitrate = int(bitrate)
        #     except ValueError:
        #       print("Data entered is not correct.\nExiting.")
        #       continue
        #   if bitrate < 500 or bitrate > 5000:
        #     print("Data entered is not correct.\nExiting.")
        #     continue
        #   break
