import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(initialdir=entrada_ruta.get())
    if carpeta:
        entrada_ruta.delete(0, tk.END)
        entrada_ruta.insert(0, carpeta)

def comprobar_ytdlp():
    return shutil.which("yt-dlp") is not None

def descargar():
    if not comprobar_ytdlp():
        messagebox.showerror("Error", "No se encontró 'yt-dlp' en el sistema.\nPor favor, instálalo para continuar.")
        return

    enlace = entrada_enlace.get().strip()
    ruta = entrada_ruta.get().strip()
    tipo = variable_tipo.get()

    # Validaciones básicas
    if not enlace:
        messagebox.showwarning("Falta información", "Por favor, pega un enlace válido.")
        return
    if not os.path.exists(ruta):
        messagebox.showwarning("Ruta inválida", "La carpeta de destino no existe.")
        return

    # Mostrar que el programa está trabajando
    boton_confirmar.config(text="Descargando... (por favor espera)", state=tk.DISABLED)
    root.update()

    try:
        # Armar el comando según lo que elegiste
        if tipo == "Video":
            comando = ['yt-dlp', enlace]
        else:
            comando = ['yt-dlp', '-x', '--audio-format', 'mp3', '--audio-quality', '0', enlace]

        # Ejecutar yt-dlp silenciosamente en segundo plano
        subprocess.run(comando, cwd=ruta, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        messagebox.showinfo("¡Éxito!", f"Descarga de {tipo} completada en:\n{ruta}")
        entrada_enlace.delete(0, tk.END) # Limpia el campo para el próximo video
    except Exception as e:
        messagebox.showerror("Error", "Ocurrió un error. Asegúrate de que el enlace sea correcto o que yt-dlp esté actualizado.")
    finally:
        # Restaurar el botón a la normalidad
        boton_confirmar.config(text="Confirmar y Descargar", state=tk.NORMAL)

# --- CONFIGURACIÓN DE LA VENTANA ---
root = tk.Tk()
root.title("Pulsar v1.0 - Descargador")
root.geometry("450x250")
root.eval('tk::PlaceWindow . center') # Centrar la ventana en la pantalla

# 1. Campo para el enlace
tk.Label(root, text="Enlace de YouTube/Video:").pack(pady=(15, 5))
entrada_enlace = tk.Entry(root, width=55)
entrada_enlace.pack()

# 2. Opciones de tipo de archivo
variable_tipo = tk.StringVar(value="Video")
frame_opciones = tk.Frame(root)
frame_opciones.pack(pady=10)
tk.Radiobutton(frame_opciones, text="Video (Máxima calidad)", variable=variable_tipo, value="Video").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_opciones, text="Audio (MP3 320kbps)", variable=variable_tipo, value="Audio").pack(side=tk.LEFT, padx=10)

# 3. Selección de carpeta
tk.Label(root, text="Carpeta de destino:").pack(pady=(5, 5))
frame_ruta = tk.Frame(root)
frame_ruta.pack()
entrada_ruta = tk.Entry(frame_ruta, width=40)

# Ruta por defecto mejorada
def_path = os.path.join(os.path.expanduser("~"), "Downloads", "Pulsar")
if not os.path.exists(def_path):
    try:
        os.makedirs(def_path, exist_ok=True)
    except:
        def_path = os.getcwd()
entrada_ruta.insert(0, def_path)

entrada_ruta.pack(side=tk.LEFT, padx=(0, 5))
tk.Button(frame_ruta, text="Buscar", command=seleccionar_carpeta).pack(side=tk.LEFT)

# 4. Botón Confirmar
boton_confirmar = tk.Button(root, text="Confirmar y Descargar", command=descargar, bg="#d4edda", font=("Arial", 10, "bold"))
boton_confirmar.pack(pady=20)

root.mainloop()