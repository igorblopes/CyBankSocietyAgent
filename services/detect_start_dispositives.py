import subprocess
from repository import start_dispositives_repository
from entity import start_dispositives_entity

def setup_dispostives():
    command_out = subprocess.run('ioreg -p IOUSB', shell=True, stdout=subprocess.PIPE, text=True, encoding="cp437")
    results = command_out.stdout.split("\n")
    
    for index, result in enumerate(results):
        if "AppleUSBDevice" in result:
            dispositive = start_dispositives_entity.start_dispositives(get_name_dispositive(result), "start_dispositive")
            start_dispositives_repository.insert(dispositive)



def get_name_dispositive(result):
    result = result.replace("+-o", "").strip()
    split_results = result.split(" ")
    if len(split_results) > 1:
        return split_results[2]
