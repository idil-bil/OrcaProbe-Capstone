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
	GPIO_PinState RelayState;
	GPIO_TypeDef *AssociatedGPIOPort;
	uint16_t AssociatedGPIO;
} SwitchRelay_TypeDef;

typedef struct{
	SwitchRelay_TypeDef Relays[DVC_TOTAL_RELAY_COUNT];
	bool ValidSwitchNetwork;
} SwitchNetwork_TypeDef;

void DVC_Clear_Switch_Network(SwitchNetwork_TypeDef switch_network);
void DVC_Set_Switch_Network(SwitchNetwork_TypeDef switch_network);
void DVC_Map_Switch_Network(SwitchNetwork_TypeDef switch_network, uint32_t switch_network_state);

#endif /* INC_SWITCH_NETWORK_H_ */
