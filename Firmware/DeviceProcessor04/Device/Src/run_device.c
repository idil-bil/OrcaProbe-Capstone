/*
 * run_device.c
 *
 *  Created on: Nov 16, 2024
 *      Author: User
 */

#include "device_constants.h"
#include "main.h"
#include "run_device.h"
#include "switch_network.h"
#include "device_registers.h"
#include "measurement_routines.h"
#include "device_sourcing.h"
#include "device_monitoring.h"

extern TIM_HandleTypeDef htim8;
extern DMA_HandleTypeDef handle_GPDMA1_Channel12;
extern DMA_HandleTypeDef handle_GPDMA1_Channel13;
extern DMA_HandleTypeDef handle_GPDMA1_Channel14;

uint16_t adc_samples_1[DVC_MAX_NUM_ADC_SAMPLES];
uint16_t adc_samples_2[DVC_MAX_NUM_ADC_SAMPLES];
uint16_t adc_samples_3[DVC_MAX_NUM_ADC_SAMPLES];

uint8_t i2c_tx_buf_dac_1_pot[] = {0xff,0xff};
uint8_t i2c_tx_buf_dac_2_pot[] = {0xff,0xff};
uint8_t i2c_tx_buf_curr_mrr_pot[] = {0xff,0xff};

uint8_t spi_tx_buf_dac_1_freq[] = {0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff};
uint8_t spi_tx_buf_dac_2_freq[] = {0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff};

RegisterMap_TypeDef device_registers;
SwitchNetwork_TypeDef device_switch_network;

void run_device(){
	HAL_GPIO_WritePin(GPIOC,USER_LED_Pin,GPIO_PIN_SET); // Alive LED
	MeasurementCfg_Type measurement_type = 0;

	init_register_map(&device_registers);
	init_switch_network(&device_switch_network);
	clear_switch_network(&device_switch_network);
//	pot_val_test();
	set_adc_sampling_freq(10000000UL);
	set_adc_dma_callback_routines();
	for(int i = 0; i < DVC_MAX_NUM_ADC_SAMPLES; i++){
		adc_samples_1[i] = 0xdead;
		adc_samples_2[i] = 0xdead;
		adc_samples_3[i] = 0xdead;
	}

	while(1){
		if(get_register(&device_registers,DVC_MEASUREMENT_CONFIG)%2){
			measurement_type = (get_register(&device_registers,DVC_MEASUREMENT_CONFIG)>>6) & 0xF;
			switch (measurement_type) {
				case DC_RESISTANCE:
					dvc_exec_msr_dc_resistance_2p();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				case CURRENT_VOLTAGE:
					dvc_exec_msr_current_voltage();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				case CAPACITANCE_VOLTAGE_2P:
					dvc_exec_msr_capacitance_voltage_2p();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				case IMPEDANCE_SPECTROSCOPY_2P:
					dvc_exec_msr_impedance_spectroscopy_2p();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				case TRANSFER_CHARACTERISTICS:
					dvc_exec_msr_transfer_characteristics();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				case OUTPUT_CHARACTERISTICS:
					dvc_exec_msr_output_characteristics();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				case CAPACITANCE_VOLTAGE_3P:
					dvc_exec_msr_capacitance_voltage_3p();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				case ELECTROCHEMICAL:
					dvc_exec_msr_electrochemical();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				case LOW_RESISTANCE:
					dvc_exec_msr_low_resistance();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				case PROBE_RESISTANCE:
					dvc_exec_msr_dc_resistance_4p();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				case IMPEDANCE_SPECTROSCOPY_4P:
					dvc_exec_msr_impedance_spectroscopy_4p();
					set_register(&device_registers,DVC_MEASUREMENT_CONFIG,0);
					break;
				default:
					break;
			}
		}
	}
}
