import subprocess

def apply_network_conditions(interface, rate=None, delay=None, loss=None):
    command = ['sudo', 'tcset', interface]
    if rate:
        command += ['--rate', rate]
    if delay:
        command += ['--delay', delay]
    if loss:
        command += ['--loss', loss]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode(), result.stderr.decode()

def clear_network_conditions(interface):
    result = subprocess.run(['sudo', 'tcdel', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode(), result.stderr.decode()
