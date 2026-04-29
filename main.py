import eel
import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import re
import shutil
import sys
import json
import glob
import time

# --- CONFIGURACIÓN PARA PORTABILIDAD (EXE) ---
def resource_path(relative_path):
    """ Obtiene la ruta absoluta para recursos, funciona para dev y para PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Añadir carpeta 'bin' al PATH para que yt-dlp encuentre ffmpeg automáticamente
bin_path = resource_path('bin')
if os.path.exists(bin_path):
    os.environ['PATH'] = bin_path + os.pathsep + os.environ.get('PATH', '')

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

active_process = None
archivos_lote = set()

@eel.expose
def iniciar_lote():
    global archivos_lote
    archivos_lote.clear()

@eel.expose
def cancelar_descarga(ruta):
    global active_process, archivos_lote
    if active_process:
        try:
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(active_process.pid)], creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            print("Error al cancelar proceso:", e)
        active_process = None
    
    # Pequeño retraso para que el OS libere los archivos recién cerrados por taskkill
    time.sleep(1)

    # Eliminar archivos del lote actual
    for arch in list(archivos_lote):
        try:
            if os.path.exists(arch):
                os.remove(arch)
        except:
            pass
    archivos_lote.clear()

    # Eliminar archivos temporales .part o .ytdl en la ruta
    try:
        if os.path.exists(ruta):
            for ext in ('*.part', '*.ytdl', '*.temp'):
                for temp_file in glob.glob(os.path.join(ruta, ext)):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
    except:
        pass
    
    return True

@eel.expose
def obtener_info_playlist(url):
    try:
        yt_dlp_path = shutil.which("yt-dlp") or "yt-dlp"
        comando = [yt_dlp_path, '--flat-playlist', '--dump-json', '--ignore-errors', '--no-warnings', url]
        result = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        videos = []
        for line in result.stdout.split('\n'):
            if not line.strip(): continue
            try:
                data = json.loads(line)
                if data.get('id') and data.get('title'):
                    videos.append({
                        'id': data.get('id'),
                        'title': data.get('title'),
                        'url': data.get('url') or f"https://www.youtube.com/watch?v={data.get('id')}"
                    })
            except:
                pass
        return {"status": "success", "videos": videos}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

@eel.expose
def descargar_video(enlace, formato, ruta):
    global active_process, archivos_lote
    if not shutil.which("yt-dlp"): return {"status": "error", "mensaje": "No se encontró 'yt-dlp' en el sistema."}
    if not enlace: return {"status": "error", "mensaje": "Enlace vacío."}
    if not os.path.exists(ruta): return {"status": "error", "mensaje": "Ruta inválida."}

    try:
        # Comando base mejorado para asegurar MP4 (mismo que en V1.1)
        if formato == "video":
            comando = [
                'yt-dlp', 
                '--no-playlist', 
                '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
                '--merge-output-format', 'mp4',
                '-o', '%(title)s.%(ext)s',
                '--newline',
                '--no-colors',
                enlace
            ]
        else:
            comando = [
                'yt-dlp', 
                '--no-playlist', 
                '-x', 
                '--audio-format', 'mp3', 
                '--audio-quality', '0', 
                '-o', '%(title)s.%(ext)s',
                '--newline',
                '--no-colors',
                enlace
            ]
        
        active_process = subprocess.Popen(comando, cwd=ruta, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        for linea in active_process.stdout:
            # Rastrear archivos que se están descargando para eliminarlos si se cancela
            m1 = re.search(r'\[download\] Destination: (.*)', linea)
            if m1: archivos_lote.add(os.path.join(ruta, m1.group(1).strip()))
            
            m2 = re.search(r'\[Merger\] Merging formats into "(.*)"', linea)
            if m2: archivos_lote.add(os.path.join(ruta, m2.group(1).strip()))
            
            m3 = re.search(r'\[ExtractAudio\] Destination: (.*)', linea)
            if m3: archivos_lote.add(os.path.join(ruta, m3.group(1).strip()))

            if "[download]" in linea and "%" in linea:
                # Esta nueva regla agarra números con o sin decimales perfectamente
                match = re.search(r'(\d+(?:\.\d+)?)%', linea)
                if match:
                    porcentaje = float(match.group(1))
                    eel.actualizar_progreso(porcentaje)()
        
        active_process.wait()
        
        if active_process.returncode == 0:
            active_process = None
            return {"status": "success", "ruta": ruta}
        else:
            active_process = None
            return {"status": "error", "mensaje": "Fallo en la descarga o fue cancelada."}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

eel.start('index.html', mode='default', size=(750, 650), position=(300, 100))