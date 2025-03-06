# interface.py

import comm_device

from registers import *

def read_register(ser,register_address):
    valW = comm_device.pack_32bit(register_address,0)
    comm_device.send_value(ser,valW)
    # valR = comm_device.receive_value(ser)
    # while valR is None:
    #     valR = comm_device.receive_value(ser)
    # return valR

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

def write_reg_DVC_SAMPLE_DATA(ser, reg_map):
    write_register(ser, DVC_SAMPLE_DATA, 
                  (reg_map.DVC_SAMPLE_DATA.Sample_1[0] << reg_map.DVC_SAMPLE_DATA.Sample_1[1])
                 |(reg_map.DVC_SAMPLE_DATA.Sample_2[0] << reg_map.DVC_SAMPLE_DATA.Sample_2[1]))

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

def read_reg_DVC_SAMPLE_DATA(ser, reg_map):
    valR = read_register(ser, DVC_SAMPLE_DATA)
    reg_map.DVC_SAMPLE_DATA.Sample_1[0] = (valR >> reg_map.DVC_SAMPLE_DATA.Sample_1[1]) & ((1 << reg_map.DVC_SAMPLE_DATA.Sample_1[2]) - 1)
    reg_map.DVC_SAMPLE_DATA.Sample_2[0] = (valR >> reg_map.DVC_SAMPLE_DATA.Sample_2[1]) & ((1 << reg_map.DVC_SAMPLE_DATA.Sample_2[2]) - 1)

