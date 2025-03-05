import matplotlib.pyplot as plt
import numpy as np

from constants import *

def dc_resistance(voltage, current):
    """
    Calculates DC resistance using the formula R = V / I
    Asks for user inputs for voltage and current values.
    Displays the calculated resistance.
    """
    if current == 0:
        return "Error: Current cannot be zero."
    
    resistance = voltage / current
    return f"Resistance: {resistance:.2f} Ω"

import numpy as np
import matplotlib.pyplot as plt

def current_voltage(y_values):
    """
    Generates a current-voltage plot based on given inputs and computes the average of y_values.
    
    Parameters:
    - sweep (str): What is being swept ('voltage' or 'current').
    - start (float): Starting value of the sweep.
    - end (float): Ending value of the sweep.
    - increment (float): Increment value for the sweep.
    - y_values (np.array): Array of measured values corresponding to the sweep values.
    
    Returns:
    - float: Average of y_values.
    """
    return np.mean(y_values)  # Compute and return the average of y_values


def capacitance_voltage_2p():
    """
    Calculates capacitance for a 2-probe system and generates a capacitance-voltage plot.
    Prompts the user for AC voltage values and corresponding current values.
    """
    start_voltage = float(input("Enter the starting AC voltage value (V): "))
    end_voltage = float(input("Enter the ending AC voltage value (V): "))
    increment_voltage = float(input("Enter the increment AC voltage value (V): "))

    if increment_voltage <= 0:
        print("Increment value must be greater than zero.")
        return

    if end_voltage < start_voltage:
        print("Ending value has to be bigger than the starting value.")
        return

    voltage_values = [start_voltage + i * increment_voltage for i in range(int((end_voltage - start_voltage) / increment_voltage) + 1)]
    current_values = []

    for voltage in voltage_values:
        current = float(input(f"Enter the current value corresponding to {voltage} V: "))
        current_values.append(current)

    capacitances = [v / i if i != 0 else float('inf') for v, i in zip(voltage_values, current_values)]

    plt.plot(voltage_values, capacitances, marker='o')
    plt.xlabel("Voltage (V)")
    plt.ylabel("Capacitance (F)")
    plt.title("Capacitance-Voltage Plot (2-probe)")
    plt.grid(True)
    plt.show()

def impedance_spectroscopy_2p():
    """
    Calculates impedance for a 2-probe system and generates an impedance-frequency plot.
    Prompts the user for peak voltages, frequency range, and current parameters.
    """
    max_voltage = float(input("Enter the maximum peak voltage (V): "))
    min_voltage = float(input("Enter the minimum peak voltage (V): "))
    amplitude = (max_voltage - min_voltage) / 2

    start_frequency = float(input("Enter the starting frequency (Hz): "))
    end_frequency = float(input("Enter the ending frequency (Hz): "))
    increment_frequency = float(input("Enter the increment frequency (Hz): "))

    if increment_frequency <= 0:
        print("Increment value must be greater than zero.")
        return

    if end_frequency < start_frequency:
        print("Ending value has to be bigger than the starting value.")
        return

    frequencies = np.arange(start_frequency, end_frequency + increment_frequency, increment_frequency)
    angular_frequencies = 2 * np.pi * frequencies

    current_amplitudes = []
    current_phases = []

    for freq in frequencies:
        current_amplitude = float(input(f"Enter the amplitude of current at {freq} Hz: "))
        current_phase = float(input(f"Enter the phase of current at {freq} Hz (in degrees): "))
        current_amplitudes.append(current_amplitude)
        current_phases.append(np.radians(current_phase))

    impedance_values = [amplitude / (current_amplitudes[i] * np.cos(current_phases[i])) for i in range(len(frequencies))]

    plt.plot(frequencies, impedance_values, marker='o')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Impedance (Ohms)")
    plt.title("Impedance Spectroscopy (2-probe)")
    plt.grid(True)
    plt.show()

