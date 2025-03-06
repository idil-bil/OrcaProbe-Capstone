# interface.py

import comm_device

from registers import *

def read_register(ser,register_address):
    valW = comm_device.pack_32bit(register_address,0)
    comm_device.send_value(ser,valW)
    data = comm_device.receive_value(ser)
    while data is None:
        data = comm_device.receive_value(ser)
    _, valR = comm_device.unpack_32bit(data)
    return valR

def write_register(ser,register_address, value):
    valW = comm_device.pack_32bit(128+register_address,value)
    comm_device.send_value(ser,valW)
    return

def write_reg_DVC_STATUS(ser, reg_map):
    write_register(ser, DVC_STATUS, 
                  (reg_map.DVC_STATUS.Power_Good[0] << reg_map.DVC_STATUS.Power_Good[1])
                 |(reg_map.DVC_STATUS.USB_Connected[0] << reg_map.DVC_STATUS.USB_Connected[1])
                 |(reg_map.DVC_STATUS.Selected_Probes[0] << reg_map.DVC_STATUS.Selected_Probes[1]))

def write_reg_DVC_MEASUREMENT_CONFIG(ser, reg_map):
    write_register(ser, DVC_MEASUREMENT_CONFIG, 
                  (reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] << reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[1])
                 |(reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] << reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[1])
                 |(reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] << reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[1])
                 |(reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] << reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[1])
                 |(reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] << reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[1])
                 |(reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] << reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[1]))

def write_reg_DVC_PROBE_CONFIG(ser, reg_map):
    write_register(ser, DVC_PROBE_CONFIG, 
                  (reg_map.DVC_PROBE_CONFIG.Used_Probes[0] << reg_map.DVC_PROBE_CONFIG.Used_Probes[1])
                 |(reg_map.DVC_PROBE_CONFIG.Probe_1_Config[0] << reg_map.DVC_PROBE_CONFIG.Probe_1_Config[1])
                 |(reg_map.DVC_PROBE_CONFIG.Probe_2_Config[0] << reg_map.DVC_PROBE_CONFIG.Probe_2_Config[1])
                 |(reg_map.DVC_PROBE_CONFIG.Probe_3_Config[0] << reg_map.DVC_PROBE_CONFIG.Probe_3_Config[1])
                 |(reg_map.DVC_PROBE_CONFIG.Probe_4_Config[0] << reg_map.DVC_PROBE_CONFIG.Probe_4_Config[1]))

def write_reg_DVC_2PM_DCRESISTANCE_1(ser, reg_map):
    write_register(ser, DVC_2PM_DCRESISTANCE_1, 
                  (reg_map.DVC_2PM_DCRESISTANCE_1.Test_Current_Value[0] << reg_map.DVC_2PM_DCRESISTANCE_1.Test_Current_Value[1]))

def write_reg_DVC_2PM_CURRVOLT_1(ser, reg_map):
    write_register(ser, DVC_2PM_CURRVOLT_1, 
                  (reg_map.DVC_2PM_CURRVOLT_1.Sweep_Param[0] << reg_map.DVC_2PM_CURRVOLT_1.Sweep_Param[1]))

def write_reg_DVC_2PM_CURRVOLT_2(ser, reg_map):
    write_register(ser, DVC_2PM_CURRVOLT_2, 
                  (reg_map.DVC_2PM_CURRVOLT_2.Starting_Param[0] << reg_map.DVC_2PM_CURRVOLT_2.Starting_Param[1]))

def write_reg_DVC_2PM_CURRVOLT_3(ser, reg_map):
    write_register(ser, DVC_2PM_CURRVOLT_3, 
                  (reg_map.DVC_2PM_CURRVOLT_3.Ending_Param[0] << reg_map.DVC_2PM_CURRVOLT_3.Ending_Param[1]))

def write_reg_DVC_2PM_CURRVOLT_4(ser, reg_map):
    write_register(ser, DVC_2PM_CURRVOLT_4, 
                  (reg_map.DVC_2PM_CURRVOLT_4.Increment_Param[0] << reg_map.DVC_2PM_CURRVOLT_4.Increment_Param[1]))

def write_reg_DVC_2PM_CAPVOLT_1(ser, reg_map):
    write_register(ser, DVC_2PM_CAPVOLT_1, 
                  (reg_map.DVC_2PM_CAPVOLT_1.Starting_Volt[0] << reg_map.DVC_2PM_CAPVOLT_1.Starting_Volt[1]))

