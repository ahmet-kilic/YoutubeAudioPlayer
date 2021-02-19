from __future__ import unicode_literals
import pygame
import youtube_dl
import os
from os import listdir
from os.path import isfile
from os.path import join
# add function
# @input: youtube link as string
# @output: none
# basically adds audio file of the youtube video to current file

pygame.mixer.init()

filenames = []

def createDir():
    if not os.path.exists('Musics'):
        os.makedirs('Musics')

def load():
    global filenames
    mypath = './Musics/'
    filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def listMusics():
    global filenames
    for i in range(0,len(filenames)):
        print(str(i) + " " + filenames[i])
    

def play(name):
    global filenames
    if (type(name) is str):
        mp3format = name + ".mp3"
    else:
        mp3format = filenames[name]
    mp3format = './Musics/' + mp3format
    pygame.mixer.music.load(mp3format)
    pygame.mixer.music.play()
    print("Volume: " + str(pygame.mixer.music.get_volume() * 100))

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

def delete(index):
    global filenames
    fileformat = "./Musics/" + filenames[index]
    filenames.pop(index)
    if os.path.exists(fileformat):
        os.remove(fileformat)
        print("Deleted successfully")
    else:
        print("The file does not exist")

def stop():
    pygame.mixer.music.stop()

def pause():
    pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()

def set_volume(volume):
    if volume > 100 or volume < 0:
        print ("Volume value out of bounds, volume should be between 0-100")
        return
    pygame.mixer.music.set_volume( volume/float(100))

createDir()
load()

while True:
    x = input("Enter command: ")
    x = x.split()
    if x[0] == "list":
        listMusics()
    elif x[0] == "add":
        add(x[1],x[2] == 'True')
        load()
    elif x[0] == "play":
        play(int(x[1]))
    elif x[0] == "pause":
        pause()
    elif x[0] == "stop":
        stop()
    elif x[0] == "unpause":
        unpause()
    elif x[0] == "delete":
        delete(int(x[1]))
    elif x[0] == "volume":
        set_volume(int(x[1]))
    elif x[0] == "quit":
        break
