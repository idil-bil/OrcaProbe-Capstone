# Register Addresses
DVC_STATUS = 0x0  # Address in decimal: 0
DVC_MEASUREMENT_CONFIG = 0x1  # Address in decimal: 1
DVC_PROBE_CONFIG = 0x2  # Address in decimal: 2
DVC_SAMPLE_DATA = 0x64  # Address in decimal: 100

# Bitfields
# DVC_STATUS
DVC_STATUS_Power_Good_POSITION = 0
DVC_STATUS_Power_Good_LENGTH = 1
DVC_STATUS_USB_Connected_POSITION = 1
DVC_STATUS_USB_Connected_LENGTH = 1
DVC_STATUS_Selected_Probes_POSITION = 2
DVC_STATUS_Selected_Probes_LENGTH = 4

# DVC_MEASUREMENT_CONFIG
DVC_MEASUREMENT_CONFIG_Start_Measure_POSITION = 0
DVC_MEASUREMENT_CONFIG_Start_Measure_LENGTH = 1
DVC_MEASUREMENT_CONFIG_Stop_Measure_POSITION = 1
DVC_MEASUREMENT_CONFIG_Stop_Measure_LENGTH = 1
DVC_MEASUREMENT_CONFIG_Measure_In_Progress_POSITION = 2
DVC_MEASUREMENT_CONFIG_Measure_In_Progress_LENGTH = 1
DVC_MEASUREMENT_CONFIG_Valid_Measure_Config_POSITION = 3
DVC_MEASUREMENT_CONFIG_Valid_Measure_Config_LENGTH = 1
DVC_MEASUREMENT_CONFIG_Measure_Probe_Config_POSITION = 4
DVC_MEASUREMENT_CONFIG_Measure_Probe_Config_LENGTH = 2
DVC_MEASUREMENT_CONFIG_Measure_Type_Config_POSITION = 6
DVC_MEASUREMENT_CONFIG_Measure_Type_Config_LENGTH = 4

# DVC_PROBE_CONFIG
DVC_PROBE_CONFIG_Used_Probes_POSITION = 0
DVC_PROBE_CONFIG_Used_Probes_LENGTH = 4
DVC_PROBE_CONFIG_Probe_1_Config_POSITION = 4
DVC_PROBE_CONFIG_Probe_1_Config_LENGTH = 5
DVC_PROBE_CONFIG_Probe_2_Config_POSITION = 9
DVC_PROBE_CONFIG_Probe_2_Config_LENGTH = 5
DVC_PROBE_CONFIG_Probe_3_Config_POSITION = 14
DVC_PROBE_CONFIG_Probe_3_Config_LENGTH = 5
DVC_PROBE_CONFIG_Probe_4_Config_POSITION = 19
DVC_PROBE_CONFIG_Probe_4_Config_LENGTH = 5

# DVC_SAMPLE_DATA
DVC_SAMPLE_DATA_Sample_1_POSITION = 0
DVC_SAMPLE_DATA_Sample_1_LENGTH = 12
DVC_SAMPLE_DATA_Sample_2_POSITION = 12
DVC_SAMPLE_DATA_Sample_2_LENGTH = 12

# Register Classes
class DVC_DVC_STATUS:
    def __init__(self):
        self.Power_Good = (0xDEAD,DVC_STATUS_Power_Good_POSITION, DVC_STATUS_Power_Good_LENGTH)
        self.USB_Connected = (0xDEAD,DVC_STATUS_USB_Connected_POSITION, DVC_STATUS_USB_Connected_LENGTH)
        self.Selected_Probes = (0xDEAD,DVC_STATUS_Selected_Probes_POSITION, DVC_STATUS_Selected_Probes_LENGTH)

class DVC_DVC_MEASUREMENT_CONFIG:
    def __init__(self):
        self.Start_Measure = (0xDEAD,DVC_MEASUREMENT_CONFIG_Start_Measure_POSITION, DVC_MEASUREMENT_CONFIG_Start_Measure_LENGTH)
        self.Stop_Measure = (0xDEAD,DVC_MEASUREMENT_CONFIG_Stop_Measure_POSITION, DVC_MEASUREMENT_CONFIG_Stop_Measure_LENGTH)
        self.Measure_In_Progress = (0xDEAD,DVC_MEASUREMENT_CONFIG_Measure_In_Progress_POSITION, DVC_MEASUREMENT_CONFIG_Measure_In_Progress_LENGTH)
        self.Valid_Measure_Config = (0xDEAD,DVC_MEASUREMENT_CONFIG_Valid_Measure_Config_POSITION, DVC_MEASUREMENT_CONFIG_Valid_Measure_Config_LENGTH)
        self.Measure_Probe_Config = (0xDEAD,DVC_MEASUREMENT_CONFIG_Measure_Probe_Config_POSITION, DVC_MEASUREMENT_CONFIG_Measure_Probe_Config_LENGTH)
        self.Measure_Type_Config = (0xDEAD,DVC_MEASUREMENT_CONFIG_Measure_Type_Config_POSITION, DVC_MEASUREMENT_CONFIG_Measure_Type_Config_LENGTH)

class DVC_DVC_PROBE_CONFIG:
    def __init__(self):
        self.Used_Probes = (0xDEAD,DVC_PROBE_CONFIG_Used_Probes_POSITION, DVC_PROBE_CONFIG_Used_Probes_LENGTH)
        self.Probe_1_Config = (0xDEAD,DVC_PROBE_CONFIG_Probe_1_Config_POSITION, DVC_PROBE_CONFIG_Probe_1_Config_LENGTH)
        self.Probe_2_Config = (0xDEAD,DVC_PROBE_CONFIG_Probe_2_Config_POSITION, DVC_PROBE_CONFIG_Probe_2_Config_LENGTH)
        self.Probe_3_Config = (0xDEAD,DVC_PROBE_CONFIG_Probe_3_Config_POSITION, DVC_PROBE_CONFIG_Probe_3_Config_LENGTH)
        self.Probe_4_Config = (0xDEAD,DVC_PROBE_CONFIG_Probe_4_Config_POSITION, DVC_PROBE_CONFIG_Probe_4_Config_LENGTH)

class DVC_DVC_SAMPLE_DATA:
    def __init__(self):
        self.Sample_1 = (0xDEAD,DVC_SAMPLE_DATA_Sample_1_POSITION, DVC_SAMPLE_DATA_Sample_1_LENGTH)
        self.Sample_2 = (0xDEAD,DVC_SAMPLE_DATA_Sample_2_POSITION, DVC_SAMPLE_DATA_Sample_2_LENGTH)

class DVC_RegisterMap:
    def __init__(self):
        self.DVC_STATUS = DVC_DVC_STATUS()
        self.DVC_MEASUREMENT_CONFIG = DVC_DVC_MEASUREMENT_CONFIG()
        self.DVC_PROBE_CONFIG = DVC_DVC_PROBE_CONFIG()
        self.DVC_SAMPLE_DATA = DVC_DVC_SAMPLE_DATA()