def write_reg_DVC_2PM_CAPVOLT_2(ser, reg_map):
    write_register(ser, DVC_2PM_CAPVOLT_2, 
                  (reg_map.DVC_2PM_CAPVOLT_2.Ending_Volt[0] << reg_map.DVC_2PM_CAPVOLT_2.Ending_Volt[1]))

def write_reg_DVC_2PM_CAPVOLT_3(ser, reg_map):
    write_register(ser, DVC_2PM_CAPVOLT_3, 
                  (reg_map.DVC_2PM_CAPVOLT_3.Increment_Volt[0] << reg_map.DVC_2PM_CAPVOLT_3.Increment_Volt[1]))

def write_reg_DVC_2PM_IMPSPEC_1(ser, reg_map):
    write_register(ser, DVC_2PM_IMPSPEC_1, 
                  (reg_map.DVC_2PM_IMPSPEC_1.Starting_Freq[0] << reg_map.DVC_2PM_IMPSPEC_1.Starting_Freq[1]))

def write_reg_DVC_2PM_IMPSPEC_2(ser, reg_map):
    write_register(ser, DVC_2PM_IMPSPEC_2, 
                  (reg_map.DVC_2PM_IMPSPEC_2.Ending_Freq[0] << reg_map.DVC_2PM_IMPSPEC_2.Ending_Freq[1]))

def write_reg_DVC_2PM_IMPSPEC_3(ser, reg_map):
    write_register(ser, DVC_2PM_IMPSPEC_3, 
                  (reg_map.DVC_2PM_IMPSPEC_3.Increment_Freq[0] << reg_map.DVC_2PM_IMPSPEC_3.Increment_Freq[1]))

def write_reg_DVC_2PM_IMPSPEC_4(ser, reg_map):
    write_register(ser, DVC_2PM_IMPSPEC_4, 
                  (reg_map.DVC_2PM_IMPSPEC_4.Max_Peak_Volt[0] << reg_map.DVC_2PM_IMPSPEC_4.Max_Peak_Volt[1]))

def write_reg_DVC_2PM_IMPSPEC_5(ser, reg_map):
    write_register(ser, DVC_2PM_IMPSPEC_5, 
                  (reg_map.DVC_2PM_IMPSPEC_5.Min_Peak_Volt[0] << reg_map.DVC_2PM_IMPSPEC_5.Min_Peak_Volt[1]))

def write_reg_DVC_3PM_TRANSCHAR_1(ser, reg_map):
    write_register(ser, DVC_3PM_TRANSCHAR_1, 
                  (reg_map.DVC_3PM_TRANSCHAR_1.Starting_Volt[0] << reg_map.DVC_3PM_TRANSCHAR_1.Starting_Volt[1]))

def write_reg_DVC_3PM_TRANSCHAR_2(ser, reg_map):
    write_register(ser, DVC_3PM_TRANSCHAR_2, 
                  (reg_map.DVC_3PM_TRANSCHAR_2.Ending_Volt[0] << reg_map.DVC_3PM_TRANSCHAR_2.Ending_Volt[1]))

def write_reg_DVC_3PM_TRANSCHAR_3(ser, reg_map):
    write_register(ser, DVC_3PM_TRANSCHAR_3, 
                  (reg_map.DVC_3PM_TRANSCHAR_3.Increment_Volt[0] << reg_map.DVC_3PM_TRANSCHAR_3.Increment_Volt[1]))

def write_reg_DVC_3PM_OUTCHAR_1(ser, reg_map):
    write_register(ser, DVC_3PM_OUTCHAR_1, 
                  (reg_map.DVC_3PM_OUTCHAR_1.Starting_Volt[0] << reg_map.DVC_3PM_OUTCHAR_1.Starting_Volt[1]))

def write_reg_DVC_3PM_OUTCHAR_2(ser, reg_map):
    write_register(ser, DVC_3PM_OUTCHAR_2, 
                  (reg_map.DVC_3PM_OUTCHAR_2.Ending_Volt[0] << reg_map.DVC_3PM_OUTCHAR_2.Ending_Volt[1]))

def write_reg_DVC_3PM_OUTCHAR_3(ser, reg_map):
    write_register(ser, DVC_3PM_OUTCHAR_3, 
                  (reg_map.DVC_3PM_OUTCHAR_3.Increment_Volt[0] << reg_map.DVC_3PM_OUTCHAR_3.Increment_Volt[1]))

