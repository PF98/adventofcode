from PIL import Image, ImageDraw, ImageTk
#import ImageTk
import tkinter as tk

window = tk.Tk()
window.geometry("500x500")
img = Image.new("RGB", (100, 100), color=(0,0,0))

img = Image.open("out.png")
tkimg = ImageTk.PhotoImage(img)
tk.Label(window, image = tkimg).pack()

#while True:
    #pass
window.mainloop()

print("ciao")
