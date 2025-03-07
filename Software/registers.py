# Register Addresses
DVC_STATUS = 0x0  # Address in decimal: 0
DVC_MEASUREMENT_CONFIG = 0x1  # Address in decimal: 1
DVC_PROBE_CONFIG = 0x2  # Address in decimal: 2
DVC_2PM_DCRESISTANCE_1 = 0x3  # Address in decimal: 3
DVC_2PM_CURRVOLT_1 = 0x4  # Address in decimal: 4
DVC_2PM_CURRVOLT_2 = 0x5  # Address in decimal: 5
DVC_2PM_CURRVOLT_3 = 0x6  # Address in decimal: 6
DVC_2PM_CURRVOLT_4 = 0x7  # Address in decimal: 7
DVC_2PM_CAPVOLT_1 = 0x8  # Address in decimal: 8
DVC_2PM_CAPVOLT_2 = 0x9  # Address in decimal: 9
DVC_2PM_CAPVOLT_3 = 0xA  # Address in decimal: 10
DVC_2PM_IMPSPEC_1 = 0xB  # Address in decimal: 11
DVC_2PM_IMPSPEC_2 = 0xC  # Address in decimal: 12
DVC_2PM_IMPSPEC_3 = 0xD  # Address in decimal: 13
DVC_2PM_IMPSPEC_4 = 0xE  # Address in decimal: 14
DVC_2PM_IMPSPEC_5 = 0xF  # Address in decimal: 15
DVC_3PM_TRANSCHAR_1 = 0x10  # Address in decimal: 16
DVC_3PM_TRANSCHAR_2 = 0x11  # Address in decimal: 17
DVC_3PM_TRANSCHAR_3 = 0x12  # Address in decimal: 18
DVC_3PM_TRANSCHAR_4 = 0x13  # Address in decimal: 19
DVC_3PM_TRANSCHAR_5 = 0x14  # Address in decimal: 20
DVC_3PM_OUTCHAR_1 = 0x15  # Address in decimal: 21
DVC_3PM_OUTCHAR_2 = 0x16  # Address in decimal: 22
DVC_3PM_OUTCHAR_3 = 0x17  # Address in decimal: 23
DVC_3PM_OUTCHAR_4 = 0x18  # Address in decimal: 24
DVC_3PM_OUTCHAR_5 = 0x19  # Address in decimal: 25
DVC_3PM_CAPVOLT_1 = 0x1A  # Address in decimal: 26
DVC_3PM_CAPVOLT_2 = 0x1B  # Address in decimal: 27
DVC_3PM_CAPVOLT_3 = 0x1C  # Address in decimal: 28
DVC_3PM_ELECHEM_1 = 0x1D  # Address in decimal: 29
DVC_3PM_ELECHEM_2 = 0x1E  # Address in decimal: 30
DVC_3PM_ELECHEM_3 = 0x1F  # Address in decimal: 31
DVC_3PM_ELECHEM_4 = 0x20  # Address in decimal: 32
DVC_3PM_ELECHEM_5 = 0x21  # Address in decimal: 33
DVC_4PM_PROBERESISTANCE_1 = 0x22  # Address in decimal: 34
DVC_2PM_LOWRESISTANCE_1 = 0x23  # Address in decimal: 35
DVC_4PM_IMPSPEC_1 = 0x24  # Address in decimal: 36
DVC_4PM_IMPSPEC_2 = 0x25  # Address in decimal: 37
DVC_4PM_IMPSPEC_3 = 0x26  # Address in decimal: 38
DVC_4PM_IMPSPEC_4 = 0x27  # Address in decimal: 39
DVC_4PM_IMPSPEC_5 = 0x28  # Address in decimal: 40
DVC_FLUSH_SAMPLE_DATA_1 = 0x64  # Address in decimal: 100
DVC_FLUSH_SAMPLE_DATA_2 = 0x65  # Address in decimal: 101
DVC_FLUSH_SAMPLE_DATA_3 = 0x66  # Address in decimal: 102

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

# DVC_2PM_DCRESISTANCE_1
DVC_2PM_DCRESISTANCE_1_Test_Current_Value_POSITION = 0
DVC_2PM_DCRESISTANCE_1_Test_Current_Value_LENGTH = 24

