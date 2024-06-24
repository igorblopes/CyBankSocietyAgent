from services import api_gateway_service
from services.DTO import logs_dto
from datetime import datetime
from enums.LogSubType import SubType
from enums.LogType import Type
from repository import start_dispositives_repository
import threading
import subprocess

def start():
    thread = threading.Thread(target=start_connected_devices_check)
    thread.start()

def start_connected_devices_check():
    try:
        suspectLog, objectSuspect = verify_connected_devices_suspects()
        if(suspectLog):
            api_gateway_service.send_logs(objectSuspect)

        print("running check connected devices:", datetime.now())
    except Exception as e:
        api_gateway_service.send_logs(
            logs_dto.Logs(str(e), Type.agentError, SubType.connected_devices, "", "")
        )  

def verify_connected_devices_suspects():
    command_out = subprocess.run('ioreg -p IOUSB', shell=True, stdout=subprocess.PIPE, text=True, encoding="cp437")
    results = command_out.stdout.split("\n")

    dispostives_on_start = start_dispositives_repository.get_dispositives()
    
    for _, result in enumerate(results):
        if "AppleUSBDevice" in result:
            name = get_name_dispositive(result)
            if check_new_dispostive(name, dispostives_on_start):
                return True, logs_dto.Logs(f"Detected suspect devices connected: {name}", Type.suspectLog , SubType.connected_devices, "", "")

    return False, logs_dto.Logs("", Type.suspectLog , SubType.connected_devices, "", "")


def check_new_dispostive(name, dispostives_on_start):
    for dispositive in dispostives_on_start:
        if name in dispositive['name']:
            return False
    return True

def get_name_dispositive(result):
    result = result.replace("+-o", "").strip()
    split_results = result.split(" ")
    if len(split_results) > 1:
        return split_results[2]