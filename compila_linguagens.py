import tkinter as tk
from tkinter import messagebox, scrolledtext


def adivinhar_linguagem(codigo):
    """O Autônomo: analisa o texto e adivinha a linguagem por palavras-chave."""
    codigo_linhas = codigo.split("\n")

    # Contadores de relevância para cada linguagem
    pontos = {"Python": 0, "Java": 0, "JavaScript": 0, "C++": 0, "Go": 0}

    # Palavras-chave exclusivas ou muito comuns de cada linguagem
    if "def " in codigo or "import os" in codigo or "print(" in codigo:
        pontos["Python"] += 2
    if "public class" in codigo or "System.out.print" in codigo or "String[] args" in codigo:
        pontos["Java"] += 5
    if "const " in codigo or "let " in codigo or "console.log" in codigo or "function " in codigo:
        pontos["JavaScript"] += 3
    if "#include" in codigo or "std::" in codigo or "cout <<" in codigo:
        pontos["C++"] += 5
    if "package main" in codigo or "func main()" in codigo or "import \"fmt\"" in codigo:
        pontos["Go"] += 5

    # Identifica qual linguagem somou mais pontos
    linguagem_detectada = max(pontos, key=pontos.get)

    # Se nenhuma palavra-chave foi engatilhada, retorna inconclusivo
    if pontos[linguagem_detectada] == 0:
        return "Desconhecida (Tente colar um código mais completo)"

    return linguagem_detectada


# --- CONFIGURAÇÃO DA INTERFACE (FRONT-END NATIVO) ---
def acao_botao():
    texto_codigo = campo_texto.get("1.0", tk.END).strip()

    if not texto_codigo:
        messagebox.showwarning("Aviso", "Por favor, cole algum código primeiro!")
        return

    # O autônomo processa o código
    resposta = adivinhar_linguagem(texto_codigo)

    # Atualiza a resposta na tela
    label_resposta.config(text=f"Linguagem Detectada: {resposta}")


# Criação da janela principal (Tema Escuro integrado)
janela = tk.Tk()
janela.title("Detector de Linguagem Autônomo")
janela.geometry("600x450")
janela.configure(bg="#1e1e1e")

# Título
titulo = tk.Label(
    janela,
    text="🤖 Cole seu código abaixo:",
    fg="#4CAF50",
    bg="#1e1e1e",
    font=("Arial", 14, "bold"),
)
titulo.pack(pady=10)

# Input de Texto (Caixa grande com scroll)
campo_texto = scrolledtext.ScrolledText(
    janela,
    wrap=tk.WORD,
    width=65,
    height=15,
    bg="#2d2d2d",
    fg="#85e89d",
    insertbackground="white",
    font=("Consolas", 10),
)
campo_texto.pack(pady=10)

# Botão de Ação
botao = tk.Button(
    janela,
    text="Adivinhar Linguagem ⚡",
    command=acao_botao,
    bg="#4CAF50",
    fg="black",
    font=("Arial", 10, "bold"),
    activebackground="#45a049",
    cursor="hand2",
)
botao.pack(pady=10)

# Resposta Desejada
label_resposta = tk.Label(
    janela,
    text="Linguagem Detectada: ---",
    fg="#ffffff",
    bg="#1e1e1e",
    font=("Arial", 12, "bold"),
)
label_resposta.pack(pady=10)

# Inicia a aplicação
janela.mainloop()