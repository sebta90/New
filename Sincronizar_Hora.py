import sys
import ctypes
import subprocess
import ntplib
import os
from datetime import datetime, timezone


def win7_xd():
    return sys.getwindowsversion().major == 6 and sys.getwindowsversion().minor == 1

def ejecutar_como_admin():
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            params = ' '.join(['"{}"'.format(x) for x in sys.argv])
            # Método compatible con Win7
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            sys.exit(0)
    except Exception as e:
        print("Error de permisos:", str(e))
        sys.exit(1)

def cambiar_hora_win7():
    try:
        
        print("Conectando a servidor NTP...")
        cliente = ntplib.NTPClient()
        
        respuesta = cliente.request("172.17.111.1", timeout=10, version=3)
        hora_ntp = datetime.fromtimestamp(respuesta.tx_time, timezone.utc)
        hora_local = hora_ntp.astimezone()
        
        fecha_str = hora_local.strftime("%d-%m-%Y")
        hora_str = hora_local.strftime("%H:%M:%S")
        
        os.system("date {}".format(fecha_str))
        os.system("time {}".format(hora_str))
        
        print("\n ¡Hora actualizda en Windows 7!")
        print("Fecha:", hora_local.strftime("%d/%m/%Y"))
        print("Hora", hora_local.strftime("%I:%M %p").lower())
        
    except Exception as e:
        print("Error win 7", str(e))

def cambiar_hora():
    try:
        print("Conectando al servidor NTP 172.17.111.1...")
        ntp_client = ntplib.NTPClient()
        res = ntp_client.request('172.17.111.1')
        hora_ntp = datetime.fromtimestamp(res.tx_time, timezone.utc)
        hora_local = hora_ntp.astimezone()
        
        fecha_str = hora_local.strftime("%d-%m-%Y")
        hora_str = hora_local.strftime("%H:%M:%S")
        
        print(f"\nActualizando sistema a: {fecha_str} {hora_str}")
        
        subprocess.run(f"date {fecha_str}", shell = True, check = True)
        subprocess.run(f"time {hora_str}", shell = True, check = True)
        
        print("¡Hora del sistema actualizada correctamente!")
        print(f"Nueva fecha: {hora_local.strftime('%d/%m/%Y')}")
        print(f"Nueva hora: {hora_local.strftime('%I:%M %p').lower()}")
        
        
        
    except Exception as e:
        print(f"Error al actualizar hora en windows {e}")
        return None
    

if __name__ == "__main__":
    ejecutar_como_admin()
    if win7_xd():
        cambiar_hora_win7()
    else:
        cambiar_hora()