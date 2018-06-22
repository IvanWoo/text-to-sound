import tkinter as tk
from tkinter import ttk
from gtts import gTTS

import subprocess
import pathlib
import os


class GoogleNyan:
    """
    谷歌娘殿下
    @author: Yifan Wu
    @version: 0.2.333
    tkinter wrap up into one file follow the tips in:
    http://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
    """

    def __init__(self, master):
        self.create_folders()
        self.master = master
        self.master.title("Google Voice Downloader")
        self.mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.message = tk.StringVar()
        self.execution_log = tk.StringVar()
        self.execution_log.set('Please type content...')

        self.message_entry = ttk.Entry(self.mainframe, width=80, textvariable=self.message)
        self.message_entry.grid(column=1, row=1, columnspan=4, rowspan=2, sticky=tk.W)

        self.execution_log_label = ttk.Label(self.mainframe, textvariable=self.execution_log).grid(column=1, row=3,
                                                                                                   sticky=tk.W)
        self.download_voice_button = ttk.Button(self.mainframe, text="Download", command=self.download_voice).grid(
            column=2,
            row=3,
            sticky=tk.W)
        self.stream_voice_button = ttk.Button(self.mainframe, text="Play Voice", command=self.stream_voice).grid(
            column=3, row=3, sticky=tk.W)
        self.open_finder_button = ttk.Button(self.mainframe, text="Open Folder", command=self.open_finder).grid(
            column=4, row=3,
            sticky=tk.W)

        # Add logo of google nyan
        # http://stackoverflow.com/questions/10133856/how-to-add-an-image-in-tkinter-python-2-7
        self.image = tk.PhotoImage(file='img/google_nyan.gif')
        self.photo_label = ttk.Label(self.mainframe, image=self.image).grid(column=2, row=4, columnspan=4, sticky=tk.W)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)

        self.message_entry.focus()
        # Press the <Return> key will download voice
        self.master.bind('<Return>', self.download_voice)
        

    def create_folders(self):
        pathlib.Path('store/').mkdir(exist_ok=True)
        pathlib.Path('temp/').mkdir(exist_ok=True)
    
    def download_voice(self):
        """
        gtts official manual: https://pypi.python.org/pypi/gTTS
        :return: download google voice
        """
        text = self.message_entry.get()
        tts = gTTS(text=text, lang='en')
        tts.save("store/" + text + ".mp3")
        self.execution_log.set('Download successfully!')

    def open_finder(self):
        """
        http://stackoverflow.com/questions/3520493/python-show-in-finder
        :return: open the store folder
        """
        file_to_show = "store/"
        subprocess.call(["open", "-R", file_to_show])

    def stream_voice(self):
        """
        http://stackoverflow.com/questions/3498313/how-to-trigger-from-python-playing-of-a-wav-or-mp3-audio-file-on-a-mac
        :return: cache the voice and play, after play delete.
        """
        text = self.message_entry.get()
        tts = gTTS(text=text, lang='en')
        tts.save("temp/" + text + ".mp3")
        subprocess.call(["afplay", "temp/" + text + ".mp3"])

        os.remove("temp/" + text + ".mp3")  # remove temporary file


def main():
    root = tk.Tk()
    GoogleNyan(root)
    root.mainloop()


if __name__ == '__main__':
    main()
