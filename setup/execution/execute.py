import subprocess

def execute_ping(ip):
    output = list()
    tempOutput = subprocess.check_output("ping " + ip, shell = True, universal_newlines = True)
    if (tempOutput):
        output = tempOutput.split('\n')
    return output
