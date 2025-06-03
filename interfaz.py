import tkinter as tk
from tkinter import filedialog, scrolledtext
import re
from parser_descendente import analizar_sintaxis, leer_simbolos
from tabla_simbolos import crear_archivo


RESERVED_WORDS = {"if", "else", "while", "for", "def", "bool", "int", "float"}

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "r") as file:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, file.read())
        add_error_message(f"Archivo cargado: {filepath}")

def add_error_message(message):
    error_widget.config(state=tk.NORMAL)
    error_widget.insert(tk.END, message + "\n")
    error_widget.config(state=tk.DISABLED)
    error_widget.see(tk.END)

def highlight_syntax(event=None):
    text_widget.tag_remove("keyword", "1.0", tk.END)
    text_widget.tag_remove("number", "1.0", tk.END)
    text_widget.tag_remove("operator", "1.0", tk.END)
    text_widget.tag_remove("parens", "1.0", tk.END)

    content = text_widget.get("1.0", tk.END)

    # Palabras reservadas
    for word in RESERVED_WORDS:
        for match in re.finditer(rf'\b{word}\b', content):
            start, end = match.start(), match.end()
            start_index = f"1.0 + {start} chars"
            end_index = f"1.0 + {end} chars"
            text_widget.tag_add("keyword", start_index, end_index)

    # Números
    for match in re.finditer(r"\b\d+\b", content):
        start, end = match.start(), match.end()
        start_index = f"1.0 + {start} chars"
        end_index = f"1.0 + {end} chars"
        text_widget.tag_add("number", start_index, end_index)

    # Operadores
    for match in re.finditer(r"==|!=|<=|>=|=|\+|\-|\*|/|<|>", content):
        start, end = match.start(), match.end()
        start_index = f"1.0 + {start} chars"
        end_index = f"1.0 + {end} chars"
        text_widget.tag_add("operator", start_index, end_index)

    # Paréntesis y llaves
    for match in re.finditer(r"[(){}]", content):
        start, end = match.start(), match.end()
        start_index = f"1.0 + {start} chars"
        end_index = f"1.0 + {end} chars"
        text_widget.tag_add("parens", start_index, end_index)

    # Estilos
    text_widget.tag_config("keyword", foreground="blue", font=("Courier", 12, "bold"))
    text_widget.tag_config("number", foreground="purple")
    text_widget.tag_config("operator", foreground="orange")
    text_widget.tag_config("parens", foreground="green")

def compilar():
    error_widget.config(state=tk.NORMAL)
    error_widget.delete(1.0, tk.END)
    error_widget.config(state=tk.DISABLED)

    #Borra la tabla de símbolos para empezar limpio (opcional, según tu necesidad)
    import os
    if os.path.exists("tabla_simbolos.dat"):
        os.remove("tabla_simbolos.dat")
    
    crear_archivo()
    codigo = text_widget.get("1.0", tk.END)
    try:
        resultado = analizar_sintaxis(codigo)
        add_error_message(resultado)
    except Exception as e:
        add_error_message(str(e))

    leer_simbolos(add_error_message)

# --- Interfaz ---
root = tk.Tk()
root.title("Compilador en Python")
root.geometry("800x600")

main_panel = tk.PanedWindow(root, orient=tk.VERTICAL)
main_panel.pack(fill=tk.BOTH, expand=True)

text_frame = tk.Frame(main_panel)
text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Courier", 12))
text_widget.pack(expand=True, fill=tk.BOTH)
text_widget.bind("<KeyRelease>", highlight_syntax)
main_panel.add(text_frame)

error_frame = tk.Frame(main_panel)
error_label = tk.Label(error_frame, text="Mensajes:", bg="lightgray")
error_label.pack(fill=tk.X)

error_widget = tk.Text(error_frame, wrap=tk.WORD, height=8, state=tk.DISABLED, bg="black", fg="white")
error_widget.pack(fill=tk.BOTH, expand=True)
main_panel.add(error_frame)

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Abrir", command=open_file)
menu_bar.add_cascade(label="Archivo", menu=file_menu)

compile_menu = tk.Menu(menu_bar, tearoff=0)
compile_menu.add_command(label="Compilar", command=compilar)
menu_bar.add_cascade(label="Compilar", menu=compile_menu)

root.config(menu=menu_bar)
root.mainloop()
