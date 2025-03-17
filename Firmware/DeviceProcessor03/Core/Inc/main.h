/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32u5xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define ADCV1_D13_Pin GPIO_PIN_2
#define ADCV1_D13_GPIO_Port GPIOE
#define ADCV1_D12_Pin GPIO_PIN_3
#define ADCV1_D12_GPIO_Port GPIOE
#define ADCV1_D11_Pin GPIO_PIN_4
#define ADCV1_D11_GPIO_Port GPIOE
#define ADCV1_D10_Pin GPIO_PIN_5
#define ADCV1_D10_GPIO_Port GPIOE
#define ADCV1_D09_Pin GPIO_PIN_6
#define ADCV1_D09_GPIO_Port GPIOE
#define ADCV2_D00_Pin GPIO_PIN_0
#define ADCV2_D00_GPIO_Port GPIOF
#define ADCV2_D01_Pin GPIO_PIN_1
#define ADCV2_D01_GPIO_Port GPIOF
#define ADCV2_D02_Pin GPIO_PIN_2
#define ADCV2_D02_GPIO_Port GPIOF
#define ADCV2_D03_Pin GPIO_PIN_3
#define ADCV2_D03_GPIO_Port GPIOF
#define ADCV2_D04_Pin GPIO_PIN_4
#define ADCV2_D04_GPIO_Port GPIOF
#define ADCV2_D05_Pin GPIO_PIN_5
#define ADCV2_D05_GPIO_Port GPIOF
#define ADCV2_D06_Pin GPIO_PIN_6
#define ADCV2_D06_GPIO_Port GPIOF
#define ADCV2_D07_Pin GPIO_PIN_7
#define ADCV2_D07_GPIO_Port GPIOF
#define ADCV2_D08_Pin GPIO_PIN_8
#define ADCV2_D08_GPIO_Port GPIOF
#define ADCV2_D09_Pin GPIO_PIN_9
#define ADCV2_D09_GPIO_Port GPIOF
#define ADCV2_D10_Pin GPIO_PIN_10
#define ADCV2_D10_GPIO_Port GPIOF
#define I2C_DAC1_POT_SCL_Pin GPIO_PIN_0
#define I2C_DAC1_POT_SCL_GPIO_Port GPIOC
#define I2C_DAC1_POT_SDA_Pin GPIO_PIN_1
#define I2C_DAC1_POT_SDA_GPIO_Port GPIOC
#define SPI_DAC1_MISO_Pin GPIO_PIN_2
#define SPI_DAC1_MISO_GPIO_Port GPIOC
#define SPI_DAC2_SCK_Pin GPIO_PIN_1
#define SPI_DAC2_SCK_GPIO_Port GPIOA
#define SPI_DAC2_NSS_Pin GPIO_PIN_4
#define SPI_DAC2_NSS_GPIO_Port GPIOA
#define SPI_DAC2_MISO_Pin GPIO_PIN_6
#define SPI_DAC2_MISO_GPIO_Port GPIOA
#define SPI_DAC2_MOSI_Pin GPIO_PIN_7
#define SPI_DAC2_MOSI_GPIO_Port GPIOA
#define ADCV2_D11_Pin GPIO_PIN_11
#define ADCV2_D11_GPIO_Port GPIOF
#define ADCV2_D12_Pin GPIO_PIN_12
#define ADCV2_D12_GPIO_Port GPIOF
#define ADCV2_D13_Pin GPIO_PIN_13
#define ADCV2_D13_GPIO_Port GPIOF
#define ADCV2_D14_Pin GPIO_PIN_14
#define ADCV2_D14_GPIO_Port GPIOF
#define ADCV2_D15_Pin GPIO_PIN_15
#define ADCV2_D15_GPIO_Port GPIOF
#define SWNT_CTRL_01_Pin GPIO_PIN_0
#define SWNT_CTRL_01_GPIO_Port GPIOG
#define SWNT_CTRL_02_Pin GPIO_PIN_1
#define SWNT_CTRL_02_GPIO_Port GPIOG
#define ADCV1_D08_Pin GPIO_PIN_7
#define ADCV1_D08_GPIO_Port GPIOE
#define ADCV1_D07_Pin GPIO_PIN_8
#define ADCV1_D07_GPIO_Port GPIOE
#define ADCV1_D06_Pin GPIO_PIN_9
#define ADCV1_D06_GPIO_Port GPIOE
#define ADCV1_D05_Pin GPIO_PIN_10
#define ADCV1_D05_GPIO_Port GPIOE
#define ADCV1_D04_Pin GPIO_PIN_11
#define ADCV1_D04_GPIO_Port GPIOE
#define ADCV1_D03_Pin GPIO_PIN_12
#define ADCV1_D03_GPIO_Port GPIOE
#define ADCV1_D02_Pin GPIO_PIN_13
#define ADCV1_D02_GPIO_Port GPIOE
#define ADCV1_D01_Pin GPIO_PIN_14
#define ADCV1_D01_GPIO_Port GPIOE
#define ADCV1_D00_Pin GPIO_PIN_15
#define ADCV1_D00_GPIO_Port GPIOE
#define I2C_DAC2_CURR_POT_SCL_Pin GPIO_PIN_13
#define I2C_DAC2_CURR_POT_SCL_GPIO_Port GPIOB
#define I2C_DAC2_CURR_POT_SDA_Pin GPIO_PIN_14
#define I2C_DAC2_CURR_POT_SDA_GPIO_Port GPIOB
#define SWNT_CTRL_20_Pin GPIO_PIN_8
#define SWNT_CTRL_20_GPIO_Port GPIOD
#define SWNT_CTRL_21_Pin GPIO_PIN_9
#define SWNT_CTRL_21_GPIO_Port GPIOD
#define SWNT_CTRL_03_Pin GPIO_PIN_2
#define SWNT_CTRL_03_GPIO_Port GPIOG
#define SWNT_CTRL_04_Pin GPIO_PIN_3
#define SWNT_CTRL_04_GPIO_Port GPIOG
#define SWNT_CTRL_05_Pin GPIO_PIN_4
#define SWNT_CTRL_05_GPIO_Port GPIOG
#define SWNT_CTRL_06_Pin GPIO_PIN_5
#define SWNT_CTRL_06_GPIO_Port GPIOG
#define SWNT_CTRL_07_Pin GPIO_PIN_6
#define SWNT_CTRL_07_GPIO_Port GPIOG
#define SWNT_CTRL_08_Pin GPIO_PIN_7
#define SWNT_CTRL_08_GPIO_Port GPIOG
#define SWNT_CTRL_09_Pin GPIO_PIN_8
#define SWNT_CTRL_09_GPIO_Port GPIOG
#define ADC_CLK_Pin GPIO_PIN_7
#define ADC_CLK_GPIO_Port GPIOC
#define SPI_DAC1_NSS_Pin GPIO_PIN_0
#define SPI_DAC1_NSS_GPIO_Port GPIOD
#define ADCV1_OTR_Pin GPIO_PIN_1
#define ADCV1_OTR_GPIO_Port GPIOD
#define ADCV2_OTR_Pin GPIO_PIN_2
#define ADCV2_OTR_GPIO_Port GPIOD
#define SPI_DAC1_SCK_Pin GPIO_PIN_3
#define SPI_DAC1_SCK_GPIO_Port GPIOD
#define SPI_DAC1_MOSI_Pin GPIO_PIN_4
#define SPI_DAC1_MOSI_GPIO_Port GPIOD
#define SWNT_CTRL_17_Pin GPIO_PIN_5
#define SWNT_CTRL_17_GPIO_Port GPIOD
#define SWNT_CTRL_18_Pin GPIO_PIN_6
#define SWNT_CTRL_18_GPIO_Port GPIOD
#define SWNT_CTRL_19_Pin GPIO_PIN_7
#define SWNT_CTRL_19_GPIO_Port GPIOD
#define SWNT_CTRL_10_Pin GPIO_PIN_9
#define SWNT_CTRL_10_GPIO_Port GPIOG
#define SWNT_CTRL_11_Pin GPIO_PIN_10
#define SWNT_CTRL_11_GPIO_Port GPIOG
#define SWNT_CTRL_12_Pin GPIO_PIN_11
#define SWNT_CTRL_12_GPIO_Port GPIOG
#define SWNT_CTRL_13_Pin GPIO_PIN_12
#define SWNT_CTRL_13_GPIO_Port GPIOG
#define SWNT_CTRL_14_Pin GPIO_PIN_13
#define SWNT_CTRL_14_GPIO_Port GPIOG
#define SWNT_CTRL_15_Pin GPIO_PIN_14
#define SWNT_CTRL_15_GPIO_Port GPIOG
#define SWNT_CTRL_16_Pin GPIO_PIN_15
#define SWNT_CTRL_16_GPIO_Port GPIOG
#define ADCV1_D15_Pin GPIO_PIN_0
#define ADCV1_D15_GPIO_Port GPIOE
#define ADCV1_D14_Pin GPIO_PIN_1
#define ADCV1_D14_GPIO_Port GPIOE

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