def write_reg_DVC_3PM_CAPVOLT_1(ser, reg_map):
    write_register(ser, DVC_3PM_CAPVOLT_1, 
                  (reg_map.DVC_3PM_CAPVOLT_1.Starting_Volt[0] << reg_map.DVC_3PM_CAPVOLT_1.Starting_Volt[1]))

def write_reg_DVC_3PM_CAPVOLT_2(ser, reg_map):
    write_register(ser, DVC_3PM_CAPVOLT_2, 
                  (reg_map.DVC_3PM_CAPVOLT_2.Ending_Volt[0] << reg_map.DVC_3PM_CAPVOLT_2.Ending_Volt[1]))

def write_reg_DVC_3PM_CAPVOLT_3(ser, reg_map):
    write_register(ser, DVC_3PM_CAPVOLT_3, 
                  (reg_map.DVC_3PM_CAPVOLT_3.Increment_Volt[0] << reg_map.DVC_3PM_CAPVOLT_3.Increment_Volt[1]))

def write_reg_DVC_3PM_ELECHEM_1(ser, reg_map):
    write_register(ser, DVC_3PM_ELECHEM_1, 
                  (reg_map.DVC_3PM_ELECHEM_1.Starting_Freq[0] << reg_map.DVC_3PM_ELECHEM_1.Starting_Freq[1]))

def write_reg_DVC_3PM_ELECHEM_2(ser, reg_map):
    write_register(ser, DVC_3PM_ELECHEM_2, 
                  (reg_map.DVC_3PM_ELECHEM_2.Ending_Freq[0] << reg_map.DVC_3PM_ELECHEM_2.Ending_Freq[1]))

def write_reg_DVC_3PM_ELECHEM_3(ser, reg_map):
    write_register(ser, DVC_3PM_ELECHEM_3, 
                  (reg_map.DVC_3PM_ELECHEM_3.Increment_Freq[0] << reg_map.DVC_3PM_ELECHEM_3.Increment_Freq[1]))

def write_reg_DVC_3PM_ELECHEM_4(ser, reg_map):
    write_register(ser, DVC_3PM_ELECHEM_4, 
                  (reg_map.DVC_3PM_ELECHEM_4.Max_Peak_Volt[0] << reg_map.DVC_3PM_ELECHEM_4.Max_Peak_Volt[1]))

def write_reg_DVC_3PM_ELECHEM_5(ser, reg_map):
    write_register(ser, DVC_3PM_ELECHEM_5, 
                  (reg_map.DVC_3PM_ELECHEM_5.Min_Peak_Volt[0] << reg_map.DVC_3PM_ELECHEM_5.Min_Peak_Volt[1]))

def write_reg_DVC_4PM_PROBERESISTANCE_1(ser, reg_map):
    write_register(ser, DVC_4PM_PROBERESISTANCE_1, 
                  (reg_map.DVC_4PM_PROBERESISTANCE_1.Test_Current_Value[0] << reg_map.DVC_4PM_PROBERESISTANCE_1.Test_Current_Value[1]))

def write_reg_DVC_2PM_LOWRESISTANCE_1(ser, reg_map):
    write_register(ser, DVC_2PM_LOWRESISTANCE_1, 
                  (reg_map.DVC_2PM_LOWRESISTANCE_1.Test_Current_Value[0] << reg_map.DVC_2PM_LOWRESISTANCE_1.Test_Current_Value[1]))

def write_reg_DVC_4PM_IMPSPEC_1(ser, reg_map):
    write_register(ser, DVC_4PM_IMPSPEC_1, 
                  (reg_map.DVC_4PM_IMPSPEC_1.Starting_Freq[0] << reg_map.DVC_4PM_IMPSPEC_1.Starting_Freq[1]))

def write_reg_DVC_4PM_IMPSPEC_2(ser, reg_map):
    write_register(ser, DVC_4PM_IMPSPEC_2, 
                  (reg_map.DVC_4PM_IMPSPEC_2.Ending_Freq[0] << reg_map.DVC_4PM_IMPSPEC_2.Ending_Freq[1]))

def write_reg_DVC_4PM_IMPSPEC_3(ser, reg_map):
    write_register(ser, DVC_4PM_IMPSPEC_3, 
                  (reg_map.DVC_4PM_IMPSPEC_3.Increment_Freq[0] << reg_map.DVC_4PM_IMPSPEC_3.Increment_Freq[1]))

