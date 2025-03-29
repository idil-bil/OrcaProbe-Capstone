/*
 * device_monitoring.c
 *
 *  Created on: Mar 6, 2025
 *      Author: User
 */

#include "main.h"
#include "device_constants.h"
extern TIM_HandleTypeDef htim8;
extern DMA_HandleTypeDef handle_GPDMA1_Channel12;
extern DMA_HandleTypeDef handle_GPDMA1_Channel13;
extern DMA_HandleTypeDef handle_GPDMA1_Channel14;
extern uint16_t adc_samples_1[DVC_MAX_NUM_ADC_SAMPLES];
extern uint16_t adc_samples_2[DVC_MAX_NUM_ADC_SAMPLES];
extern uint16_t adc_samples_3[DVC_MAX_NUM_ADC_SAMPLES];

uint32_t dma_trig_test[DVC_MAX_NUM_ADC_SAMPLES];

volatile uint8_t adc_1_busy;
volatile uint8_t adc_2_busy;
volatile uint8_t adc_3_busy;
volatile uint8_t adc_1_full;
volatile uint8_t adc_2_full;
volatile uint8_t adc_3_full;

void dma_adc_1_cplt_callback(DMA_HandleTypeDef *hdma);
void dma_adc_2_cplt_callback(DMA_HandleTypeDef *hdma);
void dma_adc_3_cplt_callback(DMA_HandleTypeDef *hdma);

void set_adc_sampling_freq(uint32_t sample_freq){
	uint32_t sample_freq_div;
	sample_freq_div = 160000000UL / sample_freq;
//	TIM8->ARR = sample_freq_div-1;
//	TIM8->CCR1 = TIM8->ARR/2;
	TIM8->CCR2 = TIM8->ARR/2;
	TIM8->DIER |= TIM_DIER_UDE;
	HAL_TIM_PWM_Start(&htim8, TIM_CHANNEL_2);
	for(int i = 0; i <DVC_MAX_NUM_ADC_SAMPLES; i++){
		if(i%2){
			dma_trig_test[i] = (1 << 12);
		}
		else{
			dma_trig_test[i] = (1 << (12 + 16));
		}
	}
}

void set_adc_dma_callback_routines(void){
	adc_1_busy = 0;
	adc_2_busy = 0;
	adc_3_busy = 0;
	handle_GPDMA1_Channel12.XferCpltCallback = &dma_adc_1_cplt_callback;
	handle_GPDMA1_Channel13.XferCpltCallback = &dma_adc_2_cplt_callback;
	handle_GPDMA1_Channel14.XferCpltCallback = &dma_adc_3_cplt_callback;
}

HAL_StatusTypeDef collect_adc_samples(DMA_HandleTypeDef *dma_ptr, uint8_t adc_num, uint16_t *sample_buf){
	HAL_StatusTypeDef result;
    HAL_DMA_Abort(dma_ptr);
	if(adc_num == 1){
		HAL_DMA_Start(dma_ptr,(uint32_t)&GPIOE->IDR,(uint32_t)sample_buf,DVC_MAX_NUM_ADC_SAMPLES*sizeof(uint16_t));
		while(HAL_DMA_PollForTransfer(dma_ptr, HAL_DMA_FULL_TRANSFER, 100) != HAL_OK)
		{
		  __NOP();
		}
		reverse_buffer_bits_16(sample_buf, DVC_MAX_NUM_ADC_SAMPLES);
	}
	else if(adc_num == 2){
		result = HAL_DMA_Start(dma_ptr,(uint32_t)&GPIOF->IDR,(uint32_t)sample_buf,DVC_MAX_NUM_ADC_SAMPLES*sizeof(uint16_t));
		while(HAL_DMA_PollForTransfer(dma_ptr, HAL_DMA_FULL_TRANSFER, 100) != HAL_OK)
		{
		  __NOP();
		}
	}
	else if(adc_num == 3){
		result = HAL_ERROR;
	}
    if(result == HAL_OK) {
        HAL_DMA_Abort(dma_ptr);
    }
	return result;
}

HAL_StatusTypeDef collect_adc_samples2(uint8_t adc_num){
	HAL_StatusTypeDef result1, result2, result3;
	result1 = HAL_OK;
	result2 = HAL_OK;
	result3 = HAL_OK;
	if(adc_num & 0x1){
		adc_1_busy = 1;
		HAL_TIM_Base_Start(&htim8);
		result1 = HAL_DMA_Start_IT(&handle_GPDMA1_Channel12,(uint32_t)&GPIOE->IDR,(uint32_t)adc_samples_1,DVC_MAX_NUM_ADC_SAMPLES*sizeof(uint16_t));
	}
	if(adc_num & 0x2){
		adc_2_busy = 1;
		HAL_TIM_Base_Start(&htim8);
		result2 = HAL_DMA_Start_IT(&handle_GPDMA1_Channel13,(uint32_t)&GPIOF->IDR,(uint32_t)adc_samples_2,DVC_MAX_NUM_ADC_SAMPLES*sizeof(uint16_t));
	}
	if(adc_num & 0x4){
		adc_3_busy = 1;
		HAL_TIM_Base_Start(&htim8);
		result3 = HAL_DMA_Start_IT(&handle_GPDMA1_Channel14,(uint32_t)&GPIOF->IDR,(uint32_t)adc_samples_3,DVC_MAX_NUM_ADC_SAMPLES*sizeof(uint16_t));
	}
	return result1 | result2 | result3;
}

uint16_t reverse_bits_16(uint16_t num) {
    uint16_t reversed = 0;
    for (int i = 0; i < 16; i++) {
        reversed |= ((num >> i) & 1) << (15 - i);
    }
    return reversed;
}

void reverse_buffer_bits_16(uint16_t *buffer, size_t size) {
    for (size_t i = 0; i < size; i++) {
        buffer[i] = reverse_bits_16(buffer[i]);
    }
}

void dma_adc_1_cplt_callback(DMA_HandleTypeDef *hdma){
	reverse_buffer_bits_16(adc_samples_1,DVC_MAX_NUM_ADC_SAMPLES);
	adc_1_busy = 0;
	adc_1_full = 1;
}

void dma_adc_2_cplt_callback(DMA_HandleTypeDef *hdma){
	adc_2_busy = 0;
	adc_2_full = 1;
}

void dma_adc_3_cplt_callback(DMA_HandleTypeDef *hdma){
	adc_3_busy = 0;
	adc_3_full = 1;
}