# DVC_2PM_CURRVOLT_1
DVC_2PM_CURRVOLT_1_Sweep_Param_POSITION = 0
DVC_2PM_CURRVOLT_1_Sweep_Param_LENGTH = 2

# DVC_2PM_CURRVOLT_2
DVC_2PM_CURRVOLT_2_Starting_Param_POSITION = 0
DVC_2PM_CURRVOLT_2_Starting_Param_LENGTH = 24

# DVC_2PM_CURRVOLT_3
DVC_2PM_CURRVOLT_3_Ending_Param_POSITION = 0
DVC_2PM_CURRVOLT_3_Ending_Param_LENGTH = 24

# DVC_2PM_CURRVOLT_4
DVC_2PM_CURRVOLT_4_Increment_Param_POSITION = 0
DVC_2PM_CURRVOLT_4_Increment_Param_LENGTH = 24

# DVC_2PM_CAPVOLT_1
DVC_2PM_CAPVOLT_1_Starting_Volt_POSITION = 0
DVC_2PM_CAPVOLT_1_Starting_Volt_LENGTH = 24

# DVC_2PM_CAPVOLT_2
DVC_2PM_CAPVOLT_2_Ending_Volt_POSITION = 0
DVC_2PM_CAPVOLT_2_Ending_Volt_LENGTH = 24

# DVC_2PM_CAPVOLT_3
DVC_2PM_CAPVOLT_3_Increment_Volt_POSITION = 0
DVC_2PM_CAPVOLT_3_Increment_Volt_LENGTH = 24

# DVC_2PM_IMPSPEC_1
DVC_2PM_IMPSPEC_1_Starting_Freq_POSITION = 0
DVC_2PM_IMPSPEC_1_Starting_Freq_LENGTH = 14

# DVC_2PM_IMPSPEC_2
DVC_2PM_IMPSPEC_2_Ending_Freq_POSITION = 0
DVC_2PM_IMPSPEC_2_Ending_Freq_LENGTH = 14

# DVC_2PM_IMPSPEC_3
DVC_2PM_IMPSPEC_3_Increment_Freq_POSITION = 0
DVC_2PM_IMPSPEC_3_Increment_Freq_LENGTH = 14

# DVC_2PM_IMPSPEC_4
DVC_2PM_IMPSPEC_4_Max_Peak_Volt_POSITION = 0
DVC_2PM_IMPSPEC_4_Max_Peak_Volt_LENGTH = 24

# DVC_2PM_IMPSPEC_5
DVC_2PM_IMPSPEC_5_Min_Peak_Volt_POSITION = 0
DVC_2PM_IMPSPEC_5_Min_Peak_Volt_LENGTH = 24

# DVC_3PM_TRANSCHAR_1
DVC_3PM_TRANSCHAR_1_Gate_Probe_POSITION = 0
DVC_3PM_TRANSCHAR_1_Gate_Probe_LENGTH = 24
DVC_3PM_TRANSCHAR_1_Drain_Probe_POSITION = 0
DVC_3PM_TRANSCHAR_1_Drain_Probe_LENGTH = 24

# DVC_3PM_TRANSCHAR_2
DVC_3PM_TRANSCHAR_2_Drain_Volt_POSITION = 0
DVC_3PM_TRANSCHAR_2_Drain_Volt_LENGTH = 24

# DVC_3PM_TRANSCHAR_3
DVC_3PM_TRANSCHAR_3_Starting_Volt_POSITION = 0
DVC_3PM_TRANSCHAR_3_Starting_Volt_LENGTH = 24

# DVC_3PM_TRANSCHAR_4
DVC_3PM_TRANSCHAR_4_Ending_Volt_POSITION = 0
DVC_3PM_TRANSCHAR_4_Ending_Volt_LENGTH = 24

# DVC_3PM_TRANSCHAR_5
DVC_3PM_TRANSCHAR_5_Increment_Volt_POSITION = 0
DVC_3PM_TRANSCHAR_5_Increment_Volt_LENGTH = 24

# DVC_3PM_OUTCHAR_1
DVC_3PM_OUTCHAR_1_Gate_Probe_POSITION = 0
DVC_3PM_OUTCHAR_1_Gate_Probe_LENGTH = 24
DVC_3PM_OUTCHAR_1_Drain_Probe_POSITION = 0
DVC_3PM_OUTCHAR_1_Drain_Probe_LENGTH = 24

