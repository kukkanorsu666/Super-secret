import os
import time
import shutil
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import font as tkFont
from tendo import singleton
import ttkbootstrap as ttk
import filecmp
import webbrowser
import ctypes
import pyglet
import threading

myappid = '93769867239679234696'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def updater():
	script_dir = os.getcwd()
	with open("Filepath.txt", "r") as game_path:
		game_path_str = game_path.read()
	old_file = f"{script_dir}/Original/data.win"
	new_file = f"{game_path_str}/data.win"
	try:
		if filecmp.cmp(old_file, new_file, shallow=False):
			canvas.itemconfigure(updater_label, text = "Data file up to date!", fill = "green")
			canvas.after(3000, lambda: canvas.itemconfigure(updater_label, text = "", fill = "green"))
			canvas.itemconfigure(swap, text= "data.win found", fill = "green")
			canvas.after(1500, lambda: canvas.itemconfigure(swap, text = ""))
		else:
			canvas.itemconfigure(swap, text= "data.win found", fill = "green")
			canvas.after(2000, lambda: canvas.itemconfigure(swap, text = ""))
			launch_modified_button.config(state='disabled')
			launch_modified_button.after(3000, lambda: launch_modified_button.config(state='active'))
			launch_unmodified_button.config(state='disabled')
			launch_unmodified_button.after(3000, lambda: launch_unmodified_button.config(state='active'))
			canvas.itemconfigure(updater_label, text = "Updating data.win...", fill = "orange")
			shutil.copy(f"{new_file}",f"{script_dir}/Original")
			canvas.after(3000, lambda: canvas.itemconfigure(updater_label, text = "Update complete", fill = "green"))
			canvas.after(6000, lambda: canvas.itemconfigure(updater_label, text = "", fill = "green"))
	except Exception as e:
		canvas.itemconfigure(swap, text= "Error: data.win not found in this directory!", fill = "red")
		print(f"updater() Error: {e}")
		
def init():
	game_path = askdirectory(title='Where is data.win hiding?')
	with open("Filepath.txt", "w") as file:
		file.write(game_path)

	if not os.path.exists("Original"):
		os.mkdir("Original")
	if not os.path.exists("Modified"):
		os.mkdir("Modified")
	with open("settings.txt", "w") as file:
		file.write("")
	
	script_dir = os.getcwd()
	path = (f"{script_dir}/Original")
	file_name = "data.win"
	file_path = os.path.join(path, file_name)
	if os.path.isfile(file_path):
		print("Unmodified file already saved.")
	else:
		try:
			shutil.copy(f"{game_path}/data.win",f"{script_dir}/Original")
			canvas.itemconfigure(swap, text = "data.win found!", fill = "green")
			updater()
		except:
			print("Wrong folder")
			canvas.itemconfigure(swap, text = "Error: data.win not found in this directory!", fill = "red")
	return game_path

def change():
	game_path = askdirectory(title='Select Folder')
	script_dir = os.getcwd()
	path = (f"{game_path}")
	file_name = "data.win"
	file_path = os.path.join(path, file_name)
	if os.path.isfile(file_path):
		try:
			shutil.copy(f"{game_path}/data.win",f"{script_dir}/Original")
			canvas.itemconfigure(swap, text = "data.win found!", fill = "green")
		except FileNotFoundError:
			canvas.itemconfigure(swap, text = "Error: data.win not found in this directory!", fill = "red")
		except Exception as e:
			print(f"change() Error:{e}")
	else:
		print("Unmodified file already saved.")

	canvas.itemconfigure(data_win_path, text = f"data.win path:  {game_path}", fill = "white")
	
	with open("Filepath.txt", "w") as file:
		file.write(game_path)
	updater()

def swap2unmodified():
	script_dir = os.getcwd()
	with open("Filepath.txt", "r") as game_path:
		game_path_str = game_path.read()
	try:
		shutil.copy(f"{script_dir}/Original/data.win", game_path_str)
		canvas.itemconfigure(swap, text = "Unmodified win.data loaded to game directory.", fill = "white")
		canvas.after(2000, lambda: canvas.itemconfigure(swap, text = "", fill = "green"))
	except FileNotFoundError:
		canvas.itemconfigure(swap, text = "Error: Unmodified file not found!", fill = "red")
	except:
		canvas.itemconfigure(swap, text = "Error: Something went wrong!", fill = "red")

def swap2modified():
	script_dir = os.getcwd()
	with open("Filepath.txt", "r") as game_path:
		game_path_str = game_path.read()
	try:
		shutil.copy(f"{script_dir}/Modified/data.win", game_path_str)
		canvas.itemconfigure(swap, text = "Modified win.data loaded to game directory.", fill = "white")
	except FileNotFoundError:
		canvas.itemconfigure(swap, text = "Error: Modified file not found!", fill = "red")
	except Exception as e:
		canvas.itemconfigure(swap, text = f"Error: {e}!", fill = "red")