def write_reg_DVC_4PM_IMPSPEC_4(ser, reg_map):
    write_register(ser, DVC_4PM_IMPSPEC_4, 
                  (reg_map.DVC_4PM_IMPSPEC_4.Max_Peak_Volt[0] << reg_map.DVC_4PM_IMPSPEC_4.Max_Peak_Volt[1]))

def write_reg_DVC_4PM_IMPSPEC_5(ser, reg_map):
    write_register(ser, DVC_4PM_IMPSPEC_5, 
                  (reg_map.DVC_4PM_IMPSPEC_5.Min_Peak_Volt[0] << reg_map.DVC_4PM_IMPSPEC_5.Min_Peak_Volt[1]))

def write_reg_DVC_FLUSH_SAMPLE_DATA_1(ser, reg_map):
    write_register(ser, DVC_FLUSH_SAMPLE_DATA_1, 
                  (reg_map.DVC_FLUSH_SAMPLE_DATA_1.Sample[0] << reg_map.DVC_FLUSH_SAMPLE_DATA_1.Sample[1]))

def write_reg_DVC_FLUSH_SAMPLE_DATA_2(ser, reg_map):
    write_register(ser, DVC_FLUSH_SAMPLE_DATA_2, 
                  (reg_map.DVC_FLUSH_SAMPLE_DATA_2.Sample[0] << reg_map.DVC_FLUSH_SAMPLE_DATA_2.Sample[1]))

def write_reg_DVC_FLUSH_SAMPLE_DATA_3(ser, reg_map):
    write_register(ser, DVC_FLUSH_SAMPLE_DATA_3, 
                  (reg_map.DVC_FLUSH_SAMPLE_DATA_3.Sample[0] << reg_map.DVC_FLUSH_SAMPLE_DATA_3.Sample[1]))

def read_reg_DVC_STATUS(ser, reg_map):
    valR = read_register(ser, DVC_STATUS)
    reg_map.DVC_STATUS.Power_Good[0] = (valR >> reg_map.DVC_STATUS.Power_Good[1]) & ((1 << reg_map.DVC_STATUS.Power_Good[2]) - 1)
    reg_map.DVC_STATUS.USB_Connected[0] = (valR >> reg_map.DVC_STATUS.USB_Connected[1]) & ((1 << reg_map.DVC_STATUS.USB_Connected[2]) - 1)
    reg_map.DVC_STATUS.Selected_Probes[0] = (valR >> reg_map.DVC_STATUS.Selected_Probes[1]) & ((1 << reg_map.DVC_STATUS.Selected_Probes[2]) - 1)

def read_reg_DVC_MEASUREMENT_CONFIG(ser, reg_map):
    valR = read_register(ser, DVC_MEASUREMENT_CONFIG)
    reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = (valR >> reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[1]) & ((1 << reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[2]) - 1)
    reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = (valR >> reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[1]) & ((1 << reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[2]) - 1)
    reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = (valR >> reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[1]) & ((1 << reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[2]) - 1)
    reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = (valR >> reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[1]) & ((1 << reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[2]) - 1)
    reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = (valR >> reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[1]) & ((1 << reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[2]) - 1)
    reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = (valR >> reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[1]) & ((1 << reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[2]) - 1)

def read_reg_DVC_PROBE_CONFIG(ser, reg_map):
    valR = read_register(ser, DVC_PROBE_CONFIG)
    reg_map.DVC_PROBE_CONFIG.Used_Probes[0] = (valR >> reg_map.DVC_PROBE_CONFIG.Used_Probes[1]) & ((1 << reg_map.DVC_PROBE_CONFIG.Used_Probes[2]) - 1)
    reg_map.DVC_PROBE_CONFIG.Probe_1_Config[0] = (valR >> reg_map.DVC_PROBE_CONFIG.Probe_1_Config[1]) & ((1 << reg_map.DVC_PROBE_CONFIG.Probe_1_Config[2]) - 1)
    reg_map.DVC_PROBE_CONFIG.Probe_2_Config[0] = (valR >> reg_map.DVC_PROBE_CONFIG.Probe_2_Config[1]) & ((1 << reg_map.DVC_PROBE_CONFIG.Probe_2_Config[2]) - 1)
    reg_map.DVC_PROBE_CONFIG.Probe_3_Config[0] = (valR >> reg_map.DVC_PROBE_CONFIG.Probe_3_Config[1]) & ((1 << reg_map.DVC_PROBE_CONFIG.Probe_3_Config[2]) - 1)
    reg_map.DVC_PROBE_CONFIG.Probe_4_Config[0] = (valR >> reg_map.DVC_PROBE_CONFIG.Probe_4_Config[1]) & ((1 << reg_map.DVC_PROBE_CONFIG.Probe_4_Config[2]) - 1)

