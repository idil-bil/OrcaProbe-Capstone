/*
 * measurement_routines.c
 *
 *  Created on: Feb 27, 2025
 *      Author: User
 */

#include "switch_network.h"
#include "device_sourcing.h"
#include "device_monitoring.h"
#include "device_registers.h"
#include "run_device.h"
#include "main.h"

extern I2C_HandleTypeDef hi2c2;
extern I2C_HandleTypeDef hi2c3;

extern SPI_HandleTypeDef hspi1;
extern SPI_HandleTypeDef hspi2;

extern DMA_HandleTypeDef handle_GPDMA1_Channel12;
extern DMA_HandleTypeDef handle_GPDMA1_Channel13;
extern DMA_HandleTypeDef handle_GPDMA1_Channel14;

uint8_t volt_src_dds_spi_tx_buf[] = {0x21,0x00,0x61,0x8E,0x40,0x00,0xC0,0x00,0x20,0x00};  // 400Hz
uint8_t volt_src_gain_i2c_tx_buf[] = {0,126};
uint8_t volt_src_offset_i2c_tx_buf[] = {0,126};
uint8_t curr_mrr_i2c_tx_buf[] = {0,100};

extern uint16_t adc_samples_1[DVC_MAX_NUM_ADC_SAMPLES];
extern uint16_t adc_samples_2[DVC_MAX_NUM_ADC_SAMPLES];
extern uint16_t adc_samples_3[DVC_MAX_NUM_ADC_SAMPLES];

extern RegisterMap_TypeDef device_registers;
extern SwitchNetwork_TypeDef device_switch_network;

extern volatile uint8_t adc_1_busy;
extern volatile uint8_t adc_2_busy;
extern volatile uint8_t adc_3_busy;

extern volatile uint8_t adc_1_full;
extern volatile uint8_t adc_2_full;
extern volatile uint8_t adc_3_full;

void dvc_exec_msr_dc_resistance_2p(void){
	uint32_t pot_val;
	// set busy flag to indicate a measurement is in progress
	set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
				 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) | 0x4);

	// get potentiometer value to configure current mirror
	pot_val = get_register(&device_registers,DVC_2PM_DCRESISTANCE_1);

	// prepare buffer for potentiometer I2C tx
	set_pot_buffer(curr_mrr_i2c_tx_buf,DVC_POT_AD5245_WP_WR_CMD,pot_val);

	// configure the switch network
	map_switch_network(&device_switch_network,get_register(&device_registers,DVC_PROBE_CONFIG));
	set_switch_network(&device_switch_network);

	// configure the current mirror (2 seconds delay for stabilization)
	config_current_mirror(&hi2c2,DVC_CURR_MRR_POT_I2C_ADDR,curr_mrr_i2c_tx_buf);
	HAL_Delay(2000);

	// collect ADC samples
	collect_adc_samples2(DVC_USE_ADC_2_SAMPLING);

	// wait for adc dma to complete
	while(adc_2_busy);

	// disconnect switch network to cut power
	clear_switch_network(&device_switch_network);

	// clear busy flag to indicate a measurement is complete
	set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
				 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) & ~(0x4));

}

