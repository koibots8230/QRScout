import tkinter
import sqlite3
import pyodbc

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
    "initials, "
    "matchnum, "
    "startpos, "
    "teamnum, "
    "noshow, "
    "automobile, "
    "autoamp, "
    "autoampmiss, "
    "autospeaker, "
    "autospeakermiss, "
    "coop, "
    "teleamp, "
    "teleampmiss, "
    "telespeaker, "
    "telespeakermiss, "
    "trap, "
    "endpos, "
    "harmony, "
    "spotlight, "
    "offence, "
    "defence, "
    "died, "
    "tipped, "
    "defended, "
    "card, "
    "foul, "
    "comments"
    ")"
)

cur.execute(
    "CREATE TABLE IF NOT EXISTS pitScouting"
    "("
    "id INT PRIMARY KEY"
    "initials, "
    "matchnum, "
    "startpos, "
    "teamnum, "
    "dimensions, "
    "measuredWithOrWithoutBumpers, "
    "shootAmpOrSpeaker, "
    "preferAmpOrSpeaker, "
    "preferedPicupLocation, "
    "shootingDistance, "
    "autos, "
    "defenseExperience, "
    "drivetrainType, "
    "speed, "
    "whereClimbChain, "
    "otherClimb, "
    "numOfDriveMotors, "
    "gearRatio"
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

input: str = input("Stand or Pit Scouting? [S/p]: ")

if input.lower() != 's' or input.lower() != 'p':
    input = 's'

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

    if input == 's':
        cur.execute(
            "INSERT INTO scouting"
            "("
            "initials, "
            "matchnum, "
            "startpos, "
            "teamnum, "
            "noshow, "
            "automobile, "
            "autoamp, "
            "autoampmiss, "
            "autospeaker, "
            "autospeakermiss, "
            "coop, "
            "teleamp, "
            "teleampmiss, "
            "telespeaker, "
            "telespeakermiss, "
            "trap, "
            "endpos, "
            "harmony, "
            "spotlight, "
            "offence, "
            "defence, "
            "died, "
            "tipped, "
            "defended, "
            "card, "
            "foul, "
            "comments"
            ") "
            "VALUES"
            "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                data['pre']['i'],        # initials
                        int(data['pre']['matchNumber']),   # matchnum
                        data['pre']['p'],        # startpos
                        int(data['pre']['t']),   # teamnum
                        int(data['pre']['n']),   # noshow
                        int(data['auto']['m']),  # automobile
                        int(data['auto']['A']),  # autoamp
                        int(data['auto']['a']),  # autoampmiss
                        int(data['auto']['S']),  # autospeaker
                        int(data['auto']['s']),  # autospeakermiss
                        int(data['tele']['cc']),  # coop
                        int(data['tele']['AA']),  # teleamp
                        int(data['tele']['am']),  # teleampmiss
                        int(data['tele']['SS']),  # telespeaker
                        int(data['tele']['ss']),  # telespeakermiss
                        int(data['tele']['tt']),  # trap
                        data['end']['p'],        # endpos
                        int(data['end']['h']),   # harmony
                        data['end']['a'],        # spotlight
                        int(data['post']['o']),  # offence
                        int(data['post']['d']),  # defence
                        int(data['post']['D']),  # died
                        int(data['post']['t']),  # tipped
                        int(data['post']['w']),  # defended
                        data['post']['c'],       # card
                        int(data['post']['f']),  # foul
                        data['post']['C']        # comments
            )
        )
    else:
        cur.execute(
            "INSERT INTO pitScouting"
            "("
            "initials, "
            "matchnum, "
            "startpos, "
            "teamnum, "
            "dimensions, "
            "measuredWithOrWithoutBumpers, "
            "shootAmpOrSpeaker, "
            "preferAmpOrSpeaker, "
            "preferedPicupLocation, "
            "shootingDistance, "
            "autos, "
            "defenseExperience, "
            "drivetrainType, "
            "speed, "
            "whereClimbChain, "
            "otherClimb, "
            "numOfDriveMotors, "
            "gearRatio"
            ") "
            "VALUES"
            "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                data['pre']['i'],
                data['pre']['p'],
                int(data['pre']['t']),
                data['pitScouting']['dimension'],
                data['pitScouting']['measuredWithOrWithoutBumper'],
                data['pitScouting']['shootAmpOrSpeaker'],
                data['pitScouting']['peferAmpSpeaker'],
                data['pitScouting']['preferedPickupLocation'],
                int(data['pitScouting']['shootingDistance']),
                int(data['pitScouting']['autos']),
                data['pitScouting']['defenseExperience'],
                data['pitScouting']['drivetrainType'],
                int(data['pitScouting']['speed']),
                data['pitScouting']['whereClimbChain'],
                data['pitScouting']['otherClimb'],
                int(data['pitScouting']['numOfDriveMotor'],
                data['pitScouting']['gearRatio'],
            )
        ))
    cur.connection.commit()
    