# DVC_3PM_OUTCHAR_2
DVC_3PM_OUTCHAR_2_Gate_Volt_POSITION = 0
DVC_3PM_OUTCHAR_2_Gate_Volt_LENGTH = 24

# DVC_3PM_OUTCHAR_3
DVC_3PM_OUTCHAR_3_Starting_Volt_POSITION = 0
DVC_3PM_OUTCHAR_3_Starting_Volt_LENGTH = 24

# DVC_3PM_OUTCHAR_4
DVC_3PM_OUTCHAR_4_Ending_Volt_POSITION = 0
DVC_3PM_OUTCHAR_4_Ending_Volt_LENGTH = 24

# DVC_3PM_OUTCHAR_5
DVC_3PM_OUTCHAR_5_Increment_Volt_POSITION = 0
DVC_3PM_OUTCHAR_5_Increment_Volt_LENGTH = 24

# DVC_3PM_CAPVOLT_1
DVC_3PM_CAPVOLT_1_Starting_Volt_POSITION = 0
DVC_3PM_CAPVOLT_1_Starting_Volt_LENGTH = 24

# DVC_3PM_CAPVOLT_2
DVC_3PM_CAPVOLT_2_Ending_Volt_POSITION = 0
DVC_3PM_CAPVOLT_2_Ending_Volt_LENGTH = 24

# DVC_3PM_CAPVOLT_3
DVC_3PM_CAPVOLT_3_Increment_Volt_POSITION = 0
DVC_3PM_CAPVOLT_3_Increment_Volt_LENGTH = 24

# DVC_3PM_ELECHEM_1
DVC_3PM_ELECHEM_1_Starting_Freq_POSITION = 0
DVC_3PM_ELECHEM_1_Starting_Freq_LENGTH = 14

# DVC_3PM_ELECHEM_2
DVC_3PM_ELECHEM_2_Ending_Freq_POSITION = 0
DVC_3PM_ELECHEM_2_Ending_Freq_LENGTH = 14

# DVC_3PM_ELECHEM_3
DVC_3PM_ELECHEM_3_Increment_Freq_POSITION = 0
DVC_3PM_ELECHEM_3_Increment_Freq_LENGTH = 14

# DVC_3PM_ELECHEM_4
DVC_3PM_ELECHEM_4_Max_Peak_Volt_POSITION = 0
DVC_3PM_ELECHEM_4_Max_Peak_Volt_LENGTH = 24

# DVC_3PM_ELECHEM_5
DVC_3PM_ELECHEM_5_Min_Peak_Volt_POSITION = 0
DVC_3PM_ELECHEM_5_Min_Peak_Volt_LENGTH = 24

# DVC_4PM_PROBERESISTANCE_1
DVC_4PM_PROBERESISTANCE_1_Test_Current_Value_POSITION = 0
DVC_4PM_PROBERESISTANCE_1_Test_Current_Value_LENGTH = 24

# DVC_2PM_LOWRESISTANCE_1
DVC_2PM_LOWRESISTANCE_1_Test_Current_Value_POSITION = 0
DVC_2PM_LOWRESISTANCE_1_Test_Current_Value_LENGTH = 24

# DVC_4PM_IMPSPEC_1
DVC_4PM_IMPSPEC_1_Starting_Freq_POSITION = 0
DVC_4PM_IMPSPEC_1_Starting_Freq_LENGTH = 14

# DVC_4PM_IMPSPEC_2
DVC_4PM_IMPSPEC_2_Ending_Freq_POSITION = 0
DVC_4PM_IMPSPEC_2_Ending_Freq_LENGTH = 14

# DVC_4PM_IMPSPEC_3
DVC_4PM_IMPSPEC_3_Increment_Freq_POSITION = 0
DVC_4PM_IMPSPEC_3_Increment_Freq_LENGTH = 14

# DVC_4PM_IMPSPEC_4
DVC_4PM_IMPSPEC_4_Max_Peak_Volt_POSITION = 0
DVC_4PM_IMPSPEC_4_Max_Peak_Volt_LENGTH = 24

# DVC_4PM_IMPSPEC_5
DVC_4PM_IMPSPEC_5_Min_Peak_Volt_POSITION = 0
DVC_4PM_IMPSPEC_5_Min_Peak_Volt_LENGTH = 24

