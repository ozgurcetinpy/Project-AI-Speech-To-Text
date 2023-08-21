import tkinter as tk
from tkinter import *
from tkinter import filedialog
# import openai
import json
from tkinter import END
import threading
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from PIL import Image, ImageTk
import re


root = tk.Tk()
root.geometry("800x550")
root.title("Speech To Text")
root.config(bg="gray")
root.resizable(0,0)

user = os.getlogin()
image = Image.open(r"C:\Users\ozgur\Downloads\abra_staj\Project-AI-Speech-To-Text\ai.jpg".format(user))

render = ImageTk.PhotoImage(image)
img = tk.Label(root, image=render) 
img.image = render
img.place(x=0, y=0,width=800,height=550)

wav_file = ""
json_file = ""
a = 0


def select_wav_file():
    wav_liste = []
    global wav_file
    wav_file = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
    wav_liste.append(wav_file.split("/"))
    wav_label.config(text=wav_liste[0][-1],font=10,foreground="white")
    to_label.config(text="To")

def select_json_file():
    json_liste = []
    global json_file
    json_file = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    json_liste.append(json_file.split("/"))
    json_label.config(text=json_liste[0][-1],font=10,foreground="white")

# Removes sounds under the -70 decibels
def SignalProcessing(mp3_adress):
    message_label.config(text="Cleaning Audio File...")
    sound_file = AudioSegment.from_wav(mp3_adress)

    silence_threshold = -70 

    audio_chunks = split_on_silence(sound_file,
                                    min_silence_len = 500,
                                    silence_thresh = silence_threshold)

    clean_sound_file = AudioSegment.empty()

    for chunk in audio_chunks:
        clean_sound_file += chunk

    clean_sound_file.export(r"C:\Users\{}\Desktop/temizlenmis_sesdosyasi.wav".format(user), format="wav")
    cleaned_audio = r"C:\Users\{}\Desktop/temizlenmis_sesdosyasi.wav".format(user)
    
    return cleaned_audio

def Delete():
    try:
        os.remove(r"C:\Users\{}\Desktop/temizlenmis_sesdosyasi.wav".format(user))
        message_label.config(text="Restarted")
        output = 0
    except FileNotFoundError:
        message_label.config(text="No Restart Needed")


def ChooseAll():
    audio_adress = filedialog.askdirectory()
    json_adress = filedialog.askdirectory()
    
    audio_list = []
    json_list = []
    for audio in os.listdir(audio_adress):
        audio_file_path = os.path.join(audio_adress, audio)
        if os.path.isfile(audio_file_path):
            audio_list.append(audio_file_path)

    for json in os.listdir(json_adress):
        json_file_path = os.path.join(json_adress,json)
        if os.path.isfile(json_file_path):
            json_list.append(json_file_path)
    
    audios = audio_list
    jsons = json_list
    full_list = []
    for zipped in zip(audios,jsons):
        full_list.append(zipped)

    return full_list
def Thread2():
    threading.Thread(target=ConvertAll).start()
def ConvertAll():
    global choose_all_list
    global a
    choose_all_list = ChooseAll()
    to_label.config(text="To")
    for i in range(len(choose_all_list)):
        mp3_adress = choose_all_list[i][0]
        json_adress = choose_all_list[i][1]
        splitted_mp3_adress = mp3_adress.split("/")[-1]
        splitted_json_adress = json_adress.split("/")[-1]
        splitted_mp3_adress = splitted_mp3_adress.split("\\")[-1]
        splitted_json_adress = splitted_json_adress.split("\\")[-1]
        wav_label.config(text=splitted_mp3_adress,font=10,foreground="white")
        json_label.config(text=splitted_json_adress,font=10,foreground="white")
        Speech2Text2(mp3_adress,json_adress,message_label)
        Delete()
        a=a+1
        number_label.config(text=f"Converted Files: {i+1}")
    number_label.config(text=f"Converted Files: {i+1}")
    message_label.config(text="All Files Converted") 
     
      
def Speech2Text2(mp3_adress,json_adress, message_label):
    global output
    output = 0
    noise_address = mp3_adress
    mp3_adress = SignalProcessing(noise_address)
    message_label.config(text="")
    message_label.config(text=f"Converting In Progress %{100/len(choose_all_list)*a}")
    openai.api_key ="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"
    audio_file= open(mp3_adress, "rb")
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        with open(json_adress,'r',encoding="utf8") as f:
            data = json.load(f)
        data["resultText"] = transcript["text"]

        with open(json_adress,'w',encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=9)
    except:
        with open(r"C:\Users\{}\Desktop\AbraAudioConverter\logs.json".format(user),"a",encoding="utf8") as f:
            f.write(noise_address + "\n")
        pass
    output = 1 
    message_label.config(text="")
    message_label.config(text="Conversion Is Finished")

