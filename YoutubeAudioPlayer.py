from __future__ import unicode_literals
import pygame
import youtube_dl
import os
from os import listdir
from os.path import isfile
from os.path import join
from tkinter import *
import tkinter.simpledialog as tkSimpleDialog
import time
from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from mutagen.mp3 import MP3
# add function
# @input: youtube link as string
# @output: none
# basically adds audio file of the youtube video to current file

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
paused = False
plusfactor = 0

def createDir():
    if not os.path.exists('Musics'):
        os.makedirs('Musics')


def play():
    global stopped
    global paused
    stopped = True
    pygame.mixer.music.stop()
    status_bar.config(text='')
    my_slider.set(0)

    paused = False
    global plusfactor
    plusfactor = 0

    mp3format = playlist_box.get(ACTIVE)
    mp3format = './Musics/' + mp3format
    pygame.mixer.music.load(mp3format)
    stopped = False
    pygame.mixer.music.play(loops=0)

    grabTime()
    
def add(url, playlist):
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': './Musics/%(title)s.%(ext)s',
    'ignoreerrors': True,
    'noplaylist': not playlist,
    'ffmpeg_location' : ".",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def delete():
    mp3format = playlist_box.get(ACTIVE)
    mp3format = './Musics/' + mp3format
    stop()
    pygame.mixer.music.unload()
    if os.path.exists(mp3format):
        os.remove(mp3format)
    refresh_playlist()

stopped = False
def stop():
    pygame.mixer.music.stop()
    playlist_box.selection_clear(ACTIVE)
    status_bar.config(text='')
    my_slider.set(0)
    pygame.mixer.music.unload()
    global stopped
    stopped = True
    global plusfactor
    plusfactor = 0

def pause():
    global paused
    if (paused):
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def forward():
    nextsong = playlist_box.curselection()
    nextsong = nextsong[0] + 1

    #stop()

    playlist_box.selection_clear(0, END)
    playlist_box.activate(nextsong)
    playlist_box.selection_set(nextsong,last=None)
    
    play()

def back():
    nextsong = playlist_box.curselection()
    nextsong = nextsong[0] - 1

    #stop()

    playlist_box.selection_clear(0, END)
    playlist_box.activate(nextsong)
    playlist_box.selection_set(nextsong,last=None)
    
    play()


def set_volume(volume):
    volume = int(volume)
    pygame.mixer.music.set_volume( volume/float(100))

def grabTime():
    global stopped
    if stopped:
        return
    global current_pos
    global plusfactor
    current_pos = plusfactor + int(pygame.mixer.music.get_pos() / float(1000))
    
    testlabel.config(text=f'{int(current_pos)} | {plusfactor} | {int(pygame.mixer.music.get_pos() / float(1000))}')

    current_time = time.strftime('%M:%S', time.gmtime(current_pos))

    song = playlist_box.get(ACTIVE)
    song = './Musics/' + song

    songMP3 = MP3(song)
    global song_length
    song_length = songMP3.info.length
    csong_length = time.strftime('%M:%S', time.gmtime(song_length))

    #current_pos += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'{csong_length} | {csong_length}')
    elif paused:
        pass
    else:
        pos = int(song_length)
        my_slider.config(to=pos)
        my_slider.set(current_pos)
        status_bar.config(text=f'{current_time} | {csong_length}')
    # else:
    #     pos = int(song_length)
    #     my_slider.config(to=pos)
    #     my_slider.set(int(my_slider.get()))

    #     #converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
    #     #status_bar.config(text=f'{converted_current_time} | {csong_length}')

    #     #next_time = int(my_slider.get()) + 1
    #     #my_slider.set(next_time)
    #     status_bar.config(text=f'{current_time} | {csong_length}')
    


    
    status_bar.after(1000,grabTime)




createDir()

#########################################
#### GUI ################################
#########################################

root = Tk()
root.title('Youtube MP3 Downloader And Player')
root.geometry("600x600")

my_frame = Frame(root)
my_scrollbar = Scrollbar(my_frame, orient=VERTICAL)

playlist_box = Listbox(my_frame, bg="#F0F0F0", fg="#434040",width=500, yscrollcommand=my_scrollbar.set, selectbackground="#434040", selectforeground="#F0F0F0")

my_scrollbar.config(command=playlist_box.yview)
my_scrollbar.pack(side=RIGHT,fill=Y)
my_frame.pack()

playlist_box.pack(pady=20)

def add_song():
    url = tkSimpleDialog.askstring("Add a Song", "Enter Valid URL of Youtube Video")
    add(url, False)
    refresh_playlist()

def add_playlist():
    url = tkSimpleDialog.askstring("Add a Youtube Playlist", "Enter Valid URL of Youtube Playlist")
    add(url, True)
    refresh_playlist()

def refresh_playlist():
    mypath = './Musics/'
    filename = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    playlist_box.delete(0,'end')
    for name in filename:
        playlist_box.insert('end', name)
    
def slide(x):
    global plusfactor
    global current_pos
    global stopped
    global paused
    if stopped:
        return
    if my_slider.get() == current_pos:
        return
    else:
        plusfactor = my_slider.get()

        pygame.mixer.music.play(loops=0,start=int(my_slider.get()))
        if paused:
            pygame.mixer.music.pause()
    
    

back_img = PhotoImage(file="GUI/back_50x50.png")
forward_img = PhotoImage(file="GUI/forward_50x50.png")
play_img =  PhotoImage(file="GUI/play_50x50.png")
pause_img = PhotoImage(file="GUI/pause_50x50.png")
stop_img = PhotoImage(file="GUI/stop_50x50.png")

status_bar = Label(root, text='', bd=1,relief=GROOVE,width=5)
status_bar.pack(fill=X,ipady=5)

my_slider = Scale(root, from_=0,to=100, orient=HORIZONTAL,length=500,command=slide,resolution=1,showvalue=0)
my_slider.pack(pady=20)

controls_frame = Frame(root)
controls_frame.pack(pady=10)

back_btn = Button(controls_frame, image=back_img, borderwidth = 0,command=back)
forward_btn = Button(controls_frame, image=forward_img, borderwidth = 0,command=forward)
pause_btn = Button(controls_frame, image=pause_img, borderwidth = 0, command=pause,cursor="hand2")
stop_btn = Button(controls_frame, image=stop_img, borderwidth = 0, command=stop)
play_btn = Button(controls_frame, image=play_img, borderwidth = 0, command=play)

back_btn.grid(row=0, column = 0,padx=10)
forward_btn.grid(row= 0, column = 1,padx=10)
pause_btn.grid(row=0, column = 3,padx=10)
stop_btn.grid(row = 0, column = 4,padx=10)
play_btn.grid(row = 0, column = 2,padx=10)

my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Options", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song with URL", command=add_song)
add_song_menu.add_command(label="Add Playlist with URL", command=add_playlist)
add_song_menu.add_command(label="Refresh Playlist", command=refresh_playlist)
add_song_menu.add_command(label="Delete Selected Song", command=delete)



volume_bar = Scale(root, from_=0, to=100, label="Volume", orient=HORIZONTAL,length=350,fg="black",command=set_volume)
volume_bar.pack(pady=20)
volume_bar.set(50)

testlabel = Label(root, text="")
testlabel.pack()

refresh_playlist()



root.mainloop()
