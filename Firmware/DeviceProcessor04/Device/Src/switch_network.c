/**
  ******************************************************************************
  * @file    switch_network.c
  * @brief   Relay control of the switch network.
  ******************************************************************************
  */

/*
 *	Author: JY-85
 */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "device_constants.h"
#include "device_registers.h"
#include "../Inc/switch_network.h"

extern RegisterMap_TypeDef device_registers;

static uint32_t swnt_pin_list[] = {
		 SWTCH_RLY_01_Pin,SWTCH_RLY_02_Pin,SWTCH_RLY_03_Pin,SWTCH_RLY_04_Pin
        ,SWTCH_RLY_05_Pin,SWTCH_RLY_06_Pin,SWTCH_RLY_07_Pin,SWTCH_RLY_08_Pin
        ,SWTCH_RLY_09_Pin,SWTCH_RLY_10_Pin,SWTCH_RLY_11_Pin,SWTCH_RLY_12_Pin
        ,SWTCH_RLY_13_Pin,SWTCH_RLY_14_Pin,SWTCH_RLY_15_Pin,SWTCH_RLY_16_Pin
		,SWTCH_RLY_17_Pin,SWTCH_RLY_18_Pin,SWTCH_RLY_19_Pin,SWTCH_RLY_20_Pin
		,SWTCH_RLY_21_Pin,SWTCH_RLY_22_Pin,SWTCH_RLY_23_Pin};

void init_switch_network(SwitchNetwork_TypeDef* switch_network){
	for(int i = 1; i <= DVC_TOTAL_RELAY_COUNT; i++){
		switch_network->Relays[i].RelayId = i;
		switch_network->Relays[i].AssociatedProbe = 0;
		switch_network->Relays[i].RelayState = GPIO_PIN_RESET;
		if(i < 17){
			switch_network->Relays[i].AssociatedGPIOPort = GPIOF;
		}
		else if(i == 18 || i == 19 || i == 20 || i == 23){
			switch_network->Relays[i].AssociatedGPIOPort = GPIOB;
		}
		else if(i == 17 || i == 21 || i == 22){
			switch_network->Relays[i].AssociatedGPIOPort = GPIOC;
		}
		switch_network->Relays[i].AssociatedGPIO = swnt_pin_list[i-1];
	}
	return;
}

void clear_switch_network(SwitchNetwork_TypeDef* switch_network){
	for(int i = 1; i <= DVC_TOTAL_RELAY_COUNT; i++){
		switch_network->Relays[i].RelayState = GPIO_PIN_RESET;
		HAL_GPIO_WritePin(switch_network->Relays[i].AssociatedGPIOPort,
						  switch_network->Relays[i].AssociatedGPIO,
						  switch_network->Relays[i].RelayState);
	}
	return;
}

void set_switch_network(SwitchNetwork_TypeDef* switch_network){
	if(!switch_network->ValidSwitchNetwork) return;
	for(int i = 1; i <= DVC_TOTAL_RELAY_COUNT; i++){
		HAL_GPIO_WritePin(switch_network->Relays[i].AssociatedGPIOPort,
						  switch_network->Relays[i].AssociatedGPIO,
						  switch_network->Relays[i].RelayState);
	}
	return;
}

