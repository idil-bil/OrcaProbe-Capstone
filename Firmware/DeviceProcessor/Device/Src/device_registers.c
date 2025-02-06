/*
 * device_registers.c
 *
 *  Created on: Nov 16, 2024
 *      Author: User
 */

#include "../Inc/device_registers.h"

void init_register_map(RegisterMap_TypeDef* RegMap){
	for(int i = 0; i < DVC_TOTAL_REGISTER_NUMBER; i++){
		RegMap->RegisterArray[i].RegData = 0xdeadbeef;
	}
}

uint32_t get_register(RegisterMap_TypeDef* RegMap, uint32_t reg_addr){
	return (REG_DATA_MASK & RegMap->RegisterArray[reg_addr].RegData);
}

void set_register(RegisterMap_TypeDef* RegMap, uint32_t reg_addr, uint32_t data){
	RegMap->RegisterArray[reg_addr].RegData = (REG_DATA_MASK & data);
}
