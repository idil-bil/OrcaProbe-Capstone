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
#define ADC1_D02_Pin GPIO_PIN_2
#define ADC1_D02_GPIO_Port GPIOE
#define ADC1_D03_Pin GPIO_PIN_3
#define ADC1_D03_GPIO_Port GPIOE
#define ADC1_D04_Pin GPIO_PIN_4
#define ADC1_D04_GPIO_Port GPIOE
#define ADC1_D05_Pin GPIO_PIN_5
#define ADC1_D05_GPIO_Port GPIOE
#define ADC1_D06_Pin GPIO_PIN_6
#define ADC1_D06_GPIO_Port GPIOE
#define USER_LED_Pin GPIO_PIN_13
#define USER_LED_GPIO_Port GPIOC
#define SWTCH_RLY_01_Pin GPIO_PIN_0
#define SWTCH_RLY_01_GPIO_Port GPIOF
#define SWTCH_RLY_02_Pin GPIO_PIN_1
#define SWTCH_RLY_02_GPIO_Port GPIOF
#define SWTCH_RLY_03_Pin GPIO_PIN_2
#define SWTCH_RLY_03_GPIO_Port GPIOF
#define SWTCH_RLY_04_Pin GPIO_PIN_3
#define SWTCH_RLY_04_GPIO_Port GPIOF
#define SWTCH_RLY_05_Pin GPIO_PIN_4
#define SWTCH_RLY_05_GPIO_Port GPIOF
#define SWTCH_RLY_06_Pin GPIO_PIN_5
#define SWTCH_RLY_06_GPIO_Port GPIOF
#define SWTCH_RLY_07_Pin GPIO_PIN_6
#define SWTCH_RLY_07_GPIO_Port GPIOF
#define SWTCH_RLY_08_Pin GPIO_PIN_7
#define SWTCH_RLY_08_GPIO_Port GPIOF
#define SWTCH_RLY_09_Pin GPIO_PIN_8
#define SWTCH_RLY_09_GPIO_Port GPIOF
#define SWTCH_RLY_10_Pin GPIO_PIN_9
#define SWTCH_RLY_10_GPIO_Port GPIOF
#define SWTCH_RLY_11_Pin GPIO_PIN_10
#define SWTCH_RLY_11_GPIO_Port GPIOF
#define I2C_DAC2_CURMR_POT_SCL_Pin GPIO_PIN_0
#define I2C_DAC2_CURMR_POT_SCL_GPIO_Port GPIOC
#define I2C_DAC2_CURMR_POT_SDA_Pin GPIO_PIN_1
#define I2C_DAC2_CURMR_POT_SDA_GPIO_Port GPIOC
#define SPI_DAC1_MISO_Pin GPIO_PIN_2
#define SPI_DAC1_MISO_GPIO_Port GPIOC
#define SWTCH_RLY_21_Pin GPIO_PIN_3
#define SWTCH_RLY_21_GPIO_Port GPIOC
#define SPI_DAC2_SCK_Pin GPIO_PIN_1
#define SPI_DAC2_SCK_GPIO_Port GPIOA
#define SPI_DAC2_NSS_Pin GPIO_PIN_4
#define SPI_DAC2_NSS_GPIO_Port GPIOA
#define SPI_DAC2_MISO_Pin GPIO_PIN_6
#define SPI_DAC2_MISO_GPIO_Port GPIOA
#define SPI_DAC2_MOSI_Pin GPIO_PIN_7
#define SPI_DAC2_MOSI_GPIO_Port GPIOA
#define SWTCH_RLY_22_Pin GPIO_PIN_4
#define SWTCH_RLY_22_GPIO_Port GPIOC
#define SWTCH_RLY_17_Pin GPIO_PIN_5
#define SWTCH_RLY_17_GPIO_Port GPIOC
#define SWTCH_RLY_18_Pin GPIO_PIN_0
#define SWTCH_RLY_18_GPIO_Port GPIOB
#define SWTCH_RLY_19_Pin GPIO_PIN_1
#define SWTCH_RLY_19_GPIO_Port GPIOB
#define SWTCH_RLY_20_Pin GPIO_PIN_2
#define SWTCH_RLY_20_GPIO_Port GPIOB
#define SWTCH_RLY_12_Pin GPIO_PIN_11
#define SWTCH_RLY_12_GPIO_Port GPIOF
#define SWTCH_RLY_13_Pin GPIO_PIN_12
#define SWTCH_RLY_13_GPIO_Port GPIOF
#define SWTCH_RLY_14_Pin GPIO_PIN_13
#define SWTCH_RLY_14_GPIO_Port GPIOF
#define SWTCH_RLY_15_Pin GPIO_PIN_14
#define SWTCH_RLY_15_GPIO_Port GPIOF
#define SWTCH_RLY_16_Pin GPIO_PIN_15
#define SWTCH_RLY_16_GPIO_Port GPIOF
#define ADC3_D00_Pin GPIO_PIN_0
#define ADC3_D00_GPIO_Port GPIOG
#define ADC3_D01_Pin GPIO_PIN_1
#define ADC3_D01_GPIO_Port GPIOG
#define ADC1_D07_Pin GPIO_PIN_7
#define ADC1_D07_GPIO_Port GPIOE
#define ADC1_D08_Pin GPIO_PIN_8
#define ADC1_D08_GPIO_Port GPIOE
#define ADC1_D09_Pin GPIO_PIN_9
#define ADC1_D09_GPIO_Port GPIOE
#define ADC1_D10_Pin GPIO_PIN_10
#define ADC1_D10_GPIO_Port GPIOE
#define ADC1_D11_Pin GPIO_PIN_11
#define ADC1_D11_GPIO_Port GPIOE
#define ADC1_OTR_Pin GPIO_PIN_12
#define ADC1_OTR_GPIO_Port GPIOE
#define ADC1_D13_Pin GPIO_PIN_13
#define ADC1_D13_GPIO_Port GPIOE
#define ADC1_D14_Pin GPIO_PIN_14
#define ADC1_D14_GPIO_Port GPIOE
#define ADC1_D15_Pin GPIO_PIN_15
#define ADC1_D15_GPIO_Port GPIOE
#define SWTCH_RLY_23_Pin GPIO_PIN_12
#define SWTCH_RLY_23_GPIO_Port GPIOB
#define SPI_DAC1_SCK_Pin GPIO_PIN_13
#define SPI_DAC1_SCK_GPIO_Port GPIOB
#define SPI_DAC1_MOSI_Pin GPIO_PIN_15
#define SPI_DAC1_MOSI_GPIO_Port GPIOB
#define ADC2_D08_Pin GPIO_PIN_8
#define ADC2_D08_GPIO_Port GPIOD
#define ADC2_D09_Pin GPIO_PIN_9
#define ADC2_D09_GPIO_Port GPIOD
#define ADC2_D10_Pin GPIO_PIN_10
#define ADC2_D10_GPIO_Port GPIOD
#define ADC2_D11_Pin GPIO_PIN_11
#define ADC2_D11_GPIO_Port GPIOD
#define ADC2_OTR_Pin GPIO_PIN_12
#define ADC2_OTR_GPIO_Port GPIOD
#define ADC2_D13_Pin GPIO_PIN_13
#define ADC2_D13_GPIO_Port GPIOD
#define ADC2_D14_Pin GPIO_PIN_14
#define ADC2_D14_GPIO_Port GPIOD
#define ADC2_D15_Pin GPIO_PIN_15
#define ADC2_D15_GPIO_Port GPIOD
#define ADC3_D02_Pin GPIO_PIN_2
#define ADC3_D02_GPIO_Port GPIOG
#define ADC3_D03_Pin GPIO_PIN_3
#define ADC3_D03_GPIO_Port GPIOG
#define ADC3_D04_Pin GPIO_PIN_4
#define ADC3_D04_GPIO_Port GPIOG
#define ADC3_D05_Pin GPIO_PIN_5
#define ADC3_D05_GPIO_Port GPIOG
#define ADC3_D06_Pin GPIO_PIN_6
#define ADC3_D06_GPIO_Port GPIOG
#define ADC3_D07_Pin GPIO_PIN_7
#define ADC3_D07_GPIO_Port GPIOG
#define ADC3_D08_Pin GPIO_PIN_8
#define ADC3_D08_GPIO_Port GPIOG
#define ADC_CLK_Pin GPIO_PIN_7
#define ADC_CLK_GPIO_Port GPIOC
#define ADC2_D00_Pin GPIO_PIN_0
#define ADC2_D00_GPIO_Port GPIOD
#define ADC2_D01_Pin GPIO_PIN_1
#define ADC2_D01_GPIO_Port GPIOD
#define ADC2_D02_Pin GPIO_PIN_2
#define ADC2_D02_GPIO_Port GPIOD
#define ADC2_D03_Pin GPIO_PIN_3
#define ADC2_D03_GPIO_Port GPIOD
#define ADC2_D04_Pin GPIO_PIN_4
#define ADC2_D04_GPIO_Port GPIOD
#define ADC2_D05_Pin GPIO_PIN_5
#define ADC2_D05_GPIO_Port GPIOD
#define ADC2_D06_Pin GPIO_PIN_6
#define ADC2_D06_GPIO_Port GPIOD
#define ADC2_D07_Pin GPIO_PIN_7
#define ADC2_D07_GPIO_Port GPIOD
#define ADC3_D09_Pin GPIO_PIN_9
#define ADC3_D09_GPIO_Port GPIOG
#define ADC3_D10_Pin GPIO_PIN_10
#define ADC3_D10_GPIO_Port GPIOG
#define ADC3_D11_Pin GPIO_PIN_11
#define ADC3_D11_GPIO_Port GPIOG
#define ADC3_OTR_Pin GPIO_PIN_12
#define ADC3_OTR_GPIO_Port GPIOG
#define ADC3_D13_Pin GPIO_PIN_13
#define ADC3_D13_GPIO_Port GPIOG
#define ADC3_D14_Pin GPIO_PIN_14
#define ADC3_D14_GPIO_Port GPIOG
#define ADC3_D15_Pin GPIO_PIN_15
#define ADC3_D15_GPIO_Port GPIOG
#define I2C_DAC1_POT_SDA_Pin GPIO_PIN_3
#define I2C_DAC1_POT_SDA_GPIO_Port GPIOB
#define I2C_DAC1_POT_SCL_Pin GPIO_PIN_6
#define I2C_DAC1_POT_SCL_GPIO_Port GPIOB
#define SPI_DAC1_NSS_Pin GPIO_PIN_9
#define SPI_DAC1_NSS_GPIO_Port GPIOB
#define ADC1_D00_Pin GPIO_PIN_0
#define ADC1_D00_GPIO_Port GPIOE
#define ADC1_D01_Pin GPIO_PIN_1
#define ADC1_D01_GPIO_Port GPIOE

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
