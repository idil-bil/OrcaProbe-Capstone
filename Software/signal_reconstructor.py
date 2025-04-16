import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

# Define parameters
V_REF = 1.0  # Reference voltage in volts
RESOLUTION = 12  # ADC resolution in bits
FULL_SCALE = 2**(RESOLUTION - 1)  # Full-scale value for 12-bit signed integer
SAMPLE_FREQ = 5e6  

def sine_wave(t, amplitude, frequency, phase, offset):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase) + offset


def reconstruct_signal(data):
    # Sample data (replace with your actual data)
    Fs = SAMPLE_FREQ

    # Step 1: Perform FFT to estimate frequency
    n = len(data)  # Length of data
    f = fftfreq(n, 1/Fs)  # Frequency axis
    Y = fft(data)  # FFT of the signal

    # Get the magnitude of the FFT
    magnitude = np.abs(Y)

    # Find the peak frequency
    peakIdx = np.argmax(magnitude[1:]) + 1  # Ignore DC component
    peakFrequency = f[peakIdx]

    print(f"Estimated Frequency (via FFT): {peakFrequency} Hz")

    # Step 2: Remove noise using MAD filtering
    threshold = 3  # Threshold for outlier detection using MAD
    mad_value = np.median(np.abs(data - np.median(data)))  # Compute the MAD (Median Absolute Deviation)
    median_value = np.median(data)  # Compute the median value

    # Filter out the outliers based on MAD
    filtered_data = data[np.abs(data - median_value) <= threshold * mad_value]

    # Ensure the filtered data is the same length as the original data
    filtered_time_intervals = np.arange(len(filtered_data)) / Fs

    # Step 3: Interpolate the data to reconstruct the signal
    # Create a time vector (assuming the samples are equally spaced)
    time_intervals = np.arange(len(data)) / Fs  # Adjust if your time intervals are non-uniform

    # Perform spline interpolation to reconstruct the continuous signal
    interp_func = interp1d(time_intervals, data, kind='cubic', fill_value="extrapolate")
    interpolated_signal = interp_func(time_intervals)

    # Initial guess for parameters: [amplitude, frequency, phase, offset]
    initial_guess = [np.max(filtered_data) - np.min(filtered_data), peakFrequency, 0, np.median(filtered_data)]

    # Perform nonlinear curve fitting to find the best sine wave parameters
    params, _ = curve_fit(sine_wave, filtered_time_intervals, filtered_data, p0=initial_guess)

    # Extract the fitted parameters
    fitted_amplitude, fitted_frequency, fitted_phase, fitted_offset = params

    # Ensure positive amplitude by adjusting phase
    if fitted_amplitude < 0:
        fitted_amplitude = -fitted_amplitude
        fitted_phase += np.pi

    print("signal reconstruction done")

    # # Display the results
    # print(f"Fitted Amplitude: {fitted_amplitude}")
    # print(f"Fitted Frequency: {fitted_frequency} Hz")
    # print(f"Fitted Phase: {fitted_phase}")
    # print(f"Fitted Offset: {fitted_offset}")

    # # Step 5: Plot the results separately

    # # Create a new figure with three subplots
    # plt.figure(figsize=(10, 8))

    # # Plot the initial reconstructed data with outliers (raw data)
    # plt.subplot(3, 1, 1)  # First plot
    # plt.plot(time_intervals, data, 'k-', label='Initial Data with Outliers')
    # plt.title('Initial Reconstructed Data (With Outliers)')
    # plt.xlabel('Time (seconds)')
    # plt.ylabel('Amplitude')
    # plt.legend()

    # # Plot filtered data (after MAD filtering)
    # plt.subplot(3, 1, 2)  # Second plot
    # plt.plot(filtered_time_intervals, filtered_data, 'b-', label='Filtered Data')
    # plt.title('Filtered Data (After MAD Filtering)')
    # plt.xlabel('Time (seconds)')
    # plt.ylabel('Amplitude')
    # plt.legend()

    # # Plot fitted sine wave (from the filtered data)
    # plt.subplot(3, 1, 3)  # Third plot
    # plt.plot(time_intervals, sine_wave(time_intervals, *params), 'r--', label='Fitted Sine Wave')
    # plt.title('Fitted Sine Wave')
    # plt.xlabel('Time (seconds)')
    # plt.ylabel('Amplitude')
    # plt.legend()

    # # Show the plots
    # plt.tight_layout()
    # plt.show()

    return time_intervals, sine_wave(time_intervals, *params), fitted_amplitude, fitted_frequency, fitted_phase, fitted_offset