# DVC_FLUSH_SAMPLE_DATA_1
DVC_FLUSH_SAMPLE_DATA_1_Sample_POSITION = 0
DVC_FLUSH_SAMPLE_DATA_1_Sample_LENGTH = 12

# DVC_FLUSH_SAMPLE_DATA_2
DVC_FLUSH_SAMPLE_DATA_2_Sample_POSITION = 0
DVC_FLUSH_SAMPLE_DATA_2_Sample_LENGTH = 12

# DVC_FLUSH_SAMPLE_DATA_3
DVC_FLUSH_SAMPLE_DATA_3_Sample_POSITION = 0
DVC_FLUSH_SAMPLE_DATA_3_Sample_LENGTH = 12

# Register Classes
class DVC_DVC_STATUS:
    def __init__(self):
        self.Power_Good = [0xDEAD,DVC_STATUS_Power_Good_POSITION, DVC_STATUS_Power_Good_LENGTH]
        self.USB_Connected = [0xDEAD,DVC_STATUS_USB_Connected_POSITION, DVC_STATUS_USB_Connected_LENGTH]
        self.Selected_Probes = [0xDEAD,DVC_STATUS_Selected_Probes_POSITION, DVC_STATUS_Selected_Probes_LENGTH]

class DVC_DVC_MEASUREMENT_CONFIG:
    def __init__(self):
        self.Start_Measure = [0xDEAD,DVC_MEASUREMENT_CONFIG_Start_Measure_POSITION, DVC_MEASUREMENT_CONFIG_Start_Measure_LENGTH]
        self.Stop_Measure = [0xDEAD,DVC_MEASUREMENT_CONFIG_Stop_Measure_POSITION, DVC_MEASUREMENT_CONFIG_Stop_Measure_LENGTH]
        self.Measure_In_Progress = [0xDEAD,DVC_MEASUREMENT_CONFIG_Measure_In_Progress_POSITION, DVC_MEASUREMENT_CONFIG_Measure_In_Progress_LENGTH]
        self.Valid_Measure_Config = [0xDEAD,DVC_MEASUREMENT_CONFIG_Valid_Measure_Config_POSITION, DVC_MEASUREMENT_CONFIG_Valid_Measure_Config_LENGTH]
        self.Measure_Probe_Config = [0xDEAD,DVC_MEASUREMENT_CONFIG_Measure_Probe_Config_POSITION, DVC_MEASUREMENT_CONFIG_Measure_Probe_Config_LENGTH]
        self.Measure_Type_Config = [0xDEAD,DVC_MEASUREMENT_CONFIG_Measure_Type_Config_POSITION, DVC_MEASUREMENT_CONFIG_Measure_Type_Config_LENGTH]

class DVC_DVC_PROBE_CONFIG:
    def __init__(self):
        self.Used_Probes = [0xDEAD,DVC_PROBE_CONFIG_Used_Probes_POSITION, DVC_PROBE_CONFIG_Used_Probes_LENGTH]
        self.Probe_1_Config = [0xDEAD,DVC_PROBE_CONFIG_Probe_1_Config_POSITION, DVC_PROBE_CONFIG_Probe_1_Config_LENGTH]
        self.Probe_2_Config = [0xDEAD,DVC_PROBE_CONFIG_Probe_2_Config_POSITION, DVC_PROBE_CONFIG_Probe_2_Config_LENGTH]
        self.Probe_3_Config = [0xDEAD,DVC_PROBE_CONFIG_Probe_3_Config_POSITION, DVC_PROBE_CONFIG_Probe_3_Config_LENGTH]
        self.Probe_4_Config = [0xDEAD,DVC_PROBE_CONFIG_Probe_4_Config_POSITION, DVC_PROBE_CONFIG_Probe_4_Config_LENGTH]

class DVC_DVC_2PM_DCRESISTANCE_1:
    def __init__(self):
        self.Test_Current_Value = [0xDEAD,DVC_2PM_DCRESISTANCE_1_Test_Current_Value_POSITION, DVC_2PM_DCRESISTANCE_1_Test_Current_Value_LENGTH]

class DVC_DVC_2PM_CURRVOLT_1:
    def __init__(self):
        self.Sweep_Param = [0xDEAD,DVC_2PM_CURRVOLT_1_Sweep_Param_POSITION, DVC_2PM_CURRVOLT_1_Sweep_Param_LENGTH]