def read_reg_DVC_2PM_DCRESISTANCE_1(ser, reg_map):
    valR = read_register(ser, DVC_2PM_DCRESISTANCE_1)
    reg_map.DVC_2PM_DCRESISTANCE_1.Test_Current_Value[0] = (valR >> reg_map.DVC_2PM_DCRESISTANCE_1.Test_Current_Value[1]) & ((1 << reg_map.DVC_2PM_DCRESISTANCE_1.Test_Current_Value[2]) - 1)

def read_reg_DVC_2PM_CURRVOLT_1(ser, reg_map):
    valR = read_register(ser, DVC_2PM_CURRVOLT_1)
    reg_map.DVC_2PM_CURRVOLT_1.Sweep_Param[0] = (valR >> reg_map.DVC_2PM_CURRVOLT_1.Sweep_Param[1]) & ((1 << reg_map.DVC_2PM_CURRVOLT_1.Sweep_Param[2]) - 1)

def read_reg_DVC_2PM_CURRVOLT_2(ser, reg_map):
    valR = read_register(ser, DVC_2PM_CURRVOLT_2)
    reg_map.DVC_2PM_CURRVOLT_2.Starting_Param[0] = (valR >> reg_map.DVC_2PM_CURRVOLT_2.Starting_Param[1]) & ((1 << reg_map.DVC_2PM_CURRVOLT_2.Starting_Param[2]) - 1)

def read_reg_DVC_2PM_CURRVOLT_3(ser, reg_map):
    valR = read_register(ser, DVC_2PM_CURRVOLT_3)
    reg_map.DVC_2PM_CURRVOLT_3.Ending_Param[0] = (valR >> reg_map.DVC_2PM_CURRVOLT_3.Ending_Param[1]) & ((1 << reg_map.DVC_2PM_CURRVOLT_3.Ending_Param[2]) - 1)

def read_reg_DVC_2PM_CURRVOLT_4(ser, reg_map):
    valR = read_register(ser, DVC_2PM_CURRVOLT_4)
    reg_map.DVC_2PM_CURRVOLT_4.Increment_Param[0] = (valR >> reg_map.DVC_2PM_CURRVOLT_4.Increment_Param[1]) & ((1 << reg_map.DVC_2PM_CURRVOLT_4.Increment_Param[2]) - 1)

def read_reg_DVC_2PM_CAPVOLT_1(ser, reg_map):
    valR = read_register(ser, DVC_2PM_CAPVOLT_1)
    reg_map.DVC_2PM_CAPVOLT_1.Starting_Volt[0] = (valR >> reg_map.DVC_2PM_CAPVOLT_1.Starting_Volt[1]) & ((1 << reg_map.DVC_2PM_CAPVOLT_1.Starting_Volt[2]) - 1)

def read_reg_DVC_2PM_CAPVOLT_2(ser, reg_map):
    valR = read_register(ser, DVC_2PM_CAPVOLT_2)
    reg_map.DVC_2PM_CAPVOLT_2.Ending_Volt[0] = (valR >> reg_map.DVC_2PM_CAPVOLT_2.Ending_Volt[1]) & ((1 << reg_map.DVC_2PM_CAPVOLT_2.Ending_Volt[2]) - 1)

def read_reg_DVC_2PM_CAPVOLT_3(ser, reg_map):
    valR = read_register(ser, DVC_2PM_CAPVOLT_3)
    reg_map.DVC_2PM_CAPVOLT_3.Increment_Volt[0] = (valR >> reg_map.DVC_2PM_CAPVOLT_3.Increment_Volt[1]) & ((1 << reg_map.DVC_2PM_CAPVOLT_3.Increment_Volt[2]) - 1)

def read_reg_DVC_2PM_IMPSPEC_1(ser, reg_map):
    valR = read_register(ser, DVC_2PM_IMPSPEC_1)
    reg_map.DVC_2PM_IMPSPEC_1.Starting_Freq[0] = (valR >> reg_map.DVC_2PM_IMPSPEC_1.Starting_Freq[1]) & ((1 << reg_map.DVC_2PM_IMPSPEC_1.Starting_Freq[2]) - 1)

