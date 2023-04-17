import tkinter as tk
import random
import vlc
from pytube import YouTube

class App:
    def __init__(self, master):
        self.master = master
        master.title("Assistir Vídeos Aleatórios")

        self.channel_label = tk.Label(master, text="Insira o link do canal do YouTube:")
        self.channel_label.pack()

        self.channel_entry = tk.Entry(master)
        self.channel_entry.pack()

        self.play_button = tk.Button(master, text="Assistir Vídeo Aleatório", command=self.play_random_video)
        self.play_button.pack()

        self.stop_button = tk.Button(master, text="Finalizar", command=master.quit)
        self.stop_button.pack()

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def play_random_video(self):
        channel_link = self.channel_entry.get()
        playlist = YouTube(channel_link).videos

        if playlist:
            video = random.choice(playlist)
            video_url = video.streams.filter(progressive=True, file_extension='mp4').first().url
            media = self.instance.media_new(video_url)
            media.get_mrl()
            self.player.set_media(media)
            self.player.play()
        else:
            tk.messagebox.showinfo("Erro", "Canal inválido ou sem vídeos.")

root = tk.Tk()
app = App(root)
root.mainloop()
