import numpy as np
import pandas as pd
from bodies import body_system
import sys
from parameters import *


def get_dim() -> int:
    print("Dimension of the system (2 or 3, default: " + str(DEFAULT_dim) + ")")
    while True:
        try:
            dim = input()
        except KeyboardInterrupt:
            sys.exit(0)
        if dim == '':
            dim = DEFAULT_dim
        else:
            try:
                dim = int(dim)
            except ValueError:
                print("The dimension is not correct. Enter it again.")
                continue
        if dim not in [2, 3]:
            print("The dimension is not correct. Enter it again.")
        else:
            break
    return dim


def get_bodies(filename: str) -> body_system:
    print("Random or Predefined systems for the initial states of the bodies: (r/p, default: " + DEFAULT_system_type + ")")
    while True:
        try:
            p = input()
        except KeyboardInterrupt:
            sys.exit(0)
        if p == '':
            p = DEFAULT_system_type
        if p not in ['r', 'p', '']:
            print("Data entered is not correct. Enter it again.")
        else:
            break

    def get_years(default_years: float) -> float:
        print("Number of years to simulate: (default: " + str(default_years) + ")")
        while True:
            try:
                years = input()
            except KeyboardInterrupt:
                sys.exit(0)
            if years == '':
                years = default_years
            else:
                try:
                    years = float(years)
                except ValueError:
                    print("The number of years is not correct. Enter it again.")
                    continue
            if years <= 0:
                print("The number of years does not make sense. Enter it again.")
            else:
                break
        return years

    dim = get_dim()
    if p == 'r':
        print("Number of bodies: (default: " + str(DEFAULT_num_bodies) + ")")
        while True:
            try:
                n = input()
            except KeyboardInterrupt:
                sys.exit(0)
            if n == '':
                n = DEFAULT_num_bodies
            else:
                try:
                    n = int(n)
                except ValueError:
                    print("The number of bodies is not correct. Enter it again.")
                    continue
            if n <= 1:
                print("The number of bodies does not make sense. Enter it again.")
            else:
                break

        years = get_years(DEFAULT_years)
        days = int(365 * years)  # number of days to simulate (real days)

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
        system = body_system(
            "Random System",
            dim,
            days,
            n,
            names,
            mass,
            r0)
    else:
        df = pd.read_csv(filename, sep=' ', header=0)

        syst_names = pd.value_counts(df[df.columns[0]]).index
        syst_names = syst_names.sort_values()
        num_sys = len(syst_names)

        print("Which system do you want to see? (default: 0)")
        for i, system in enumerate(syst_names):
            print(str(i) + ") " + system)
        while True:
            try:
                k = input()
            except KeyboardInterrupt:
                sys.exit(0)
            if k == '':
                k = 0
            else:
                try:
                    k = int(k)
                except ValueError:
                    print("Data entered is not correct. Enter it again.")
                    continue
            if k not in range(num_sys):
                print("Data entered is not correct. Enter it again.")
            else:
                break
        data = df.loc[df["system_name"] == syst_names[k]]
        n = len(data)

        bodies_names = np.array(data["body_name"])
        mass = np.array(data["mass"])
        r0 = np.zeros((n, 2 * dim))

        if dim == 3:
            r0[:, 0:] = np.array(data[["x", "y", "z", "vx", "vy", "vz"]])
        if dim == 2:
            r0[:, 0:] = np.array(data[["x", "y", "vx", "vy"]])

        # if "solar_system_2d_rocky" in syst_names[k]:
        #     speed_up = DEFAULT_speed_up_solar_syst_rock
        #     days = DEFAULT_days_solar_syst_rock
        # elif "solar_system_2d" in syst_names[k]:
        #     speed_up = DEFAULT_speed_up_solar_syst
        #     days = DEFAULT_days_solar_syst
        # else:
        #     speed_up = DEFAULT_speedup
        #     days = DEFAULT_days

        def get_default_days(system_name: str) -> int:
            if "solar_system_2d_rocky" in system_name:
                return DEFAULT_years_solar_syst_rock
            elif "solar_system_2d" in system_name:
                return DEFAULT_years_solar_syst
            else:
                return DEFAULT_years

        years = get_years(get_default_days(syst_names[k]))
        days = int(365 * years)

        system = body_system(
            syst_names[k],
            dim,
            days,
            n,
            bodies_names,
            mass,
            r0)
    return system