def read_reg_DVC_2PM_IMPSPEC_2(ser, reg_map):
    valR = read_register(ser, DVC_2PM_IMPSPEC_2)
    reg_map.DVC_2PM_IMPSPEC_2.Ending_Freq[0] = (valR >> reg_map.DVC_2PM_IMPSPEC_2.Ending_Freq[1]) & ((1 << reg_map.DVC_2PM_IMPSPEC_2.Ending_Freq[2]) - 1)

def read_reg_DVC_2PM_IMPSPEC_3(ser, reg_map):
    valR = read_register(ser, DVC_2PM_IMPSPEC_3)
    reg_map.DVC_2PM_IMPSPEC_3.Increment_Freq[0] = (valR >> reg_map.DVC_2PM_IMPSPEC_3.Increment_Freq[1]) & ((1 << reg_map.DVC_2PM_IMPSPEC_3.Increment_Freq[2]) - 1)

def read_reg_DVC_2PM_IMPSPEC_4(ser, reg_map):
    valR = read_register(ser, DVC_2PM_IMPSPEC_4)
    reg_map.DVC_2PM_IMPSPEC_4.Max_Peak_Volt[0] = (valR >> reg_map.DVC_2PM_IMPSPEC_4.Max_Peak_Volt[1]) & ((1 << reg_map.DVC_2PM_IMPSPEC_4.Max_Peak_Volt[2]) - 1)

def read_reg_DVC_2PM_IMPSPEC_5(ser, reg_map):
    valR = read_register(ser, DVC_2PM_IMPSPEC_5)
    reg_map.DVC_2PM_IMPSPEC_5.Min_Peak_Volt[0] = (valR >> reg_map.DVC_2PM_IMPSPEC_5.Min_Peak_Volt[1]) & ((1 << reg_map.DVC_2PM_IMPSPEC_5.Min_Peak_Volt[2]) - 1)

def read_reg_DVC_3PM_TRANSCHAR_1(ser, reg_map):
    valR = read_register(ser, DVC_3PM_TRANSCHAR_1)
    reg_map.DVC_3PM_TRANSCHAR_1.Starting_Volt[0] = (valR >> reg_map.DVC_3PM_TRANSCHAR_1.Starting_Volt[1]) & ((1 << reg_map.DVC_3PM_TRANSCHAR_1.Starting_Volt[2]) - 1)

def read_reg_DVC_3PM_TRANSCHAR_2(ser, reg_map):
    valR = read_register(ser, DVC_3PM_TRANSCHAR_2)
    reg_map.DVC_3PM_TRANSCHAR_2.Ending_Volt[0] = (valR >> reg_map.DVC_3PM_TRANSCHAR_2.Ending_Volt[1]) & ((1 << reg_map.DVC_3PM_TRANSCHAR_2.Ending_Volt[2]) - 1)

def read_reg_DVC_3PM_TRANSCHAR_3(ser, reg_map):
    valR = read_register(ser, DVC_3PM_TRANSCHAR_3)
    reg_map.DVC_3PM_TRANSCHAR_3.Increment_Volt[0] = (valR >> reg_map.DVC_3PM_TRANSCHAR_3.Increment_Volt[1]) & ((1 << reg_map.DVC_3PM_TRANSCHAR_3.Increment_Volt[2]) - 1)

def read_reg_DVC_3PM_OUTCHAR_1(ser, reg_map):
    valR = read_register(ser, DVC_3PM_OUTCHAR_1)
    reg_map.DVC_3PM_OUTCHAR_1.Starting_Volt[0] = (valR >> reg_map.DVC_3PM_OUTCHAR_1.Starting_Volt[1]) & ((1 << reg_map.DVC_3PM_OUTCHAR_1.Starting_Volt[2]) - 1)

def read_reg_DVC_3PM_OUTCHAR_2(ser, reg_map):
    valR = read_register(ser, DVC_3PM_OUTCHAR_2)
    reg_map.DVC_3PM_OUTCHAR_2.Ending_Volt[0] = (valR >> reg_map.DVC_3PM_OUTCHAR_2.Ending_Volt[1]) & ((1 << reg_map.DVC_3PM_OUTCHAR_2.Ending_Volt[2]) - 1)

