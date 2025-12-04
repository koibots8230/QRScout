import tkinter
import cv2
from PIL import ImageTk, Image

keys = []

def keydown(event):
    keys.append(event.keysym)


def keyup(event):
    keys.remove(event.keysym)


decoder = cv2.QRCodeDetector()
camera = cv2.VideoCapture(0)
root = tkinter.Tk()
root.bind("<KeyPress>", keydown)
root.bind("<KeyRelease>", keyup)
video = tkinter.Label(root)
video.pack()
text = tkinter.Text(font="Courier")
text.pack(padx=10, pady=10)

def settext(_text):
    text.delete("0.0", tkinter.END)
    text.insert("0.0", _text)

if not camera.isOpened():
    print("Could not open camera")
    quit()

root.clipboard_clear()

data = None
lastData = None
loops = 0

settext("")

while True:
    while True:
        loops += 1
        
        if loops == 150:
            settext("")

        errors, image = camera.read()

        display_image = cv2.flip(image, 1)
        display_image = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGBA)
        display_image = Image.fromarray(display_image)
        display_image = display_image.resize((display_image.size[0]//3, display_image.size[1]//3))
        display_image = ImageTk.PhotoImage(display_image)

        video.configure(image=display_image)

        root.update()
        root.update_idletasks()

        if 'q' in keys or 'Escape' in keys:
            quit()

        try:
            decoder.detect(image)[0]
            break
        except IndexError:
            continue


    try:
        if decoder.detectAndDecode(image)[0] == lastData:
            continue
        else:
            data = decoder.detectAndDecode(image)[0]
            if data == lastData:
                continue;
            else:
                lastData = data
                loops = 0
                settext("Data copied to clipboard!")
                settext(f"\n{data}")

    except IndexError:
        #settext("No QR Code detected, please scan again")
        continue

    if not data:
        #settext("QR Code is unreadable, please scan again")
        continue
    root.clipboard_clear()    
    root.clipboard_append(f"{data}")
    #print(root.clipboard_get())

