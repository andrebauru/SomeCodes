import os
import requests
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# Configurações do Facebook API
FACEBOOK_GRAPH_API_BASE_URL = 'https://graph.facebook.com/v12.0/'
ACCESS_TOKEN = 'your_access_token'

# Lista para armazenar os posts agendados
scheduled_posts = []

# Função para selecionar uma imagem para o post
def post_image():
    # Abre a janela de seleção de arquivo e obtém o caminho do arquivo selecionado
    file_path = filedialog.askopenfilename()

    # Exibe o caminho do arquivo selecionado na interface
    file_path_label.config(text=file_path)

# Função para agendar um post
def schedule_post():
    # Obtém os valores dos campos da interface
    message = message_entry.get()
    date_str = date_entry.get()
    time_str = time_entry.get()
    datetime_str = f"{date_str} {time_str}"
    datetime_obj = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')
    timestamp = datetime_obj.timestamp()
    file_path = file_path_label.cget('text')

    # Adiciona o post agendado à lista
    scheduled_posts.append({'file_path': file_path, 'timestamp': timestamp, 'message': message})

    # Limpa os campos da interface
    message_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    file_path_label.config(text='')

# Função para exibir os posts agendados em uma nova janela
def show_scheduled_posts():
    # Cria a nova janela de listagem de posts
    scheduled_posts_window = tk.Toplevel(root)
    scheduled_posts_window.title('Posts Agendados')
    scheduled_posts_window.geometry('600x400')

    # Adiciona a lista de posts à interface
    scheduled_posts_listbox = tk.Listbox(scheduled_posts_window)
    for post in scheduled_posts:
        file_name = os.path.basename(post['file_path'])
        timestamp_str = datetime.fromtimestamp(post['timestamp']).strftime('%d/%m/%Y %H:%M')
        scheduled_posts_listbox.insert(tk.END, f'{file_name} - {post["message"]} - {timestamp_str}')
    scheduled_posts_listbox.pack()

    # Adiciona botão para editar um post agendado
    edit_post_button = tk.Button(scheduled_posts_window, text='Editar', command=edit_scheduled_post)
    edit_post_button.pack(pady=10)

    # Adiciona botão para remover um post agendado
    remove_post_button = tk.Button(scheduled_posts_window, text='Remover', command=remove_scheduled_post)
    remove_post_button.pack(pady=10)

# Função para editar um post agendado
def edit_scheduled_post():
    # Obtém o post selecionado na lista
    selected_index = scheduled_posts_listbox.curselection()
    if not selected_index:
        return
    selected_post = scheduled_posts[
        selected_index[0]]

    # Cria a nova janela de edição
    edit_post_window = tk.Toplevel(root)
    edit_post_window.title('Editar Post Agendado')
    edit_post_window.geometry('400x300')

    # Adiciona os widgets à interface
    message_label = tk.Label(edit_post_window, text='Mensagem:')
    message_label.pack()
    message_entry = tk.Entry(edit_post_window)
    message_entry