def read_reg_DVC_3PM_OUTCHAR_3(ser, reg_map):
    valR = read_register(ser, DVC_3PM_OUTCHAR_3)
    reg_map.DVC_3PM_OUTCHAR_3.Increment_Volt[0] = (valR >> reg_map.DVC_3PM_OUTCHAR_3.Increment_Volt[1]) & ((1 << reg_map.DVC_3PM_OUTCHAR_3.Increment_Volt[2]) - 1)

def read_reg_DVC_3PM_CAPVOLT_1(ser, reg_map):
    valR = read_register(ser, DVC_3PM_CAPVOLT_1)
    reg_map.DVC_3PM_CAPVOLT_1.Starting_Volt[0] = (valR >> reg_map.DVC_3PM_CAPVOLT_1.Starting_Volt[1]) & ((1 << reg_map.DVC_3PM_CAPVOLT_1.Starting_Volt[2]) - 1)

def read_reg_DVC_3PM_CAPVOLT_2(ser, reg_map):
    valR = read_register(ser, DVC_3PM_CAPVOLT_2)
    reg_map.DVC_3PM_CAPVOLT_2.Ending_Volt[0] = (valR >> reg_map.DVC_3PM_CAPVOLT_2.Ending_Volt[1]) & ((1 << reg_map.DVC_3PM_CAPVOLT_2.Ending_Volt[2]) - 1)

def read_reg_DVC_3PM_CAPVOLT_3(ser, reg_map):
    valR = read_register(ser, DVC_3PM_CAPVOLT_3)
    reg_map.DVC_3PM_CAPVOLT_3.Increment_Volt[0] = (valR >> reg_map.DVC_3PM_CAPVOLT_3.Increment_Volt[1]) & ((1 << reg_map.DVC_3PM_CAPVOLT_3.Increment_Volt[2]) - 1)

def read_reg_DVC_3PM_ELECHEM_1(ser, reg_map):
    valR = read_register(ser, DVC_3PM_ELECHEM_1)
    reg_map.DVC_3PM_ELECHEM_1.Starting_Freq[0] = (valR >> reg_map.DVC_3PM_ELECHEM_1.Starting_Freq[1]) & ((1 << reg_map.DVC_3PM_ELECHEM_1.Starting_Freq[2]) - 1)

def read_reg_DVC_3PM_ELECHEM_2(ser, reg_map):
    valR = read_register(ser, DVC_3PM_ELECHEM_2)
    reg_map.DVC_3PM_ELECHEM_2.Ending_Freq[0] = (valR >> reg_map.DVC_3PM_ELECHEM_2.Ending_Freq[1]) & ((1 << reg_map.DVC_3PM_ELECHEM_2.Ending_Freq[2]) - 1)

def read_reg_DVC_3PM_ELECHEM_3(ser, reg_map):
    valR = read_register(ser, DVC_3PM_ELECHEM_3)
    reg_map.DVC_3PM_ELECHEM_3.Increment_Freq[0] = (valR >> reg_map.DVC_3PM_ELECHEM_3.Increment_Freq[1]) & ((1 << reg_map.DVC_3PM_ELECHEM_3.Increment_Freq[2]) - 1)

def read_reg_DVC_3PM_ELECHEM_4(ser, reg_map):
    valR = read_register(ser, DVC_3PM_ELECHEM_4)
    reg_map.DVC_3PM_ELECHEM_4.Max_Peak_Volt[0] = (valR >> reg_map.DVC_3PM_ELECHEM_4.Max_Peak_Volt[1]) & ((1 << reg_map.DVC_3PM_ELECHEM_4.Max_Peak_Volt[2]) - 1)

def read_reg_DVC_3PM_ELECHEM_5(ser, reg_map):
    valR = read_register(ser, DVC_3PM_ELECHEM_5)
    reg_map.DVC_3PM_ELECHEM_5.Min_Peak_Volt[0] = (valR >> reg_map.DVC_3PM_ELECHEM_5.Min_Peak_Volt[1]) & ((1 << reg_map.DVC_3PM_ELECHEM_5.Min_Peak_Volt[2]) - 1)

def read_reg_DVC_4PM_PROBERESISTANCE_1(ser, reg_map):
    valR = read_register(ser, DVC_4PM_PROBERESISTANCE_1)
    reg_map.DVC_4PM_PROBERESISTANCE_1.Test_Current_Value[0] = (valR >> reg_map.DVC_4PM_PROBERESISTANCE_1.Test_Current_Value[1]) & ((1 << reg_map.DVC_4PM_PROBERESISTANCE_1.Test_Current_Value[2]) - 1)

