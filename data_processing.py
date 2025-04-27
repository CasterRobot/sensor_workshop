import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def reconstruct_circle(distances, angles):
    """
    Reconstruct the diameter of the cube and the circle of the inner surface.

    Parameters:
    distances (list): Distances from the sensor to the surface of the cube.
    angles (list): Angles of the rotator in degrees.

    Returns:
    tuple: diameter of the cube, circle points (x, y)
    """
    # Convert angles from degrees to radians
    angles_rad = np.radians(angles)

    # Calculate the coordinates of points on the inner surface of the cube
    x_points = []
    y_points = []

    for distance, angle in zip(distances, angles_rad):
        # Calculate the x and y coordinates
        x = distance * np.cos(angle)
        y = distance * np.sin(angle)
        x_points.append(x)
        y_points.append(y)

    # Calculate the diameter of the cube
    # The diameter is twice the maximum distance from the center to the edge
    max_distance = max(distances)
    diameter = 2 * max_distance

    return diameter, x_points, y_points

def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

if __name__ == "__main__":

    # Sample Rate and Frequency
    fs = 500.0  # Sample rate, Hz
    cutoff = 50.0  # Desired cutoff frequency of the filter, Hz

    # Create a sample signal: 1 Hz and 100 Hz sine waves
    t = np.arange(0, 1.0, 1.0/fs)
    a = 0.5
    f1 = 1.0  # Frequency of the first signal
    f2 = 100.0  # Frequency of the second signal
    data = a * np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)

    # Apply low-pass filter
    filtered_data = lowpass_filter(data, cutoff, fs, order=6)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, data, label='Noisy Signal')
    plt.title('Noisy Signal')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(t, filtered_data, label='Filtered Signal', color='orange')
    plt.title('Filtered Signal (Low-pass)')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()