def Speech2Text(mp3_adress,json_adress, message_label):
    global output
    output = 0
    noise_address = wav_file
    mp3_adress = SignalProcessing(noise_address)
    message_label.config(text="")
    message_label.config(text="Converting In Progress...")
    openai.api_key ="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"
    audio_file= open(mp3_adress, "rb")
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        with open(json_adress,'r',encoding="utf8") as f:
            data = json.load(f)
        data["resultText"] = transcript["text"]

        with open(json_adress,'w',encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=9)
    except:
        with open(r"C:\Users\{}\Desktop\AbraAudioConverter\logs.json".format(user),"a",encoding="utf8") as f:
            f.write(noise_address)
        pass
    output = 1 
    message_label.config(text="")
    message_label.config(text="Conversion Is Finished")
    # print("Json adress:",json_adress,"transcript:",transcript)

def Convert():
    mp3_address = wav_file
    json_address = json_file

    if mp3_address and json_address:
        threading.Thread(target=Speech2Text, args=(mp3_address, json_address, message_label)).start()
    else:
        message_label.config(text="Select Your Files")

def CheckAll():
    os.remove(r"C:\Users\ozgur\Desktop\AbraAudioConverter\check_logs.json".format(user))
    json_file_adress = filedialog.askdirectory()
    regex = r'[\u0400-\u04FF\uAC00-\uD7AF\u3040-\u30FF\u4E00-\u9FFF]+'
    for jsons in os.listdir(json_file_adress):
        jsons_file_path = os.path.join(json_file_adress, jsons)
        with open(jsons_file_path, "r", encoding="utf8") as f:
            readed_json = json.load(f)
            readed_json = readed_json["resultText"]
            matches = re.findall(regex,readed_json)
        if "Altyazı" in readed_json:
            with open(r"C:\Users\ozgur\Desktop\AbraAudioConverter\check_logs.json","a",encoding="utf8") as file:
                file.write(jsons_file_path + "\n")
        elif  len(matches) > 0:
            with open(r"C:\Users\ozgur\Desktop\AbraAudioConverter\check_logs.json","a",encoding="utf8") as file:
                file.write(jsons_file_path + "\n")
        else:
            pass
    message_label.config(text="Checking Process Finished")
        
wav_frame = tk.Frame(root, width=600, height=200,background="#0a0930")
wav_frame.place(relx=0.1, rely=0.1)

wav_label = tk.Label(root, text="",foreground="#0a0930",activebackground="#0a0930",background="#0a0930")
wav_label.place(relx=0.1,rely=0.68)

wav_drop = tk.Label(wav_frame, text="Choose WAV File", width=30, height=5, bg="gray",borderwidth=10, relief="raised")
wav_drop.pack(padx=10, pady=10)

wav_drop.bind("<Button-1>", lambda event: select_wav_file())

json_frame = tk.Frame(root, width=600, height=200,background="#0a0930")
json_frame.place(relx=0.6, rely=0.1)

json_label = tk.Label(root, text="",foreground="#0a0930",activebackground="#0a0930",background="#0a0930")
json_label.place(relx=0.1,rely=0.82)

json_drop = tk.Label(json_frame, text="Choose JSON File", width=30, height=5, bg="gray",borderwidth=10, relief="raised")
json_drop.pack(padx=10, pady=10)

json_drop.bind("<Button-1>", lambda event: select_json_file())

message_label = tk.Label(root, text="",background="#0a0930",foreground="white",activebackground="#0a0930",font=16)
message_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

to_label = tk.Label(root,text="",foreground="white",activebackground="#0a0930",background="#0a0930",font=12)
to_label.place(relx=0.2,rely=0.75)

number_label = tk.Label(root, text="",background="#0a0930",foreground="white",activebackground="#0a0930",font=10)
number_label.place(relx=0.5, rely=0.96, anchor=tk.CENTER)

convert_button = tk.Button(root, text="Convert", command=Convert,background="gray",borderwidth=8, relief="raised")
convert_button.place(relx=0.51, rely=0.20, anchor=tk.CENTER,width=100,height=50)

convert_all_button = tk.Button(root,text="Convert All",width=10,height=2,borderwidth=5,bg="gray",relief="raised",command=Thread2)
convert_all_button.place(relx=0.455,rely=0.32)

delete_button = tk.Button(root, text="Restart", command=Delete,background="gray",borderwidth=6, relief="raised")
delete_button.place(relx=0.89, rely=0.91, anchor=tk.CENTER,width=75,height=33)

check_button = tk.Button(root, text="Check All",command=CheckAll,background="gray",borderwidth=6, relief="raised")
check_button.place(relx=0.79, rely=0.91, anchor=tk.CENTER,width=75,height=33)


root.mainloop()