def read_reg_DVC_2PM_LOWRESISTANCE_1(ser, reg_map):
    valR = read_register(ser, DVC_2PM_LOWRESISTANCE_1)
    reg_map.DVC_2PM_LOWRESISTANCE_1.Test_Current_Value[0] = (valR >> reg_map.DVC_2PM_LOWRESISTANCE_1.Test_Current_Value[1]) & ((1 << reg_map.DVC_2PM_LOWRESISTANCE_1.Test_Current_Value[2]) - 1)

def read_reg_DVC_4PM_IMPSPEC_1(ser, reg_map):
    valR = read_register(ser, DVC_4PM_IMPSPEC_1)
    reg_map.DVC_4PM_IMPSPEC_1.Starting_Freq[0] = (valR >> reg_map.DVC_4PM_IMPSPEC_1.Starting_Freq[1]) & ((1 << reg_map.DVC_4PM_IMPSPEC_1.Starting_Freq[2]) - 1)

def read_reg_DVC_4PM_IMPSPEC_2(ser, reg_map):
    valR = read_register(ser, DVC_4PM_IMPSPEC_2)
    reg_map.DVC_4PM_IMPSPEC_2.Ending_Freq[0] = (valR >> reg_map.DVC_4PM_IMPSPEC_2.Ending_Freq[1]) & ((1 << reg_map.DVC_4PM_IMPSPEC_2.Ending_Freq[2]) - 1)

def read_reg_DVC_4PM_IMPSPEC_3(ser, reg_map):
    valR = read_register(ser, DVC_4PM_IMPSPEC_3)
    reg_map.DVC_4PM_IMPSPEC_3.Increment_Freq[0] = (valR >> reg_map.DVC_4PM_IMPSPEC_3.Increment_Freq[1]) & ((1 << reg_map.DVC_4PM_IMPSPEC_3.Increment_Freq[2]) - 1)

def read_reg_DVC_4PM_IMPSPEC_4(ser, reg_map):
    valR = read_register(ser, DVC_4PM_IMPSPEC_4)
    reg_map.DVC_4PM_IMPSPEC_4.Max_Peak_Volt[0] = (valR >> reg_map.DVC_4PM_IMPSPEC_4.Max_Peak_Volt[1]) & ((1 << reg_map.DVC_4PM_IMPSPEC_4.Max_Peak_Volt[2]) - 1)

def read_reg_DVC_4PM_IMPSPEC_5(ser, reg_map):
    valR = read_register(ser, DVC_4PM_IMPSPEC_5)
    reg_map.DVC_4PM_IMPSPEC_5.Min_Peak_Volt[0] = (valR >> reg_map.DVC_4PM_IMPSPEC_5.Min_Peak_Volt[1]) & ((1 << reg_map.DVC_4PM_IMPSPEC_5.Min_Peak_Volt[2]) - 1)

def read_reg_DVC_FLUSH_SAMPLE_DATA_1(ser, reg_map):
    valR = read_register(ser, DVC_FLUSH_SAMPLE_DATA_1)
    reg_map.DVC_FLUSH_SAMPLE_DATA_1.Sample[0] = (valR >> reg_map.DVC_FLUSH_SAMPLE_DATA_1.Sample[1]) & ((1 << reg_map.DVC_FLUSH_SAMPLE_DATA_1.Sample[2]) - 1)

def read_reg_DVC_FLUSH_SAMPLE_DATA_2(ser, reg_map):
    valR = read_register(ser, DVC_FLUSH_SAMPLE_DATA_2)
    reg_map.DVC_FLUSH_SAMPLE_DATA_2.Sample[0] = (valR >> reg_map.DVC_FLUSH_SAMPLE_DATA_2.Sample[1]) & ((1 << reg_map.DVC_FLUSH_SAMPLE_DATA_2.Sample[2]) - 1)

def read_reg_DVC_FLUSH_SAMPLE_DATA_3(ser, reg_map):
    valR = read_register(ser, DVC_FLUSH_SAMPLE_DATA_3)
    reg_map.DVC_FLUSH_SAMPLE_DATA_3.Sample[0] = (valR >> reg_map.DVC_FLUSH_SAMPLE_DATA_3.Sample[1]) & ((1 << reg_map.DVC_FLUSH_SAMPLE_DATA_3.Sample[2]) - 1)