def transfer_characteristics():
    """
    Generates a transfer characteristics plot (IDS vs VGS) for a 3-probe system.
    Prompts the user for DC voltage range and current values.
    """
    start_voltage = float(input("Enter the starting DC voltage value (VGS): "))
    end_voltage = float(input("Enter the ending DC voltage value (VGS): "))
    increment_voltage = float(input("Enter the increment DC voltage value (VGS): "))

    if increment_voltage <= 0:
        print("Increment value must be greater than zero.")
        return

    if end_voltage < start_voltage:
        print("Ending value has to be bigger than the starting value.")
        return

    voltage_values = [start_voltage + i * increment_voltage for i in range(int((end_voltage - start_voltage) / increment_voltage) + 1)]
    current_values = []

    for voltage in voltage_values:
        current = float(input(f"Enter the current IDS value corresponding to {voltage} V: "))
        current_values.append(current)

    plt.plot(voltage_values, current_values, marker='o')
    plt.xlabel("Gate-Source Voltage VGS (V)")
    plt.ylabel("Gate-Source Voltage IGS (A)")
    plt.title("Transfer Characteristics (VGS vs IGS)")
    plt.grid(True)
    plt.show()

def output_characteristics():
    """
    Generates an output characteristics plot (IDS vs VDS) for a 3-probe system.
    Prompts the user for DC voltage range and current values.
    """
    start_voltage = float(input("Enter the starting DC voltage value (VDS): "))
    end_voltage = float(input("Enter the ending DC voltage value (VDS): "))
    increment_voltage = float(input("Enter the increment DC voltage value (VDS): "))

    if increment_voltage <= 0:
        print("Increment value must be greater than zero.")
        return

    if end_voltage < start_voltage:
        print("Ending value has to be bigger than the starting value.")
        return

    voltage_values = [start_voltage + i * increment_voltage for i in range(int((end_voltage - start_voltage) / increment_voltage) + 1)]
    current_values = []

    for voltage in voltage_values:
        current = float(input(f"Enter the current IDS value corresponding to {voltage} V: "))
        current_values.append(current)

    plt.plot(voltage_values, current_values, marker='o')
    plt.xlabel("Drain-Source Voltage VDS (V)")
    plt.ylabel("Drain-Source Current IDS (A)")
    plt.title("Output Characteristics (VDS vs IDS)")
    plt.grid(True)
    plt.show()

def capacitance_voltage_3p():
    """
    Calculates capacitance for a 3-probe system and generates a capacitance-voltage plot.
    Prompts the user for AC voltage values and corresponding current values.
    """
    start_voltage = float(input("Enter the starting AC voltage value (V): "))
    end_voltage = float(input("Enter the ending AC voltage value (V): "))
    increment_voltage = float(input("Enter the increment AC voltage value (V): "))

    if increment_voltage <= 0:
        print("Increment value must be greater than zero.")
        return

    if end_voltage < start_voltage:
        print("Ending value has to be bigger than the starting value.")
        return

    voltage_values = [start_voltage + i * increment_voltage for i in range(int((end_voltage - start_voltage) / increment_voltage) + 1)]
    current_values = []

    for voltage in voltage_values:
        current = float(input(f"Enter the current value corresponding to {voltage} V: "))
        current_values.append(current)

    capacitances = [v / i if i != 0 else float('inf') for v, i in zip(voltage_values, current_values)]

    plt.plot(voltage_values, capacitances, marker='o')
    plt.xlabel("Voltage (V)")
    plt.ylabel("Capacitance (F")
    plt.title("Capacitance-Voltage Plot (3-probe)")
    plt.grid(True)
    plt.show()

