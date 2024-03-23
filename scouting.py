import tkinter
import sqlite3
import psycopg

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


con = psycopg.connect(
    "dbname=scouting user=postgres host=localhost password=postgres port=5432"
)

cur = con.cursor()
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


    if data.get('tele', {}).get('tt'):
        print("stand scouting")
        print((data['auto']['a']), int(data['auto']['a']))
        cur.execute(
            """
            INSERT INTO stand_scouting 
            (
            initals,
            match_number,
            start_position,
            teamnum,
            no_show,
            automobile,
            auto_amp,
            auto_amp_miss,
            auto_speaker,
            auto_speaker_miss,
            coop,
            tele_amp,
            tele_amp_miss,
            tele_speaker,
            tele_speaker_miss,
            trap,
            end_position,
            harmony,
            spotlight,
            offense,
            defense,
            died,
            tipped,
            defended,
            card,
            foul,
            comments
            ) VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )""", 
            (
                data['pre']['i'],        # initials
                int(data['pre']['matchNumber']),   # matchnum
                data['pre']['p'],        # startpos
                int(data['pre']['t']),   # teamnum
                data['pre']['n'],   # noshow
                data['auto']['m'],  # automobile
                int(data['auto']['A']),  # autoamp
                int(data['auto']['a']),  # autoampmiss
                int(data['auto']['S']),  # autospeaker
                int(data['auto']['s']),  # autospeakermiss
                data['tele']['cc'],  # coop
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
                data['post']['D'],  # died
                data['post']['t'],  # tipped
                data['post']['w'],  # defended
                data['post']['c'],       # card
                int(data['post']['f']),  # foul
                data['post']['C']        # comments
            )
        )
    else:
        print("pit scouting")
        cur.execute(
            """
            INSERT INTO pit_scouting (
                initals,
                starting_position,
                teamnum,
                dimensions, 
                measured_with_or_without_bumpers,
                can_shoot_amp_or_speaker,
                prefers_amp_or_speaker,
                preferred_pickup_location,
                shooting_distance,
                autos, 
                defense_experience,
                drivetrain_type, 
                estimated_speed, 
                where_can_robot_climb_a_chain,
                different_climb,
                drive_motors,
                gear_ratios
            ) VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                data['pre']['i'],
                data['pre']['p'],
                int(data['pre']['t']),
                data['pitScouting']['dimensions'],
                data['pitScouting']['measuredWithOrWithoutBumpers'],
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
                int(data['pitScouting']['numOfDriveMotors']),
                data['pitScouting']['gearRatio'],
            
        ))
    cur.connection.commit()
    
