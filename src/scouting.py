import tkinter
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


con = sqlite3.connect(
    database="scouting"
)

con.autocommit = True

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
    except KeyError:
        print("girlie your qr is screwed")
        settext("girlie your qr code is screwed")
        continue

    if not data:
        print("QR Code is unreadable, please scan again")
        settext("QR Code is unreadable, please scan again")
        continue

    data = json.loads(data)

    if DEBUG:
        print(f"Data: {data}")
    settext(data)

#:)
    if data.get('pitScouting') == None:
        print("stand scouting")
        print((data['auto']['m']),int(data['auto']['m']))
        cur.execute(
            """
            INSERT INTO stand_scouting 
            (
            initals,
            match_number,
            teamnum,
            start_position,
            no_show,
            cage_position,
            automobile,
            auto_l1,
            auto_l2,
            auto_l3,
            auto_l4,
            auto_algae_barge,
            auto_algae_processor,
            auto_algae_dislodged,
            auto_foul,
            tele_algae_dislodged,
            coral_intake,
            algae_intake,
            tele_l1,
            tele_l2,
            tele_l3,
            tele_l4,
            tele_algae_barge,
            tele_algae_processor,
            end_position,
            touched_opps_cage,
            coral_RP,
            barge_RP,
            auto_RP,
            offense,
            defense,
            was_defended,
            died,
            tipped,
            card,
            comments
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, 
            (
                data['pre']['i'],        # initials
                int(data['pre']['matchNumber']),   # matchnum
                int(data['pre']['team']),   # teamnum
                data['pre']['p'],        # startpos
                data['pre']['n'],   # noshow
                data['pre']['cage'],    #cage position
                data['auto']['m'],  # automobile
                int(data['auto']['ellwan']),  # l1
                int(data['auto']['elltwo']),  # l2
                int(data['auto']['ellthre']),  # l3
                int(data['auto']['ellfor']),  # l4
                int(data['auto']['S']),  # barge algae
                int(data['auto']['s']),  # processor algae
                int(data['auto']['Di']),  # auto dislodged algae
                int(data['auto']['f']),  # auto foul
                data['tele']['d'],  # tele dislodged algae
                data['tele']['I'],  # coral intake position
                data['tele']['gi'], #algae intake positon
                int(data['tele']['L']),  # L1
                int(data['tele']['l']),  # L2
                int(data['tele']['T']),  # L3
                int(data['tele']['F']),  # L4
                int(data['tele']['p']),   # barge algae
                int(data['tele']['h']),   # processor algae
                data['end']['ps'],  #end position
                data['end']['a'],        # touched opps cage
                data["post"]["rp"],    #coral rp
                data["post"]["pr"], #barge rp
                data["post"]["ar"], # auto rp
                int(data['post']['o']),  # offence
                int(data['post']['de']),  # defence
                data['post']['w'],  # was defended
                data['post']['D'],  # died
                data['post']['ti'],  # tipped
                data['post']['c'],       # card
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
                doAlgae,


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
        
    #cur.connection.commit() //autocommit already enabled
    
