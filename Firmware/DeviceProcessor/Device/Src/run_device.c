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

extern ADC_HandleTypeDef hadc1;

extern UART_HandleTypeDef huart1;

extern PCD_HandleTypeDef hpcd_USB_OTG_FS;

extern SPI_HandleTypeDef hspi1;

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

uint8_t uartRxBuffer[4];  // 12Hz

void run_device(){
	init_register_map(&device_registers);

	HAL_SPI_Transmit(&hspi1, spiTxBuffer1, 10, 1000); //Sending in Blocking mode
	HAL_Delay(100);
	while(1){
        if (HAL_UART_Receive(&huart1, uartRxBuffer, 4, HAL_MAX_DELAY) == HAL_OK) {
            // Combine the received bytes into a 32-bit variable
            uint32_t receivedData = (uartRxBuffer[3] << 24) |
                                    (uartRxBuffer[2] << 16) |
                                    (uartRxBuffer[1] << 8)  |
                                     uartRxBuffer[0];

            // Parse the received data
            uint8_t address = (receivedData >> 24) & 0xFF; // Upper 8 bits
			uint32_t data = receivedData & 0xFFFFFF;       // Lower 24 bits

			if(address == 0){
				if(data == 1){
					HAL_SPI_Transmit(&hspi1, spiTxBuffer1, 10, 1000); //Sending in Blocking mode
					HAL_Delay(100);
				}
				else if(data == 2){
					HAL_SPI_Transmit(&hspi1, spiTxBuffer2, 10, 1000); //Sending in Blocking mode
					HAL_Delay(100);
				}
				else if(data == 3){
					HAL_SPI_Transmit(&hspi1, spiTxBuffer3, 10, 1000); //Sending in Blocking mode
					HAL_Delay(100);
				}
				else if(data == 4){
					HAL_SPI_Transmit(&hspi1, spiTxBuffer4, 10, 1000); //Sending in Blocking mode
					HAL_Delay(100);
				}
				else if(data == 5){
					HAL_SPI_Transmit(&hspi1, spiTxBuffer5, 10, 1000); //Sending in Blocking mode
					HAL_Delay(100);
				}
				else if(data == 6){
					HAL_SPI_Transmit(&hspi1, spiTxBuffer6, 10, 1000); //Sending in Blocking mode
					HAL_Delay(100);
				}
				else if(data == 7){
					HAL_SPI_Transmit(&hspi1, spiTxBuffer7, 10, 1000); //Sending in Blocking mode
					HAL_Delay(100);
				}
				else if(data == 8){
					HAL_SPI_Transmit(&hspi1, spiTxBuffer8, 10, 1000); //Sending in Blocking mode
					HAL_Delay(100);
				}
				else if(data == 9){
					HAL_SPI_Transmit(&hspi1, spiTxBuffer9, 10, 1000); //Sending in Blocking mode
					HAL_Delay(100);
				}
			}
			else if(address == 1){
				HAL_GPIO_WritePin(GPIOB,GPIO_PIN_11,GPIO_PIN_RESET);
				HAL_Delay(300);
				HAL_GPIO_WritePin(GPIOB,GPIO_PIN_10,GPIO_PIN_RESET);
				HAL_Delay(300);
				HAL_GPIO_WritePin(GPIOE,GPIO_PIN_15,GPIO_PIN_RESET);
				HAL_Delay(300);
				HAL_GPIO_WritePin(GPIOE,GPIO_PIN_14,GPIO_PIN_RESET);
				HAL_Delay(300);
				if(data == 1){
					HAL_GPIO_WritePin(GPIOB,GPIO_PIN_11,GPIO_PIN_SET);
					HAL_Delay(100);
				}
				else if(data == 2){
					HAL_GPIO_WritePin(GPIOB,GPIO_PIN_10,GPIO_PIN_SET);
					HAL_Delay(100);
				}
				else if(data == 3){
					HAL_GPIO_WritePin(GPIOE,GPIO_PIN_15,GPIO_PIN_SET);
					HAL_Delay(100);
				}
				else if(data == 4){
					HAL_GPIO_WritePin(GPIOE,GPIO_PIN_14,GPIO_PIN_SET);
					HAL_Delay(100);
				}
			}
        }
	}
}
