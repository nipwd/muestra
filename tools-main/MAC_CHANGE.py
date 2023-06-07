import subprocess
import optparse
import re
def get_arguments():
    parser= optparse.OptionParser()
    parser.add_option("-i" , "--interface", dest="interface", help="interface para cambiar MAC")
    parser.add_option("-m" , "--mac", dest="new_mac", help="nueva direccion MAC")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Por favor indincar una interfaz, --help para ayuda")
    elif not options.new_mac:
        parser.error("[-] Por favor indincar una direccion MAC, --help para ayuda")
    return options

def change_mac(interface, new_mac):
    print("[+] cambiando Mac para " + interface + "a " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    # ejemplo:  sudo python mac_change.py -i eth0 -m 00:22:44:55:66:65

def get_current_mac(interface):
    ifconfig_results = subprocess.check_output(["ifconfig", options.interface])
    mac_addres_search_ressult = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_results))
    if mac_addres_search_ressult:
        return(mac_addres_search_ressult.group(0))
    else:
        print("[-] No funciono")

(options) = get_arguments()

current_mac = get_current_mac(options.interface)
print("current mac = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac= get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC nueva" , current_mac)
else:
    print("[-] ERROR EN CAMBIO")
