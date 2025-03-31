import tkinter as tk
from tkinter import filedialog, scrolledtext
import re

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

# Crear la ventana principal
root = tk.Tk()
root.title("Editor de Código")

# Crear el área de texto
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 12))
text_widget.pack(expand=True, fill="both")
text_widget.bind("<KeyRelease>", highlight_syntax)

# Crear el menú
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Abrir", command=open_file)
menu_bar.add_cascade(label="Archivo", menu=file_menu)
root.config(menu=menu_bar)

# Iniciar la aplicación
root.mainloop()

#cambio de prueba
#******************
