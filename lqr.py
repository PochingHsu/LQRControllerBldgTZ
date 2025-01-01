import numpy as np
from scipy.integrate import solve_ivp


# Solve Riccati Differential Equation
def riccati_ode(t, P_flat, A, B, Q, R):
    P = P_flat.reshape((2, 2))  # Reshape flat P into 2x2 matrix
    dPdt = -(A.T @ P + P @ A - P @ B @ np.linalg.inv(R) @ B.T @ P + Q)  # Riccati differential equation
    return dPdt.flatten()  # Return as a flat array


def solve_riccati(A, B, Q, R, T):
    # solve the Riccati equation backward in time.
    P_final = Q.flatten()
    sol = solve_ivp(
        lambda t, P: riccati_ode(t, P, A, B, Q, R),
        [T, 0],
        P_final,
        method='RK45',
    )
    return sol.t[::-1], sol.y[:, ::-1]  # reverse time for forward use