void dvc_exec_msr_current_voltage(void){
	HAL_StatusTypeDef result;
	uint32_t pot_val_gain, pot_val_offset, pot_val_curr_mirr, method_sel, dds_freq_val;
	uint32_t start_param, end_param, incr_param;

	// set busy flag to indicate a measurement is in progress
	set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
				 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) | 0x4);

	// grab the measurement parameters from the registers;
	method_sel = get_register(&device_registers,DVC_2PM_CURRVOLT_1) & 0x3;
	start_param = get_register(&device_registers,DVC_2PM_CURRVOLT_2);
	end_param = get_register(&device_registers,DVC_2PM_CURRVOLT_3);
	incr_param = get_register(&device_registers,DVC_2PM_CURRVOLT_4);

	// configure the basic DC voltage source with 0Hz
	dds_freq_val = 4295;
	pot_val_offset = 64;
	set_ad9833_dds_buffer(volt_src_dds_spi_tx_buf,dds_freq_val);
	set_pot_buffer(volt_src_offset_i2c_tx_buf,DVC_POT_MCP4531_WP0_WR_CMD,pot_val_offset);
	config_dds_freq(&hspi2,volt_src_dds_spi_tx_buf);
	config_volt_src_offset(&hi2c3,DVC_VOLT_SRC_1_OFS_POT_I2C_ADDR,volt_src_offset_i2c_tx_buf);

	// configure the switch network
	map_switch_network(&device_switch_network,get_register(&device_registers,DVC_PROBE_CONFIG));
	set_switch_network(&device_switch_network);

	for(int param = start_param; param <= end_param; param += incr_param){
		if(method_sel == DVC_CUR_VOLT_2P_SEL_VOLT){
			pot_val_gain = param;
			set_pot_buffer(volt_src_gain_i2c_tx_buf,DVC_POT_MCP4531_WP0_WR_CMD,pot_val_gain);
			config_volt_src_gain(&hi2c3,DVC_VOLT_SRC_1_AMP_POT_I2C_ADDR,volt_src_gain_i2c_tx_buf);
			HAL_Delay(6000);
		}
		else if (method_sel == DVC_CUR_VOLT_2P_SEL_CURR){
			pot_val_curr_mirr = calculate_pot_value_curr_mirr((float)param);
			set_pot_buffer(curr_mrr_i2c_tx_buf,DVC_POT_AD5245_WP_WR_CMD,pot_val_curr_mirr);
			config_current_mirror(&hi2c2,DVC_CURR_MRR_POT_I2C_ADDR,curr_mrr_i2c_tx_buf);
			HAL_Delay(3000);
		}

		// collect ADC samples
		collect_adc_samples2(DVC_USE_ADC_2_SAMPLING);

		// wait for adc dma to complete
		while(adc_2_busy);

		// clear busy flag to indicate a measurement is complete
		set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
					 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) & ~(0x4));

		// wait for python to grab the data
		while(adc_2_full);

		// set busy flag to indicate a measurement is in progress
		set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
					 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) | 0x4);
	}

	// disconnect switch network to cut power
	clear_switch_network(&device_switch_network);

	// clear busy flag to indicate a measurement is complete
	set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
				 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) & ~(0x4));
}

void dvc_exec_msr_capacitance_voltage_2p(void){

}

