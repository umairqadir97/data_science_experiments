from tkinter import *
from tkinter.filedialog import askopenfilename
import os
import csv


path = "directory/to/images"
new_path = "directory/to/store/coordinates"
images = sorted(os.listdir(path))
images = [image for image in images if '.png' in image]
for index, image in enumerate(images):
    event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))
    coords = []

    root = Tk()
    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    # File = askopenfilename(parent=root, initialdir="M:/",title='Choose an image.')
    File = path + image
    print("opening %s" % File, "\t\t processed {} files".format(index))
    img = PhotoImage(file=File)
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        cx, cy = event2canvas(event, canvas)
        coords.append([int(cy), int(cx)])
        print ("(%d, %d)" % (cy,cx))
        canvas.create_rectangle(cx-6, cy-6, cx+6, cy+6, fill="red", outline = 'red')
        return (cy, cx)
    #mouseclick event
    canvas.bind("<ButtonPress-1>",printcoords)
    root.mainloop()

    with open(new_path+image[:-3]+'csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for coord in coords:
            csvwriter.writerow([coord[0], coord[1]])
    print("got {} coordinates for image {} ".format(len(coords), image))
