/*
 * run_device.c
 *
 *  Created on: Nov 16, 2024
 *      Author: User
 */

#include "main.h"
#include "../Inc/run_device.h"
#include "../Inc/switch_network.h"
#include "../Inc/device_registers.h"

//extern ADC_HandleTypeDef hadc1;

extern UART_HandleTypeDef huart1;

extern PCD_HandleTypeDef hpcd_USB_OTG_FS;
extern TIM_HandleTypeDef htim8;
extern DMA_HandleTypeDef handle_GPDMA1_Channel12;

extern SPI_HandleTypeDef hspi1;
extern SPI_HandleTypeDef hspi3;

RegisterMap_TypeDef device_registers;

uint8_t spiTxBuffer1[] = {0x21,0x00,0x50,0xC7,0x40,0x00,0xC0,0x00,0x20,0x00};  // 400Hz
uint8_t spiTxBuffer2[] = {0x21,0x00,0x61,0x8E,0x40,0x00,0xC0,0x00,0x20,0x00};  // 800Hz
uint8_t spiTxBuffer3[] = {0x21,0x00,0x63,0x6E,0x40,0x06,0xC0,0x00,0x20,0x00};  // 10kHz
uint8_t spiTxBuffer4[] = {0x21,0x00,0x6B,0x85,0x41,0x47,0xC0,0x00,0x20,0x00};  // 0.5MHz
uint8_t spiTxBuffer5[] = {0x21,0x00,0x59,0x9A,0x46,0x66,0xC0,0x00,0x20,0x00};  // 2.5MHz
uint8_t spiTxBuffer6[] = {0x21,0x00,0x66,0x66,0x59,0x99,0xC0,0x00,0x20,0x00};  // 10MHz

uint8_t spiTxBuffer7[] = {0x21,0x00,0x40,0x6B,0x40,0x00,0xC0,0x00,0x20,0x00};  // 10Hz
uint8_t spiTxBuffer8[] = {0x21,0x00,0x40,0x76,0x40,0x00,0xC0,0x00,0x20,0x00};  // 11Hz
uint8_t spiTxBuffer9[] = {0x21,0x00,0x40,0x81,0x40,0x00,0xC0,0x00,0x20,0x00};  // 12Hz


uint8_t spiTxBuffer10[] = {0,118}; //0.050
uint8_t spiTxBuffer11[] = {0,98};  //0.060
uint8_t spiTxBuffer12[] = {0,83};  //0.070
uint8_t spiTxBuffer13[] = {0,64};  //0.080
uint8_t spiTxBuffer14[] = {0,64}; //0.040

uint8_t uartRxBuffer[4];  // 12Hz
uint16_t uartTxBuffer[16];  // 12Hz

void run_device(){
	uint16_t dmaValCheck[500];
	uint16_t dmaValCheck2[500];
	for(int i = 0; i < 500; i++){
	  dmaValCheck[i] = i;
	}
	for(int i = 0; i < 500; i++){
		dmaValCheck2[i] = i;
	}
	init_register_map(&device_registers);
	HAL_Delay(100);
	TIM8->ARR = 32-1;
	TIM8->DIER = TIM_DIER_UDE;
	HAL_TIM_OC_Start(&htim8, TIM_CHANNEL_1);
	TIM8->DIER = TIM_DIER_UDE;
	while(1){
//		HAL_SPI_Transmit(&hspi1, spiTxBuffer14, 2, 1000);
//		HAL_DMA_Start(&handle_GPDMA1_Channel12,(uint32_t)&GPIOE->IDR,(uint32_t)&dmaValCheck2,500*sizeof(uint16_t));
//		HAL_DMA_Abort(&handle_GPDMA1_Channel12);
	}
}
