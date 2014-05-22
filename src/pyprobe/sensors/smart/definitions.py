from collections import OrderedDict

__author__ = 'Dirk Dittert'

ERROR_CODE_DRIVE_FAILING = 100
ERROR_CODE_SMART_FAILURE = 101

# All attributes that are exported as channels. The key denotes the name of the SMART attribute, the value
# denotes the name of the channel. This is an ordered dictionary because the channels are assigned IDs in the
# order that they are passed to PRTG -- and temperature should be the first one (which is displayed in large).
# More information abount attributes: http://en.wikipedia.org/wiki/S.M.A.R.T.#Known_ATA_S.M.A.R.T._attributes
ATTRIBUTES_EXPORTED_AS_CHANNEL = OrderedDict([
    (194, 'Temperatur'),                       # Temperature_Celsius
    (190, 'Temperatur'),                       # Airflow_Temperature_Cel
    (1,   'Raw Read Error Rate'),              # Raw_Read_Error_Rate
    (5,   'Reallocated Sector Count'),         # Reallocated_Sector_Ct
    (7,   'Seek Error Rate'),                  # Seek_Error_Rate
    (10,  'Spin Retry Count'),                 # Spin_Retry_Count
    (11,  'Calibration Retry Count'),          # Calibration_Retry_Count
    (196, 'Reallocated Event Count'),          # Reallocated_Event_Count
    (197, 'Current Pending Sector'),           # Current_Pending_Sector
    (198, 'Offline Uncorrectable'),            # Offline_Uncorrectable
    (200, 'Multi Zone Error Rate'),            # Multi_Zone_Error_Rate
    (179, 'Used Reserved Block Count Total'),  # Used_Rsvd_Blk_Cnt_Tot
    (192, 'Erase Fail Count'),                 # Erase_Fail_Count_Total
    (183, 'Runtime Bad Block'),                # Runtime_Bad_Block
])

# All attributes that cause failures, i.e. if their value is above zero a SensorError is returned.
ATTRIBUTES_CAUSING_FAILURE = [1,    # Raw_Read_Error_Rate
                              5,    # Reallocated_Sector_Ct
                              10,   # Spin_Retry_Count
                              11,   # Calibration_Retry_Count
                              179,  # Used_Rsvd_Blk_Cnt_Tot
                              183,  # Runtime_Bad_Block
                              192,  # Erase_Fail_Count_Total
                              196,  # Reallocated_Event_Count
                              197,  # Current_Pending_Sector
                              198,  # Offline_Uncorrectable
                              200,  # Multi_Zone_Error_Rate
                              201,  # Soft Read Error Rate
                              230,  # Drive Life Protection Status
                              ]