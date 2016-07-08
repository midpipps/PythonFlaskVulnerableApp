'''
Helper for all the execute functions from the execute pages
'''
import subprocess

def execute_ping(ip_address):
    '''
    A very vulnerable execute script for pinging an ip address
    '''
    output = list()
    tempoutput = subprocess.check_output("ping " + ip_address, shell=True, universal_newlines=True)
    if tempoutput:
        output = tempoutput.split('\n')
    return output
