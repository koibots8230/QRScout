import tkinter
import pyodbc
import sqlite3

from cv2 import VideoCapture, flip, cvtColor, COLOR_BGR2RGBA
from PIL import ImageTk, Image
from qreader import QReader

import json


keys = []


def keydown(event):
    keys.append(event.keysym)


def keyup(event):
    keys.remove(event.keysym)


def settext(_text):
    text.delete("0.0", tkinter.END)
    text.insert("0.0", _text)


DEBUG = True

con = pyodbc.connect(
    "Driver={SQL Server};SERVER=localhost;DATABASE=Scouting;UID=******;PWD=******"
)
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS scouting"
    "("
    "id INT PRIMARY KEY, "
    "initials VARCHAR(16), "
    "matchnum INT, "
    "startpos VARCHAR(16), "
    "teamnum INT, "
    "noshow BIT, "
    "automobile BIT, "
    "autoL1 INT, "
    "autol1miss INT, "
    "autoL2 INT, "
    "autol2miss INT, "
    "autoL3 INT, "
    "autol3miss INT, "
    "autoL4 INT, "
    "autol4miss INT, "
    "autoprocessor INT, "
    "coop BIT, "
    "teleL1 INT, "
    "teleL2 INT, "
    "teleL3 INT, "
    "teleL4 INT, "
    "teleprocessor INT, "
    "net INT, "
    "endpos VARCHAR(16), "
    "offence INT, "
    "defence INT, "
    "died BIT, "
    "tipped BIT, "
    "defended BIT, "
    "card VARCHAR(16), "
    "foul INT, "
    "RP VARCHAR(16), "
    "comments VARCHAR(512)"
    ")"
)

decoder = QReader()
camera = VideoCapture(0)
root = tkinter.Tk()
root.bind("<KeyPress>", keydown)
root.bind("<KeyRelease>", keyup)
video = tkinter.Label(root)
video.pack()
text = tkinter.Text(font="Courier")
text.pack(padx=10, pady=10)

if not camera.isOpened():
    print("Camera could not be opened")
    quit()

while True:
    while True:
        errors, image = camera.read()

        display_image = flip(image, 1)
        display_image = cvtColor(display_image, COLOR_BGR2RGBA)
        display_image = Image.fromarray(display_image)
        display_image = display_image.resize((display_image.size[0]//3, display_image.size[1]//3))
        display_image = ImageTk.PhotoImage(display_image)

        video.configure(image=display_image)
        video.image = display_image

        root.update()
        root.update_idletasks()

        if 'q' in keys or 'Escape' in keys:
            quit()

        if 'space' in keys or 'Return' in keys:
            break

    try:
        data = decoder.detect_and_decode(image=image)[0]
    except IndexError:
        print("No QR Code detected, please scan again")
        settext("No QR Code detected, please scan again")
        continue

    if not data:
        print("QR Code is unreadable, please scan again")
        settext("QR Code is unreadable, please scan again")
        continue

    data = json.loads(data)

    if DEBUG:
        print(f"Data: {data}")
    settext(data)

    cur.execute(
        "INSERT INTO scouting"
        "("
        "initials, "
        "matchnum, "
        "startpos, "
        "teamnum, "
        "noshow, "
        "automobile, "
        "autoL1, "
        "autol1miss, "
        "autoL2, "
        "autol2miss, "
        "autoL3, "
        "autol3miss, "
        "autoL4, "
        "autol4miss, "
        "autoprocessor, "
        "coop, "
        "teleL1, "
        "teleL2, "
        "teleL3, "
        "teleL4, "
        "teleprocessor, "
        "net, "
        "offence, "
        "defence, "
        "died, "
        "tipped, "
        "defended, "
        "card, "
        "foul, "
        "RP, "
        "comments"
        ") "
        "VALUES"
        "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            data['pre']['i'],        # initials
                    int(data['pre']['m']),   # matchnum
                    data['pre']['p'],        # startpos
                    int(data['pre']['t']),   # teamnum
                    int(data['pre']['n']),   # noshow
                    int(data['auto']['m']),  # automobile
                    int(data['auto']['o']),  # autoL1
                    int(data['auto']['O']),  # autoL1miss
                    int(data['auto']['t']),  # autoL2
                    int(data['auto']['T']),  # autoL2miss
                    int(data['auto']['h']),  # autoL3
                    int(data['auto']['H']),  # autoL3miss
                    int(data['auto']['f']),  # autoL4
                    int(data['auto']['F']),  # autoL4miss
                    int(data['auto']['p']),  # autoprocessor
                    int(data['tele']['c']),  # coop
                    int(data['tele']['o']),  # teleL1
                    int(data['tele']['t']),  # teleL2
                    int(data['tele']['r']),  # teleL3
                    int(data['tele']['f']),  # teleL4
                    int(data['tele']['p']),  # teleprocessor
                    data['end']['p'],        # endpos
                    data['end']['h'],        # spotlight
                    int(data['post']['o']),  # offence
                    int(data['post']['d']),  # defence
                    int(data['post']['D']),  # died
                    int(data['post']['t']),  # tipped
                    int(data['post']['w']),  # defended
                    data['post']['c'],       # card
                    int(data['post']['f']),  # foul
                    data['post']['R'],        # RP
                    data['post']['C']        # comments
        )
    )
    cur.connection.commit()
    