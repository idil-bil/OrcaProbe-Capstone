# Classes for each register and their bitfields
from constants import *

class DVC_Status:
    def __init__(self):
        self.powerGood = (0xDEAD, DVC_STATUS_POWER_GOOD_POSITION, DVC_STATUS_POWER_GOOD_LENGTH)  # Bitfield position and length
        self.usbConnected = (0xDEAD, DVC_STATUS_USB_CONNECTED_POSITION, DVC_STATUS_USB_CONNECTED_LENGTH)  # Bitfield position and length

class DVC_MeasurementConfig:
    def __init__(self):
        self.startMeasure = (0xDEAD, DVC_MEASUREMENT_CONFIG_START_MEASURE_POSITION, DVC_MEASUREMENT_CONFIG_START_MEASURE_LENGTH)  # Bitfield position and length
        self.stopMeasure = (0xDEAD, DVC_MEASUREMENT_CONFIG_STOP_MEASURE_POSITION, DVC_MEASUREMENT_CONFIG_STOP_MEASURE_LENGTH)  # Bitfield position and length
        self.measureInterval = (0xDEAD, DVC_MEASUREMENT_CONFIG_MEASURE_INTERVAL_POSITION, DVC_MEASUREMENT_CONFIG_MEASURE_INTERVAL_LENGTH)  # Bitfield position and length

class DVC_ProbeConfig:
    def __init__(self):
        self.usedProbes = (0xDEAD, DVC_PROBE_CONFIG_USED_PROBES_POSITION, DVC_PROBE_CONFIG_USED_PROBES_LENGTH)  # Bitfield position and length
        self.probe1Config = (0xDEAD, DVC_PROBE_CONFIG_PROBE_1_CONFIG_POSITION, DVC_PROBE_CONFIG_PROBE_1_CONFIG_LENGTH)  # Bitfield position and length
        self.probe2Config = (0xDEAD, DVC_PROBE_CONFIG_PROBE_2_CONFIG_POSITION, DVC_PROBE_CONFIG_PROBE_2_CONFIG_LENGTH)  # Bitfield position and length
        self.probe3Config = (0xDEAD, DVC_PROBE_CONFIG_PROBE_3_CONFIG_POSITION, DVC_PROBE_CONFIG_PROBE_3_CONFIG_LENGTH)  # Bitfield position and length
        self.probe4Config = (0xDEAD, DVC_PROBE_CONFIG_PROBE_4_CONFIG_POSITION, DVC_PROBE_CONFIG_PROBE_4_CONFIG_LENGTH)  # Bitfield position and length

class DVC_SampleData:
    def __init__(self):
        self.sample1 = (0xDEAD, DVC_SAMPLE_DATA_SAMPLE_1_POSITION, DVC_SAMPLE_DATA_SAMPLE_1_LENGTH)  # Bitfield position and length
        self.sample2 = (0xDEAD, DVC_SAMPLE_DATA_SAMPLE_2_POSITION, DVC_SAMPLE_DATA_SAMPLE_2_LENGTH)  # Bitfield position and length

class DVC_RegisterMap:
    def __init__(self):
        self.STATUS = DVC_Status()
        self.MEASUREMENT_CONFIG = DVC_MeasurementConfig()
        self.PROBE_CONFIG = DVC_ProbeConfig()
        self.SAMPLE_DATA = DVC_SampleData()

testClass = DVC_RegisterMap
import pdb; pdb.set_trace()