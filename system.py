import numpy as np
# room properties
rho_air = 1.29  # [kg/m^3] air density
SP_air = 1005  # [J/(kg·K)] specific heat of air
V_room = 10  # [m^3] volume of room
Cr = rho_air*SP_air*V_room  # [J/K]
R_ra = 1/(65.8*20)  # [m^2K/W] resistance of room to ambient
Cm = 50  # [J/K]
R_rm = 1/(65.8*2)  # [m^2K/W] resistance of room to bldg. thermal mass


def system_matrices():
    # System matrices A(t), B(t), G(t)
    # A = np.array([[-1, 0.05], [0.02, -1]])
    A = np.array([[-(1/(Cr*R_rm)+1/(Cr*R_ra)), 1/(Cr*R_rm)],
                  [1/(Cm*R_rm), -1/(Cm*R_rm)]])
    B = np.array([[1], [0.0]])
    # G = np.array([[0.01], [0.0]])
    G = np.array([[1/(Cr*R_ra)], [0.0]])
    return A, B, G


def disturbance(t):
    # outdoor temperature
    return 5 + 2 * np.sin(2 * np.pi * t / 24)  # sinusoidal temperature variation
