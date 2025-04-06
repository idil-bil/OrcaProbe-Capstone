/*
 * device_monitoring.h
 *
 *  Created on: Mar 6, 2025
 *      Author: User
 */

#ifndef INC_DEVICE_MONITORING_H_
#define INC_DEVICE_MONITORING_H_

void set_adc_sampling_freq(uint32_t sample_freq);
HAL_StatusTypeDef collect_adc_samples(DMA_HandleTypeDef *dma_ptr, uint8_t adc_num, uint16_t *sample_buf);
HAL_StatusTypeDef collect_adc_samples_it(uint8_t adc_num);
uint16_t reverse_bits_16(uint16_t num);
void reverse_buffer_bits_16(uint16_t *buffer, size_t size);
void set_adc_dma_callback_routines(void);


#endif /* INC_DEVICE_MONITORING_H_ */
