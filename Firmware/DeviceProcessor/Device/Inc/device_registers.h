/*
 * device_registers.h
 *
 *  Created on: Nov 16, 2024
 *      Author: User
 */

#ifndef INC_DEVICE_REGISTERS_H_
#define INC_DEVICE_REGISTERS_H_

#include "main.h"
#include "DeviceConstants.h"

#define REG_DATA_MASK ((1 << (DVC_REGISTER_DATA_WIDTH)) - 1)

typedef struct{
	uint32_t RegData;
} Register_TypeDef;

typedef struct{
	Register_TypeDef RegisterArray[DVC_TOTAL_REGISTER_NUMBER];
} RegisterMap_TypeDef;

void init_register_map(RegisterMap_TypeDef* RegMap);
void set_register(RegisterMap_TypeDef* RegMap, uint32_t reg_addr, uint32_t data);
uint32_t get_register(RegisterMap_TypeDef* RegMap, uint32_t reg_addr);

#endif /* INC_DEVICE_REGISTERS_H_ */
