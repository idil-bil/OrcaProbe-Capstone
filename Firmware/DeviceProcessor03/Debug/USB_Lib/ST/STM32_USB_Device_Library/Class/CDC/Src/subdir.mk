################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/usbd_cdc.c 

OBJS += \
./USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/usbd_cdc.o 

C_DEPS += \
./USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/usbd_cdc.d 


# Each subdirectory must supply rules for building sources it contributes
USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/%.o USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/%.su USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/%.cyclo: ../USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/%.c USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m33 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32U575xx -c -I../Core/Inc -I../Drivers/STM32U5xx_HAL_Driver/Inc -I../Drivers/STM32U5xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32U5xx/Include -I../Drivers/CMSIS/Include -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor03/USB_Lib/ST/STM32_USB_Device_Library/Core/Inc" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor03/USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Inc" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor03/Device/Inc" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor03/USB_Device/Target" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor03/USB_Device/App" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-USB_Lib-2f-ST-2f-STM32_USB_Device_Library-2f-Class-2f-CDC-2f-Src

clean-USB_Lib-2f-ST-2f-STM32_USB_Device_Library-2f-Class-2f-CDC-2f-Src:
	-$(RM) ./USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/usbd_cdc.cyclo ./USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/usbd_cdc.d ./USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/usbd_cdc.o ./USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/usbd_cdc.su

.PHONY: clean-USB_Lib-2f-ST-2f-STM32_USB_Device_Library-2f-Class-2f-CDC-2f-Src

