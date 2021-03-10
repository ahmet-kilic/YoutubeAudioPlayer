from __future__ import unicode_literals
import pygame
import youtube_dl
import os
from os import listdir
from os.path import isfile
from os.path import join
from tkinter import *
import tkinter.simpledialog as tkSimpleDialog
# add function
# @input: youtube link as string
# @output: none
# basically adds audio file of the youtube video to current file

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
paused = False

def createDir():
    if not os.path.exists('Musics'):
        os.makedirs('Musics')


def play():
    global paused
    paused = False
    mp3format = playlist_box.get(ACTIVE)
    mp3format = './Musics/' + mp3format
    pygame.mixer.music.load(mp3format)
    pygame.mixer.music.play()

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
    pygame.mixer.music.unload()
    if os.path.exists(mp3format):
        os.remove(mp3format)
        print("Deleted successfully")
    else:
        print("The file does not exist")
    refresh_playlist()

def stop():
    pygame.mixer.music.stop()
    playlist_box.selection_clear(ACTIVE)


def pause():
    global paused
    if (paused):
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def forward():
    global paused
    paused = False
    nextsong = playlist_box.curselection()
    nextsong = nextsong[0] + 1
    song = playlist_box.get(nextsong)
    song = './Musics/' + song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    playlist_box.selection_clear(0, END)
    playlist_box.activate(nextsong)
    playlist_box.selection_set(nextsong,last=None)

def back():
    global paused
    paused = False
    nextsong = playlist_box.curselection()
    nextsong = nextsong[0] - 1
    song = playlist_box.get(nextsong)
    song = './Musics/' + song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    playlist_box.selection_clear(0, END)
    playlist_box.activate(nextsong)
    playlist_box.selection_set(nextsong,last=None)


def set_volume(volume):
    if volume > 100 or volume < 0:
        print ("Volume value out of bounds, volume should be between 0-100")
        return
    pygame.mixer.music.set_volume( volume/float(100))

createDir()

#########################################
#### GUI ################################
#########################################

root = Tk()
root.title('Youtube MP3 Downloader And Player')
root.geometry("500x400")

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
    
def volumeup():
    volume = round(pygame.mixer.music.get_volume(),1)
    volume = round(volume + 0.1,1)
    pygame.mixer.music.set_volume(volume)

def volumedown():
    volume = round(pygame.mixer.music.get_volume(),1)
    volume = round(volume - 0.1,1)
    pygame.mixer.music.set_volume(volume)

back_img = PhotoImage(file="GUI/back_50x50.png")
forward_img = PhotoImage(file="GUI/forward_50x50.png")
play_img =  PhotoImage(file="GUI/play_50x50.png")
pause_img = PhotoImage(file="GUI/pause_50x50.png")
stop_img = PhotoImage(file="GUI/stop_50x50.png")

controls_frame = Frame(root)
controls_frame.pack()

back_btn = Button(controls_frame, image=back_img, borderwidth = 0,command=back)
forward_btn = Button(controls_frame, image=forward_img, borderwidth = 0,command=forward)
pause_btn = Button(controls_frame, image=pause_img, borderwidth = 0, command=pause)
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
volume_menu = Menu(my_menu)
my_menu.add_cascade(label="Options", menu=add_song_menu)
my_menu.add_cascade(label="Volume", menu=volume_menu)
add_song_menu.add_command(label="Add One Song with URL", command=add_song)
add_song_menu.add_command(label="Add Playlist with URL", command=add_playlist)
add_song_menu.add_command(label="Refresh Playlist", command=refresh_playlist)
add_song_menu.add_command(label="Delete Selected Song", command=delete)
volume_menu.add_command(label="+10",command=volumeup)
volume_menu.add_command(label="-10",command=volumedown)

refresh_playlist()

root.mainloop()
