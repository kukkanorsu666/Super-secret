import os
import time
import shutil
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import font as tkFont
from tendo import singleton
import ttkbootstrap as ttk
import webbrowser
import ctypes
import pyglet


def init():
	game_path = askdirectory(title='Where is data.win hiding?')
	with open("Filepath.txt", "w") as file:
		file.write(game_path)

	os.mkdir("Original")
	os.mkdir("Modified")
	with open("settings.txt", "w") as file:
			file.write("")
	
	script_dir = os.getcwd()

	dir = os.listdir(f"{script_dir}/Original")

	if len(dir) == 0:
		try:
			shutil.copy(f"{game_path}/data.win",f"{script_dir}/Original")
			canvas.itemconfigure(swap, text = "data.win found!", fill = "green")
		except:
			print("Wrong folder")
			canvas.itemconfigure(swap, text = "Error: data.win not found in this directory!", fill = "red")

	else:
		print("Unmodified file already saved.")

	return game_path

def change():
	game_path = askdirectory(title='Select Folder')

	script_dir = os.getcwd()

	dir = os.listdir(f"{script_dir}/Original")

	if len(dir) == 0:
		try:
			shutil.copy(f"{game_path}/data.win",f"{script_dir}/Original")
			canvas.itemconfigure(swap, text = "data.win found!", fill = "green")

		except FileNotFoundError:
			canvas.itemconfigure(swap, text = "Error: data.win not found in this directory!", fill = "red")

		except:
			canvas.itemconfigure(swap, text = "Error: Something went wrong!", fill = "red")
	else:
		print("Unmodified file already saved.")

	canvas.itemconfigure(data_win_path, text = f"data.win path:  {game_path}", fill = "white")
	
	with open("Filepath.txt", "w") as file:
		file.write(game_path)

def swap2unmodified():
	script_dir = os.getcwd()
	game_path = open("Filepath.txt", "r")
	try:
		shutil.copy(f"{script_dir}/Original/data.win", game_path.read())
		canvas.itemconfigure(swap, text = "Unodified win.data loaded to game directory.", fill = "white")

	except FileNotFoundError:
		canvas.itemconfigure(swap, text = "Error: Unmodified file not found!", fill = "red")

	except:
		canvas.itemconfigure(swap, text = "Error: Something went wrong!", fill = "red")

def swap2modified():
	script_dir = os.getcwd()
	game_path = open("Filepath.txt", "r")
	try:
		shutil.copy(f"{script_dir}/Modified/data.win", game_path.read())
		canvas.itemconfigure(swap, text = "Modified win.data loaded to game directory.", fill = "white")

	except FileNotFoundError:
		canvas.itemconfigure(swap, text = "Error: Modified file not found!", fill = "red")

	except:
		canvas.itemconfigure(swap, text = "Error: Something went wrong!", fill = "red")

def launch():
	game_path = open("Filepath.txt", "r")
	x = game_path.read()
	game_path_replace = x.replace("/","\\")
	try:
		os.startfile(rf"{game_path_replace}/data.win")
		time.sleep(8)
		swap2unmodified()
		canvas.itemconfigure(swap, text = "Game is ready to be launched!", fill = "green")

	except FileNotFoundError:
		canvas.itemconfigure(swap, text = "Error: data.win not found in game directory!", fill = "red")

def adfree():
	window.geometry("600x400")
	window.title("Hero Siege Manager PRO by Kukkanorsu666")
	
donation = 0
def ploxplox(event):
	global donation
	donation += 10
	canvas.itemconfigure(swap, text = f"Thanks for donate {donation} €", fill = "green")
	if donation >= 1000:
		with open("settings.txt", "w") as file:
			file.write("Pro user = True")
		adfree()

def ad(event):
	webbrowser.open('http://monday.com')

def pro():
	pro = open("settings.txt", "r")
	x = pro.read()
	if x == "Pro user = True":
		adfree()

#Bunch of dogshit
pyglet.font.add_file('font/Fontin-Regular.ttf')
pyglet.font.add_file('font/Fontin-Bold.ttf')
myappid = '93769867239679234696'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

try:
	game_path = open("Filepath.txt", "r")

except:
	print("data.win path not found.")

#Window config
window = ttk.Window(themename = "darkly")
window.title("Hero Siege Manager by Kukkanorsu666 (FREE TRIAL)")
window.iconbitmap("images/icon.ico")
window.geometry("800x400")
window.resizable(False, False)

#font
font_custom_label = tkFont.Font(family="Fontin", size=12, weight=tkFont.BOLD)
font_custom_button = tkFont.Font(family="Fontin", size=12, weight=tkFont.BOLD)

#images
background = PhotoImage(file = "images/background.png")
plox = PhotoImage(file = "images/plox.png")
banner_ad = PhotoImage(file = "images/banner1.png")

#canvas config
canvas = Canvas(window, width = 800, height = 400)
canvas.pack(fill = "both", expand = True)

canvas.create_image(0,0, image = background, anchor = "nw")

#buttons
button_style = ttk.Style()
button_style.configure('TButton', font=('Fontin', 14))

change_dir_button = ttk.Button(window, text = "Change", style = "warning, outline, ", command = change)
change_dir_button_window = canvas.create_window(300, 50, anchor = "c", window = change_dir_button)

swap2unmodified_button = ttk.Button(window, text = "Load unmodified", bootstyle = "warning, outline", command = swap2unmodified)
swap2unmodified_button_window = canvas.create_window(200, 150, anchor = "c", window = swap2unmodified_button)

swap2modified_button = ttk.Button(window, text = "Load modified", bootstyle = "warning, outline", command = swap2modified)
swap2modified_button_window = canvas.create_window(400, 150, anchor = "c", window = swap2modified_button)

launch_button = ttk.Button(window, text = "Launch editor", bootstyle = "warning, outline", command = launch)
launch_button_window = canvas.create_window(300, 300, anchor = "c", window = launch_button)

donate_button_window = canvas.create_image(300, 400, anchor = "s", image = plox)
canvas.tag_bind(donate_button_window, "<Button-1>", ploxplox)

ad_button_window = canvas.create_image(800, 0, anchor = "ne", image = banner_ad)
canvas.tag_bind(ad_button_window, "<Button-1>", ad)

#text widgets
swap = canvas.create_text(300, 210, font = font_custom_label, fill = "White", text = "")

try:
	data_win_path = canvas.create_text(300, 10, font = font_custom_label, fill = "White", text = f"data.win path:  {game_path.read()}")
except:
	canvas.itemconfigure(swap, text = "Please select a folder", fill = "white")
	data_win_path = canvas.create_text(300, 10, font = font_custom_label, fill = "White", text = f"data.win path:  {init()}")

#Run
me = singleton.SingleInstance()
pro()
window.mainloop()
