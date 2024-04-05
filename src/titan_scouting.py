import tkinter
from cv2 import VideoCapture, flip, cvtColor, COLOR_BGR2RGBA
from PIL import ImageTk, Image
from qreader import QReader
from time import sleep

keys = []

def keydown(event):
    keys.append(event.keysym)


def keyup(event):
    keys.remove(event.keysym)


decoder = QReader()
camera = VideoCapture(0)
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
shouldRead = True

while True:
    while True:
        errors, image = camera.read()

        display_image = flip(image, 1)
        display_image = cvtColor(display_image, COLOR_BGR2RGBA)
        display_image = Image.fromarray(display_image)
        display_image = display_image.resize((display_image.size[0]//3, display_image.size[1]//3))
        display_image = ImageTk.PhotoImage(display_image)

        video.configure(image=display_image)

        root.update()
        root.update_idletasks()

        if 'q' in keys or 'Escape' in keys:
            quit()

        # if 'space' in keys or 'Return' in keys:
        #     break

        try:
            decoder.detect(image=image)[0]
            break
        except IndexError:
            continue

    try:
        if decoder.detect_and_decode(image=image)[0] == data:
            continue
        else:
            if shouldRead :
                data = decoder.detect_and_decode(image=image)[0]
                print("Data copied to clipboard!")
            else:
                continue

    except IndexError:
        print("No QR Code detected, please scan again")
        settext("No QR Code detected, please scan again")
        continue

    if not data:
        print("QR Code is unreadable, please scan again")
        settext("QR Code is unreadable, please scan again")
        continue
    
    root.clipboard_append(f"{data}")
    #print(root.clipboard_get())