void test_switch_network(SwitchNetwork_TypeDef* switch_network){
//	for(int i = 1; i <= DVC_TOTAL_RELAY_COUNT; i++){
//		HAL_GPIO_TogglePin(switch_network->Relays[i].AssociatedGPIOPort,
//						  switch_network->Relays[i].AssociatedGPIO);
//		HAL_Delay(2000);
//		HAL_GPIO_TogglePin(switch_network->Relays[i].AssociatedGPIOPort,
//						  switch_network->Relays[i].AssociatedGPIO);
//		HAL_Delay(2000);
//	}
	HAL_GPIO_TogglePin(switch_network->Relays[3].AssociatedGPIOPort,
					  switch_network->Relays[3].AssociatedGPIO);
	HAL_Delay(2000);
	HAL_GPIO_TogglePin(switch_network->Relays[3].AssociatedGPIOPort,
					  switch_network->Relays[3].AssociatedGPIO);
	HAL_Delay(2000);
	HAL_GPIO_TogglePin(switch_network->Relays[17].AssociatedGPIOPort,
					  switch_network->Relays[17].AssociatedGPIO);
	HAL_Delay(2000);
	HAL_GPIO_TogglePin(switch_network->Relays[17].AssociatedGPIOPort,
					  switch_network->Relays[17].AssociatedGPIO);
	HAL_Delay(2000);
	HAL_GPIO_TogglePin(switch_network->Relays[20].AssociatedGPIOPort,
					  switch_network->Relays[20].AssociatedGPIO);
	HAL_Delay(2000);
	HAL_GPIO_TogglePin(switch_network->Relays[20].AssociatedGPIOPort,
					  switch_network->Relays[20].AssociatedGPIO);
	HAL_Delay(2000);
	return;
}

