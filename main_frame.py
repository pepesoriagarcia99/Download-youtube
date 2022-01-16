from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import youtube_dl
import threading


class MainFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.parent = master
        self.grid()

        self.renderView()

    def renderView(self):
        #Label
        self.urlLabel = Label(self, text="Insert url YouTube: ")
        self.urlLabel.grid(column=0, row=0)

        self.urlValue = StringVar(value="")
        self.urlEntry = Entry(self, width=45, textvariable=self.urlValue)
        self.urlEntry.grid(column=1, row=0)
     
        # Btn
        self.downloadButton = Button(
            self, text="Download", command=self.initDownload, state='normal')
        self.downloadButton.grid(column=4, row=0)

        self.cleanButton = Button(
            self, text="Clean", command=self.clean, state='normal')
        self.cleanButton.grid(column=5, row=0)

    def clean(self):
        self.urlEntry.delete(0, END)

    def initDownload(self):
        try:
            self.downloadThread = threading.Thread(target=self.download)
            self.downloadThread.start()
        except:
            print("Exception in Thread!!")

    def download(self):
        self.downloadButton.configure(state='disable')

        videoInfo = youtube_dl.YoutubeDL().extract_info(
            url = self.urlValue.get(),download=False
        )

        title=videoInfo['title']
        downloadingTitleVar = StringVar(value=(title))

        self.downloadingTitle = Label(self, textvariable=downloadingTitleVar, height=3, wraplength=100)
        self.downloadingTitle.grid(column=0, row=1)

        self.progressbarDownloading = ttk.Progressbar(self,orient='horizontal',length=300,mode='determinate')
        self.progressbarDownloading.grid(column=1, row=1, columnspan=4)

        self.progressLabel = Label(self, text="0%")
        self.progressLabel.grid(column=5, row=1)

        filename = f"{title}.mp3"
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':filename,
            'progress_hooks': [self.progressHooks]
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([videoInfo['webpage_url']])
    
    def progressHooks(self,d):
        if d['status'] == 'finished':
            self.downloadingTitle.grid_remove()
            self.progressbarDownloading.grid_remove()
            self.progressLabel.grid_remove()
            self.urlEntry.delete(0, END)
            self.downloadButton.configure(state='normal')
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%','')
            self.progressLabel.configure(text=f"{p} %")
            self.progressbarDownloading['value']=float(p)