class DVC_DVC_2PM_CURRVOLT_2:
    def __init__(self):
        self.Starting_Param = [0xDEAD,DVC_2PM_CURRVOLT_2_Starting_Param_POSITION, DVC_2PM_CURRVOLT_2_Starting_Param_LENGTH]

class DVC_DVC_2PM_CURRVOLT_3:
    def __init__(self):
        self.Ending_Param = [0xDEAD,DVC_2PM_CURRVOLT_3_Ending_Param_POSITION, DVC_2PM_CURRVOLT_3_Ending_Param_LENGTH]

class DVC_DVC_2PM_CURRVOLT_4:
    def __init__(self):
        self.Increment_Param = [0xDEAD,DVC_2PM_CURRVOLT_4_Increment_Param_POSITION, DVC_2PM_CURRVOLT_4_Increment_Param_LENGTH]

class DVC_DVC_2PM_CAPVOLT_1:
    def __init__(self):
        self.Starting_Volt = [0xDEAD,DVC_2PM_CAPVOLT_1_Starting_Volt_POSITION, DVC_2PM_CAPVOLT_1_Starting_Volt_LENGTH]

class DVC_DVC_2PM_CAPVOLT_2:
    def __init__(self):
        self.Ending_Volt = [0xDEAD,DVC_2PM_CAPVOLT_2_Ending_Volt_POSITION, DVC_2PM_CAPVOLT_2_Ending_Volt_LENGTH]

class DVC_DVC_2PM_CAPVOLT_3:
    def __init__(self):
        self.Increment_Volt = [0xDEAD,DVC_2PM_CAPVOLT_3_Increment_Volt_POSITION, DVC_2PM_CAPVOLT_3_Increment_Volt_LENGTH]

class DVC_DVC_2PM_IMPSPEC_1:
    def __init__(self):
        self.Starting_Freq = [0xDEAD,DVC_2PM_IMPSPEC_1_Starting_Freq_POSITION, DVC_2PM_IMPSPEC_1_Starting_Freq_LENGTH]

class DVC_DVC_2PM_IMPSPEC_2:
    def __init__(self):
        self.Ending_Freq = [0xDEAD,DVC_2PM_IMPSPEC_2_Ending_Freq_POSITION, DVC_2PM_IMPSPEC_2_Ending_Freq_LENGTH]

class DVC_DVC_2PM_IMPSPEC_3:
    def __init__(self):
        self.Increment_Freq = [0xDEAD,DVC_2PM_IMPSPEC_3_Increment_Freq_POSITION, DVC_2PM_IMPSPEC_3_Increment_Freq_LENGTH]

class DVC_DVC_2PM_IMPSPEC_4:
    def __init__(self):
        self.Max_Peak_Volt = [0xDEAD,DVC_2PM_IMPSPEC_4_Max_Peak_Volt_POSITION, DVC_2PM_IMPSPEC_4_Max_Peak_Volt_LENGTH]

class DVC_DVC_2PM_IMPSPEC_5:
    def __init__(self):
        self.Min_Peak_Volt = [0xDEAD,DVC_2PM_IMPSPEC_5_Min_Peak_Volt_POSITION, DVC_2PM_IMPSPEC_5_Min_Peak_Volt_LENGTH]

class DVC_DVC_3PM_TRANSCHAR_1:
    def __init__(self):
        self.Gate_Probe = [0xDEAD,DVC_3PM_TRANSCHAR_1_Gate_Probe_POSITION, DVC_3PM_TRANSCHAR_1_Gate_Probe_LENGTH]
        self.Drain_Probe = [0xDEAD,DVC_3PM_TRANSCHAR_1_Drain_Probe_POSITION, DVC_3PM_TRANSCHAR_1_Drain_Probe_LENGTH]

class DVC_DVC_3PM_TRANSCHAR_2:
    def __init__(self):
        self.Drain_Volt = [0xDEAD,DVC_3PM_TRANSCHAR_2_Drain_Volt_POSITION, DVC_3PM_TRANSCHAR_2_Drain_Volt_LENGTH]

class DVC_DVC_3PM_TRANSCHAR_3:
    def __init__(self):
        self.Starting_Volt = [0xDEAD,DVC_3PM_TRANSCHAR_3_Starting_Volt_POSITION, DVC_3PM_TRANSCHAR_3_Starting_Volt_LENGTH]

