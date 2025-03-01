/*
 * DeviceConstants.h
 *
 *  Created on: Nov 16, 2024
 *      Author: JY85
 */

#ifndef INC_DEVICECONSTANTS_H_
#define INC_DEVICECONSTANTS_H_

#define DVC_NUM_PROBES 				4
#define DVC_NUM_RELAYS_PER_PROBE 	8
#define DVC_TOTAL_RELAY_COUNT		20
#define DVC_REGISTER_WIDTH 			32
#define DVC_REGISTER_ADDR_WIDTH		8
#define DVC_REGISTER_DATA_WIDTH		DVC_REGISTER_WIDTH-DVC_REGISTER_ADDR_WIDTH
#define DVC_TOTAL_REGISTER_NUMBER  1<<(DVC_REGISTER_ADDR_WIDTH)

#define DVC_STATUS 					0
#define DVC_MEASUREMENT_CONFIG  	1
#define DVC_PROBE_CONFIG  			2
#define DVC_SAMPLE_DATA            	100

/*
 * Enum name: Probe Configurations
 * Description:
 * 	All available probe configurations.
 *
 */
typedef enum
{
	PROBES_2 = 1,		/*!< Probe Configuration: 2 probes */
	PROBES_3 = 2,		/*!< Probe Configuration: 3 probes */
	PROBES_4 = 3,		/*!< Probe Configuration: 4 probes */
} ProbeCfg_Type;


/*
 * Enum name: Measurements Configurations
 * Description:
 * 	All available measurement configurations.
 * 	Different probe configurations can interpret the same measurement configuration differently.
 *
 */
typedef enum
{
	DC_RESISTANCE 			  = 1,
	CURRENT_VOLTAGE 		  = 2,
	CAPACITANCE_VOLTAGE_2P    = 3,
	IMPEDANCE_SPECTROSCOPY_2P = 4,
	TRANSFER_CHARACTERISTICS  = 5,
	OUTPUT_CHARACTERISTICS 	  = 6,
	CAPACITANCE_VOLTAGE_3P    = 7,
	ELECTROCHEMICAL 		  = 8,
	LOW_RESISTANCE 			  = 9,
	PROBE_RESISTANCE 		  = 10,
	IMPEDANCE_SPECTROSCOPY_4P = 11,
} MeasurementCfg_Type;

/*
 * Enum name: Measurements Configurations
 * Description:
 * 	All available measurement configurations.
 * 	Different probe configurations can interpret the same measurement configuration differently.
 *
 */
typedef enum
{
	ProbeId_0 			= 0, 	/*!< Probe Identifier: Probe 0 */
	ProbeId_1 			= 1,	/*!< Probe Identifier: Probe 1 */
	ProbeId_2 			= 2,	/*!< Probe Identifier: Probe 2 */
	ProbeId_3			= 3,	/*!< Probe Identifier: Probe 3 */
	ProbeId_MultiProbe	= 4,	/*!< Probe Identifier: Multiple Probes */
} ProbeId_Type;

#endif /* INC_DEVICECONSTANTS_H_ */
