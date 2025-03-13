/*
 * device_monitoring.c
 *
 *  Created on: Mar 6, 2025
 *      Author: User
 */

#include "main.h"
#include "device_constants.h"

void set_adc_sampling_freq(uint32_t sample_freq){
	uint32_t sample_freq_div;
	sample_freq_div = 160000000UL / sample_freq;
	TIM8->ARR = sample_freq_div-1;
	TIM8->CCR1 = TIM8->ARR/2;
	TIM8->CCR2 = TIM8->ARR/2;
}

HAL_StatusTypeDef collect_adc_samples(DMA_HandleTypeDef *dma_ptr, uint8_t adc_num, uint16_t *sample_buf){
	HAL_StatusTypeDef result;
    HAL_DMA_Abort(dma_ptr);
	if(adc_num == 1){
		result = HAL_DMA_Start(dma_ptr,(uint32_t)&GPIOE->IDR,(uint32_t)sample_buf,DVC_MAX_NUM_ADC_SAMPLES*sizeof(uint16_t));
		reverse_buffer_bits_16(sample_buf,DVC_MAX_NUM_ADC_SAMPLES);
	}
	else if(adc_num == 2){
		result = HAL_DMA_Start(dma_ptr,(uint32_t)&GPIOF->IDR,(uint32_t)sample_buf,DVC_MAX_NUM_ADC_SAMPLES*sizeof(uint16_t));
	}
	else if(adc_num == 3){
		result = HAL_ERROR;
	}
    if(result == HAL_OK) {
        HAL_DMA_Abort(dma_ptr);
    }
	return result;
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