class DVC_DVC_3PM_TRANSCHAR_4:
    def __init__(self):
        self.Ending_Volt = [0xDEAD,DVC_3PM_TRANSCHAR_4_Ending_Volt_POSITION, DVC_3PM_TRANSCHAR_4_Ending_Volt_LENGTH]

class DVC_DVC_3PM_TRANSCHAR_5:
    def __init__(self):
        self.Increment_Volt = [0xDEAD,DVC_3PM_TRANSCHAR_5_Increment_Volt_POSITION, DVC_3PM_TRANSCHAR_5_Increment_Volt_LENGTH]

class DVC_DVC_3PM_OUTCHAR_1:
    def __init__(self):
        self.Gate_Probe = [0xDEAD,DVC_3PM_OUTCHAR_1_Gate_Probe_POSITION, DVC_3PM_OUTCHAR_1_Gate_Probe_LENGTH]
        self.Drain_Probe = [0xDEAD,DVC_3PM_OUTCHAR_1_Drain_Probe_POSITION, DVC_3PM_OUTCHAR_1_Drain_Probe_LENGTH]

class DVC_DVC_3PM_OUTCHAR_2:
    def __init__(self):
        self.Gate_Volt = [0xDEAD,DVC_3PM_OUTCHAR_2_Gate_Volt_POSITION, DVC_3PM_OUTCHAR_2_Gate_Volt_LENGTH]

class DVC_DVC_3PM_OUTCHAR_3:
    def __init__(self):
        self.Starting_Volt = [0xDEAD,DVC_3PM_OUTCHAR_3_Starting_Volt_POSITION, DVC_3PM_OUTCHAR_3_Starting_Volt_LENGTH]

class DVC_DVC_3PM_OUTCHAR_4:
    def __init__(self):
        self.Ending_Volt = [0xDEAD,DVC_3PM_OUTCHAR_4_Ending_Volt_POSITION, DVC_3PM_OUTCHAR_4_Ending_Volt_LENGTH]

class DVC_DVC_3PM_OUTCHAR_5:
    def __init__(self):
        self.Increment_Volt = [0xDEAD,DVC_3PM_OUTCHAR_5_Increment_Volt_POSITION, DVC_3PM_OUTCHAR_5_Increment_Volt_LENGTH]

class DVC_DVC_3PM_CAPVOLT_1:
    def __init__(self):
        self.Starting_Volt = [0xDEAD,DVC_3PM_CAPVOLT_1_Starting_Volt_POSITION, DVC_3PM_CAPVOLT_1_Starting_Volt_LENGTH]

class DVC_DVC_3PM_CAPVOLT_2:
    def __init__(self):
        self.Ending_Volt = [0xDEAD,DVC_3PM_CAPVOLT_2_Ending_Volt_POSITION, DVC_3PM_CAPVOLT_2_Ending_Volt_LENGTH]

class DVC_DVC_3PM_CAPVOLT_3:
    def __init__(self):
        self.Increment_Volt = [0xDEAD,DVC_3PM_CAPVOLT_3_Increment_Volt_POSITION, DVC_3PM_CAPVOLT_3_Increment_Volt_LENGTH]

class DVC_DVC_3PM_ELECHEM_1:
    def __init__(self):
        self.Starting_Freq = [0xDEAD,DVC_3PM_ELECHEM_1_Starting_Freq_POSITION, DVC_3PM_ELECHEM_1_Starting_Freq_LENGTH]

class DVC_DVC_3PM_ELECHEM_2:
    def __init__(self):
        self.Ending_Freq = [0xDEAD,DVC_3PM_ELECHEM_2_Ending_Freq_POSITION, DVC_3PM_ELECHEM_2_Ending_Freq_LENGTH]

class DVC_DVC_3PM_ELECHEM_3:
    def __init__(self):
        self.Increment_Freq = [0xDEAD,DVC_3PM_ELECHEM_3_Increment_Freq_POSITION, DVC_3PM_ELECHEM_3_Increment_Freq_LENGTH]

class DVC_DVC_3PM_ELECHEM_4:
    def __init__(self):
        self.Max_Peak_Volt = [0xDEAD,DVC_3PM_ELECHEM_4_Max_Peak_Volt_POSITION, DVC_3PM_ELECHEM_4_Max_Peak_Volt_LENGTH]

