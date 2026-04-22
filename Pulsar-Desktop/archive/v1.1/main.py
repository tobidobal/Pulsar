import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil

# --- TEMA Y COLORES DE CUSTOMTKINTER ---
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(initialdir=entrada_ruta.get())
    if carpeta:
        entrada_ruta.delete(0, 'end')
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

    if not enlace:
        messagebox.showwarning("Falta información", "Por favor, pega un enlace válido.")
        return
    if not os.path.exists(ruta):
        messagebox.showwarning("Ruta inválida", "La carpeta de destino no existe.")
        return

    boton_confirmar.configure(text="Descargando...", state="disabled")
    root.update()

    try:
        if tipo == "Video":
            comando = ['yt-dlp', '--no-playlist', enlace]
        else:
            comando = ['yt-dlp', '--no-playlist', '-x', '--audio-format', 'mp3', '--audio-quality', '0', enlace]

        subprocess.run(comando, cwd=ruta, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        messagebox.showinfo("¡Éxito!", f"Descarga de {tipo} completada en:\n{ruta}")
        entrada_enlace.delete(0, 'end') 
    except Exception as e:
        messagebox.showerror("Error", "Ocurrió un error. Asegúrate de que el enlace sea correcto.")
    finally:
        boton_confirmar.configure(text="Confirmar y Descargar", state="normal")

# --- CONFIGURACIÓN DE LA VENTANA ---
root = ctk.CTk()
root.title("Pulsar v0.2")
root.geometry("500x320")

# Centrar la ventana de forma manual para evitar problemas con root.eval
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

center_window(root, 500, 320)

# Título principal
ctk.CTkLabel(root, text="Pulsar", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(20, 5))
ctk.CTkLabel(root, text="Descargador de YouTube", font=ctk.CTkFont(size=14)).pack(pady=(0, 10))

# 1. Campo para el enlace
entrada_enlace = ctk.CTkEntry(root, width=420, placeholder_text="Pega el enlace del video o canción aquí...")
entrada_enlace.pack(pady=10)

# 2. Opciones de tipo de archivo
variable_tipo = ctk.StringVar(value="Video")
frame_opciones = ctk.CTkFrame(root, fg_color="transparent")
frame_opciones.pack(pady=10)
ctk.CTkRadioButton(frame_opciones, text="Video (MP4)", variable=variable_tipo, value="Video").pack(side="left", padx=20)
ctk.CTkRadioButton(frame_opciones, text="Audio (MP3 320kbps)", variable=variable_tipo, value="Audio").pack(side="left", padx=20)

# 3. Selección de carpeta
frame_ruta = ctk.CTkFrame(root, fg_color="transparent")
frame_ruta.pack(pady=15)
entrada_ruta = ctk.CTkEntry(frame_ruta, width=330)

# Ruta por defecto mejorada
def_path = os.path.join(os.path.expanduser("~"), "Downloads", "Pulsar")
if not os.path.exists(def_path):
    try:
        os.makedirs(def_path, exist_ok=True)
    except:
        def_path = os.getcwd()
entrada_ruta.insert(0, def_path)

entrada_ruta.pack(side="left", padx=(0, 10))
ctk.CTkButton(frame_ruta, text="Buscar", width=80, fg_color="#555555", hover_color="#333333", command=seleccionar_carpeta).pack(side="left")

# 4. Botón Confirmar
boton_confirmar = ctk.CTkButton(root, text="Confirmar y Descargar", font=ctk.CTkFont(size=14, weight="bold"), fg_color="#28a745", hover_color="#218838", command=descargar)
boton_confirmar.pack(pady=10)

if __name__ == "__main__":
    try:
        root.mainloop()
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        dummy = tk.Tk()
        dummy.withdraw()
        messagebox.showerror("Error de Inicio", f"El programa no pudo iniciarse:\n{e}")
        dummy.destroy()
