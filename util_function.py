import matplotlib.pyplot as plt


def plot(time, x_history, d_history, u_history):
    time = time + 6  # start at 6:00 am
    # room temp.
    plt.figure(figsize=(12, 6))
    plt.subplot(3, 1, 1)
    plt.plot(time, x_history[:, 0], label="Room Temp.")
    plt.plot(time, x_history[:, 1], label="Thermal Mass Temp.")
    plt.xlabel("Time (hours)")
    plt.ylabel("Temperature (C)")
    plt.ylim([15, 25])
    # plt.xlim([2, 3])
    plt.legend()
    plt.grid()
    # outdoor temp.
    plt.subplot(3, 1, 2)
    plt.plot(time, d_history, label="Outdoor Temp.")
    plt.xlabel("Time (hours)")
    plt.ylabel("Temperature (C)")
    plt.legend()
    plt.grid()
    # plt.xlim([2, 3])
    # control input
    plt.subplot(3, 1, 3)
    plt.plot(time, u_history, label="Control Input")
    plt.xlabel("Time (hours)")
    plt.ylabel("Control Input")
    plt.legend()
    plt.grid()
    # plt.xlim([2, 3])
    plt.tight_layout()
    plt.show()