class DVC_DVC_3PM_ELECHEM_5:
    def __init__(self):
        self.Min_Peak_Volt = [0xDEAD,DVC_3PM_ELECHEM_5_Min_Peak_Volt_POSITION, DVC_3PM_ELECHEM_5_Min_Peak_Volt_LENGTH]

class DVC_DVC_4PM_PROBERESISTANCE_1:
    def __init__(self):
        self.Test_Current_Value = [0xDEAD,DVC_4PM_PROBERESISTANCE_1_Test_Current_Value_POSITION, DVC_4PM_PROBERESISTANCE_1_Test_Current_Value_LENGTH]

class DVC_DVC_2PM_LOWRESISTANCE_1:
    def __init__(self):
        self.Test_Current_Value = [0xDEAD,DVC_2PM_LOWRESISTANCE_1_Test_Current_Value_POSITION, DVC_2PM_LOWRESISTANCE_1_Test_Current_Value_LENGTH]

class DVC_DVC_4PM_IMPSPEC_1:
    def __init__(self):
        self.Starting_Freq = [0xDEAD,DVC_4PM_IMPSPEC_1_Starting_Freq_POSITION, DVC_4PM_IMPSPEC_1_Starting_Freq_LENGTH]

class DVC_DVC_4PM_IMPSPEC_2:
    def __init__(self):
        self.Ending_Freq = [0xDEAD,DVC_4PM_IMPSPEC_2_Ending_Freq_POSITION, DVC_4PM_IMPSPEC_2_Ending_Freq_LENGTH]

class DVC_DVC_4PM_IMPSPEC_3:
    def __init__(self):
        self.Increment_Freq = [0xDEAD,DVC_4PM_IMPSPEC_3_Increment_Freq_POSITION, DVC_4PM_IMPSPEC_3_Increment_Freq_LENGTH]

class DVC_DVC_4PM_IMPSPEC_4:
    def __init__(self):
        self.Max_Peak_Volt = [0xDEAD,DVC_4PM_IMPSPEC_4_Max_Peak_Volt_POSITION, DVC_4PM_IMPSPEC_4_Max_Peak_Volt_LENGTH]

class DVC_DVC_4PM_IMPSPEC_5:
    def __init__(self):
        self.Min_Peak_Volt = [0xDEAD,DVC_4PM_IMPSPEC_5_Min_Peak_Volt_POSITION, DVC_4PM_IMPSPEC_5_Min_Peak_Volt_LENGTH]

class DVC_DVC_FLUSH_SAMPLE_DATA_1:
    def __init__(self):
        self.Sample = [0xDEAD,DVC_FLUSH_SAMPLE_DATA_1_Sample_POSITION, DVC_FLUSH_SAMPLE_DATA_1_Sample_LENGTH]

class DVC_DVC_FLUSH_SAMPLE_DATA_2:
    def __init__(self):
        self.Sample = [0xDEAD,DVC_FLUSH_SAMPLE_DATA_2_Sample_POSITION, DVC_FLUSH_SAMPLE_DATA_2_Sample_LENGTH]

class DVC_DVC_FLUSH_SAMPLE_DATA_3:
    def __init__(self):
        self.Sample = [0xDEAD,DVC_FLUSH_SAMPLE_DATA_3_Sample_POSITION, DVC_FLUSH_SAMPLE_DATA_3_Sample_LENGTH]