def electrochemical():
    """
    Calculates impedance for a 3-probe system and generates an impedance-frequency plot.
    Prompts the user for peak voltages, frequency range, and current parameters.
    """
    max_voltage = float(input("Enter the maximum peak voltage (V): "))
    min_voltage = float(input("Enter the minimum peak voltage (V): "))
    amplitude = (max_voltage - min_voltage) / 2

    start_frequency = float(input("Enter the starting frequency (Hz): "))
    end_frequency = float(input("Enter the ending frequency (Hz): "))
    increment_frequency = float(input("Enter the increment frequency (Hz): "))

    if increment_frequency <= 0:
        print("Increment value must be greater than zero.")
        return

    if end_frequency < start_frequency:
        print("Ending value has to be bigger than the starting value.")
        return

    frequencies = np.arange(start_frequency, end_frequency + increment_frequency, increment_frequency)
    angular_frequencies = 2 * np.pi * frequencies

    current_amplitudes = []
    current_phases = []

    for freq in frequencies:
        current_amplitude = float(input(f"Enter the amplitude of current at {freq} Hz: "))
        current_phase = float(input(f"Enter the phase of current at {freq} Hz (in degrees): "))
        current_amplitudes.append(current_amplitude)
        current_phases.append(np.radians(current_phase))

    impedance_values = [amplitude / (current_amplitudes[i] * np.cos(current_phases[i])) for i in range(len(frequencies))]

    plt.plot(frequencies, impedance_values, marker='o')
    plt.xlabel("Frequency (Hz")
    plt.ylabel("Impedance (Ohms")
    plt.title("Electrochemical Measurement")
    plt.grid(True)
    plt.show()

def probe_resistance():
    """
    Calculates Probe resistance using the formula R = V / I
    Asks for user inputs for voltage and current values.
    Displays the calculated resistance.
    """
    voltage = float(input("Enter the voltage value (V): "))
    current = float(input("Enter the current value (A): "))

    if current == 0:
        print("Current cannot be zero to calculate resistance.")
        return

    resistance = voltage / current
    print(f"The calculated resistance is {resistance:.2f} ohms.")

def low_resistance():
    """
    Calculates Low resistance using the formula R = V / I
    Asks for user inputs for voltage and current values.
    Displays the calculated resistance.
    """
    voltage = float(input("Enter the voltage value (V): "))
    current = float(input("Enter the current value (A): "))

    if current == 0:
        print("Current cannot be zero to calculate resistance.")
        return

    resistance = voltage / current
    print(f"The calculated resistance is {resistance:.2f} ohms.")

def impedance_spectroscopy_4p():
    """
    Calculates impedance for a 4-probe system and generates an impedance-frequency plot.
    Prompts the user for peak voltages, frequency range, and current parameters.
    """
    max_voltage = float(input("Enter the maximum peak voltage (V): "))
    min_voltage = float(input("Enter the minimum peak voltage (V): "))
    amplitude = (max_voltage - min_voltage) / 2

    start_frequency = float(input("Enter the starting frequency (Hz): "))
    end_frequency = float(input("Enter the ending frequency (Hz): "))
    increment_frequency = float(input("Enter the increment frequency (Hz): "))

    if increment_frequency <= 0:
        print("Increment value must be greater than zero.")
        return

    if end_frequency < start_frequency:
        print("Ending value has to be bigger than the starting value.")
        return

    frequencies = np.arange(start_frequency, end_frequency + increment_frequency, increment_frequency)
    angular_frequencies = 2 * np.pi * frequencies

    current_amplitudes = []
    current_phases = []

    for freq in frequencies:
        current_amplitude = float(input(f"Enter the amplitude of current at {freq} Hz: "))
        current_phase = float(input(f"Enter the phase of current at {freq} Hz (in degrees): "))
        current_amplitudes.append(current_amplitude)
        current_phases.append(np.radians(current_phase))

    impedance_values = [amplitude / (current_amplitudes[i] * np.cos(current_phases[i])) for i in range(len(frequencies))]

    plt.plot(frequencies, impedance_values, marker='o')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Impedance (Ohms)")
    plt.title("Impedance Spectroscopy (4-probe)")
    plt.grid(True)
    plt.show()

def adc_sample_to_voltage(data):
    """
    Converts ADC samples to voltage values.
    Asks for the ADC sample value and displays the corresponding voltage value.
    """
    return data * GUI_VREF / (2 ** GUI_ADC_RESOLUTION - 1) 