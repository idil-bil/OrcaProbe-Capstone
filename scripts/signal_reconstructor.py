import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

# Sample data (replace with your actual data)
Fs = 5e6  # Sampling frequency (16 MHz)

# Define parameters
V_REF = 1.0  # Reference voltage in volts
RESOLUTION = 12  # ADC resolution in bits
FULL_SCALE = 2**(RESOLUTION - 1)  # Full-scale value for 12-bit signed integer

# Sample data (16-bit format, 12 data bits between bits 13 and 2)
# data = np.array([5064, 5064, 4768, 4940, 5072, 5204, 5152, 5080, 5152, 5208, 5240, 5056, 5120, 5160, 5268, 4992, 5232, 5128, 5084, 5244, 5288, 5048, 5064, 5168, 5116, 5192, 4972, 5100, 5232, 5148, 5164, 5188, 4968, 5248, 5140, 4552, 5040, 5100, 5120, 5192, 5104, 5228, 5096, 5008, 5096, 5036, 5280, 5024, 4932, 5172, 5168, 5220, 5020, 5056, 5240, 5128, 5052, 5032, 5112, 5076, 5024, 5152, 4988, 5172, 4956, 5124, 5012, 5072, 5120, 5156, 4936, 5116, 5300, 4952, 5108, 5080, 5256, 5064, 5008, 5016, 5260, 5132, 4988, 5108, 5252, 5112, 5156, 5108, 21516, 5176, 5024, 5160, 5240, 4988, 5232, 5616, 5000, 5208, 5056, 5092])
data = np.array([6976,6668,6740,6860,6764,6904,6596,6780,7016,6644,6696,6880,6736,6820,6692,6716,7052,6672,6768,6972,6752,6828,6720,6728,6976,6656,6684,6924,6752,6792,6704,6712,6988,6612,6676,6920,6732,6828,6688,6704,6940,6612,6692,6956,6688,6744,6748,6704,6892,6576,6708,6960,6720,6720,6720,6752,6880,6584,6516,6752,6688,6828,6652,6520,6812,6480,6608,6812,6668,6728,6532,6640,6952,6632,6648,6680,6684,6868,6556,6608,6848,6652,6760,6604,6648,6908,6596,6676,6740,6628,6876,6524,6604,6868,6716,6764,6604,6648,6888,6552,6648,6764,6664,6772,6544,6608,6916,6624,6644,6652,6708,6836,6548,6608,6892,6660,6728,6568,6692,6888])
# Scale to voltage
data = data/(2**14)*5

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

# Step 4: Fit a sine wave to the reconstructed signal
# Sine wave fitting function
def sine_wave(t, amplitude, frequency, phase, offset):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase) + offset

# Initial guess for parameters: [amplitude, frequency, phase, offset]
initial_guess = [np.max(filtered_data) - np.min(filtered_data), peakFrequency, 0, np.median(filtered_data)]

# Perform nonlinear curve fitting to find the best sine wave parameters
params, _ = curve_fit(sine_wave, filtered_time_intervals, filtered_data, p0=initial_guess)

# Extract the fitted parameters
amplitude, fitted_frequency, phase, offset = params

# Display the results
print(f"Fitted Amplitude: {amplitude}")
print(f"Fitted Frequency: {fitted_frequency} Hz")
print(f"Fitted Phase: {phase}")
print(f"Fitted Offset: {offset}")
print(f"Resistance: {offset/0.048}")

# Step 5: Plot the results separately

# Create a new figure with three subplots
plt.figure(figsize=(10, 8))

# Plot the initial reconstructed data with outliers (raw data)
plt.subplot(3, 1, 1)  # First plot
plt.plot(time_intervals, data, 'k-', label='Initial Data with Outliers')
plt.title('Initial Reconstructed Data (With Outliers)')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()

# Plot filtered data (after MAD filtering)
plt.subplot(3, 1, 2)  # Second plot
plt.plot(filtered_time_intervals, filtered_data, 'b-', label='Filtered Data')
plt.title('Filtered Data (After MAD Filtering)')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()

# Plot fitted sine wave (from the filtered data)
plt.subplot(3, 1, 3)  # Third plot
plt.plot(time_intervals, sine_wave(time_intervals, *params), 'r--', label='Fitted Sine Wave')
plt.title('Fitted Sine Wave')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()

# Show the plots
plt.tight_layout()
plt.show()