class DVC_RegisterMap:
    def __init__(self):
        self.DVC_STATUS = DVC_DVC_STATUS()
        self.DVC_MEASUREMENT_CONFIG = DVC_DVC_MEASUREMENT_CONFIG()
        self.DVC_PROBE_CONFIG = DVC_DVC_PROBE_CONFIG()
        self.DVC_2PM_DCRESISTANCE_1 = DVC_DVC_2PM_DCRESISTANCE_1()
        self.DVC_2PM_CURRVOLT_1 = DVC_DVC_2PM_CURRVOLT_1()
        self.DVC_2PM_CURRVOLT_2 = DVC_DVC_2PM_CURRVOLT_2()
        self.DVC_2PM_CURRVOLT_3 = DVC_DVC_2PM_CURRVOLT_3()
        self.DVC_2PM_CURRVOLT_4 = DVC_DVC_2PM_CURRVOLT_4()
        self.DVC_2PM_CAPVOLT_1 = DVC_DVC_2PM_CAPVOLT_1()
        self.DVC_2PM_CAPVOLT_2 = DVC_DVC_2PM_CAPVOLT_2()
        self.DVC_2PM_CAPVOLT_3 = DVC_DVC_2PM_CAPVOLT_3()
        self.DVC_2PM_IMPSPEC_1 = DVC_DVC_2PM_IMPSPEC_1()
        self.DVC_2PM_IMPSPEC_2 = DVC_DVC_2PM_IMPSPEC_2()
        self.DVC_2PM_IMPSPEC_3 = DVC_DVC_2PM_IMPSPEC_3()
        self.DVC_2PM_IMPSPEC_4 = DVC_DVC_2PM_IMPSPEC_4()
        self.DVC_2PM_IMPSPEC_5 = DVC_DVC_2PM_IMPSPEC_5()
        self.DVC_3PM_TRANSCHAR_1 = DVC_DVC_3PM_TRANSCHAR_1()
        self.DVC_3PM_TRANSCHAR_2 = DVC_DVC_3PM_TRANSCHAR_2()
        self.DVC_3PM_TRANSCHAR_3 = DVC_DVC_3PM_TRANSCHAR_3()
        self.DVC_3PM_TRANSCHAR_4 = DVC_DVC_3PM_TRANSCHAR_4()
        self.DVC_3PM_TRANSCHAR_5 = DVC_DVC_3PM_TRANSCHAR_5()
        self.DVC_3PM_OUTCHAR_1 = DVC_DVC_3PM_OUTCHAR_1()
        self.DVC_3PM_OUTCHAR_2 = DVC_DVC_3PM_OUTCHAR_2()
        self.DVC_3PM_OUTCHAR_3 = DVC_DVC_3PM_OUTCHAR_3()
        self.DVC_3PM_OUTCHAR_4 = DVC_DVC_3PM_OUTCHAR_4()
        self.DVC_3PM_OUTCHAR_5 = DVC_DVC_3PM_OUTCHAR_5()
        self.DVC_3PM_CAPVOLT_1 = DVC_DVC_3PM_CAPVOLT_1()
        self.DVC_3PM_CAPVOLT_2 = DVC_DVC_3PM_CAPVOLT_2()
        self.DVC_3PM_CAPVOLT_3 = DVC_DVC_3PM_CAPVOLT_3()
        self.DVC_3PM_ELECHEM_1 = DVC_DVC_3PM_ELECHEM_1()
        self.DVC_3PM_ELECHEM_2 = DVC_DVC_3PM_ELECHEM_2()
        self.DVC_3PM_ELECHEM_3 = DVC_DVC_3PM_ELECHEM_3()
        self.DVC_3PM_ELECHEM_4 = DVC_DVC_3PM_ELECHEM_4()
        self.DVC_3PM_ELECHEM_5 = DVC_DVC_3PM_ELECHEM_5()
        self.DVC_4PM_PROBERESISTANCE_1 = DVC_DVC_4PM_PROBERESISTANCE_1()
        self.DVC_2PM_LOWRESISTANCE_1 = DVC_DVC_2PM_LOWRESISTANCE_1()
        self.DVC_4PM_IMPSPEC_1 = DVC_DVC_4PM_IMPSPEC_1()
        self.DVC_4PM_IMPSPEC_2 = DVC_DVC_4PM_IMPSPEC_2()
        self.DVC_4PM_IMPSPEC_3 = DVC_DVC_4PM_IMPSPEC_3()
        self.DVC_4PM_IMPSPEC_4 = DVC_DVC_4PM_IMPSPEC_4()
        self.DVC_4PM_IMPSPEC_5 = DVC_DVC_4PM_IMPSPEC_5()
        self.DVC_FLUSH_SAMPLE_DATA_1 = DVC_DVC_FLUSH_SAMPLE_DATA_1()
        self.DVC_FLUSH_SAMPLE_DATA_2 = DVC_DVC_FLUSH_SAMPLE_DATA_2()
        self.DVC_FLUSH_SAMPLE_DATA_3 = DVC_DVC_FLUSH_SAMPLE_DATA_3()


reg_map = DVC_RegisterMap()