sleep_event = threading.Event()

def sleep_func():
	sleep_event.set()
	time.sleep(6)
	swap2unmodified()
	sleep_event.clear()

def sleep_thread():
	if not sleep_event.is_set():
		threading.Thread(target=sleep_func, daemon=True).start()

def cooldown_modified():
	launch_modified_button.config(state='disabled')
	launch_modified_button.after(2000, lambda: launch_modified_button.config(state='active'))
	launch_unmodified_button.config(state='disabled')
	launch_unmodified_button.after(2000, lambda: launch_unmodified_button.config(state='active'))
	launch_modified()

def launch_modified():
	script_dir = os.getcwd()
	path = (f"{script_dir}/Modified")
	file_name = "data.win"
	file_path = os.path.join(path, file_name)
	if os.path.isfile(file_path):
		swap2modified()
	else:
		canvas.itemconfigure(swap, text = "Error: Modified file not found!", fill = "red")
		return
	with open("Filepath.txt", "r") as game_path:
		x = game_path.read()
	game_path_replace = x.replace("/","\\")
	try:
		os.startfile(rf"{game_path_replace}/data.win")
		sleep_thread()
		canvas.after(2000, lambda: canvas.itemconfigure(swap, text = "Game is ready to be launched!", fill = "green"))
	except FileNotFoundError:
		canvas.itemconfigure(swap, text = "Error: data.win not found in game directory!", fill = "red")

def cooldown_unmodified():
	launch_unmodified_button.config(state='disabled')
	launch_unmodified_button.after(2000, lambda: launch_unmodified_button.config(state='active'))
	launch_modified_button.config(state='disabled')
	launch_modified_button.after(2000, lambda: launch_modified_button.config(state='active'))
	launch_unmodified()

def launch_unmodified():
	swap2unmodified()
	with open("Filepath.txt", "r") as game_path:
		x = game_path.read()
	game_path_replace = x.replace("/","\\")
	try:
		os.startfile(rf"{game_path_replace}/data.win")
		canvas.after(2000, lambda: canvas.itemconfigure(swap, text = "Game is ready to be launched!", fill = "green"))
	except FileNotFoundError:
		canvas.itemconfigure(swap, text = "Error: data.win not found in game directory!", fill = "red")

def adfree():
	canvas.delete(ad_button_window)
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
	with open("settings.txt", "r") as pro:
		x = pro.read()
	if x == "Pro user = True":
		adfree()

#Bunch of dogshit
pyglet.font.add_file('font/Fontin-Regular.ttf')
pyglet.font.add_file('font/Fontin-Bold.ttf')

try:
	game_path = open("Filepath.txt", "r")

except:
	print("data.win path not found.")

#Window config
window = ttk.Window(themename = "darkly")
window.title("Hero Siege Manager by Kukkanorsu666 (FREE TRIAL)")
window.iconbitmap("images/icon.ico")

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (WINDOW_WIDTH/2))
y = int((screen_height/2) - (WINDOW_HEIGHT/2))

window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
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

change_dir_button = ttk.Button(window, text = "Change",takefocus=False, style = "warning, outline, ", command = change)
change_dir_button_window = canvas.create_window(300, 50, anchor = "c", window = change_dir_button)

launch_modified_button = ttk.Button(window, text = "Launch editor (modified)", takefocus=False, style = "success, outline", command = cooldown_modified)
launch_modified_button_window = canvas.create_window(150, 220, anchor = "c", window = launch_modified_button)

launch_unmodified_button = ttk.Button(window, text = "Launch editor (original)", takefocus=False, style = "success, outline", command = cooldown_unmodified)
launch_unmodified_button_window = canvas.create_window(450, 220, anchor = "c", window = launch_unmodified_button)

donate_button_window = canvas.create_image(300, 400, anchor = "s", image = plox)
canvas.tag_bind(donate_button_window, "<Button-1>", ploxplox)

ad_button_window = canvas.create_image(800, 0, anchor = "ne", image = banner_ad)
canvas.tag_bind(ad_button_window, "<Button-1>", ad)

#text widgets
swap = canvas.create_text(300, 170, font = font_custom_label, fill = "White", text = "")
updater_label = canvas.create_text(500, 380, font = font_custom_label, fill = "White", text = "")

try:
	data_win_path = canvas.create_text(300, 10, font = font_custom_label, fill = "White", text = f"data.win path:  {game_path.read()}")
except:
	canvas.itemconfigure(swap, text = "Please select a folder", fill = "white")
	data_win_path = canvas.create_text(300, 10, font = font_custom_label, fill = "White", text = f"data.win path:  {init()}")

#Run
me = singleton.SingleInstance()
updater()
pro()
window.iconbitmap("images/icon.ico")
window.mainloop()
