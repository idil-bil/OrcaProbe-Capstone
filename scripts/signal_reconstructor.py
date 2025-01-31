import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

# Sample data (replace with your actual data)
Fs = 16e6  # Sampling frequency (16 MHz)

# Define parameters
V_REF = 1.0  # Reference voltage in volts
RESOLUTION = 12  # ADC resolution in bits
FULL_SCALE = 2**(RESOLUTION - 1)  # Full-scale value for 12-bit signed integer

# Sample data (16-bit format, 12 data bits between bits 13 and 2)
data = np.array([6412, 6412, 7020, 7288, 7944, 7988, 8204, 8480, 8224, 8136, 7720, 7416, 7112, 6652, 6448, 6336, 6244, 6500, 6948, 7484, 7544, 8000, 8204, 8384, 8256, 8068, 7760, 7404, 7024, 6680, 6396, 6340, 6428, 6436, 6900, 7156, 7592, 8012, 8264, 8300, 8248, 8088, 7256, 7108, 6488, 6440, 6268, 6400, 0, 6632, 6824, 7408, 7584, 8160, 8168, 8288, 8152, 7904, 7760, 7104, 6992, 460, 6820, 6260, 6584, 6480, 6672, 7128, 7500, 7868, 8412, 8276, 8148, 7872, 7548, 7196, 6912, 6232, 6464, 6628, 6376, 6468, 6820, 7036, 7688, 7824, 8140, 8344, 8320, 7908, 7548, 7420, 6888, 6260, 6844, 6388, 6344, 6472, 6708, 7092, 7360, 7844, 8272, 8244, 8256, 8176, 7956, 7856, 7220, 6860, 6764, 6352, 6340, 6348, 6660, 7012, 7384, 7364, 8096, 8116, 8152, 8264, 7700, 7004, 6896, 6584, 5852, 8, 6480, 6712, 7156, 7260, 7424, 0, 8136, 8136, 7940, 8268, 8284, 7684, 7532, 6880, 6972, 6380, 6320, 6196, 6608, 6568, 7468, 7864, 7900, 8236, 7708, 7960, 7952, 7200, 6836, 7036, 6508, 6368, 6384, 6652, 6912, 7116, 7040, 7684, 7936, 8284, 8344, 8328, 8024, 7808, 7248, 7048, 6700, 6148, 6352, 6404, 6548, 6804, 7444, 7588, 7944, 7908, 8304, 8288, 8120, 7800, 7344, 6580, 6848, 6708, 6148, 6352, 6164, 6892, 7316, 7524, 8032, 8272, 8272, 8292, 8132, 7960, 7396, 7180, 6676, 6512, 6568, 6332, 6452, 6872, 7112, 7716, 7852, 8120, 8292, 8152, 8004, 7612, 6784, 6900, 6552, 6380, 6244, 6588, 6716, 7168, 7172, 7384, 7824, 8072, 8248, 8296, 8192, 7952, 7608, 7232, 6864, 6564, 6352, 6340, 6256, 6584, 7072, 7320, 7744, 7676, 7996, 8304, 7940, 7840, 7288, 6872, 6896, 6540, 6420, 5904, 6416, 6732, 7108, 7340, 8004, 8052, 8388, 8372, 8408, 8008, 7692, 7556, 6976, 6680, 6424, 6344, 6392, 6588, 7120, 7292, 7596, 8056, 8444, 8288, 8240, 8108, 7764, 7532, 6980, 6576, 6432, 6292, 6424, 6656, 6824, 7496, 7640, 7844, 8228, 8156, 1888, 7784, 7276, 7068, 6396, 6652, 6680, 6644, 6392, 6516, 6852, 6912, 7636, 7732, 8268, 8368, 8372, 8108, 7812, 7420, 7168, 6584, 6448, 6016, 6440, 6496, 6948, 7224, 7568, 7912, 8228, 8296, 8136, 7868, 7680, 7164, 8180, 6876, 6368, 6344, 5984, 6448, 6720, 7208, 7512, 7956, 8128, 8276, 7968, 8196, 8132, 7552, 7200, 6900, 6508, 6232, 6384, 6656, 6780, 7072, 7496, 7812, 8292, 8256, 8304, 8164, 7952, 7640, 7044, 7120, 6544, 6412, 6352, 6432, 6688, 7040, 7464, 7744, 8076, 8264, 8392, 8332, 7964, 7632, 7364, 7032, 6568, 6372, 6340, 6500, 6644, 7040, 7536, 7748, 8308, 8484, 8288, 8236, 8008, 7688, 7484, 6992, 6524, 6404, 6384, 6388, 6688, 7112, 7340, 7520, 8020, 8188, 8532, 7724, 7248, 6452, 6968, 6484, 0, 6808, 6104, 6084, 6708, 6880, 7364, 7656, 7976, 8188, 8252, 7784, 7804, 7616, 7032, 6656, 6728, 6504, 6320, 6004, 6580, 6464, 7160, 7596, 8064, 8164, 8264, 8544, 8100, 8004, 7460, 6996, 6928, 6468, 6388, 6356, 6176, 6848, 7324, 7544, 7928, 8184, 8496, 8080, 7812, 7568, 7040, 6656, 6132, 6564, 5992, 6404, 6528, 6784, 7124, 7492, 8124, 7936, 8112, 8140, 7888, 7552, 7176, 0, 6864, 6540, 6484, 6360, 6296, 6724, 7088, 7492, 7444, 8068, 8300, 8296, 8160, 7808, 7572, 7268, 6988, 6552, 6180, 6400],dtype=np.uint16)  # Replace with your actual samples

# Extract 12 bits from the relevant positions (shift right by 2)
data = data >> 2

# Convert from unsigned to signed 12-bit two's complement

# Scale to voltage
# data = (data - 2048) / (4095 - 2048) * V_REF
data = data/(2**12)

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
