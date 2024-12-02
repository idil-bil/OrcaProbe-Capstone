/*
 * switch_network.h
 *
 *  Created on: Nov 16, 2024
 *      Author: User
 */

#ifndef INC_SWITCH_NETWORK_H_
#define INC_SWITCH_NETWORK_H_

#include "run_device.h"

typedef struct{
	uint8_t RelayId;
	ProbeId_Type AssociatedProbe;
	bool RelayState;
	GPIO_TypeDef AssociatedGPIOPort;
	uint16_t AssociatedGPIO;
} SwitchRelay_TypeDef;

typedef struct{
	SwitchRelay_TypeDef Relays[DVC_TOTAL_RELAY_COUNT];
	bool ValidSwitchNetwork;
} SwitchNetwork_TypeDef;

#endif /* INC_SWITCH_NETWORK_H_ */
