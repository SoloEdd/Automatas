import tkinter as tk
from tkinter import filedialog, scrolledtext
import re
from tabla_simbolos import crear_archivo, tokenizar, leer_simbolos


#******************
# Definir palabras reservadas de ejemplo
RESERVED_WORDS = {"if", "else", "while", "for", "def", "return", "class", "import", "from", "as"}

def highlight_syntax(event=None):
    text_widget.tag_remove("keyword", "1.0", tk.END)
    content = text_widget.get("1.0", tk.END)
    for word in RESERVED_WORDS:
        matches = [(m.start(), m.end()) for m in re.finditer(rf'\b{word}\b', content)]
        for start, end in matches:
            start_index = f"1.0 + {start} chars"
            end_index = f"1.0 + {end} chars"
            text_widget.tag_add("keyword", start_index, end_index)
    text_widget.tag_config("keyword", foreground="blue")

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "r") as file:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, file.read())
        highlight_syntax()
        add_error_message(f"Archivo cargado: {filepath}")

def add_error_message(message):
    error_widget.config(state=tk.NORMAL)
    error_widget.insert(tk.END, message + "\n")
    error_widget.config(state=tk.DISABLED)
    error_widget.see(tk.END)

def analizar_codigo():
    crear_archivo()
    codigo = text_widget.get("1.0", tk.END)
    tokens = tokenizar(codigo)
    add_error_message("Análisis completado. Tokens generados:")
    for t in tokens:
        add_error_message(f"  -> {t}")
    leer_simbolos()

# Crear la ventana principal
root = tk.Tk()
root.title("Editor de Código")
root.geometry("800x600")

# Crear un panel principal para dividir las áreas
main_panel = tk.PanedWindow(root, orient=tk.VERTICAL)
main_panel.pack(fill=tk.BOTH, expand=True)

# Crear el área de texto
text_frame = tk.Frame(main_panel)
text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Courier", 12))
text_widget.pack(expand=True, fill=tk.BOTH)
text_widget.bind("<KeyRelease>", highlight_syntax)
main_panel.add(text_frame)

# Área de errores (parte inferior)
error_frame = tk.Frame(main_panel)
error_label = tk.Label(error_frame, text="Errores:", bg="lightgray")
error_label.pack(fill=tk.X)

error_widget = tk.Text(error_frame, wrap=tk.WORD, height=8, state=tk.DISABLED, bg="black", fg="white")
error_widget.pack(fill=tk.BOTH, expand=True)

# Crear el menú
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Abrir", command=open_file)
menu_bar.add_cascade(label="Archivo", menu=file_menu)

analizar_menu = tk.Menu(menu_bar, tearoff=0)
analizar_menu.add_command(label="Analizar Código", command=analizar_codigo)
menu_bar.add_cascade(label="Analizar", menu=analizar_menu)

root.config(menu=menu_bar)

# Barra de desplazamiento para errores
error_scroll = tk.Scrollbar(error_widget)
error_scroll.pack(side=tk.RIGHT, fill=tk.Y)
error_widget.config(yscrollcommand=error_scroll.set)
error_scroll.config(command=error_widget.yview)

main_panel.add(error_frame)

# Configurar el menú
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Abrir", command=open_file)
menu_bar.add_cascade(label="Archivo", menu=file_menu)
root.config(menu=menu_bar)

# Configurar tags para errores
error_widget.tag_config("error", foreground="red")
error_widget.tag_config("warning", foreground="yellow")
error_widget.tag_config("info", foreground="lightblue")

# Iniciar la aplicación
root.mainloop()