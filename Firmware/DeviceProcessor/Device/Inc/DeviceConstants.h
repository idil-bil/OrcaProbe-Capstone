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
/*
 * Enum name: Probe Configurations
 * Description:
 * 	All available probe configurations.
 *
 */
typedef enum
{
	ProbeCfg_2 = 0,		/*!< Probe Configuration: 2 probes */
	ProbeCfg_3 = 1,		/*!< Probe Configuration: 3 probes */
	ProbeCfg_4 = 2,		/*!< Probe Configuration: 4 probes */
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
	MeasurementCfg_DCRes 			= 0, 	/*!< Measurement Configuration: DC resistance */
	MeasurementCfg_IV 				= 1,	/*!< Measurement Configuration: Current against Voltage plot */
	MeasurementCfg_CV 				= 2,	/*!< Measurement Configuration: Capacitance against Voltage plot */
	MeasurementCfg_ImpdnSpec		= 3,	/*!< Measurement Configuration: Impedance Spectroscopy */
	MeasurementCfg_XferCharIdsVgs	= 4,	/*!< Measurement Configuration: Transfer characteristics of a transistor (Ids vs Vgs) */
	MeasurementCfg_OutCharIdsVds	= 5,	/*!< Measurement Configuration: Output characteristics of a transistor (Ids vs Vds) */
	MeasurementCfg_ElecChem			= 6,	/*!< Measurement Configuration: Electrochemical measurement */
} MeasurmentCfg_Type;

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