void map_switch_network(SwitchNetwork_TypeDef* switch_network, uint32_t switch_network_config){
	MeasurementCfg_Type measurement_type = 0;
	measurement_type = (get_register(&device_registers,DVC_MEASUREMENT_CONFIG)>>6) & 0xF;
	// set the basic flags
	switch_network->ValidSwitchNetwork = 1;
	uint8_t volt_src_1_used = 0;
	uint8_t adc_1_used = 0;
	uint8_t adc_2_used = 0;
	uint8_t adc_3_used = 0;
	uint8_t used_probes = switch_network_config & 0x0F;

	// decode configuration values
	uint8_t probe_1_cfg = (switch_network_config >> 4) & 0x1F;
	uint8_t probe_2_cfg = (switch_network_config >> 9) & 0x1F;
	uint8_t probe_3_cfg = (switch_network_config >> 14)& 0x1F;
	uint8_t probe_4_cfg = (switch_network_config >> 19)& 0x1F;

	// decode source configurations
	uint8_t probe_1_cfg_src = (probe_1_cfg >> 2) & 0x07;
	uint8_t probe_2_cfg_src = (probe_2_cfg >> 2) & 0x07;
	uint8_t probe_3_cfg_src = (probe_3_cfg >> 2) & 0x07;
	uint8_t probe_4_cfg_src = (probe_4_cfg >> 2) & 0x07;

	// decode monitor configurations
	uint8_t probe_1_cfg_mon = (probe_1_cfg) & 0x03;
	uint8_t probe_2_cfg_mon = (probe_2_cfg) & 0x03;
	uint8_t probe_3_cfg_mon = (probe_3_cfg) & 0x03;
	uint8_t probe_4_cfg_mon = (probe_4_cfg) & 0x03;

	// --------------------------------------------------------------------
	// PROBE 1 CFG
	if(used_probes & 0x01){
		if(probe_1_cfg_src == 0){}
		else if(probe_1_cfg_src == DVC_PROBE_SUPPLY_DCV || probe_1_cfg_src == DVC_PROBE_SUPPLY_ACV){
			if(!volt_src_1_used){
				switch_network->Relays[1].RelayState = GPIO_PIN_SET;
				volt_src_1_used = 1;
			}
			else{
				switch_network->Relays[2].RelayState = GPIO_PIN_SET;
			}
		}
		else if(probe_1_cfg_src == DVC_PROBE_SUPPLY_DCI){
			switch_network->Relays[3].RelayState = GPIO_PIN_SET;
		}
		else if(probe_1_cfg_src == DVC_PROBE_SUPPLY_ACI){
			switch_network->Relays[3].RelayState = GPIO_PIN_SET;
			switch_network->Relays[21].RelayState = GPIO_PIN_SET;
		}
		else if(probe_1_cfg_src == DVC_PROBE_SUPPLY_GND){}

		if(probe_1_cfg_mon == 0){}
		else if(probe_1_cfg_mon == DVC_PROBE_MEASURE_VOL){
			adc_1_used = 1;
		}
		else if(probe_1_cfg_mon == DVC_PROBE_MEASURE_CUR){
			switch_network->Relays[4].RelayState = GPIO_PIN_SET;
			if(measurement_type == CAPACITANCE_VOLTAGE_2P || measurement_type == CAPACITANCE_VOLTAGE_3P || measurement_type == IMPEDANCE_SPECTROSCOPY_2P ){
				switch_network->Relays[22].RelayState = GPIO_PIN_SET;
				switch_network->Relays[23].RelayState = GPIO_PIN_SET;
			}
			if(measurement_type == TRANSFER_CHARACTERISTICS || measurement_type == OUTPUT_CHARACTERISTICS){
				switch_network->Relays[23].RelayState = GPIO_PIN_SET;
			}
		}

	}
	// --------------------------------------------------------------------

	// --------------------------------------------------------------------
	// PROBE 2 CFG
	if(used_probes & 0x02){
		if(probe_2_cfg_src == 0){}
		else if(probe_2_cfg_src == DVC_PROBE_SUPPLY_DCV || probe_2_cfg_src == DVC_PROBE_SUPPLY_ACV){
			if(!volt_src_1_used){
				switch_network->Relays[5].RelayState = GPIO_PIN_SET;
				volt_src_1_used = 1;
			}
			else{
				switch_network->Relays[6].RelayState = GPIO_PIN_SET;
			}
		}
		else if(probe_2_cfg_src == DVC_PROBE_SUPPLY_DCI){
			switch_network->Relays[7].RelayState = GPIO_PIN_SET;
		}
		else if(probe_2_cfg_src == DVC_PROBE_SUPPLY_ACI){
			switch_network->Relays[7].RelayState = GPIO_PIN_SET;
			switch_network->Relays[21].RelayState = GPIO_PIN_SET;
		}
		else if(probe_2_cfg_src == DVC_PROBE_SUPPLY_GND){}

		if(probe_2_cfg_mon == 0){}
		else if(probe_2_cfg_mon == DVC_PROBE_MEASURE_VOL){
			if(adc_1_used){
				switch_network->Relays[18].RelayState = GPIO_PIN_SET;
				adc_2_used = 1;
			}
			else{
				switch_network->Relays[17].RelayState = GPIO_PIN_SET;
				adc_1_used = 1;
			}
		}
		else if(probe_2_cfg_mon == DVC_PROBE_MEASURE_CUR){
			switch_network->Relays[8].RelayState = GPIO_PIN_SET;
			if(measurement_type == CAPACITANCE_VOLTAGE_2P || measurement_type == CAPACITANCE_VOLTAGE_3P || measurement_type == IMPEDANCE_SPECTROSCOPY_2P ){
				switch_network->Relays[22].RelayState = GPIO_PIN_SET;
				switch_network->Relays[23].RelayState = GPIO_PIN_SET;
			}
			if(measurement_type == TRANSFER_CHARACTERISTICS || measurement_type == OUTPUT_CHARACTERISTICS){
				switch_network->Relays[23].RelayState = GPIO_PIN_SET;
			}
		}

	}
	// --------------------------------------------------------------------

	// --------------------------------------------------------------------
	// PROBE 3 CFG
	if(used_probes & 0x04){
		if(probe_3_cfg_src == 0){}
		else if(probe_3_cfg_src == DVC_PROBE_SUPPLY_DCV || probe_3_cfg_src == DVC_PROBE_SUPPLY_ACV){
			if(!volt_src_1_used){
				switch_network->Relays[9].RelayState = GPIO_PIN_SET;
				volt_src_1_used = 1;
			}
			else{
				switch_network->Relays[10].RelayState = GPIO_PIN_SET;
			}
		}
		else if(probe_3_cfg_src == DVC_PROBE_SUPPLY_DCI){
			switch_network->Relays[11].RelayState = GPIO_PIN_SET;
		}
		else if(probe_3_cfg_src == DVC_PROBE_SUPPLY_ACI){
			switch_network->Relays[11].RelayState = GPIO_PIN_SET;
			switch_network->Relays[21].RelayState = GPIO_PIN_SET;
		}
		else if(probe_3_cfg_src == DVC_PROBE_SUPPLY_GND){}

		if(probe_3_cfg_mon == 0){}
		else if(probe_3_cfg_mon == DVC_PROBE_MEASURE_VOL){
			if(adc_1_used){
				switch_network->Relays[20].RelayState = GPIO_PIN_SET;
				adc_2_used = 1;
			}
			else{
				switch_network->Relays[19].RelayState = GPIO_PIN_SET;
				adc_1_used = 1;
			}
		}
		else if(probe_3_cfg_mon == DVC_PROBE_MEASURE_CUR){
			switch_network->Relays[12].RelayState = GPIO_PIN_SET;
			if(measurement_type == CAPACITANCE_VOLTAGE_2P || measurement_type == CAPACITANCE_VOLTAGE_3P || measurement_type == IMPEDANCE_SPECTROSCOPY_2P ){
				switch_network->Relays[22].RelayState = GPIO_PIN_SET;
				switch_network->Relays[23].RelayState = GPIO_PIN_SET;
			}
			if(measurement_type == TRANSFER_CHARACTERISTICS || measurement_type == OUTPUT_CHARACTERISTICS){
				switch_network->Relays[23].RelayState = GPIO_PIN_SET;
			}
		}
	}
	// --------------------------------------------------------------------

	// --------------------------------------------------------------------
	// PROBE 4 CFG
	if(used_probes & 0x08){
		if(probe_4_cfg_src == 0){}
		else if(probe_4_cfg_src == DVC_PROBE_SUPPLY_DCV || probe_4_cfg_src == DVC_PROBE_SUPPLY_ACV){
			if(!volt_src_1_used){
				switch_network->Relays[13].RelayState = GPIO_PIN_SET;
				volt_src_1_used = 1;
			}
			else{
				switch_network->Relays[14].RelayState = GPIO_PIN_SET;
			}
		}
		else if(probe_4_cfg_src == DVC_PROBE_SUPPLY_DCI){
			switch_network->Relays[15].RelayState = GPIO_PIN_SET;
		}
		else if(probe_4_cfg_src == DVC_PROBE_SUPPLY_ACI){
			switch_network->Relays[15].RelayState = GPIO_PIN_SET;
			switch_network->Relays[21].RelayState = GPIO_PIN_SET;
		}
		else if(probe_4_cfg_src == DVC_PROBE_SUPPLY_GND){}

		if(probe_4_cfg_mon == 0){}
		else if(probe_4_cfg_mon == DVC_PROBE_MEASURE_VOL){
			if(adc_1_used){
				switch_network->Relays[20].RelayState = GPIO_PIN_SET;
				switch_network->Relays[18].RelayState = GPIO_PIN_SET;
				adc_2_used = 1;
			}
			else{
				switch_network->Relays[19].RelayState = GPIO_PIN_SET;
				switch_network->Relays[17].RelayState = GPIO_PIN_SET;
				adc_1_used = 1;
			}
		}
		else if(probe_4_cfg_mon == DVC_PROBE_MEASURE_CUR){
			switch_network->Relays[16].RelayState = GPIO_PIN_SET;
			if(measurement_type == CAPACITANCE_VOLTAGE_2P || measurement_type == CAPACITANCE_VOLTAGE_3P || measurement_type == IMPEDANCE_SPECTROSCOPY_2P ){
				switch_network->Relays[22].RelayState = GPIO_PIN_SET;
				switch_network->Relays[23].RelayState = GPIO_PIN_SET;
			}
			if(measurement_type == TRANSFER_CHARACTERISTICS || measurement_type == OUTPUT_CHARACTERISTICS){
				switch_network->Relays[23].RelayState = GPIO_PIN_SET;
			}
		}
	}
	// --------------------------------------------------------------------
	return;
}
