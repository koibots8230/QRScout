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
    "teamnum INT, "
    "noshow BIT, "
    "automobile BIT, "
    "autoLeave BIT, "
    "autoHigh INT, "
    "autoHighmiss INT, "
    "autoLow INT, "
    "autoLowmiss INT, "
    "shutdown BIT,"
    "shutdownOpp BIT, "
    "teleHigh INT, "
    "teleHighmiss INT, "
    "teleLow INT, "
    "teleLowmiss INT, "
    "endpos VARCHAR(16), "
    "bunny BIT, "
    "offence INT, "
    "defence INT, "
    "died BIT, "
    "tipped BIT, "
    "card VARCHAR(16), "
    "foul INT, "
    "autoRP BIT, "
    "luniteRP BIT, "
    "endgameRP BIT, "
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
        "CREATE TABLE IF NOT EXISTS scouting"
        "("
        "id, "
        "initials, "
        "matchnum, "
        "teamnum, "
        "noshow, "
        "automobile, "
        "autoLeave, "
        "autoHigh, "
        "autoHighmiss, "
        "autoLow, "
        "autoLowmiss, "
        "shutdown,"
        "shutdownOpp, "
        "teleHigh, "
        "teleHighmiss, "
        "teleLow, "
        "teleLowmiss, "
        "endpos, "
        "bunny, "
        "offence, "
        "defence, "
        "died, "
        "tipped, "
        "card, "
        "foul, "
        "autoRP, "
        "luniteRP, "
        "endgameRP, "
        "comments"
        ")"
        "VALUES"
        "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            data['pre']['i'],        # initials
            int(data['pre']['N']),   # matchnum
            int(data['pre']['t']),   # teamnum
            (data['pre']['n']),   # noshow
            (data['auto']['m']),  # automobile
            (data['auto']['M']),  # leave
            int(data['auto']['A']),  # autoHigh
            int(data['auto']['a']),  # autoHighmiss
            int(data['auto']['S']),  # autoLow
            int(data['auto']['s']),  # autoLowmiss
            (data['tele']['g']),  # gotShutdown?
            (data['tele']['O']),  # shutdownOpponent?
            int(data['tele']['H']),  # high
            int(data['tele']['h']),  # highmiss
            int(data['tele']['L']),  # low
            int(data['tele']['l']),  # lowmiss
            data['end']['e'],        # endpos
            data['end']['b'],        # bunny?
            data['post']['o'],  # offence
            data['post']['d'],  # defence
            data['post']['D'],  # died
            data['post']['t'],  # tipped
            data['post']['c'],       # card
            int(data['post']['f']),  # foul
            data['post']['aR'],        # autoRP
            data['post']['lR'],        # luniteRP
            data['post']['eR'],        # endgameRP
            data['post']['C']        # comments
        )
    )
    cur.connection.commit()
    