################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Device/Src/device_monitoring.c \
../Device/Src/device_registers.c \
../Device/Src/device_sourcing.c \
../Device/Src/measurement_routines.c \
../Device/Src/run_device.c \
../Device/Src/switch_network.c 

OBJS += \
./Device/Src/device_monitoring.o \
./Device/Src/device_registers.o \
./Device/Src/device_sourcing.o \
./Device/Src/measurement_routines.o \
./Device/Src/run_device.o \
./Device/Src/switch_network.o 

C_DEPS += \
./Device/Src/device_monitoring.d \
./Device/Src/device_registers.d \
./Device/Src/device_sourcing.d \
./Device/Src/measurement_routines.d \
./Device/Src/run_device.d \
./Device/Src/switch_network.d 


# Each subdirectory must supply rules for building sources it contributes
Device/Src/%.o Device/Src/%.su Device/Src/%.cyclo: ../Device/Src/%.c Device/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m33 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32U575xx -c -I../Core/Inc -I../Drivers/STM32U5xx_HAL_Driver/Inc -I../Drivers/STM32U5xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32U5xx/Include -I../Drivers/CMSIS/Include -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor04/USB_Lib/ST/STM32_USB_Device_Library/Core/Inc" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor04/USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Inc" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor04/Device/Inc" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor04/USB_Device/Target" -I"C:/UBC_4TH_YEAR/ELEC-491/JY-85/project/JY85/Firmware/DeviceProcessor04/USB_Device/App" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Device-2f-Src

clean-Device-2f-Src:
	-$(RM) ./Device/Src/device_monitoring.cyclo ./Device/Src/device_monitoring.d ./Device/Src/device_monitoring.o ./Device/Src/device_monitoring.su ./Device/Src/device_registers.cyclo ./Device/Src/device_registers.d ./Device/Src/device_registers.o ./Device/Src/device_registers.su ./Device/Src/device_sourcing.cyclo ./Device/Src/device_sourcing.d ./Device/Src/device_sourcing.o ./Device/Src/device_sourcing.su ./Device/Src/measurement_routines.cyclo ./Device/Src/measurement_routines.d ./Device/Src/measurement_routines.o ./Device/Src/measurement_routines.su ./Device/Src/run_device.cyclo ./Device/Src/run_device.d ./Device/Src/run_device.o ./Device/Src/run_device.su ./Device/Src/switch_network.cyclo ./Device/Src/switch_network.d ./Device/Src/switch_network.o ./Device/Src/switch_network.su

.PHONY: clean-Device-2f-Src

