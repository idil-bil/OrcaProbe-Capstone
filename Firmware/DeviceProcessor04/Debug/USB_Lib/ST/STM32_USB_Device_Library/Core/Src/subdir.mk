################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_core.c \
../USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ctlreq.c \
../USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ioreq.c 

OBJS += \
./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_core.o \
./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ctlreq.o \
./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ioreq.o 

C_DEPS += \
./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_core.d \
./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ctlreq.d \
./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ioreq.d 


# Each subdirectory must supply rules for building sources it contributes
USB_Lib/ST/STM32_USB_Device_Library/Core/Src/%.o USB_Lib/ST/STM32_USB_Device_Library/Core/Src/%.su USB_Lib/ST/STM32_USB_Device_Library/Core/Src/%.cyclo: ../USB_Lib/ST/STM32_USB_Device_Library/Core/Src/%.c USB_Lib/ST/STM32_USB_Device_Library/Core/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m33 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32U575xx -c -I../Core/Inc -I../Drivers/STM32U5xx_HAL_Driver/Inc -I../Drivers/STM32U5xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32U5xx/Include -I../Drivers/CMSIS/Include -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor03/USB_Lib/ST/STM32_USB_Device_Library/Core/Inc" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor03/USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Inc" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor03/Device/Inc" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor03/USB_Device/Target" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor03/USB_Device/App" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-USB_Lib-2f-ST-2f-STM32_USB_Device_Library-2f-Core-2f-Src

clean-USB_Lib-2f-ST-2f-STM32_USB_Device_Library-2f-Core-2f-Src:
	-$(RM) ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_core.cyclo ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_core.d ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_core.o ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_core.su ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ctlreq.cyclo ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ctlreq.d ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ctlreq.o ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ctlreq.su ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ioreq.cyclo ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ioreq.d ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ioreq.o ./USB_Lib/ST/STM32_USB_Device_Library/Core/Src/usbd_ioreq.su

.PHONY: clean-USB_Lib-2f-ST-2f-STM32_USB_Device_Library-2f-Core-2f-Src

