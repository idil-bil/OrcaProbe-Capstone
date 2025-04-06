################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include USB_Lib/ST/STM32_USB_Device_Library/Core/Src/subdir.mk
-include USB_Lib/ST/STM32_USB_Device_Library/Class/CDC/Src/subdir.mk
-include USB_Device/Target/subdir.mk
-include USB_Device/App/subdir.mk
-include Drivers/STM32U5xx_HAL_Driver/Src/subdir.mk
-include Device/Src/subdir.mk
-include Core/Startup/subdir.mk
-include Core/Src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := DeviceProcessor04
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
DeviceProcessor04.elf \

MAP_FILES += \
DeviceProcessor04.map \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
DeviceProcessor04.list \


# All Target
all: main-build

# Main-build Target
main-build: DeviceProcessor04.elf secondary-outputs

# Tool invocations
DeviceProcessor04.elf DeviceProcessor04.map: $(OBJS) $(USER_OBJS) C:\UBC_4TH_YEAR\ELEC-491\JY-85\project\JY85\Firmware\DeviceProcessor04\STM32U575ZITX_FLASH.ld makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-gcc -o "DeviceProcessor04.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m33 -T"C:\UBC_4TH_YEAR\ELEC-491\JY-85\project\JY85\Firmware\DeviceProcessor04\STM32U575ZITX_FLASH.ld" --specs=nosys.specs -Wl,-Map="DeviceProcessor04.map" -Wl,--gc-sections -static --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -Wl,--start-group -lc -lm -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

DeviceProcessor04.list: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "DeviceProcessor04.list"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) DeviceProcessor04.elf DeviceProcessor04.list DeviceProcessor04.map default.size.stdout
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents main-build fail-specified-linker-script-missing warn-no-linker-script-specified

-include ../makefile.targets
