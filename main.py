import numpy as np
from lqr import solve_riccati
from system import system_matrices, disturbance
from scipy.interpolate import interp1d
from util_function import plot
# LQR cost matrices (need tuning)
Q = np.array([[0.1, 0],
              [0, 0]])
R = np.array([[0.02]])
"""
Simulate the HVAC system with time-varying LQR control.
"""
T = 12  # simulation time in hours
dt = 0.01  # time step
# Time vector
time = np.arange(0, T, dt)
# Initial conditions
x = np.array([[10], [10]])  # initial room and thermal mass temperatures
x_history = []
d_history = []
u_history = []
T_control = 0.5
set = 22  # thermostat setting temperature
tswing = 1  # temperature dead-band
# target temperature range
min_temperature = set-tswing
max_temperature = set+tswing
A, B, G = system_matrices()
for t in time:
    d = np.array([[disturbance(t)]])
    # thermal-off when T_room > T_room_max
    if (x > max_temperature).any():
        u = np.array([[0]])
        dx = A @ x + B @ u + G @ d
    # thermal-on when T_room < T_room_max (apply LQR control)
    elif (x < min_temperature).any():
        # solve Riccati equation to get the P matrix
        riccati_time, P_sol = solve_riccati(A, B, Q, R, T_control)
        # interpolate P_sol for simulation time
        P_interp = interp1d(riccati_time, P_sol, axis=1, fill_value="extrapolate")
        P = P_interp(t).reshape((2, 2))
        # compute LQR gain
        K = np.linalg.inv(R) @ B.T @ P
        # control law
        u = -K @ (x - set) - K @ G @ d
        u = np.clip(u, 10, 300)  # max and min constraint of control input (10 [W] <= u <= 300 [W])
        dx = A @ (x - set) + B @ u + G @ d
    # thermal-off when in the dead-band: T_room_min <= T_room <= T_room_max
    else:
        u = np.array([[0]])
        dx = A @ x + B @ u + G @ d
    # update state
    x = x + dx * dt
    # log data
    x_history.append(x.flatten())
    d_history.append(d.flatten())
    u_history.append(u.flatten())

# convert lists to numpy arrays for plotting
x_history = np.array(x_history)
d_history = np.array(d_history)
u_history = np.array(u_history)
# Plot Results
plot(time, x_history, d_history, u_history)
