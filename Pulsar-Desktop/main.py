import eel
import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import re
import shutil

eel.init('web')

@eel.expose
def seleccionar_carpeta(ruta_actual):
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    carpeta = filedialog.askdirectory(initialdir=ruta_actual)
    root.destroy()  # Cerrar la ventana oculta de tkinter
    return carpeta if carpeta else ruta_actual

@eel.expose
def abrir_ubicacion(ruta):
    if os.path.exists(ruta):
        os.startfile(ruta)

@eel.expose
def obtener_ruta_defecto():
    def_path = os.path.join(os.path.expanduser("~"), "Downloads", "Pulsar")
    if not os.path.exists(def_path):
        try:
            os.makedirs(def_path, exist_ok=True)
        except:
            def_path = os.getcwd()
    return def_path

@eel.expose
def descargar_video(enlace, formato, ruta):
    if not shutil.which("yt-dlp"): return {"status": "error", "mensaje": "No se encontró 'yt-dlp' en el sistema."}
    if not enlace: return {"status": "error", "mensaje": "Enlace vacío."}
    if not os.path.exists(ruta): return {"status": "error", "mensaje": "Ruta inválida."}

    try:
        base_cmd = ['yt-dlp', '--no-playlist', '-o', '%(title)s.%(ext)s', '--newline']
        
        if formato == "video":
            comando = base_cmd + [enlace]
        else:
            comando = base_cmd + ['-x', '--audio-format', 'mp3', '--audio-quality', '0', enlace]
        
        process = subprocess.Popen(comando, cwd=ruta, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        for linea in process.stdout:
            if "[download]" in linea and "%" in linea:
                # Esta nueva regla agarra números con o sin decimales perfectamente
                match = re.search(r'(\d+(?:\.\d+)?)%', linea)
                if match:
                    porcentaje = float(match.group(1))
                    eel.actualizar_progreso(porcentaje)()
        
        process.wait()
        
        if process.returncode == 0:
            return {"status": "success", "ruta": ruta}
        else:
            return {"status": "error", "mensaje": "Fallo en la descarga."}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

eel.start('index.html', mode='default', size=(750, 650), position=(300, 100))