void dvc_exec_msr_impedance_spectroscopy_2p(void){
	HAL_StatusTypeDef result;
	uint32_t pot_val_gain, pot_val_offset;

	// set busy flag to indicate a measurement is in progress
	set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
				 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) | 0x4);

	// grab the measurement parameters from the registers;
	uint32_t start_freq_l14b = get_register(&device_registers,DVC_2PM_IMPSPEC_1);
	uint32_t start_freq_u14b = get_register(&device_registers,DVC_2PM_IMPSPEC_2);
	uint32_t end_freq_l14b = get_register(&device_registers,DVC_2PM_IMPSPEC_3);
	uint32_t end_freq_u14b = get_register(&device_registers,DVC_2PM_IMPSPEC_4);
	uint32_t incr_freq_l14b = get_register(&device_registers,DVC_2PM_IMPSPEC_5);
	uint32_t incr_freq_u14b = get_register(&device_registers,DVC_2PM_IMPSPEC_6);
	uint32_t max_volt = get_register(&device_registers,DVC_2PM_IMPSPEC_7);
	uint32_t min_volt = get_register(&device_registers,DVC_2PM_IMPSPEC_8);

	// configure the basic DC voltage source with 0Hz
	uint32_t start_freq_28b = (start_freq_u14b << 14) | start_freq_l14b;
	uint32_t end_freq_28b = (end_freq_u14b << 14) | end_freq_l14b;
	uint32_t incr_freq_28b = (incr_freq_u14b << 14) | incr_freq_l14b;
	pot_val_offset = 64;
	pot_val_gain = 64;
	set_pot_buffer(volt_src_offset_i2c_tx_buf,DVC_POT_MCP4531_WP0_WR_CMD,pot_val_offset);
	set_pot_buffer(volt_src_gain_i2c_tx_buf,DVC_POT_MCP4531_WP0_WR_CMD,pot_val_gain);
	config_volt_src_offset(&hi2c3,DVC_VOLT_SRC_1_OFS_POT_I2C_ADDR,volt_src_offset_i2c_tx_buf);
	config_volt_src_gain(&hi2c3,DVC_VOLT_SRC_1_AMP_POT_I2C_ADDR,volt_src_gain_i2c_tx_buf);

	// configure the switch network
	map_switch_network(&device_switch_network,get_register(&device_registers,DVC_PROBE_CONFIG));
	set_switch_network(&device_switch_network);

	for(int param = start_freq_28b; param <= end_freq_28b; param += incr_freq_28b){
		set_ad9833_dds_buffer(volt_src_dds_spi_tx_buf,param);
		config_dds_freq(&hspi2,volt_src_dds_spi_tx_buf);
		HAL_Delay(3000);

		// collect ADC samples
		collect_adc_samples2(DVC_USE_ADC_2_SAMPLING | DVC_USE_ADC_1_SAMPLING);

		// wait for adc dma to complete
		while(adc_2_busy || adc_1_busy);

		// clear busy flag to indicate a measurement is complete
		set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
					 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) & ~(0x4));

		// wait for python to grab the data
		while(adc_2_full || adc_1_full);

		// set busy flag to indicate a measurement is in progress
		set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
					 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) | 0x4);
	}

	// disconnect switch network to cut power
	clear_switch_network(&device_switch_network);

	// clear busy flag to indicate a measurement is complete
	set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
				 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) & ~(0x4));
}

void dvc_exec_msr_transfer_characteristics(void){

}

void dvc_exec_msr_output_characteristics(void){

}

void dvc_exec_msr_capacitance_voltage_3p(void){

}

void dvc_exec_msr_electrochemical(void){

}

void dvc_exec_msr_low_resistance(void){

}

void dvc_exec_msr_dc_resistance_4p(void){
	uint32_t pot_val;
	// set busy flag to indicate a measurement is in progress
	set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
				 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) | 0x4);

	// get potentiometer value to configure current mirror
	pot_val = get_register(&device_registers,DVC_4PM_PROBERESISTANCE_1);

	// prepare buffer for potentiometer I2C tx
	set_pot_buffer(curr_mrr_i2c_tx_buf,DVC_POT_AD5245_WP_WR_CMD,pot_val);

	// configure the switch network
	map_switch_network(&device_switch_network,get_register(&device_registers,DVC_PROBE_CONFIG));
	set_switch_network(&device_switch_network);

	// configure the current mirror (2 seconds delay for stabilization)
	config_current_mirror(&hi2c2,DVC_CURR_MRR_POT_I2C_ADDR,curr_mrr_i2c_tx_buf);
	HAL_Delay(2000);

	// collect ADC samples
	collect_adc_samples2(DVC_USE_ADC_2_SAMPLING | DVC_USE_ADC_1_SAMPLING);

	// wait for adc dma to complete
	while(adc_2_busy || adc_1_busy);

	// disconnect switch network to cut power
	clear_switch_network(&device_switch_network);

	// clear busy flag to indicate a measurement is complete
	set_register(&device_registers,DVC_MEASUREMENT_CONFIG,
				 get_register(&device_registers,DVC_MEASUREMENT_CONFIG) & ~(0x4));

	// wait for python to grab the data
	while(adc_2_full || adc_1_full);
}

void dvc_exec_msr_impedance_spectroscopy_4p(void){

}
