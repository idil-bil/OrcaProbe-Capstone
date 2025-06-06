/*
 * device_sourcing.h
 *
 *  Created on: Mar 6, 2025
 *      Author: User
 */

#ifndef INC_DEVICE_SOURCING_H_
#define INC_DEVICE_SOURCING_H_

void set_ad9833_dds_buffer(uint8_t *buffer, uint32_t freq_28b);
void set_pot_buffer(uint8_t *buffer, uint32_t cmd, uint32_t value);
int calculate_pot_value_curr_mirr(float Current);
HAL_StatusTypeDef config_dds_freq(SPI_HandleTypeDef *hspi, uint8_t *buffer);
HAL_StatusTypeDef config_volt_src_gain(I2C_HandleTypeDef *hi2c, uint16_t pot_addr, uint8_t *buffer);
HAL_StatusTypeDef config_volt_src_offset(I2C_HandleTypeDef *hi2c, uint16_t pot_addr, uint8_t *buffer);
HAL_StatusTypeDef config_current_mirror(I2C_HandleTypeDef *hi2c, uint16_t pot_addr, uint8_t *buffer);

#endif /* INC_DEVICE_SOURCING_H_ */
