import getpass
import pywifi
import time
import subprocess
from pywifi import const

wifi= pywifi.PyWiFi()
iface= wifi.interfaces()[0]

def probe(ssid_name):
    iface.scan()
    time.sleep(1)
    results = iface.scan_results()
    for data in results:
        if ssid_name==data.ssid:
            return True
    return False
def connect(ssid_name,pawd):
    profile = pywifi.Profile()
    profile.ssid = ssid_name
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = pawd
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(5)
    assert iface.status() == const.IFACE_CONNECTED



ssid_name = input("what ssid do you want to bind to? ")
pawd = getpass.getpass()
avoid_ssid= input("What SSIDs would you rather not connect to? (Enter space separated names or leave blank)").split(' ')


subprocess.call('netsh interface set interface "Wi-Fi" enable', shell=True)
print("Enabled Wifi")
while(True):
    connectionAt= subprocess.check_output("netsh wlan show interfaces")
    if probe(ssid_name) and (iface.status() != const.IFACE_CONNECTED or bytes(ssid_name,'ascii') not in \
        connectionAt):
        while probe(ssid_name)==False:
            continue
        connect(ssid_name,pawd)
    elif bytes('SSID','ascii') in connectionAt:
        for avoid in avoid_ssid:
            if bytes(avoid,'ascii') in connectionAt:
                iface.disconnect()
    
