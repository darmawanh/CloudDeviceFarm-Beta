from enum import Enum


class DataQuery(Enum):
    # ANDROID
    GET_AVAILABLE_DEVICE_ANDROID = 'SELECT device_name, os_version, port FROM device_list_android WHERE device_status ' \
                                   '= 0 ORDER BY ' \
                                   'device_name ASC limit 1 '
    UPDATE_DEVICE_ANDROID_STATUS = 'UPDATE device_list_android SET device_status = %s WHERE device_name = %s'
    UPDATE_DEVICE_ANDROID_STATUS_BY_PORT = 'UPDATE device_list_android SET device_status = %s WHERE port = %s'

    # IOS
    GET_AVAILABLE_DEVICE_IOS = 'SELECT device_id, device_name, os_version FROM device_list_ios WHERE device_status = 0 AND ' \
                               'os_version = %s ' \
                               'ORDER BY device_name ASC limit 1 '
    UPDATE_DEVICE_IOS_STATUS = 'UPDATE device_list_ios SET device_status = %s WHERE device_id = %s'

