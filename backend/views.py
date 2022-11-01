import os
import time

from django.db import connections
from django.http import JsonResponse, HttpResponseBadRequest
from appium.webdriver.appium_service import AppiumService

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from backend.enum import query
import socket


def free_port():
    """
    Determines a free port using sockets.
    """
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(('0.0.0.0', 0))
    free_socket.listen(5)
    port = free_socket.getsockname()[1]
    free_socket.close()
    return port


@csrf_exempt
def start_device_ios(request):
    if request.method == 'GET':
        try:
            if request.GET.get('os_version'):
                os_version = request.GET.get('os_version')
                conn = connections['default']
                cursor = conn.cursor()
                val = (os_version, )
                cursor.execute(query.DataQuery.GET_AVAILABLE_DEVICE_IOS.value, val)
                fetch = cursor.fetchone()
                if len(fetch) > 0:
                    device_id = fetch[0]
                    device_name = fetch[1]
                    os_version = fetch[2]
                    os.system('xcrun simctl boot %s' % device_id)
                    val = (1, device_id)
                    cursor.execute(query.DataQuery.UPDATE_DEVICE_IOS_STATUS.value, val)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    time.sleep(10)
                    msg = {'device_id': device_id, 'device_name': device_name, 'os_version': os_version}
                    return JsonResponse(msg, safe=False)
                else:
                    print('no available devices')
                    msg = {'error_code': 2, 'message': 'run out of devices'}
                    return JsonResponse(msg, safe=False)
            else:
                msg = {'error_code': 3, 'message': 'missing query param'}
                return JsonResponse(msg, safe=False)
        except Exception as e:
            print('error: ' + e)
            msg = {'error_code': 1, 'message': 'fail'}
            return JsonResponse(msg, safe=False)
    else:
        return HttpResponseBadRequest("Expecting GET request")


@csrf_exempt
def start_device_android(request):
    if request.method == 'GET':
        try:
            conn = connections['default']
            cursor = conn.cursor()
            cursor.execute(query.DataQuery.GET_AVAILABLE_DEVICE_ANDROID.value)
            fetch = cursor.fetchone()
            if len(fetch) > 0:
                device_name = fetch[0]
                os_version = fetch[1]
                device_port = fetch[2]

                val = (1, device_name)
                cursor.execute(query.DataQuery.UPDATE_DEVICE_ANDROID_STATUS.value, val)
                conn.commit()

                # If using mac
                os.popen(
                    "nohup /Users/darmawan/Library/Android/sdk/emulator/emulator -port %s -avd %s -no-snapshot-save &" % (device_port, device_name))

                # If using windows
                # os.popen(
                #     "nohup emulator -port %s -avd %s -no-snapshot-save &" % (
                #         device_port, device_name))

                cursor.close()
                conn.close()
                time.sleep(10)
                msg = {'device_name': device_name, 'device_port': device_port, 'os_version': os_version}
                return JsonResponse(msg, safe=False)
            else:
                print('no available devices')
                msg = {'error_code': 2, 'message': 'run out of devices'}
                return JsonResponse(msg, safe=False)
        except Exception as e:
            print(e)
            msg = {'error_code': 1, 'message': 'fail'}
            return JsonResponse(msg, safe=False)
    else:
        return HttpResponseBadRequest("Expecting GET request")


@csrf_exempt
def create_appium_hub(request):
    if request.method == 'GET':
        try:
            appium_service = AppiumService()
            port = free_port()
            os.system("nohup appium -p {} --address 127.0.0.1 &".format(port))
            msg = {'hub': 'http://127.0.0.1:{}/wd/hub'.format(port)}
            return JsonResponse(msg, safe=False)
        except Exception as e:
            print(e)
            msg = {'error_code': 1, 'message': 'fail'}
            return JsonResponse(msg, safe=False)
    else:
        return HttpResponseBadRequest("Expecting GET request")


@csrf_exempt
def kill_device_ios(request):
    if request.method == 'GET':
        try:
            if request.GET.get('device_id'):
                device_id = request.GET.get('device_id')
                os.system('xcrun simctl shutdown {}'.format(device_id))
                conn = connections['default']
                cursor = conn.cursor()
                val = (0, device_id)
                cursor.execute(query.DataQuery.UPDATE_DEVICE_IOS_STATUS.value, val)
                conn.commit()
                cursor.close()
                conn.close()
                msg = {'error_code': 0, 'message': 'success'}
                return JsonResponse(msg, safe=False)
            else:
                msg = {'error_code': 3, 'message': 'missing query param'}
                return JsonResponse(msg, safe=False)
        except Exception as e:
            print(e)
            msg = {'error_code': 1, 'message': 'fail'}
            return JsonResponse(msg, safe=False)
    else:
        return HttpResponseBadRequest("Expecting GET request")


@csrf_exempt
def kill_device_android(request):
    if request.method == 'GET':
        try:
            if request.GET.get('device_port'):
                device_port = request.GET.get('device_port')
                os.system("adb -s emulator-{} emu kill".format(device_port))
                conn = connections['default']
                cursor = conn.cursor()
                val = (0, device_port)
                cursor.execute(query.DataQuery.UPDATE_DEVICE_ANDROID_STATUS_BY_PORT.value, val)
                conn.commit()
                cursor.close()
                conn.close()
                msg = {'error_code': 0, 'message': 'success'}
                return JsonResponse(msg, safe=False)
            else:
                msg = {'error_code': 3, 'message': 'missing query param'}
                return JsonResponse(msg, safe=False)
        except Exception as e:
            print(e)
            msg = {'error_code': 1, 'message': 'fail'}
            return JsonResponse(msg, safe=False)
    else:
        return HttpResponseBadRequest("Expecting GET request")


# if __name__ == "__main__":
#     create_appium_hub()
